"""Cycle 172 summary: per text and cell (ix, p) the number of configurations with >= 1 Quagmire IV pair and the number of pairs,
from M/S lines; H lines give configs, prefilter pass and the chance expectation 2*nu*(nu-1)*25^-m summed over passing configs.
K4 is reported on the full family and on the same every-4th subset as the nulls (q % 4 == 0)."""
import sys, glob, collections, statistics as st
D = sys.argv[1]
def load(lab):
    H = collections.defaultdict(lambda: [0, 0, 0.0]); cfg = collections.defaultdict(set); cfg4 = collections.defaultdict(set)
    pairs = collections.Counter(); pairs4 = collections.Counter(); ends = 0
    for f in sorted(glob.glob(f"{D}/{lab}.c*.txt")):
        for l in open(f):
            t = l.split()
            if t[0] == "H": k = (int(t[2]), int(t[3])); H[k][0] += int(t[4]); H[k][1] += int(t[5]); H[k][2] += float(t[10])
            elif t[0] in "MS":
                q, ix, p = int(t[2]), int(t[3]), int(t[4]); n = 1 if t[0] == "M" else int(t[6]); k = (ix, p)
                cfg[k].add(q); pairs[k] += n
                if q % 4 == 0: cfg4[k].add(q); pairs4[k] += n
            elif t[0] == "END": ends += 1
    return H, cfg, pairs, cfg4, pairs4, ends
k4 = load("k4"); nulls = {f"null{i}": load(f"null{i}") for i in range(8)}
print("chunks finished: k4 %d/16; nulls %s" % (k4[5], " ".join(str(v[5]) for v in nulls.values())))
print("cell | K4 full: configs pass cfg>=1 pairs expected | K4 every-4th: cfg>=1 pairs | 8 nulls every-4th cfg>=1 (pairs) | nulls expected (mean)")
for ix in (0, 1):
    for p in range(1, 17):
        k = (ix, p); H = k4[0][k]
        nc = [len(v[1][k]) for v in nulls.values()]; npairs = [v[2][k] for v in nulls.values()]; ne = [v[0][k][2] for v in nulls.values()]
        print(f"ix{ix} p{p:2d} | {H[0]} {H[1]} {len(k4[1][k])} {k4[2][k]} {H[2]:.3g} | {len(k4[3][k])} {k4[4][k]} | "
              + " ".join(f"{a}({b})" for a, b in zip(nc, npairs)) + f" | {st.mean(ne):.3g}")
