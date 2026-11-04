"""Cycle 33: score the 24 derived key letters (EASTNORTHEAST / BERLINCLOCK fragments) as English running key."""
import json, sys, glob
Q = json.load(open('/workspace/kcl/data/quadgrams.json')); q, fl = Q['q'], Q['floor']
def sc(s): return [q.get(s[i:i+4], fl) for i in range(len(s)-3)]
def score(k): a, b = k[:13], k[13:]; v = sc(a) + sc(b); return sum(v)/len(v)
for f in sys.argv[1:]:
    best = []
    for line in open(f):
        p, e, k = line.split(); best.append((score(k), int(p), int(e), k[:13] + "|" + k[13:]))
    best.sort(reverse=True); print(f, len(best), "best %.3f" % best[0][0] if best else "none", best[0][1:] if best else "")
