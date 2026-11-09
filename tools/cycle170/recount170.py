"""Independent numpy recount of the Porta half-cross screen (no graph colouring, no masks): for sampled perms,
build every derived ordering (alphabet, split F/E, deduplicated), and test all 24 crib pairs directly.
Also recounts periodic consistency L 1..26 (V1/V2, A/B) for every survivor. Usage: recount170.py CT all.bin alpha.bin STRIDE OFFSET"""
import sys, numpy as np
ct, pb, ab, stride, off = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5])
P = np.fromfile(pb, dtype=np.int16).reshape(-1, 97); A = np.fromfile(ab, dtype=np.uint8).reshape(-1, 26)
O = np.concatenate([A, np.concatenate([A[:, 0::2], A[:, 1::2]], axis=1)]); O = np.unique(O, axis=0)
POS = np.argsort(O, axis=1)          # POS[o, letter] = index of letter in ordering o
CP = np.array(list(range(21, 34)) + list(range(63, 74))); PL = np.array([ord(c) - 65 for c in "EASTNORTHEASTBERLINCLOCK"])
CT = np.array([ord(c) - 65 for c in ct]); surv = 0; per = np.zeros((2, 2, 27), dtype=np.int64); nperm = 0
for p in range(off, len(P), stride):
    perm = P[p].astype(int); nperm += 1; cl = CT[perm[CP]]
    ip, ic = POS[:, PL], POS[:, cl]                                   # (nord, 24)
    ok = ((ip < 13) != (ic < 13)).all(axis=1); idx = np.nonzero(ok)[0]; surv += len(idx)
    for o in idx:
        a, b = ip[o], ic[o]; h1 = np.where(a < 13, a, b); h2 = np.where(a < 13, b, a) - 13
        for v, kv in enumerate([(h2 - h1) % 13, (h2 + h1) % 13]):
            for md, ix in enumerate([CP, perm[CP]]):
                for L in range(1, 27):
                    r = {}; good = all(r.setdefault(x % L, k) == k for x, k in zip(ix, kv)); per[v, md, L] += good
print(f"RECOUNT perms {nperm} orderings {len(O)} surv_perm_ordering {surv}")
for v in range(2):
    for md in range(2): print(f"PERIODIC V{v+1}{'AB'[md]}", ' '.join(str(x) for x in per[v, md, 1:]))
