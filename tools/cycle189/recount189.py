"""Cycle 189 independent recount (no union-find): linear algebra mod 2 and mod 13 (numpy Gaussian elimination).
For each perm row of the slice, model (P/C) and pair (m, n): design matrix D (24 x (m+n), row t = e[pos_t mod m] + e[m + pos_t mod n]);
left null space N_p of D over GF(p), p = 2, 13. A key vector K (24 crib key values) fits iff N_2 K = 0 mod 2 and N_13 K = 0 mod 13 (CRT).
usage: recount189.py slice.bin alphas.txt texts.txt mmax nmax -> F lines (label row alpha form model m n)"""
import sys
import numpy as np
P = np.fromfile(sys.argv[1], dtype=np.int16).reshape(-1, 97); AL = [l.split() for l in open(sys.argv[2])]; TX = [l.split() for l in open(sys.argv[3])]
MM, NM = int(sys.argv[4]), int(sys.argv[5])
CI = list(range(21, 34)) + list(range(63, 74)); PT = "EASTNORTHEASTBERLINCLOCK"
def leftnull(D, p):
    """rows y with y D = 0 mod p: row-reduce [D | I] and keep the identity part of the zero rows of D."""
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
            N2, N13 = leftnull(D, 2), leftnull(D, 13)
            for lab, ct in TX:
                for ai, (a, an) in enumerate(AL):
                    xp = np.array([IDX[ai][PT[t]] for t in range(24)]); xc = np.array([IDX[ai][ct[S[i]]] for i in CI])
                    for form, K in (("vig", (xc - xp) % 26), ("beau", (xc + xp) % 26)):
                        if not (N2 @ K % 2).any() and not (N13 @ K % 13).any(): print("F", lab, row, an, form, model, m, n)
    print("DONE row", row, flush=True)
