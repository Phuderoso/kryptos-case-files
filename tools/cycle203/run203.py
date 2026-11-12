#!/usr/bin/env python3
import json, random, sys, time, collections
sys.path.insert(0, '.')
from wr203 import *
t0 = time.time()
res = {}
LS = range(1, 27)
# ---------- controls ----------
def plant_r1(words, key, alph, mode):
    out = []
    for w in words:
        for j, p in enumerate(w): out.append(enc(p, key[j % len(key)], alph, mode))
    return "".join(out)
def plant_r2(words, key, alph, mode):
    out = []
    for i, w in enumerate(words):
        for p in w: out.append(enc(p, key[i % len(key)], alph, mode))
    return "".join(out)
# invented example text (labelled example data), 97 letters, cribs at carved positions
W = ["DOOR", "OPENED", "AND", "WE", "WALKED", "EAST", "NORTHEAST", "UNDER", "THE", "DUST", "WE", "SAW", "A", "GREAT",
     "RUSTED", "BERLIN", "CLOCK", "STILL", "TICKING", "INSIDE", "THE", "VAULT"]
pt = "".join(W)
assert pt[21:34] == "EASTNORTHEAST" and pt[63:74] == "BERLINCLOCK", (pt.find("EASTNORTHEAST"), pt.find("BERLINCLOCK"))
pt = pt[:97]
c1 = plant_r1(W, "ABSCISSA", KA, "vig")[:97]
s = survivors(c1, "R1", [8], SEG_E, SEG_B)
hit = [x for x in s if x['alph'] == 'KA' and x['mode'] == 'vig' and x['segE'] == 'EAST|NORTHEAST' and x['segB'] == 'BERLIN|CLOCK']
okC1 = any(all("ABSCISSA"[k] == v for k, v in x['key'].items()) for x in hit)
W2 = list(W)
c2 = plant_r2(W, "PALIMPSEST", AZ, "beau")[:97]
s2 = survivors(c2, "R2", [10], SEG_E, SEG_B)
okC2 = any(x['alph'] == 'AZ' and x['mode'] == 'beau' and x['segE'] == 'EAST|NORTHEAST' and all("PALIMPSEST"[k] == v for k, v in x['key'].items()) for x in s2)
res['controls'] = dict(C1_R1_KA_vig_ABSCISSA=okC1, C1_survivors_at_L8=len(s), C2_R2_AZ_beau_PALIMPSEST=okC2, C2_survivors_at_L10=len(s2))
print("controls", res['controls'], flush=True)
assert okC1 and okC2
# ---------- K4 ----------
for rule in ("R1", "R2"):
    s = survivors(K4, rule, LS, SEG_E, SEG_B)
    byL = collections.Counter(x['L'] for x in s)
    res[f'K4_{rule}_primary'] = dict(total=len(s), byL=dict(sorted(byL.items())), minL=min(byL) if byL else None,
                                     examples=[x for x in s if x['L'] <= 13][:20])
    print(rule, "K4 primary survivors by L", dict(sorted(byL.items())), flush=True)
# secondary: all boundary sets with internal words >= 2
gE = {"|".join(map(str, b)) or "-": b for b in all_segs(13)}
gB = {"|".join(map(str, b)) or "-": b for b in all_segs(11)}
res['secondary_nsegs'] = [len(gE), len(gB)]
for rule in ("R1",):
    s = survivors(K4, rule, range(1, 14), gE, gB)
    byL = collections.Counter(x['L'] for x in s)
    res[f'K4_{rule}_secondary_minL'] = min(byL) if byL else None
    res[f'K4_{rule}_secondary_byL'] = dict(sorted(byL.items()))
    print("secondary", dict(sorted(byL.items())), time.time() - t0, flush=True)
# ---------- nulls ----------
rng = random.Random(203203)
NN = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
nullR = {r: collections.Counter() for r in ("R1", "R2")}
nullmin = {r: [] for r in ("R1", "R2")}
for i in range(NN):
    l = list(K4); rng.shuffle(l); sh = "".join(l)
    for rule in ("R1", "R2"):
        s = survivors(sh, rule, LS, SEG_E, SEG_B)
        Ls = set(x['L'] for x in s)
        for L in Ls: nullR[rule][L] += 1
        nullmin[rule].append(min(Ls) if Ls else 99)
    if time.time() - t0 > 400: break
res['nulls_done'] = i + 1
for rule in ("R1", "R2"):
    res[f'null_{rule}_frac_any_survivor_byL'] = {L: round(nullR[rule][L] / (i + 1), 4) for L in LS}
    res[f'null_{rule}_minL_hist'] = dict(sorted(collections.Counter(nullmin[rule]).items()))
res['seconds'] = round(time.time() - t0, 1)
json.dump(res, open('results203.json', 'w'), indent=1)
print(json.dumps({k: v for k, v in res.items() if 'examples' not in str(k)}, indent=0)[:4000])
