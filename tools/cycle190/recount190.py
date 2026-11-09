"""Cycle 190 independent recount (no union-find): one-error fits by linear algebra mod 2 and mod 13 (numpy elimination).
For each perm row, model (P/C), pair (m, n): design matrix D (24 x (m+n)); a key vector K fits strictly iff N_p K = 0 for the left null
space N_p of D (p = 2, 13); it fits with one error iff it fits strictly or, for some slot t, N_p(D without row t) K' = 0 for both p.
usage: recount190.py rows.bin alphas.txt texts.txt mmax nmax -> F lines (label row alpha form model m n)"""
import sys
import numpy as np
P = np.fromfile(sys.argv[1], dtype=np.int16).reshape(-1, 97); AL = [l.split() for l in open(sys.argv[2])]; TX = [l.split() for l in open(sys.argv[3])]
MM, NM = int(sys.argv[4]), int(sys.argv[5])
CI = list(range(21, 34)) + list(range(63, 74)); PT = "EASTNORTHEASTBERLINCLOCK"
def leftnull(D, p):
    r, c = D.shape; A = np.concatenate([D % p, np.eye(r, dtype=np.int64)], 1); piv = 0
    for col in range(c):
        nz = [i for i in range(piv, r) if A[i, col] % p]
        if not nz: continue
        i = nz[0]; A[[piv, i]] = A[[i, piv]]; A[piv] = A[piv] * pow(int(A[piv, col]), -1, p) % p
        for j in range(r):
            if j != piv and A[j, col] % p: A[j] = (A[j] - A[j, col] * A[piv]) % p
        piv += 1
        if piv == r: break
    return A[piv:, c:]
pairs = [(m, n) for m in range(2, MM + 1) for n in range(m + 1, NM + 1) if n % m]
IDX = [{ch: i for i, ch in enumerate(a)} for a, _ in AL]
for row in range(P.shape[0]):
    S = P[row]
    for model in "PC":
        pos = [i if model == "P" else int(S[i]) for i in CI]
        for m, n in pairs:
            D = np.zeros((24, m + n), dtype=np.int64)
            for t, x in enumerate(pos): D[t, x % m] = 1; D[t, m + x % n] = 1
            subs = [np.arange(24)] + [np.array([r for r in range(24) if r != t]) for t in range(24)]
            NS = [(leftnull(D[s], 2), leftnull(D[s], 13), s) for s in subs]
            for lab, ct in TX:
                for ai, (a, an) in enumerate(AL):
                    xp = np.array([IDX[ai][PT[t]] for t in range(24)]); xc = np.array([IDX[ai][ct[S[i]]] for i in CI])
                    for form, K in (("vig", (xc - xp) % 26), ("beau", (xc + xp) % 26)):
                        if any(not (N2 @ K[s] % 2).any() and not (N13 @ K[s] % 13).any() for N2, N13, s in NS): print("F", lab, row, an, form, model, m, n)
    print("DONE row", row, flush=True)
