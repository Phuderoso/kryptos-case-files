#!/usr/bin/env python3
"""ladder240.py (PREREG240, I-371, tier 1): partial-English ladder priced against two bars, no search.
Levels f in {0, .3, .4, .5, .6, .7, .8, .9, 1}, models S / B, R = 500 replicates per cell, rng = random.Random(209718) in that
loop order (model outer, f, replicate). A replicate passes a bar if NC(planted plaintext) >= bar. This is the pass rate GIVEN
recovery of the planted configuration (the tool's per-text max can only be >= the planted line; other lines pass at the null rate).
Bars (frozen): B218 = bar(64, N=343) of case 218 (betas summary232.json, k_text 0.8788963), N = case 221 K4 unit N;
               BSH  = B218 - 0.2388112 (case 221 Hodges-Lehmann family shift; 'family-shifted bar').
Writes ladder240.tsv (one row per replicate) and ladder240.json; prints the table."""
import random, math, json
from partial240 import *
B = json.load(open('summary232.json')); beta = B['fit']['beta']; KT = B['bar']['k_text']
def fit(n, q): x = math.log(max(n, 10)); return beta[0] + beta[1] * x + beta[2] * x * x + beta[3] * q
B218 = fit(343, 64) + KT; SHIFT = 0.23881117221901338; BSH = B218 - SHIFT
def wilson(k, n, z=1.959964):
    ph = k / n; d = 1 + z * z / n; c = (ph + z * z / (2 * n)) / d; h = z * math.sqrt(ph * (1 - ph) / n + z * z / (4 * n * n)) / d
    return (round(max(0.0, c - h), 4), round(min(1.0, c + h), 4))
F = [0.0, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]; R = 500; rng = random.Random(209718); eng = eng_text()
out = {'B218': B218, 'BSH': BSH, 'cells': []}; fh = open('ladder240.tsv', 'w')
print(f'B218 {B218:.5f}  BSH {BSH:.5f}  (N 343, nq 64)')
for model in 'SB':
    for f in F:
        ncs = []
        for r in range(R):
            pt, m = partial(base_pt(eng, rng), f, model, rng); v = nc(pt); ncs.append(v)
            fh.write(f'{model}\t{f}\t{r}\t{m}\t{v:.5f}\t{pt}\n')
        k1 = sum(v >= B218 for v in ncs); k2 = sum(v >= BSH for v in ncs); s = sorted(ncs)
        c = dict(model=model, f=f, m=round(f * 73), p218=k1 / R, w218=wilson(k1, R), psh=k2 / R, wsh=wilson(k2, R), d=(k2 - k1) / R,
                 q05=s[int(0.05 * R)], med=s[R // 2], q95=s[int(0.95 * R) - 1])
        c['disjoint'] = c['wsh'][0] > c['w218'][1]; out['cells'].append(c)
        print(f"{model} f {f:.1f} m {c['m']:2d}  NC med {c['med']:.3f} [{c['q05']:.3f}, {c['q95']:.3f}]  pass218 {c['p218']:.3f} {c['w218']}  passSH {c['psh']:.3f} {c['wsh']}  delta {c['d']:+.3f}{' DISJOINT' if c['disjoint'] else ''}")
def f50(model, key):
    pts = [(c['f'], c[key]) for c in out['cells'] if c['model'] == model]
    for (f0, p0), (f1, p1) in zip(pts, pts[1:]):
        if p0 < 0.5 <= p1: return f0 + (0.5 - p0) * (f1 - f0) / (p1 - p0)
    return None
for model in 'SB':
    a, b = f50(model, 'p218'), f50(model, 'psh'); out[f'f50_{model}'] = (a, b)
    print(f"model {model}: f50 bar218 {a}  f50 shifted {b}  price {None if a is None or b is None else round(a - b, 3)} of the 73 non-crib letters")
md = max(c['d'] for c in out['cells'])
lab = ('COSTLY' if any(c['d'] >= 0.10 and c['disjoint'] for c in out['cells']) else 'NEGLIGIBLE' if md < 0.05 else 'FRONTEIRA')
out['verdict'] = lab; out['max_delta'] = md
print(f'L1 verdict: {lab} (max delta {md:+.3f})')
json.dump(out, open('ladder240.json', 'w'), indent=1)
