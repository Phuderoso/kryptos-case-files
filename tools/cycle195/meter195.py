"""Cycle 195 meter summary (= meter193.py): per band, pooled over the random texts: configs, fits, solutions, E (exact expected solutions), and the
text-level z of (solutions - E) (per-text sums, SD across texts). Band 25 = configs without a cyclic component (always fit, E = 1)."""
import sys, glob, math
d = {}; nt = 0
for fn in sorted(glob.glob(sys.argv[1] + '/u*.txt')):
    ls = [l.split() for l in open(fn)]
    assert ls[-1][0] == 'END', fn
    nt += 1
    for w in ls:
        if w[0] == 'B': d.setdefault(int(w[2]), []).append((int(w[3]), int(w[4]), float(w[5]), float(w[6])))
print(f"texts {nt}")
for b in sorted(d):
    v = d[b]; n = len(v); F = sum(x[1] for x in v); S = sum(x[2] for x in v); E = sum(x[3] for x in v)
    diffs = [x[2] - x[3] for x in v]; mu = sum(diffs) / n; sd = math.sqrt(sum((x - mu) ** 2 for x in diffs) / max(1, n - 1))
    zs = f"z {mu / (sd / math.sqrt(n)):+.2f}" if sd > 0 else "z n/a"
    print(f"band {b}: texts {n} configs {sum(x[0] for x in v)} fits {F} sols {S:.6g} E {E:.6g} {zs}")
