"""Cycle 182 independent recount (numpy brute force; no tables, no CRT, no syndromes, no nesting shortcut).
For every perm row in the slice, every (A, B) pair from the recount list (33 x 33, A = plaintext side, B = ciphertext side), both
forms: key values at the 24 crib slots; order L = 1: every (c, d) in Z26^2, seed k[21], propagate k[i] = c k[i-1] + d through 22..73
and compare at all 24 slots. Order L = 2 only at listed (text, row, A): every (c1, c2, d) in Z26^3, seed k[21], k[22].
usage: recount182.py slice.bin alpha_recount.txt texts.txt [L2spec: label:row:A ...]   ->  F lines (label L row A B form)"""
import sys, itertools
import numpy as np
P = np.fromfile(sys.argv[1], dtype=np.int16).reshape(-1, 97); AL = [l.split() for l in open(sys.argv[2])]
TX = [l.split() for l in open(sys.argv[3])]; L2 = [s.split(":") for s in sys.argv[4:]]
CI = list(range(21, 34)) + list(range(63, 74)); PT = "EASTNORTHEASTBERLINCLOCK"
IX = np.array([[a.index(ch) for ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"] for a, _ in AL])   # IX[alphabet, letter] = index
NA = len(AL); pidx = np.array([IX[:, ord(ch) - 65] for ch in PT]).T                     # NA x 24
def keys(ct, row):
    cl = np.array([ord(ct[P[row][i]]) - 65 for i in CI]); cidx = IX[:, cl]                # NA x 24 (B side)
    kv = (cidx[None, :, :] - pidx[:, None, :]) % 26; kb = (cidx[None, :, :] + pidx[:, None, :]) % 26
    return {"vig": kv, "beau": kb}                                                         # [A, B, slot]
def fits(k, L, cs):
    """k: (..., 24); cs: array (M, L+1) of (c1..cL, d); returns bool (..., M)"""
    full = {CI[t]: k[..., t] for t in range(24)}; s = {}
    for j in range(L): s[21 + j] = full[21 + j][..., None] * np.ones(len(cs), dtype=np.int64)
    ok = np.ones(k.shape[:-1] + (len(cs),), dtype=bool)
    for i in range(21 + L, 74):
        v = cs[:, L].copy() + sum(cs[:, j] * s[i - 1 - j] for j in range(L)); v = v % 26; s[i] = v
        if i in full: ok &= v == full[i][..., None]
    return ok
C1 = np.array(list(itertools.product(range(26), repeat=2))); C2 = np.array(list(itertools.product(range(26), repeat=3)))
for lab, ct in TX:
    for row in range(P.shape[0]):
        K = keys(ct, row)
        for fm, k in K.items():
            ok = fits(k, 1, C1).any(-1)
            for a, b in zip(*np.nonzero(ok)): print(f"F {lab} 1 {row} {AL[a][1]} {AL[b][1]} {fm}")
    for l2, r2, a2 in L2:
        if l2 != lab: continue
        row = int(r2); a = [x[1] for x in AL].index(a2); K = keys(ct, row)
        for fm, k in K.items():
            ok = fits(k[a], 2, C2).any(-1)
            for b in np.nonzero(ok)[0]: print(f"F {lab} 2 {row} {AL[a][1]} {AL[b][1]} {fm}")
    print(f"DONE {lab}", flush=True)
