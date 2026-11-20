"""Cycle 224: K4 vs null tables and PREREG224 labels from R/ (counts) and RS/ (scored K4 + null 209417). usage: summarize224.py WORKDIR"""
import sys, glob, re, json, statistics as st
W = sys.argv[1]
def S(fn):
    d = {}
    for l in open(fn):
        if l.startswith("S "):
            f = l.split(); kv = dict(t.split("=") for t in f[2:])
            key = (f[1], int(kv["p"])) if "p" in kv else ("G", int(kv["part"]) * 4 + int(kv["lay"]))
            d[key] = (int(kv["hits"]), int(kv["exact"]))
    return d
nulls = [l.split()[0] for l in open(W + "/nulls224.tsv")]
out = {"G": {}, "VQ": {}}
lines = []
# G
for sc, tag in (("direct", "direct"), ("bank", "bankG"), ("all", "allG")):
    k4 = S(f"{W}/R/k4_{sc}.txt")
    for m in range(12):
        nv = [S(f"{W}/R/null{n}_{tag if sc != 'direct' else 'direct'}.txt")[("G", m)][0] for n in nulls]
        kh = k4[("G", m)][0]; mean = sum(nv) / len(nv)
        lab = "EXACT-EXCL" if kh == 0 and mean < 0.05 else ("INSUFFICIENT-DISCRIMINATION" if mean >= 0.05 else "K4 HIT")
        out["G"][f"{sc}:part{m//4}:lay{m%4}"] = {"K4": kh, "null_mean": mean, "null_max": max(nv), "label": lab}
# V / Q
for sc in ("direct", "bank", "all"):
    k4 = S(f"{W}/R/k4_{sc}.txt")
    for model in ("V", "Q"):
        for p in range(1, 25):
            if sc == "direct":
                nv = [S(f"{W}/R/null{n}_direct.txt")[(model, p)][0] for n in nulls]; scale = 1
            else:
                nv = [S(f"{W}/R/null{n}_{sc}VQ_r10.txt")[(model, p)][0] for n in nulls[:3]]; scale = 10
            kh = k4[(model, p)][0]; mean = scale * sum(nv) / len(nv)
            lab = "EXACT-EXCL" if kh == 0 and mean < 0.05 else ("INSUFFICIENT-DISCRIMINATION" if mean >= 0.05 else "K4 HIT")
            if kh > 0 and mean >= 0.05:
                rank = sum(scale * v >= kh for v in nv); lab += f" (K4 {kh} vs null x{scale} {[scale*v for v in nv]})"
            out["VQ"][f"{sc}:{model}:p{p}"] = {"K4": kh, "null_scaled": [scale * v for v in nv], "label": lab}
json.dump(out, open(W + "/labels224.json", "w"), indent=1)
for k, v in out["G"].items():
    if v["label"] != "EXACT-EXCL" or v["null_mean"] > 0: print("G", k, v)
print("G cells EXACT-EXCL:", sum(v["label"] == "EXACT-EXCL" for v in out["G"].values()), "/", len(out["G"]))
for sc in ("direct", "bank", "all"):
    for model in ("V", "Q"):
        ex = [p for p in range(1, 25) if out["VQ"][f"{sc}:{model}:p{p}"]["label"] == "EXACT-EXCL"]
        print(sc, model, "EXACT-EXCL p:", ex)
        for p in range(1, 25):
            v = out["VQ"][f"{sc}:{model}:p{p}"]
            if v["label"] != "EXACT-EXCL": print("   p", p, v["K4"], v["null_scaled"], v["label"][:28])
