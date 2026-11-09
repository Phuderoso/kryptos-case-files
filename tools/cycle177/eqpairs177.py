"""Cycle 177 diagnostic for the C2 flag: per text, the distribution over the 165,782 perms of the number of equal-letter pairs
among the 24 carved crib-slot letters (the constraints of the partition test). Fewer equal pairs -> fewer constraints -> more
one-error fits for any key. usage: eqpairs177.py all.bin k4.txt nulls177.txt"""
import sys, numpy as np
P = np.fromfile(sys.argv[1], dtype=np.int16).reshape(-1, 97)
CI = np.array(list(range(21, 34)) + list(range(63, 74)))
texts = [("k4", open(sys.argv[2]).read().strip())] + [tuple(l.split()) for l in open(sys.argv[3])]
iu = np.triu_indices(24, 1)
for lab, ct in texts:
    C = np.array([ord(c) - 65 for c in ct]); X = C[P[:, CI]]
    e = (X[:, iu[0]] == X[:, iu[1]]).sum(1)
    print(lab, f"mean_eq_pairs {e.mean():.4f}", "frac<=6", f"{(e<=6).mean():.4f}", "frac<=4", f"{(e<=4).mean():.4f}")
