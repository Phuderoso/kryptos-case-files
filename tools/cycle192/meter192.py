"""Cycle 192 meter summary: per band, pooled over the random texts: fits, U (= exact E[S1] in bands >= 1, where U < 1 is not capped),
S1, and the text-level z of S1 - U (per-text sums, SD across texts). Band 0 contains capped configs (U >= ~0.2) and is listed only."""
import sys, glob, math
d = {}
for fn in sorted(glob.glob(sys.argv[1] + '/u*.txt')):
    ls = [l.split() for l in open(fn)]
    assert ls[-1][0] == 'END', fn
    for w in ls:
        if w[0] == 'B': d.setdefault(int(w[2]), []).append((int(w[3]), int(w[4]), float(w[5]), float(w[6])))
for b in sorted(d):
    v = d[b]; n = len(v); F = sum(x[1] for x in v); U = sum(x[2] for x in v); S = sum(x[3] for x in v)
    diffs = [x[3] - x[2] for x in v]; mu = sum(diffs) / n; sd = math.sqrt(sum((x - mu) ** 2 for x in diffs) / max(1, n - 1))
    zs = f"z {mu / (sd / math.sqrt(n)):+.2f}" if (S > 0 and sd > 0) else "z n/a (S1 = 0)"
    print(f"band {b}: texts {n} configs {sum(x[0] for x in v)} fits {F} U {U:.6g} S1 {S:.6g} {zs}" + ("  (capped band)" if b == 0 else ""))
