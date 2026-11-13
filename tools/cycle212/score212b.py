#!/usr/bin/env python3
"""Cycle 212 (PREREG212 part B, I-287): score results212b_blind.json against the Voynich desk's sealed truths (opened only after the
blind results were committed in fe71b46; sha256 checked first). Off-true lines are split into: same map (inverse twin),
crib-equivalent (map equal at all 24 crib positions; agreement count over 97 reported), other (off-target).
usage: score212b.py results212b_blind.json truths.json bank.bin OUT.json"""
import json, sys, hashlib, struct
from math import comb
def _cdf(k, n, p): return sum(comb(n, i) * p**i * (1-p)**(n-i) for i in range(k + 1))
def _bis(f, lo=0.0, hi=1.0):
    for _ in range(80):
        m = (lo + hi) / 2; lo, hi = (m, hi) if f(m) else (lo, m)
    return (lo + hi) / 2
BL, TR, BANK, OUT = sys.argv[1:5]
h = hashlib.sha256(open(TR, "rb").read()).hexdigest()
assert h == "c0e202492579741f72cd63cd3bc62b8266d4ef1e17ff69cd2440226a1283bd56", h
def smap(q, d):
    with open(BANK, "rb") as f: f.seek(q * 194); s = list(struct.unpack("<97h", f.read(194)))
    return s if d == 0 else [s.index(i) for i in range(97)]
CRIB = list(range(21, 34)) + list(range(63, 74))
blind = {p["id"]: p for p in json.load(open(BL))["plants"]}
T = json.load(open(TR)); TMI = {"AZ vig": 0, "AZ beau": 1, "KA vig": 2, "KA beau": 3}
res = []
for t in T["plants"]:
    b = blind[t["plant"]]; assert b["ct"] == t["ciphertext"]; assert TMI[t["form"]] == t["tm"]
    pre = f"perm={t['perm']} dir={t['dir']} tm={t['tm']} L=16 segE={t['segE']} segB={t['segB']} o1={t['o1']} o2={t['o2']} "
    km = lambda l: (lambda k: len(k) == 16 and all(a == c or a == "?" for a, c in zip(k, t["key"])))(l.split("key=")[1].strip())
    hit = [l for l in b["survivors"] if pre in l]; ok = any(km(l) for l in hit)
    tm = smap(t["perm"], t["dir"]); cls = collections = {"true_row": 0, "same_map": 0, "crib_equivalent": 0, "other": 0}; eqrows = {}
    for l in b["survivors"]:
        kv = dict(x.split("=", 1) for x in l.split()[1:]); q, d = int(kv["perm"]), int(kv["dir"])
        if q == t["perm"] and d == t["dir"]: cls["true_row"] += 1; continue
        m = smap(q, d)
        if m == tm: cls["same_map"] += 1
        elif all(m[i] == tm[i] for i in CRIB): cls["crib_equivalent"] += 1; eqrows[f"{q}/{d}"] = sum(m[i] == tm[i] for i in range(97))
        else: cls["other"] += 1
    und = [sum(c == "?" for c in l.split("key=")[1].strip()) for l in hit if km(l)]
    res.append(dict(plant=t["plant"], perm=t["perm"], dir=t["dir"], form=t["form"], segE=t["segE"], o1=t["o1"], o2=t["o2"],
                    n_surv=b["n_survivor_lines"], recovered=ok, true_config_lines=len(hit), line_classes=cls,
                    crib_equivalent_rows_agree97=eqrows, undetermined_key_idx_count=und))
    print(json.dumps(res[-1])[:600], flush=True)
n = sum(r["recovered"] for r in res); N = len(res)
cp = (0.0 if n == 0 else _bis(lambda p: 1 - _cdf(n - 1, N, p) < 0.025), 1.0 if n == N else _bis(lambda p: _cdf(n, N, p) > 0.025))
off = sum(r["line_classes"]["other"] for r in res)
summ = dict(recovered=[n, N], cp95=cp, off_target_lines=off, gate="PASS" if n >= 9 else "FAIL", truths_sha256=h)
json.dump(dict(summary=summ, plants=res), open(OUT, "w"), indent=1); print(json.dumps(summ))
