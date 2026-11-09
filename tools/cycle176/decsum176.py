"""Cycle 176: best decode score per text and per (model, L) band, K4 vs nulls vs plants. usage: decsum176.py decdir ctldir"""
import sys, glob, re, collections
def rows(f):
    for l in open(f):
        a = l.split()
        if not a or a[0] not in ("G", "P"): continue
        sc = float(re.search(r"score=(-?[\d.]+)", l).group(1))
        band = f"G {a[2]} {a[3]}" if a[0] == "G" else f"PG {a[2]}"
        yield a[1], band, sc, l.strip()
best = collections.defaultdict(lambda: -99); bestband = collections.defaultdict(lambda: -99); n = collections.Counter(); bad = 0; top = {}
for f in glob.glob(sys.argv[1] + "/*.txt"):
    bad += sum(l.startswith("BAD") for l in open(f))
    for lab, band, sc, l in rows(f):
        n[lab] += 1; best[lab] = max(best[lab], sc); bestband[(lab, band)] = max(bestband[(lab, band)], sc)
        if sc >= best[lab]: top[lab] = l
nulls = sorted(k for k in best if k != "k4")
print("replay BAD lines:", bad)
print("K4 fits decoded", n["k4"], "best", round(best["k4"], 3), "|", top["k4"][:200])
nv = sorted(best[k] for k in nulls)
print(f"nulls with fits {len(nulls)}/19, fits {sum(n[k] for k in nulls)}; best per null min/med/max {nv[0]:.3f}/{nv[len(nv)//2]:.3f}/{nv[-1]:.3f}; K4 rank {1+sum(x > best['k4'] for x in nv)} of {len(nv)+1}")
for band in sorted({b for (_, b) in bestband}):
    kv = bestband.get(("k4", band)); nb = [bestband[(k, band)] for k in nulls if (k, band) in bestband]
    print(f"  {band}: K4 {kv if kv is None else round(kv,3)}  nulls(n={len(nb)}) max {max(nb) if nb else '-'}")
ps = [sc for f in glob.glob(sys.argv[2] + "/dec_ctl*.txt") for lab, band, sc, l in rows(f) if sc > -5]
print("planted decodes (true fits):", len(ps), "range", min(ps), max(ps))
