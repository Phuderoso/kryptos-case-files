"""Cycle 178 independent recount (numpy brute force, no algebra, no CRT): on a perm slice,
 M0 (ix 0) L 1-3: every (c, d) in 26^(L+1), key generated from k[21..21+L-1] and compared on all 24 crib slots;
 M1 (ix 1) L 1-2: every stream (c, seed, d) in 26^(2L+1) (L 2 only for the texts in argv M1L2), compared on all 24 slots;
 W0/W1 L 6: every vocabulary stream (c in {0,1}^6\\0, d, seed word, numbering), compared on all 24 slots.
 usage: recount178.py slice.bin texts.txt seeds178.txt M1L2-labels(comma)   -> prints 'R lab mode L pa form q count'"""
import sys, itertools
import numpy as np
P = np.fromfile(sys.argv[1], dtype=np.int16).reshape(-1, 97); texts = [l.split() for l in open(sys.argv[2])]
words = open(sys.argv[3]).read().split(); l2 = set(sys.argv[4].split(","))
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"; AL = {"az": AZ, "ka": KA}
CI = list(range(21, 34)) + list(range(63, 74)); PT = "EASTNORTHEASTBERLINCLOCK"
def kobs(ct, S, pa, form, pos):     # key value at each crib slot; pos = 'pt' (ix0) or carved
    al = AL[pa]; ci = np.array([al.index(ct[S[i]]) for i in CI]); pi = np.array([al.index(c) for c in PT])
    return (ci - pi) % 26 if form == "vig" else (ci + pi) % 26
def gen(c, d, seed, n):              # c: (M,L) d: (M,) seed: (M,L) -> (M,n) int64
    M, L = seed.shape; K = np.zeros((M, n), dtype=np.int64); K[:, :L] = seed
    for i in range(L, n): K[:, i] = ((c * K[:, i - L:i][:, ::-1]).sum(1) + d) % 26
    return K
out = []
XS = {L: np.array(list(itertools.product(range(26), repeat=L + 1)), dtype=np.int64) for L in (1, 2, 3)}
items = []
for lab, ct in texts:
    for qi in range(P.shape[0]):
        S = P[qi]; J = np.array([S[i] for i in CI])
        for pa, form in itertools.product(("az", "ka"), ("vig", "beau")):
            ko = kobs(ct, S, pa, form, "pt"); kd = dict(zip(CI, ko)); items.append((lab, qi, pa, form, J, ko))
            for L in (1, 2, 3):              # M0: key from k[21..21+L-1], rolling window, filtered on every crib slot
                X = XS[L]; c, d = X[:, :L], X[:, L]; Wn = np.tile(np.array([kd[21 + j] for j in range(L)]), (len(X), 1))
                for i in range(21 + L, 74):
                    nv = ((c * Wn[:, ::-1]).sum(1) + d) % 26
                    if i in kd:
                        k = nv == kd[i]; c, d, Wn, nv = c[k], d[k], Wn[k], nv[k]
                    Wn = np.concatenate([Wn[:, 1:], nv[:, None]], 1)
                if len(d): out.append(f"R {lab} 0 {L} {pa} {form} {qi} {len(d)}")
cnt = {}
for L in (1, 2):                             # M1: every stream, c outer
    for cc in itertools.product(range(26), repeat=L):
        Y = XS[L]; K = gen(np.tile(np.array(cc), (len(Y), 1)), Y[:, L], Y[:, :L], 97)
        for (lab, qi, pa, form, J, ko) in items:
            if L == 2 and lab not in l2: continue
            r = np.nonzero(K[:, J[0]] == ko[0])[0]
            n = int((K[r][:, J] == ko).all(1).sum())
            if n: cnt[(lab, L, pa, form, qi)] = cnt.get((lab, L, pa, form, qi), 0) + n
for (lab, L, pa, form, qi), n in sorted(cnt.items()): out.append(f"R {lab} 1 {L} {pa} {form} {qi} {n}")
# W L6
Ws = []
for w in words:
    if len(w) < 6: continue
    for nb, al in (("azN", AZ), ("kaN", KA)):
        for cm in range(1, 64):
            for d in range(26): Ws.append(([(cm >> j) & 1 for j in range(6)], d, [al.index(x) for x in w[:6]], w, nb, cm))
Kw = gen(np.array([x[0] for x in Ws]), np.array([x[1] for x in Ws]), np.array([x[2] for x in Ws]), 97)
for lab, ct in texts:
    for qi in range(P.shape[0]):
        S = P[qi]; J = np.array([S[i] for i in CI])
        for pa, form in itertools.product(("az", "ka"), ("vig", "beau")):
            for ix, cols in ((0, np.array(CI)), (1, J)):
                al = AL[pa]; ci = np.array([al.index(ct[S[i]]) for i in CI]); pi = np.array([al.index(c) for c in PT])
                k = Kw[:, cols]; ok = ((ci - k) % 26 == pi) if form == "vig" else ((k - ci) % 26 == pi)
                for r in np.nonzero(ok.all(1))[0]:
                    _, d, _, w, nb, cm = Ws[r]; out.append(f"R {lab} W{ix} 6 {pa} {form} {qi} {w} {nb} c{cm} d{d}")
print("\n".join(out)); print("RECOUNT_END", len(out))
