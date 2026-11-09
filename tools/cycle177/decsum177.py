"""Cycle 177 decode summary: per text and run group, number of decoded fits, best / median score, fixed-letter range, and the
per-text best over all groups (I-131: score printed with the number of fixed alphabet letters).  usage: decsum177.py decdir"""
import sys, glob, re, collections
rows = collections.defaultdict(list)
for f in sorted(glob.glob(sys.argv[1] + "/*.dec")):
    lab, grp = f.split("/")[-1].split(".")[:2]
    for l in open(f):
        if l[:2] not in ("G ", "P "): continue
        s = float(re.search(r"score=(-?[\d.]+)", l).group(1)); m = re.search(r"fixed=(\d+)", l); fx = int(m.group(1)) if m else 26
        L = re.search(r" L(\d+) ", l); rows[(lab, grp)].append((s, fx, int(L.group(1)) if L else 0, l.strip()))
best = collections.defaultdict(lambda: (-99, ""))
for (lab, grp), v in sorted(rows.items()):
    v.sort(reverse=True); sc = [x[0] for x in v]; fx = [x[1] for x in v]
    print(f"{lab:7s} {grp:4s} n={len(v):4d} best={sc[0]:.3f} median={sc[len(sc)//2]:.3f} fixed {min(fx)}-{max(fx)}")
    if sc[0] > best[lab][0]: best[lab] = (sc[0], v[0][3])
print("== per-text best")
for lab, (s, l) in sorted(best.items(), key=lambda x: -x[1][0]): print(f"{lab:7s} {s:.3f}  {l[:200]}")
