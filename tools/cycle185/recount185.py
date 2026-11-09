"""Cycle 185 independent one-error recount (brute force; no tables, no CRT, no syndromes, no dilation, no prefilter, no elimination).
For every perm row in the slice, every (A, B) pair from the recount list (33 x 33; A plaintext side, B ciphertext side), both forms:
key values at the 24 crib slots. Order 1: every stream (c, d, seed k[21]) in Z26^3 propagated k[i] = c k[i-1] + d through 22..73; a
configuration fits strictly if some stream matches all 24 slots, and fits with slot t wild if some stream matches the 23 others
(set lookups of the 24-tuple and of the 23-tuples with t removed). Order 2 only at listed (text, row, A): every (c1, c2, d, k21, k22) in
Z26^5 by numpy, mismatch count 0 (strict) or 1 (that slot).
usage: recount185.py slice.bin alpha_recount.txt texts.txt [L2spec: label:row:A ...]  ->  F lines (label L row A B form slots)"""
import sys, itertools
import numpy as np
P = np.fromfile(sys.argv[1], dtype=np.int16).reshape(-1, 97); AL = [l.split() for l in open(sys.argv[2])]
TX = [l.split() for l in open(sys.argv[3])]; L2 = [s.split(":") for s in sys.argv[4:]]
CI = list(range(21, 34)) + list(range(63, 74)); PT = "EASTNORTHEASTBERLINCLOCK"; NA = len(AL)
def kvec(ct, row, a, b, fm):
    A, B = AL[a][0], AL[b][0]
    return tuple(((B.index(ct[P[row][i]]) - A.index(PT[t])) if fm == "vig" else (B.index(ct[P[row][i]]) + A.index(PT[t]))) % 26 for t, i in enumerate(CI))
def stream1(c, d, s):
    k = {21: s}
    for i in range(22, 74): k[i] = (c * k[i - 1] + d) % 26
    return tuple(k[i] for i in CI)
ST = [stream1(c, d, s) for c in range(26) for d in range(26) for s in range(26)]
FULL = set(ST); DROP = [set(x[:t] + x[t + 1:] for x in ST) for t in range(24)]
def slots1(K):
    if K in FULL: return "-1"
    sl = [t for t in range(24) if K[:t] + K[t + 1:] in DROP[t]]
    return ",".join(map(str, sl)) if sl else None
S2 = None
def slots2(K):
    global S2
    if S2 is None:
        g = np.array(list(itertools.product(range(26), repeat=5)), dtype=np.int16); k = {21: g[:, 3], 22: g[:, 4]}
        for i in range(23, 74): k[i] = (g[:, 0] * k[i - 1] + g[:, 1] * k[i - 2] + g[:, 2]) % 26
        S2 = np.stack([k[i] for i in CI], 1).astype(np.int8); del g, k
    mm = (S2 != np.array(K, dtype=np.int8)).sum(1)
    if (mm == 0).any(): return "-1"
    sl = sorted({int(np.nonzero(S2[r] != np.array(K, dtype=np.int8))[0][0]) for r in np.nonzero(mm == 1)[0]})
    return ",".join(map(str, sl)) if sl else None
for lab, ct in TX:
    for row in range(P.shape[0]):
        for a in range(NA):
            for b in range(NA):
                for fm in ("vig", "beau"):
                    s = slots1(kvec(ct, row, a, b, fm))
                    if s: print(f"F {lab} 1 {row} {AL[a][1]} {AL[b][1]} {fm} {s}")
    for l2, r2, a2 in L2:
        if l2 != lab: continue
        row = int(r2); a = [x[1] for x in AL].index(a2)
        for b in range(NA):
            for fm in ("vig", "beau"):
                s = slots2(kvec(ct, row, a, b, fm))
                if s: print(f"F {lab} 2 {row} {AL[a][1]} {AL[b][1]} {fm} {s}")
    print(f"DONE {lab}", flush=True)
