"""Cycle 188 independent recount (brute force over streams; no mod-2 / mod-13 split, no dilation tables, no elimination).
For every perm row in the slice, every ordered (A, B) pair from the recount list (33 x 33; A plaintext side, B ciphertext side), both
forms: key values at the carved positions of the 24 crib slots. Order 1 on the CARVED index: every stream (c, d, seed k[0]) in Z26^3
propagated k[j] = c k[j-1] + d over j = 0..96 (numpy), projected on the 24 carved crib positions. A configuration fits under ONE error
iff some stream differs from its 24-tuple in at most one slot. Screen: random 64-bit linear hashes of the 24-tuple with slot t removed
(exact for equal tuples, so no false negatives); every hit confirmed by direct comparison (min Hamming distance <= 1).
usage: recount188.py slice.bin alpha_recount.txt texts.txt -> F lines (label row A B form)"""
import sys
import numpy as np
P = np.fromfile(sys.argv[1], dtype=np.int16).reshape(-1, 97); AL = [l.split() for l in open(sys.argv[2])]; TX = [l.split() for l in open(sys.argv[3])]
CI = list(range(21, 34)) + list(range(63, 74)); PT = "EASTNORTHEASTBERLINCLOCK"
g = np.array([(c, d, s) for c in range(26) for d in range(26) for s in range(26)], dtype=np.int64)
K = np.zeros((len(g), 97), dtype=np.int64); K[:, 0] = g[:, 2]
for j in range(1, 97): K[:, j] = (g[:, 0] * K[:, j - 1] + g[:, 1]) % 26
W = np.random.default_rng(18888).integers(1, 2**63, size=24, dtype=np.uint64)
IDX = np.array([[a.index(ch) for ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"] for a, _ in AL])          # IDX[a][letter] = index
PA = np.array([[IDX[a][ord(PT[t]) - 65] for t in range(24)] for a in range(len(AL))])
nA = len(AL)
for lab, ct in TX:
    for r in range(P.shape[0]):
        pos = [int(P[r][i]) for i in CI]; Kp = K[:, pos]; Ku = Kp.astype(np.uint64)
        h = (Ku * W).sum(1); Hm = [np.unique(h - Ku[:, t] * W[t]) for t in range(24)]
        CB = np.array([[IDX[b][ord(ct[p]) - 65] for p in pos] for b in range(nA)])
        for fm in ("vig", "beau"):
            KV = (CB[None, :, :] - PA[:, None, :]) % 26 if fm == "vig" else (CB[None, :, :] + PA[:, None, :]) % 26   # [a][b][t]
            KU = KV.astype(np.uint64); hk = (KU * W).sum(-1)
            hit = np.zeros((nA, nA), bool)
            for t in range(24): hit |= np.isin(hk - KU[:, :, t] * W[t], Hm[t])
            for a, b in zip(*np.nonzero(hit)):
                if ((Kp != KV[a, b][None, :]).sum(1)).min() <= 1: print("F", lab, r, AL[a][1], AL[b][1], fm)
    print("DONE", lab, flush=True)
