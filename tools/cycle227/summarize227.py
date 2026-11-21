"""Cycle 227 summary (PREREG227): per (model, geometry file, scope, p) cell, K4 vs nulls on the same rows; I-330 NC bar (tie='?').
usage: summarize227.py WORKDIR -> summary227.json + printed table"""
import sys, json, glob, os
W = sys.argv[1]; R = W + "/R"
def parse(fn):
    S, M, G = {}, {}, {}
    for line in open(fn):
        f = line.split()
        if not f: continue
        if f[0] == "S" and f[1] == "G":
            kv = dict(t.split("=") for t in f[2:]); G[(int(kv["part"]), int(kv["lay"]))] = int(kv["hits"])
        elif f[0] == "S":
            kv = dict(t.split("=") for t in f[2:]); S[(f[1], int(kv["p"]))] = (int(kv["hits"]), int(kv["exact"]))
        elif f[0] == "M":
            kv = dict(t.split("=") for t in f[1:]); M[(kv["model"], int(kv["p"]))] = (float(kv["ncbest"]), int(kv["ncpass"]))
    return S, M, G
seeds = [l.split()[0] for l in open(W + "/nulls224.tsv")]; s12 = seeds[:12]
out = {"cells": [], "G": [], "plants": open(W + "/gateP227.tsv").read().count("found=1")}
names = {"a": open(W + "/geo227a.txt").read().split("\n"), "b": open(W + "/geo227b.txt").read().split("\n")}
lay = {g: [l.split()[0] for l in names[g] if l] for g in "ab"}
# G: direct / bank / all full scale, 20 nulls
for g in "ab":
    for sc in ("direct", "bank", "all"):
        k = parse(f"{R}/k4_{sc}_{g}.txt" if sc == "direct" else f"{R}/k4_{sc}_{g}.txt")[2]
        nl = [parse(f"{R}/null{s}_direct_{g}.txt" if sc == "direct" else f"{R}/null{s}_{sc}_G_{g}.txt")[2] for s in seeds]
        for (part, l), h in sorted(k.items()):
            nn = [x.get((part, l), 0) for x in nl]
            new = not (g == "b" and l >= 1)
            out["G"].append({"geo": lay[g][l], "part": part, "scope": sc, "k4": h, "nulls": nn, "new": new,
                             "label": ("EXACT-EXCL" if h == 0 and max(nn) == 0 else "INSUFFICIENT-DISCRIMINATION" if max(nn) > 0 and h > 0 else "K4-ONLY" if h > 0 else "NULL-ONLY")})
# V / Q
for g, models in (("a", "VQ"), ("b", "V")):
    for sc in ("direct", "bank", "all"):
        if sc == "direct":
            kf = parse(f"{R}/k4_direct_{g}.txt"); kr = kf
            nl = [parse(f"{R}/null{s}_direct_{g}.txt") for s in seeds]; scale = "full, 20 nulls"
        else:
            kf = parse(f"{R}/k4_{sc}_{g}.txt"); kr = parse(f"{R}/k4_{sc}{models}_{g}_r10.txt")
            nl = [parse(f"{R}/null{s}_{sc}{models}_{g}_r10.txt") for s in s12]; scale = "r10, 12 nulls"
        for m in models:
            for p in range(1, 25):
                kfull = kf[0].get((m, p), (0, 0))[0]; kr10 = kr[0].get((m, p), (0, 0))[0]
                nn = [x[0].get((m, p), (0, 0))[0] for x in nl]
                knc = kf[1].get((m, p), (-99, 0)); nnc = [x[1].get((m, p), (-99, 0)) for x in nl]
                cmpk = kfull if sc == "direct" else kr10
                if kfull == 0 and max(nn) == 0: lab = "EXACT-EXCL"
                elif max(nn) > 0 and (kfull > 0 or True):
                    lab = "INSUFFICIENT-DISCRIMINATION" if kfull > 0 else "EXACT-EXCL*"   # * K4 0 but nulls > 0: K4 empty, no discrimination claim beyond 'K4 0'
                else: lab = "K4-ONLY"
                pup = (1 + sum(x >= cmpk for x in nn)) / (len(nn) + 1)
                out["cells"].append({"model": m, "geo": g, "scope": sc, "p": p, "scale": scale, "k4_full": kfull, "k4_r10": kr10 if sc != "direct" else None,
                    "nulls": nn, "occ": sum(x > 0 for x in nn), "p_up": round(pup, 3), "label": lab,
                    "k4_ncbest": knc[0], "k4_ncpass": knc[1], "null_ncmax": max(x[0] for x in nnc), "null_ncpass": sum(x[1] for x in nnc)})
json.dump(out, open(W + "/summary227.json", "w"), indent=1)
# compact print: per (model, geo, scope) the EXACT-EXCL range and the rest
from itertools import groupby
for key, grp in groupby(out["cells"], key=lambda c: (c["model"], c["geo"], c["scope"])):
    grp = list(grp); ex = [c["p"] for c in grp if c["label"] == "EXACT-EXCL"]
    print(key, "EXACT-EXCL p:", (min(ex), max(ex), len(ex)) if ex else None)
    for c in grp:
        if c["label"] != "EXACT-EXCL" or c["k4_ncpass"] or c["null_ncpass"]:
            print("  p=%d %s K4 full %d r10 %s nulls %s occ %d p_up %.3f | NC K4 best %.3f pass %d; null max %.3f pass %d" % (c["p"], c["label"], c["k4_full"], c["k4_r10"], c["nulls"], c["occ"], c["p_up"], c["k4_ncbest"], c["k4_ncpass"], c["null_ncmax"], c["null_ncpass"]))
gl = [x for x in out["G"] if x["new"]]
print("G new cells:", len(gl), "labels:", {l: sum(x["label"] == l for x in gl) for l in set(x["label"] for x in gl)})
for x in out["G"]:
    if x["k4"] or max(x["nulls"]): print("  G", x)
