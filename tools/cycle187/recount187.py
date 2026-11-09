"""Cycle 187 independent recount (brute force; no mod-2 / mod-13 split, no tables, no hashing of words, no elimination).
For every perm row in the slice, every ordered (A, B) pair from the recount list (33 x 33; A plaintext side, B ciphertext side), both
forms: key values at the carved positions of the 24 crib slots. Order 1 on the CARVED index: every stream (c, d, seed k[0]) in Z26^3
propagated k[j] = c k[j-1] + d over j = 0..96 (numpy), projected on the 24 carved crib positions; a configuration fits iff its
24-tuple is in that row's stream set.   usage: recount187.py slice.bin alpha_recount.txt texts.txt -> F lines (label row A B form)"""
import sys
import numpy as np
P = np.fromfile(sys.argv[1], dtype=np.int16).reshape(-1, 97); AL = [l.split() for l in open(sys.argv[2])]; TX = [l.split() for l in open(sys.argv[3])]
CI = list(range(21, 34)) + list(range(63, 74)); PT = "EASTNORTHEASTBERLINCLOCK"
g = np.array([(c, d, s) for c in range(26) for d in range(26) for s in range(26)], dtype=np.int64)
K = np.zeros((len(g), 97), dtype=np.int64); K[:, 0] = g[:, 2]
for j in range(1, 97): K[:, j] = (g[:, 0] * K[:, j - 1] + g[:, 1]) % 26
IDX = [{ch: i for i, ch in enumerate(a)} for a, _ in AL]
for lab, ct in TX:
    for r in range(P.shape[0]):
        pos = [int(P[r][i]) for i in CI]; ST = set(map(tuple, K[:, pos].tolist()))
        for a in range(len(AL)):
            pa = [IDX[a][PT[t]] for t in range(24)]
            for b in range(len(AL)):
                cb = [IDX[b][ct[p]] for p in pos]
                for fm in ("vig", "beau"):
                    kv = tuple((cb[t] - pa[t]) % 26 if fm == "vig" else (cb[t] + pa[t]) % 26 for t in range(24))
                    if kv in ST: print("F", lab, r, AL[a][1], AL[b][1], fm)
    print("DONE", lab, flush=True)
