"""Cycle 167: independent numpy recount for shift3.c.  For one (text, layer, alphabet, form triple) it tries every shift
pair (d2, d3) in 26 x 26 and every boundary pair with all three segments non-empty (crib-index order), subtracts the shift
from each crib's key value and checks that equal residues mod 7 carry equal values.  Returns the number of boundary pairs
with at least one consistent (d2, d3)  (= shift3's n3).  No union-find, no early exits.
usage: recount167.py CT q dir ix alpha_index forms [drop]   (q = -1 for direct)"""
import sys, numpy as np
AL = np.fromfile("/home/box/kryptos_support_backup/alpha.bin", dtype=np.uint8).reshape(-1, 26)
B = None
CRIB = list(range(21, 34)) + list(range(63, 74)); PT = "EASTNORTHEASTBERLINCLOCK"
def n3(ct, q, d, ix, a, forms, drop=-1):
    global B
    if q < 0: S = list(range(97))
    else:
        if B is None: B = np.fromfile("/home/box/kryptos_support_backup/perms97.bin", dtype=np.int16).reshape(-1, 97)
        S = [int(x) for x in B[q]] if d == 0 else [int(x) for x in np.argsort(B[q])]
    inv = np.zeros(26, int); inv[AL[a]] = np.arange(26)
    rows = []
    for t, p in enumerate(CRIB):
        if t == drop: continue
        cp = S[p]; idx = cp if ix else p
        rows.append((idx, inv[ord(ct[cp]) - 65], inv[ord(PT[t]) - 65]))
    rows.sort(); n = len(rows)
    r = np.array([x[0] % 7 for x in rows]); c = np.array([x[1] for x in rows]); pp = np.array([x[2] for x in rows])
    V = [(c - pp) % 26, (c + pp) % 26]
    D2, D3 = np.meshgrid(np.arange(26), np.arange(26), indexing="ij"); D2 = D2.ravel(); D3 = D3.ravel()
    same = (r[:, None] == r[None, :])
    cnt = 0
    for e1 in range(1, n - 1):
        for e2 in range(e1 + 1, n):
            seg = np.array([0 if i < e1 else (1 if i < e2 else 2) for i in range(n)])
            v = np.array([V[int(forms[seg[i]])][i] for i in range(n)])
            sh = np.stack([np.zeros_like(D2), D2, D3], 1)[:, seg]          # (676, n)
            u = (v[None, :] - sh) % 26
            eq = (u[:, :, None] == u[:, None, :]) | ~same[None]
            if eq.all(axis=(1, 2)).any(): cnt += 1
    return cnt
if __name__ == "__main__":
    a = sys.argv
    print(n3(a[1], int(a[2]), int(a[3]), int(a[4]), int(a[5]), a[6], int(a[7]) if len(a) > 7 else -1))
