"""Cycle 226 (PREREG226) part A summary: gate T, bars per (p, kbin) from the null oracle histograms, null false-pass rates,
K4 / null passes per (model, scope, p), gate P. usage: summarize226.py WORKDIR PUBLISHED_RS_DIR OUT.json"""
import sys, glob, json, re, collections, os
W, PUB, OUT = sys.argv[1:4]
def edge(b): return -10.0 + 0.02 * (b - 1)
def parse(fn):
    X = {}; P = []; core = []
    for line in open(fn):
        if line.startswith("X "):
            a = line.split(); w = a[1]; m = a[2][6]; p = int(a[3][2:]); k = int(a[4][5:])
            X[(w, m, p, k)] = collections.Counter({int(t.split(":")[0]): int(t.split(":")[1]) for t in a[6:]})
        elif line.startswith("P "):
            a = line.split(); kv = dict(t.split("=", 1) for t in a[2:] if "=" in t); kv["model"] = a[1]; P.append(kv)
        elif not line.startswith("B "): core.append(line)
    return X, P, core
R = {"gateT": {}, "strata": {}, "cells": {}, "gateP": {}}
# gate T
for f in ("k4_direct", "k4_bank", "k4_all", "null209417_bankVQ_r10", "null209417_allVQ_r10"):
    _, _, core = parse(f"{W}/R/{f}.txt"); pub = [l for l in open(f"{PUB}/{f}.txt") if not l.startswith("B ")]
    a = [l for l in core if l[0] in "SNT"]; b = [l for l in pub if l[0] in "SNT"]
    ac = sorted(l for l in core if l[0] == "C"); bc = sorted(l for l in pub if l[0] == "C")
    R["gateT"][f] = {"SNT_identical": a == b, "n_SNT": len(a), "C_identical_sorted": ac == bc, "n_C": len(ac)}
R["gateT"]["PASS"] = all(v["SNT_identical"] and v["C_identical_sorted"] for v in R["gateT"].values())
# load
runs = {}
for fn in sorted(glob.glob(f"{W}/R/*.txt")):
    lab = os.path.basename(fn)[:-4]
    if lab == "time": continue
    runs[lab] = parse(fn)
nulls = sorted({l.split("_")[0] for l in runs if l.startswith("null")})
# bars from null oracle, pooled over model and scope
O = collections.defaultdict(collections.Counter); NH = collections.defaultdict(collections.Counter)
for lab, (X, _, _) in runs.items():
    if not lab.startswith("null"): continue
    for (w, m, p, k), c in X.items():
        if k == 0: continue
        (O if w == "oracle" else NH)[(p, k)].update(c)
bars = {}
for s in sorted(O):
    c = O[s]; n = sum(c.values()); und = c.get(0, 0); cum = 0; bb = None
    for b in range(0, 402):
        cum += c.get(b, 0)
        if cum >= 0.05 * n: bb = b; break
    ok = n >= 400 and und <= 0.05 * n and bb is not None and bb >= 1
    nh = NH[s]; nn = sum(nh.values()); fp = sum(v for b, v in nh.items() if ok and b >= bb)
    nullmax = max([b for b, v in nh.items() if b >= 1 and v], default=None)
    bars[s] = bb if ok else None
    R["strata"][f"p{s[0]}_k{s[1]}"] = {"oracle_n": n, "oracle_undef": und, "bar": round(edge(bb), 2) if ok else None,
        "null_hits": nn, "null_fp": fp, "null_fp_rate": (fp / nn if nn else None), "null_max_nc_bin_low": round(edge(nullmax), 2) if nullmax else None}
# cells
def passes(X, m, p):
    tot = bar = ps = 0
    for (w, mm, pp, k), c in X.items():
        if w != "hit" or mm != m or pp != p: continue
        n = sum(c.values()); tot += n
        if k >= 1 and bars.get((p, k)) is not None:
            bar += n; ps += sum(v for b, v in c.items() if b >= bars[(p, k)])
    return tot, bar, ps
for scope, sk in (("bank", "bank"), ("all", "all")):
    k4X, k4P, _ = runs[f"k4_{sk}"]
    for m in "VQ":
        for p in range(1, 25):
            tot, barred, kp = passes(k4X, m, p)
            if tot == 0: continue
            k4p10 = sum(1 for x in k4P if x["model"] == m and int(x["p"]) == p and int(x["perm"]) % 10 == 0 and
                        bars.get((p, 1 + (int(x["known"]) - 49) // 8)) is not None and float(x["nc"]) >= edge(bars[(p, 1 + (int(x["known"]) - 49) // 8)]))
            nv = [passes(runs[f"{nl}_{sk}VQ_r10"][0], m, p)[2] for nl in nulls]
            nt = [passes(runs[f"{nl}_{sk}VQ_r10"][0], m, p)[0] for nl in nulls]
            top = sorted([x for x in k4P if x["model"] == m and int(x["p"]) == p], key=lambda x: -float(x["nc"]))[:3]
            R["cells"][f"{m}_{scope}_p{p}"] = {"K4_hits": tot, "K4_barred": barred, "K4_pass_full": kp, "K4_pass_r10": k4p10,
                "null_hits_r10_median": sorted(nt)[len(nt)//2], "null_pass_r10": nv, "null_occ": sum(x > 0 for x in nv),
                "p_up": round((1 + sum(x >= k4p10 for x in nv)) / (len(nv) + 1), 3),
                "K4_top_P": [{k: x[k] for k in ("known", "nqnc", "nc", "qg", "pt")} for x in top]}
# direct
k4X, _, _ = runs["k4_direct"]; R["direct_hits"] = sum(sum(c.values()) for (w, m, p, k), c in k4X.items() if w == "hit")
R["P_lines"] = {lab: len(v[1]) for lab, v in runs.items()}
# gate P
gp = []
for line in open(f"{W}/gateP226.tsv"):
    a = line.rstrip("\n").split("\t"); d = {x.split("=", 1)[0]: x.split("=", 1)[1] for x in a[4:] if "=" in x}
    pid, model, scope, p = a[0], a[1], int(a[2]), int(a[3]); found = d["found"] == "1"
    if d["known"] == "<49": st = "kbin0"; ok = None
    else:
        k = 1 + (int(d["known"]) - 49) // 8; bb = bars.get((p, k))
        if bb is None: st = "unbarred"; ok = None
        elif d["nc"] == "-": st = "nc_undef"; ok = False
        else: st = "barred"; ok = float(d["nc"]) >= edge(bb)
    gp.append({"pid": pid, "model": model, "scope": scope, "p": p, "bad": d["bad"], "found": found, "known": d["known"], "nc": d["nc"], "stratum": st, "over_bar": ok})
nb = [g for g in gp if g["stratum"] in ("barred", "nc_undef") and g["found"]]
R["gateP"] = {"rows": gp, "found": sum(g["found"] for g in gp), "barred_found": len(nb), "over_bar": sum(bool(g["over_bar"]) for g in nb),
              "PASS": sum(g["found"] for g in gp) >= 19 and (len(nb) == 0 or sum(bool(g["over_bar"]) for g in nb) >= 0.9 * len(nb))}
json.dump(R, open(OUT, "w"), indent=1)
print("gateT", json.dumps(R["gateT"])); print("gateP", {k: v for k, v in R["gateP"].items() if k != "rows"})
for g in gp: print(" ", g)
for s, v in R["strata"].items(): print(s, v)
for c, v in R["cells"].items(): print(c, {k: v[k] for k in ("K4_hits", "K4_barred", "K4_pass_full", "K4_pass_r10", "null_occ", "p_up")}, "top", [(x["known"], x["nc"]) for x in v["K4_top_P"][:1]])
