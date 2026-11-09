"""Cycle 181 independent recount (numpy brute force: no CRT, no parity table, no pext, no elimination, no shortcut).
One-error fits by explicit enumeration and a mismatch count over the 24 crib slots.
 M0 (ix 0) L 1 (L 2 for texts in argv[4], only at their row and planted alphabet): every (c, d) in 26^(L+1) x every seed variant (the observed key at
   21..21+L-1, or one seed slot replaced by any other value); key propagated to 73; fit at slot t iff the only crib mismatch is t
   (a replaced seed slot counts as its own mismatch); no mismatch = strict.
 M1 (ix 1) L 1 (L 2 for texts in argv[5], only at their row and planted alphabet): every stream (c, seed, d) in 26^(2L+1); mismatches at the 24 crib
   slots' carved positions; <= 1 -> fit (0 = strict).
usage: recount181.py slice.bin alphafile texts.txt M0L2-label:row:alab[,..] M1L2-label:row:alab[,..]  -> 'R lab ix L ty form row alab slots'"""
import sys, itertools
import numpy as np
P = np.fromfile(sys.argv[1], dtype=np.int16).reshape(-1, 97); ALS = [l.split() for l in open(sys.argv[2])]
texts = [l.split() for l in open(sys.argv[3])]; m0l2 = {x.split(":")[0]: x.split(":")[1:] for x in sys.argv[4].split(",")}; m1l2 = {x.split(":")[0]: x.split(":")[1:] for x in sys.argv[5].split(",")}
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; CI = list(range(21, 34)) + list(range(63, 74)); PT = "EASTNORTHEASTBERLINCLOCK"
def tabs():
    for K, lb in ALS:
        for ty in (("q3",) if K == AZ else ("q1", "q2", "q3")):
            A, B = {"q1": (K, AZ), "q2": (AZ, K), "q3": (K, K)}[ty]; yield lb, ty, A, B
def kobs(ct, S, A, B, form):
    ci = np.array([B.index(ct[S[i]]) for i in CI]); pi = np.array([A.index(c) for c in PT])
    return (ci - pi) % 26 if form == "vig" else (ci + pi) % 26
def m0slots(ko, L):
    kd = dict(zip(CI, ko.tolist())); X = np.array(list(itertools.product(range(26), repeat=L + 1)), dtype=np.int64); c, d = X[:, :L], X[:, L]
    res = set()
    for var in [None] + [(p, v) for p in range(L) for v in range(26) if v != kd[21 + p]]:
        seed = [kd[21 + j] for j in range(L)]
        if var: seed[var[0]] = var[1]
        K = np.zeros((len(X), 74), dtype=np.int64); K[:, 21:21 + L] = seed
        for i in range(21 + L, 74): K[:, i] = ((c * K[:, i - L:i][:, ::-1]).sum(1) + d) % 26
        mm = np.stack([K[:, i] != kd[i] for i in CI], 1)
        if var: mm[:, var[0]] = True
        n = mm.sum(1)
        if (n == 0).any(): res.add("strict")
        for r in np.nonzero(n == 1)[0]: res.add(CI[int(np.argmax(mm[r]))])
    return res
def gen(c, d, seed, n):
    M, L = seed.shape; K = np.zeros((M, n), dtype=np.int64); K[:, :L] = seed
    for i in range(L, n): K[:, i] = ((c * K[:, i - L:i][:, ::-1]).sum(1) + d) % 26
    return K
def m1slots(Kall, J, ko):
    mm = Kall[:, J] != ko; n = mm.sum(1); res = set()
    if (n == 0).any(): res.add("strict")
    for r in np.nonzero(n == 1)[0]: res.add(CI[int(np.argmax(mm[r]))])
    return res
X1 = np.array(list(itertools.product(range(26), repeat=3)), dtype=np.int64); K1 = gen(X1[:, :1], X1[:, 2], X1[:, 1:2], 97)
X2 = np.array(list(itertools.product(range(26), repeat=3)), dtype=np.int64)
def m1l2slots(J, ko):
    res = set()
    for c1, c2 in itertools.product(range(26), repeat=2):
        K = gen(np.tile(np.array([c1, c2]), (len(X2), 1)), X2[:, 2], X2[:, :2], 97); res |= m1slots(K, J, ko)
    return res
fmt = lambda s: "strict" if "strict" in s else ",".join(str(x) for x in sorted(s))
out = []
for lab, ct in texts:
    for qi in range(P.shape[0]):
        S = P[qi]; J = np.array([S[i] for i in CI])
        for lb, ty, A, B in tabs():
            for form in ("vig", "beau"):
                ko = kobs(ct, S, A, B, form)
                for L in ((1, 2) if lab in m0l2 and qi == int(m0l2[lab][0]) and lb == m0l2[lab][1] else (1,)):
                    s = m0slots(ko, L)
                    if s: out.append(f"R {lab} 0 {L} {ty} {form} {qi} {lb} {fmt(s)}")
                s = m1slots(K1, J, ko)
                if s: out.append(f"R {lab} 1 1 {ty} {form} {qi} {lb} {fmt(s)}")
                if lab in m1l2 and qi == int(m1l2[lab][0]) and lb == m1l2[lab][1]:
                    s = m1l2slots(J, ko)
                    if s: out.append(f"R {lab} 1 2 {ty} {form} {qi} {lb} {fmt(s)}")
print("\n".join(out)); print("RECOUNT_END", len(out))
