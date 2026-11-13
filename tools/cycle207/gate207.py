#!/usr/bin/env python3
"""Cycle 207 (PREREG207): stratified L 16 plant gate for wrbank (case 193). Invented plaintexts, not K4 guesses.
usage: gate207.py WRBANK BANK OUT.json"""
import json, random, re, struct, subprocess, sys, time, os
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from k4_autokey_trans import family
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"; N = 97
BIN, BANK, OUT = sys.argv[1:4]
HEAD = ["AND", "THE", "GREY", "LIGHT", "TURNED"]
MID = ["OVER", "THE", "WALL", "AND", "A", "MAN", "STOOD", "BY", "THAT"]
TAIL = ["WAITING", "FOR", "THE", "SIGNAL", "AT", "MIDNIGHT", "IN", "THE", "SQUARE", "NEAR", "HIM"]
TPL = {"M": HEAD + ["EAST", "NORTHEAST"] + MID + ["BERLIN", "CLOCK"] + TAIL,
       "A": HEAD + ["EASTNORTH", "EAST"] + MID + ["BERLINCLOCK"] + TAIL}
SEG = {"M": ("EAST|NORTHEAST", "BERLIN|CLOCK"), "A": ("EASTNORTH|EAST", "BERLINCLOCK")}
TMS = [(AZ, "vig", 0), (AZ, "beau", 1), (KA, "vig", 2), (KA, "beau", 3)]
def widths_of(tag):   # as in the Voynich desk's followup_blocks.py
    if tag == "identity": return ()
    t = tag[:-3] if tag.endswith("^-1") else tag
    if t.startswith("col"): return (int(t[3]),)
    if t.startswith("rot"): return tuple(int(x) for x in re.findall(r"\((\d+),", t))
    raise ValueError(tag)
def enc(words, alph, mode, key):
    out = []
    for w in words:
        for j, p in enumerate(w):
            k = alph.index(key[j % len(key)]); pi = alph.index(p)
            out.append(alph[(pi + k) % 26] if mode == "vig" else alph[(k - pi) % 26])
    return "".join(out)[:N]
t0 = time.time()
bank = np.fromfile(BANK, dtype="<i2").reshape(-1, N)
tagged = [(np.arange(N, dtype=np.int16), "identity")] + list(family(97))
assert len(tagged) == bank.shape[0] and all(np.array_equal(bank[i], p) for i, (p, _) in enumerate(tagged))
W = [widths_of(t) for _, t in tagged]
popM = [i for i in range(len(W)) if W[i] and any(b % w for b in (25, 69) for w in W[i])]
popA = [i for i in range(len(W)) if W[i] and all(30 % w == 0 for w in W[i])]
for s in ("M", "A"):
    p = "".join(TPL[s]); assert p[21:34] == "EASTNORTHEAST" and p[63:74] == "BERLINCLOCK"
rng = random.Random(206207)
plan = []
for s, n, L in (("M", 20, 16), ("A", 20, 16), ("M", 5, 17)):
    pop = popM if s == "M" else popA
    for i in range(n):
        plan.append(dict(stratum=s, L=L, tm=TMS[i % 4][2], q=rng.choice(pop), dir=rng.randrange(2),
                         key="".join(rng.choice(AZ) for _ in range(L))))
res = []
for pl in plan:
    alph, mode, tm = TMS[pl["tm"]]; q, d, L, key = pl["q"], pl["dir"], pl["L"], pl["key"]
    lay = enc(TPL[pl["stratum"]], alph, mode, key)
    s = [int(x) for x in bank[q]]
    S = s if d == 0 else [0] * N
    if d == 1:
        for i in range(N): S[s[i]] = i
    C = [None] * N
    for i in range(N): C[S[i]] = lay[i]
    ct = "".join(C)
    out = subprocess.run([BIN, ct, BANK, str(L), str(L), "1000000"], capture_output=True, text=True, timeout=120).stdout
    surv = [l for l in out.splitlines() if l.startswith("S ")]
    segE, segB = SEG[pl["stratum"]]
    hit = [l for l in surv if f"perm={q} dir={d} tm={tm} L={L} segE={segE} segB={segB} o1=0 o2=0 " in l]
    def km(l):
        k = l.split("key=")[1].strip(); return len(k) == L and all(a == b or a == "?" for a, b in zip(k, key))
    ok = bool(hit) and any(km(l) for l in hit)
    tot = [l for l in out.splitlines() if l.startswith("T ")][0]
    r = dict(pl, tag=tagged[q][1], widths=list(W[q]), survivors=len(surv), recovered=ok, total_line=tot)
    res.append(r); print(r["stratum"], L, q, d, tm, r["tag"], "surv", len(surv), "REC" if ok else "MISS", flush=True)
def cnt(s, L): return sum(r["recovered"] for r in res if r["stratum"] == s and r["L"] == L), sum(1 for r in res if r["stratum"] == s and r["L"] == L)
summ = {"M16": cnt("M", 16), "A16": cnt("A", 16), "M17": cnt("M", 17), "popM": len(popM), "popA": len(popA),
        "seed": 206207, "next_free_seed": 206208, "wall_s": round(time.time() - t0, 1)}
summ["gate"] = "PASS" if summ["M16"][0] >= 19 and summ["A16"][0] >= 19 else "FAIL"
json.dump({"summary": summ, "plants": res}, open(OUT, "w"), indent=1)
print(json.dumps(summ))
