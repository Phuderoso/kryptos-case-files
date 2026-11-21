#!/usr/bin/env python3
"""Cycle 231 analysis (PREREG231). From w/. Gate P on plants231.tsv; fresh-null tables vs the published c230 K4 files (data/cycle230/R)."""
import sys, glob, collections
sys.path.insert(0,'../src'); import analyze230 as a
K4DIR = sys.argv[1] if len(sys.argv) > 1 else "/workspace/k4c230/w/R"
def cnt(lines, crit): return sum(1 for l in lines if (l[5] <= 9 if crit == "W9" else l[5] <= 10))
# cluster rule = clus230.clusters
exec(open('../src/clus230.py').read().split("for crit,fl")[0].replace("import sys; sys.path.insert(0,'../src'); import analyze230 as a",""))
def gateP():
    rows = [l.rstrip("\n").split("\t") for l in open("plants231.tsv")]; ok = 0
    for pid, fam, q, d, xi, yi, form, typ, size, ct, pt in rows:
        q, d, xi, yi, form = int(q), int(d), int(xi), int(yi), int(form)
        lines, T = a.parse(f"P/{pid}.txt"); off = int(open(f"P/{pid}.off").read()) if fam != "direct" else 0
        truth = (q - off if fam != "direct" else -1, d, xi, yi, form); rec = any(l[:5] == truth for l in lines); ok += rec
        print("PLANT", pid, fam, typ, size, "found" if rec else "MISSED", "lines", len(lines))
    print(f"GATE P recovered {ok}/{len(rows)} Wilson {a.wilson(ok, len(rows))} (pass >= 19/20)")
def tables():
    for sc, nn, scale, in (("direct", 8, 5), ("bank", 20, 20), ("all", 20, 20)):
        k4all = a.parse(f"{K4DIR}/k4_{sc}.txt")[0]
        for crit, fl in (("W9", lambda l: l[5] <= 9), ("W10", lambda l: l[5] <= 10)):
            k4f = [l for l in k4all if fl(l)]
            if sc == "direct": sl = [l for l in k4f if l[2] % 5 == 0]       # slice X%5==0 = null slice offset 0 (any offset equivalent by design)
            else: sl = [l for l in k4f if (l[0] % 20) == 0] 
            nl = [[l for l in a.parse(f"R/null{i}_{sc}.txt")[0] if fl(l)] for i in range(nn)]
            nraw = [len(x) for x in nl]; ncl = [clusters(x) if x else 0 for x in nl]
            # K4 slice mean over all offsets (exact by pooling): K4 full / scale
            print(f"{sc} {crit} K4 full raw {len(k4f)} clusters {clusters(k4f)} | K4 per-slice mean raw {len(k4f)/scale:.2f} | fresh nulls n={nn} raw {nraw} clusters {ncl} | null mean raw {sum(nraw)/nn:.2f} cl {sum(ncl)/nn:.2f} | null-equivalent full-scale raw {sum(nraw)*scale/nn:.1f} cl {sum(ncl)*scale/nn:.1f} | nulls with >=1: {sum(1 for x in nraw if x)}/{nn}")
if __name__ == "__main__": gateP(); tables()
