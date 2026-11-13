#!/usr/bin/env python3
"""Cycle 211 (PREREG211 part A): score results211_blind.json against the Voynich desk's sealed truths (opened only after the blind
results were committed, sha256 checked first).  usage: score211.py results211_blind.json truths.json OUT.json"""
import json, sys, hashlib, math
from math import comb
def _cdf(k, n, p): return sum(comb(n, i) * p**i * (1-p)**(n-i) for i in range(k + 1))
def _bis(f, lo=0.0, hi=1.0):
    for _ in range(80):
        m = (lo + hi) / 2; lo, hi = (m, hi) if f(m) else (lo, m)
    return (lo + hi) / 2
BL, TR, OUT = sys.argv[1:4]
h = hashlib.sha256(open(TR, "rb").read()).hexdigest()
assert h == "da448d894dc4225ee1f702f0c111112685a21a662e10f09af6889d2a751189b7", h
blind = {p["id"]: p for p in json.load(open(BL))["plants"]}
T = json.load(open(TR)); TMI = {"AZ vig": 0, "AZ beau": 1, "KA vig": 2, "KA beau": 3}
res = []
for t in T["plants"]:
    b = blind[t["plant"]]; assert b["ct"] == t["ciphertext"]
    assert TMI[t["form"]] == t["tm"]
    pre = f"perm={t['perm']} dir={t['dir']} tm={t['tm']} L=16 segE={t['segE']} segB={t['segB']} o1={t['o1']} o2={t['o2']} "
    hit = [l for l in b["survivors"] if pre in l]
    km = lambda l: (lambda k: len(k) == 16 and all(a == c or a == "?" for a, c in zip(k, t["key"])))(l.split("key=")[1].strip())
    ok = any(km(l) for l in hit)
    eq = [l for l in b["survivors"] if pre not in l and f"tm={t['tm']} L=16 segE={t['segE']} segB={t['segB']} o1={t['o1']} o2={t['o2']} " in l and km(l)]
    res.append(dict(plant=t["plant"], family=t["family"], form=t["form"], perm=t["perm"], dir=t["dir"], o1=t["o1"], o2=t["o2"],
                    wrap=t["o2"] >= 6, n_surv=b["n_survivor_lines"], recovered=ok, true_lines=len(hit),
                    equivalent_lines=len(eq), undetermined_key_idx=[sum(c == "?" for c in l.split("key=")[1].strip()) for l in hit]))
    print(res[-1], flush=True)
n = sum(r["recovered"] for r in res); N = len(res)
cp = (0.0 if n == 0 else _bis(lambda p: 1 - _cdf(n - 1, N, p) < 0.025), 1.0 if n == N else _bis(lambda p: _cdf(n, N, p) > 0.025))
sub = {f: [sum(r["recovered"] for r in res if r["family"] == f), sum(1 for r in res if r["family"] == f)] for f in sorted({r["family"] for r in res})}
wrap = [sum(r["recovered"] for r in res if r["wrap"]), sum(1 for r in res if r["wrap"])]
summ = dict(recovered=[n, N], cp95=cp, by_family=sub, wrap_o2ge6=wrap, gate="PASS" if n >= 19 else "FAIL", truths_sha256=h)
json.dump(dict(summary=summ, plants=res), open(OUT, "w"), indent=1); print(json.dumps(summ))
