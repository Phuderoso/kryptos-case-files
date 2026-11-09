"""I-133 matched null set: candidate seeds 17901, 17902, ... ; random.Random(s).shuffle(list(K4)); accept iff the mean number of
equal-letter pairs among the 24 carved crib-slot letters over the 165,782 perms (eqpairs177 definition) is within +-0.02 of
K4's; stop at 20 accepted (cap 600 candidates). usage: match133.py all.bin k4.txt out.txt"""
import sys, random, numpy as np
P = np.fromfile(sys.argv[1], dtype=np.int16).reshape(-1, 97); K4 = open(sys.argv[2]).read().strip()
CI = np.array(list(range(21, 34)) + list(range(63, 74))); iu = np.triu_indices(24, 1); PC = P[:, CI]
def eq(ct): C = np.array([ord(c) - 65 for c in ct]); X = C[PC]; return (X[:, iu[0]] == X[:, iu[1]]).sum(1).mean()
e0 = eq(K4); print(f"K4 mean_eq_pairs {e0:.4f}", file=sys.stderr); acc = []
with open(sys.argv[3], "w") as o:
    for s in range(17901, 17901 + 600):
        l = list(K4); random.Random(s).shuffle(l); ct = "".join(l); e = eq(ct)
        ok = abs(e - e0) <= 0.02; print(f"cand {s} {e:.4f} {'ACCEPT' if ok else 'reject'}", file=sys.stderr)
        if ok: acc.append(s); o.write(f"m{s} {ct} {e:.4f}\n")
        if len(acc) == 20: break
print(f"accepted {len(acc)} of {s - 17900} candidates", file=sys.stderr)
