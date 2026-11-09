"""Cycle 167: counts per cell from run167 H lines.  H fields: lab ix configs cS_AZKA hS_AZKA cS_all hS_all cM_AZKA hM_AZKA
cM_all hM_all deg.  Cells: D (direct strict, all alphabets), D1e (24 drops summed), BA (bank A-Z/KA), BE (bank A-Z/KA
drops), BS (bank every 4000th entry, all alphabets).  Per cell: K4 value, null values, nulls with any fit (I-079 gate)."""
import sys, glob, os, collections
W = sys.argv[1] if len(sys.argv) > 1 else "/workspace/k4c167/run167"
cell = collections.defaultdict(lambda: collections.defaultdict(lambda: [0] * 11))
for fn in sorted(glob.glob(os.path.join(W, "*.txt"))):
    b = os.path.basename(fn); kind = b.split("_")[0]
    if kind not in ("D", "BA", "BE", "BS"): continue
    for l in open(fn):
        w = l.split()
        if not w: continue
        if kind == "D" and w[0].startswith("D") and w[1] == "H": k, w = "D1e", w[1:]
        elif w[0] == "H": k = kind
        else: continue
        v = list(map(int, w[3:])); acc = cell[k][w[1]]
        for i, x in enumerate(v): acc[i] += x
names = ["configs", "cS_AZKA", "hS_AZKA", "cS_all", "hS_all", "cM_AZKA", "hM_AZKA", "cM_all", "hM_all", "deg"]
for k in ["D", "D1e", "BA", "BE", "BS"]:
    if k not in cell: continue
    labs = sorted(cell[k]); nulls = [l for l in labs if l != "K4"]
    print(f"== {k}: {len(labs)} texts")
    for i, nm in enumerate(names):
        vals = {l: cell[k][l][i] for l in labs}
        nz = sum(1 for l in nulls if vals[l] > 0)
        print(f"  {nm:8s} K4 {vals.get('K4', '-')}  nulls {sorted(vals[l] for l in nulls)}  nulls>0: {nz}/{len(nulls)}")
