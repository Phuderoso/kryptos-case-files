"""Cycle 198 summary (aggregation fixed before the run): per stage x solver, full-power cells (cell U <= 0.05) and their fits vs U, strict
fits there; low-power cells: searched-config fits vs their U and strict fits vs configs; list of full-power fits (to decode).
usage: summarize198.py run_dir"""
import sys, glob, collections
D = sys.argv[1]
st = collections.OrderedDict()
cells = collections.defaultdict(lambda: [0, 0, 0, 0.0, 0, 0, 0.0])
for fn in [f"{D}/k4_dir.txt"] + sorted(glob.glob(f"{D}/k4_decM98_*.txt")) + sorted(glob.glob(f"{D}/k4_decM96_*.txt")):
    stage = "direct" if "dir" in fn else ("decM98" if "M98" in fn else "decM96")
    for l in open(fn):
        w = l.split()
        if w[0] != "H": continue
        key = (stage, w[1], w[3], w[4], w[5], w[6], w[7]); c = cells[key]
        for i, x in enumerate(w[8:15]): c[i] += float(x) if i in (3, 6) else int(x)
agg = collections.defaultdict(lambda: [0, 0, 0, 0.0, 0, 0, 0.0, 0, 0])
for k, c in cells.items():
    a = agg[(k[0], k[1])]
    if c[3] <= 0.05: a[0] += 1; a[1] += c[1]; a[2] += c[2]; a[3] += c[3]
    else: a[4] += 1; a[5] += c[5]; a[6] += c[6]; a[7] += c[2]; a[8] += c[0]
for (s, sv), a in agg.items():
    print(f"{s} {sv}: full-power cells {a[0]}, fits {a[1]} (strict {a[2]}) vs U {a[3]:.3f} | low-power cells {a[4]}: searched fits {a[5]} vs U {a[6]:.1f}, strict fits {a[7]} of {a[8]} configs")
full = {k for k, c in cells.items() if c[3] <= 0.05}
print("FULL-POWER FITS:")
for fn in [f"{D}/k4_dir.txt"] + sorted(glob.glob(f"{D}/k4_decM9*_*.txt")):
    stage = "direct" if "dir" in fn else ("decM98" if "M98" in fn else "decM96")
    for l in open(fn):
        w = l.split()
        if w[0] == "M" and (stage, w[1], w[5] if w[5] != "D" else "D", w[6], w[7], w[8], w[9]) in full: print(stage, l.strip())
