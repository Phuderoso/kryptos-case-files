"""PREREG244 T5 (I-408): Hmax of 24 fresh nulls (209783-209806) + 12 case-229 nulls; gate T (K4, N209771); PH36; K4 rank p and z.
usage: h244.py REPO > h244.txt   (run in the rk243 output dir)"""
import sys, json, statistics as st
R = sys.argv[1]
def hmax(t):
    best = None
    for sc in ('S1', 'S2', 'S3a', 'S3b'):
        for ln in open(f'out/{t}/{sc}.txt'):
            if ln.startswith('H '):
                s = float(ln.split()[1]); best = s if best is None or s > best else best
    return best
old = json.load(open(R + '/data/cycle243/summary243.json'))
k4, n771 = hmax('K4'), hmax('N209771')
gT = abs(k4 - old['K4']['Hmax']) <= 1e-5 and abs(n771 - old['nulls']['209771']['Hmax']) <= 1e-5
print(f'gate T: K4 {k4:.5f} (case 229 {old["K4"]["Hmax"]}), N209771 {n771:.5f} (case 229 {old["nulls"]["209771"]["Hmax"]}) -> {"PASS" if gT else "FAIL"}')
fresh = {s: hmax(f'N{s}') for s in range(209783, 209807)}
for s, v in fresh.items(): print('fresh', s, f'{v:.5f}')
F = list(fresh.values()); O = old['null_Hmax']; P = F + O
for nm, L in (('fresh24', F), ('old12', O), ('pooled36', P)):
    print(f'{nm}: max {max(L):.5f} min {min(L):.5f} mean {st.mean(L):.5f} sd {st.stdev(L):.5f}')
from statistics import NormalDist
rp = (1 + sum(1 for v in P if v >= k4)) / 37; z = (k4 - st.mean(P)) / st.stdev(P)
print(f'K4 Hmax {k4:.5f}: rank p among 36 = {rp:.3f} (floor 1/37 = {1/37:.3f}); z {z:+.2f}, one-sided normal p {1-NormalDist().cdf(z):.3f} -> decided by rank:',
      'NO-SIGNAL' if rp >= 0.05 else 'FLAG')
PH = max(P); print(f'PH36 (registered Part H bar) = {PH:.5f}')
for pid, v in old['plants'].items():
    if v['gate'] == 'H': print(f'plant {pid}: score {v["score"]:.5f}  margin vs PH36 {v["score"] - PH:+.3f}  margin vs old max {v["score"] - max(O):+.3f}')
w = min(v['score'] for v in old['plants'].values() if v['gate'] == 'H')
print('weakest plant', w, '->', 'INSUFFICIENT-DISCRIMINATION at that English level' if w <= PH else f'above PH36 by {w - PH:.3f}')
json.dump(dict(gateT=gT, k4=k4, fresh=fresh, PH36=PH, rank_p=rp, z=z), open('h244.json', 'w'), indent=1)
