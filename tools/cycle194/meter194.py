"""Cycle 194 meter summary (meter192.py with per-tableau B lines pooled within the directory): per band e = round(-log26 U), pooled over
the random texts: fits, U (= exact E[S1] where U < 1), S1, and the text-level z of S1 - U. Band 0 holds capped configs and is listed only."""
import sys, glob, math
d = {}
for fn in sorted(glob.glob(sys.argv[1] + '/u*.txt')):
    ls = [l.split() for l in open(fn)]
    assert ls and ls[-1][0] == 'END', fn
    per = {}
    for w in ls:
        if w[0] == 'B':
            b = int(w[3]); x = per.setdefault(b, [0, 0, 0.0, 0.0])
            x[0] += int(w[4]); x[1] += int(w[5]); x[2] += float(w[6]); x[3] += float(w[7])
    for b, x in per.items(): d.setdefault(b, []).append(x)
for b in sorted(d):
    v = d[b]; n = len(v); F = sum(x[1] for x in v); U = sum(x[2] for x in v); S = sum(x[3] for x in v)
    diffs = [x[3] - x[2] for x in v]; mu = sum(diffs) / n; sd = math.sqrt(sum((x - mu) ** 2 for x in diffs) / max(1, n - 1))
    zs = f"z {mu / (sd / math.sqrt(n)):+.2f}" if (S > 0 and sd > 0) else "z n/a (S1 = 0)"
    print(f"band {b}: texts {n} configs {sum(x[0] for x in v)} fits {F} U {U:.6g} S1 {S:.6g} {zs}" + ("  (capped band)" if b == 0 else "") + ("  (no cycle)" if b == 25 else ""))
