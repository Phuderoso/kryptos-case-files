"""Cycle 175: independent recount of hill175 (Hill n 4, linear/affine) by brute force over every row vector mod 2 (2^u) and
mod 13 (13^u): a row is solvable mod 26 iff it is solvable mod 2 and mod 13 (CRT); its solution count = n2 * n13.
Builds the equations from the definitions (ix 0: Z[i] = C[S[i]], unknown row r of D sees the block containing plaintext index i;
ix 1: Z = C, known X[S[i]] = P[i]). Compares per perm and sub-cell: consistent configs (all rows solvable) and
consistent_k (checks >= KMIN) with hill175 run on the same single perm.
usage: hillrecount175.py tool CT perms.bin t1 t2 ... [KMIN=4]"""
import sys, subprocess, itertools, numpy as np
tool, ct, pf = sys.argv[1:4]; ts = [int(x) for x in sys.argv[4:]]; KMIN = 4; n = 4; N = 97
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"
CR = list(zip(list(range(21, 34)) + list(range(63, 74)), "EASTNORTHEAST" + "BERLINCLOCK"))
P = np.fromfile(pf, dtype=np.int16).reshape(-1, N)
V = {(p, u): np.array(list(itertools.product(range(p), repeat=u)), dtype=np.int64).T for p in (2, 13) for u in (4, 5)}
def nsol(A, z, p):
    if not len(A): return p ** V[(p, 4)].shape[0]
    u = A.shape[1]; M = (A % p) @ V[(p, u)] % p
    return int(np.all(M == (z % p)[:, None], axis=0).sum())
bad = 0; tot = 0
for t in ts:
    S = [int(x) for x in P[t]]; mine = {}
    for num, nm in (("AZ", AZ), ("KA", KA)):
        Cn = [nm.index(c) for c in ct]
        for ix in (0, 1):
            Z = [Cn[S[i]] for i in range(N)] if ix == 0 else Cn
            known = [(j, nm.index(pl)) for j, pl in CR] if ix == 0 else [(S[j], nm.index(pl)) for j, pl in CR]
            for off in range(n):
                for aff in (0, 1):
                    u = n + aff; rows = {r: ([], []) for r in range(n)}
                    for pos, val in known:
                        if pos < off: continue
                        b, r = divmod(pos - off, n)
                        if off + n * (b + 1) > N: continue
                        blk = Z[off + n * b: off + n * b + n]
                        rows[r][0].append(blk + ([1] if aff else [])); rows[r][1].append(val)
                    chk = sum(max(0, len(rows[r][1]) - u) for r in range(n)); cons = True
                    for r in range(n):
                        A = np.array(rows[r][0], dtype=np.int64).reshape(-1, u); z = np.array(rows[r][1], dtype=np.int64)
                        if nsol(A, z, 2) == 0 or nsol(A, z, 13) == 0: cons = False; break
                    mine[(aff, num, ix, off)] = (int(cons), int(cons and chk >= KMIN))
    out = subprocess.run([tool, ct, pf, "rc", str(t), str(t + 1), "4", "4", str(KMIN)], capture_output=True, text=True).stdout
    for l in out.splitlines():
        w = l.split()
        if w[0] != "H": continue
        k = (int(w[3]), w[4], int(w[5]), int(w[6])); theirs = (int(w[8]), int(w[10])); tot += 1
        if mine[k] != theirs: bad += 1; print("MISMATCH", t, k, mine[k], theirs)
    print(f"perm {t}: consistent sub-cells python {sum(v[0] for v in mine.values())} (checks>=4: {sum(v[1] for v in mine.values())})", flush=True)
print(f"HILL RECOUNT: {tot} sub-cell configs compared, {bad} mismatches")
