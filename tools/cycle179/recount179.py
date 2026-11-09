"""Cycle 179 independent recount (numpy brute force; no algebra, no CRT, no wildcard trick): on a perm slice,
 M0 (ix 0) L 1-2: every (c, d) in 26^(L+1) and every seed = observed k[21..21+L-1] or with ONE seed value replaced (L x 25),
   key generated 21..73, mismatches counted on the 24 crib slots (a replaced seed value counts as the error) -> fit iff <= 1;
 M1 (ix 1) L 1: every stream (c, seed, d) in 26^3; L 2 only for the texts listed in argv[4]; fit iff <= 1 crib mismatch.
 Fitting slot set = the mismatching slot, or all 24 for an exact match.
 usage: recount179.py slice.bin texts.txt M1L2-labels(comma) -> 'R lab mode L pa form q slots'"""
import sys, itertools
import numpy as np
P = np.fromfile(sys.argv[1], dtype=np.int16).reshape(-1, 97); texts = [l.split() for l in open(sys.argv[2])]
l2 = set(sys.argv[3].split(","))
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"; AL = {"az": AZ, "ka": KA}
CI = list(range(21, 34)) + list(range(63, 74)); PT = "EASTNORTHEASTBERLINCLOCK"
def kobs(ct, S, pa, form):
    al = AL[pa]; ci = np.array([al.index(ct[S[i]]) for i in CI]); pi = np.array([al.index(c) for c in PT])
    return (ci - pi) % 26 if form == "vig" else (ci + pi) % 26
out = []; res = {}
XS = {L: np.array(list(itertools.product(range(26), repeat=L + 1)), dtype=np.int64) for L in (1, 2)}
for lab, ct in texts:
    for qi in range(P.shape[0]):
        S = P[qi]
        for pa, form in itertools.product(("az", "ka"), ("vig", "beau")):
            ko = kobs(ct, S, pa, form); kd = dict(zip(CI, ko))
            for L in (1, 2):
                X = XS[L]; base = np.array([kd[21 + j] for j in range(L)])
                seeds = [(base, -1)] + [(np.where(np.arange(L) == j, v, base), j) for j in range(L) for v in range(26) if v != base[j]]
                slots = set(); exact = False
                for sd, rj in seeds:
                    c, d = X[:, :L], X[:, L]; K = np.zeros((len(X), 53), dtype=np.int64); K[:, :L] = sd
                    for i in range(L, 53): K[:, i] = ((c * K[:, i - L:i][:, ::-1]).sum(1) + d) % 26
                    mm = (K[:, [i - 21 for i in CI]] != ko)          # mismatches incl. the seed slots
                    nm = mm.sum(1)
                    if rj < 0:
                        if (nm == 0).any(): exact = True
                        for r in np.nonzero(nm == 1)[0]: slots.add(CI[int(np.nonzero(mm[r])[0][0])])
                    else:
                        if (nm == 1).any(): slots.add(21 + rj)     # the replaced seed value is the single error
                if exact: slots = set(CI)
                if slots: out.append(f"R {lab} 0 {L} {pa} {form} {qi} " + ",".join(map(str, sorted(slots))))
items = []
for lab, ct in texts:
    for qi in range(P.shape[0]):
        S = P[qi]; J = np.array([S[i] for i in CI])
        for pa, form in itertools.product(("az", "ka"), ("vig", "beau")): items.append((lab, qi, pa, form, J, kobs(ct, S, pa, form)))
def gen(c, d, seed, n):
    M, L = seed.shape; K = np.zeros((M, n), dtype=np.int64); K[:, :L] = seed
    for i in range(L, n): K[:, i] = ((c * K[:, i - L:i][:, ::-1]).sum(1) + d) % 26
    return K
cnt = {}
for L in (1, 2):
    for cc in itertools.product(range(26), repeat=L):
        Y = XS[L]; K = gen(np.tile(np.array(cc), (len(Y), 1)), Y[:, L], Y[:, :L], 97)
        for (lab, qi, pa, form, J, ko) in items:
            if L == 2 and lab not in l2: continue
            mm = K[:, J] != ko; nm = mm.sum(1); key = (lab, L, pa, form, qi)
            if (nm == 0).any(): cnt.setdefault(key, set()).update(CI)
            for r in np.nonzero(nm == 1)[0]: cnt.setdefault(key, set()).add(CI[int(np.nonzero(mm[r])[0][0])])
for (lab, L, pa, form, qi), s in sorted(cnt.items()): out.append(f"R {lab} 1 {L} {pa} {form} {qi} " + ",".join(map(str, sorted(s))))
print("\n".join(out)); print("RECOUNT_END", len(out))
