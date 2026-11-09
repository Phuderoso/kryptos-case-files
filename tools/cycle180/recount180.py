"""Cycle 180 independent recount (numpy brute force: no CRT, no parity table, no pext, no elimination).
On a perm slice and an alphabet subset, for every text, alphabet, tableau type (q1/q2/q3; A-Z only as q3) and form:
 M0 (ix 0) L 1-2 (L 3 for texts listed in argv[5]): every (c, d) in 26^(L+1); key from k[21..21+L-1], propagated to 73 and compared
   on all 24 crib slots -> number of fitting (c, d) mod 26;
 M1 (ix 1) L 1 every stream (c, seed, d) in 26^3; L 2 (texts listed in argv[6], only at the perm q given there) every stream in 26^5
   (c outer) -> number of fitting streams.
usage: recount180.py slice.bin alphafile texts.txt M0L3-labels M1L2-label:q  -> 'R lab ix L ty form q alab count' lines"""
import sys, itertools
import numpy as np
P = np.fromfile(sys.argv[1], dtype=np.int16).reshape(-1, 97); ALS = [l.split() for l in open(sys.argv[2])]
texts = [l.split() for l in open(sys.argv[3])]; l3 = set(sys.argv[4].split(",")); m1l2 = dict(x.split(":") for x in sys.argv[5].split(","))
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; CI = list(range(21, 34)) + list(range(63, 74)); PT = "EASTNORTHEASTBERLINCLOCK"
def tabs():
    for K, lb in ALS:
        for ty in (("q3",) if K == AZ else ("q1", "q2", "q3")):
            A, B = {"q1": (K, AZ), "q2": (AZ, K), "q3": (K, K)}[ty]; yield lb, ty, A, B
def kobs(ct, S, A, B, form):
    ci = np.array([B.index(ct[S[i]]) for i in CI]); pi = np.array([A.index(c) for c in PT])
    return (ci - pi) % 26 if form == "vig" else (ci + pi) % 26
XS = {L: np.array(list(itertools.product(range(26), repeat=L + 1)), dtype=np.int64) for L in (1, 2, 3)}
def m0count(kd, L):
    X = XS[L]; c, d = X[:, :L], X[:, L]; Wn = np.tile(np.array([kd[21 + j] for j in range(L)]), (len(X), 1))
    for i in range(21 + L, 74):
        nv = ((c * Wn[:, ::-1]).sum(1) + d) % 26
        if i in kd:
            k = nv == kd[i]; c, d, Wn, nv = c[k], d[k], Wn[k], nv[k]
        Wn = np.concatenate([Wn[:, 1:], nv[:, None]], 1)
    return len(d)
def gen(c, d, seed, n):
    M, L = seed.shape; K = np.zeros((M, n), dtype=np.int64); K[:, :L] = seed
    for i in range(L, n): K[:, i] = ((c * K[:, i - L:i][:, ::-1]).sum(1) + d) % 26
    return K
Y1 = XS[2]; K1 = {cc: gen(np.full((len(XS[1]), 1), cc), XS[1][:, 1], XS[1][:, :1], 97) for cc in range(26)}
out = []; L2items = []
for lab, ct in texts:
    for qi in range(P.shape[0]):
        S = P[qi]; J = np.array([S[i] for i in CI])
        for lb, ty, A, B in tabs():
            for form in ("vig", "beau"):
                ko = kobs(ct, S, A, B, form); kd = dict(zip(CI, ko))
                for L in ((1, 2, 3) if lab in l3 else (1, 2)):
                    n = m0count(kd, L)
                    if n: out.append(f"R {lab} 0 {L} {ty} {form} {qi} {lb} {n}")
                n = 0
                for cc in range(26):
                    K = K1[cc]; r = np.nonzero(K[:, J[0]] == ko[0])[0]; n += int((K[r][:, J] == ko).all(1).sum())
                if n: out.append(f"R {lab} 1 1 {ty} {form} {qi} {lb} {n}")
                if lab in m1l2 and qi == int(m1l2[lab]): L2items.append((lab, qi, ty, form, lb, J, ko))
cnt2 = {}; Y = XS[2]
for c1, c2 in itertools.product(range(26), repeat=2):            # M1 L2: c outer, every (seed, d) inner
    K = gen(np.tile(np.array([c1, c2]), (len(Y), 1)), Y[:, 2], Y[:, :2], 97)
    for (lab, qi, ty, form, lb, J, ko) in L2items:
        r = np.nonzero(K[:, J[0]] == ko[0])[0]; n = int((K[r][:, J] == ko).all(1).sum())
        if n: cnt2[(lab, qi, ty, form, lb)] = cnt2.get((lab, qi, ty, form, lb), 0) + n
for (lab, qi, ty, form, lb), n in sorted(cnt2.items()): out.append(f"R {lab} 1 2 {ty} {form} {qi} {lb} {n}")
print("\n".join(out)); print("RECOUNT_END", len(out))
