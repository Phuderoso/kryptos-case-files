"""Cycle 226 POST HOC (not pre-registered; flagged in case 212): for the case 209 cells, (a) the null maximum NC per text,
(b) NC of the 20 cycle 223 plants' planted cells (decrypt as analyze223.py), to measure the frozen bar's power under one crib error
and the post hoc NC >= -6.0 bar. usage: posthoc209_226.py W223 qg.bin REPO OUT.json"""
import sys, glob, json, runpy
W, QG, REPO, OUT = sys.argv[1:5]
sys.argv = ["x", W, QG, sys.argv[0].replace("posthoc209_226.py", "../w/oracle226.txt"), REPO, "/dev/null"]
import numpy as np, collections
sys.path.insert(0, f"{REPO}/tools/cycle219")
from plant219 import reading_order, KA, AZ, CRP, CRS
src = open(__file__.replace("posthoc209_226.py", "reread209_226.py")).read()
ns = {}; exec(src.split("cells = {}")[0], ns)  # defs only: S_of, decrypt, nc, kbin
texts = ns["texts"]; decrypt = ns["decrypt"]; nc = ns["nc"]
out = {"null_max_nc": {}, "plants": []}
for lab in texts:
    if not lab.startswith("null"): continue
    m = -99
    for f in glob.glob(f"{W}/out/{lab}/*.raw"):
        for line in open(f):
            a = line.split()
            if a[0] != "H": continue
            bar = a.index("|"); v = tuple(int(x) for x in a[2:11]); pi = tuple(int(x) for x in a[11:bar])
            if v[6] not in (20, 21): continue
            D = decrypt(texts[lab], v, pi); s, n = nc(D, D)
            if s is not None and 97 - D.count("?") >= 49: m = max(m, s)
    out["null_max_nc"][lab] = round(m, 3)
for pr in [l.rstrip("\n").split("\t") for l in open(f"{REPO}/data/cycle223/plants223.tsv")][1:]:
    pid, w, mode, dir_, al, form, model, per = map(int, pr[:8]); pi = tuple(int(x) for x in pr[9].split(",")); seat = int(pr[10]); ct = pr[13]
    be = 1 if form == 2 else 0; best = None
    for f in glob.glob(f"{W}/out/plant{pid}/*.raw"):
        for line in open(f):
            a = line.split()
            if a[0] != "H": continue
            bar = a.index("|"); v = tuple(int(x) for x in a[2:11]); pj = tuple(int(x) for x in a[11:bar])
            if v[:7] == (w, mode, dir_, al, be, model, per) and pj == pi:
                D = decrypt(ct, v, pj); s, n = nc(D, D); best = (s, n, 97 - D.count("?"), D); break
        if best: break
    out["plants"].append({"pid": pid, "p": per, "seat": seat, "nc": best and best[0], "nqnc": best and best[1], "known": best and best[2]})
v = sorted(out["null_max_nc"].values()); out["null_max_summary"] = {"n": len(v), "max": v[-1], "median": v[len(v)//2], "n_ge_-6.0": sum(x >= -6.0 for x in v)}
json.dump(out, open(OUT, "w"), indent=1); print(out["null_max_summary"]); [print(p) for p in out["plants"]]
