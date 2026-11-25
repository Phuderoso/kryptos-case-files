#!/usr/bin/env python3
"""Cycle 240 analysis (PREREG240, I-371). Frozen before the run.
Bars: bar218(N) = fit(64, N) + 0.8788963 (case 218); barSH(N) = bar218(N) - 0.2388112 (case 221 family shift).
Tier 2 plants (gate P): recovered <=> an H line with the planted (perm, dir, ix, X, Y, form) and the planted window key, and its pt
  differs from the planted plaintext in <= 1 position (0 for clean plants). Gate P PASS if >= 18/20 recovered.
  Per plant: NC of the planted line vs bar218(343) / barSH(343) (as gate P in case 221), compared with the tier-1 cell rate.
  I-386: every OTHER H line with NC >= barSH(343) is traced: Hamming distance of its window key to the planted key over the 97
  values; <= 10 = neighbour pass (expected, not a false pass), > 10 = other.
Nulls (H3): unit (text, nq 64) pooled over direct full / bank r10 / all r10. Shifted-bar per-text passes k/12:
  HOLDS (not too permissive at this resolution) if k <= 2 (P(>=3 | 1/21) = 0.017); robust if each set <= 1/6; REJECTED if k >= 3.
  bar218 passes on the same nulls reported (fresh replication of case 221 H1). Descriptive: R_t of the 12 vs case 221's 24 nulls
  (two-sided exact Mann-Whitney), i.e. whether the family shift replicates on fresh nulls.
usage: analyze240.py WORKDIR"""
import sys, re, json, math
import numpy as np
from scipy.stats import mannwhitneyu
W = sys.argv[1]
B = json.load(open(W + '/summary232.json')); beta = B['fit']['beta']; KT = B['bar']['k_text']; SH = 0.23881117221901338
def fit(N, q=64): x = math.log(max(N, 10)); return beta[0] + beta[1] * x + beta[2] * x * x + beta[3] * q
def b218(N): return fit(N) + KT
def bsh(N): return b218(N) - SH
def wilson(k, n, z=1.959964):
    if n == 0: return (0.0, 1.0)
    ph = k / n; d = 1 + z * z / n; c = (ph + z * z / (2 * n)) / d; h = z * math.sqrt(ph * (1 - ph) / n + z * z / (4 * n * n)) / d
    return (round(max(0.0, c - h), 4), round(min(1.0, c + h), 4))
L = json.load(open(W + '/ladder240.json')); cell = {(c['model'], c['f']): c for c in L['cells']}
K = open(W + '/keys233.bin', 'rb').read(); kw = lambda w: K[int(w) * 97:(int(w) + 1) * 97]
S = {'plants': []}; NK = 343
print(f'bar218(343) {b218(NK):.5f}  barSH(343) {bsh(NK):.5f}')
for l in open(W + '/plants240.tsv'):
    pid, scope, ct, qi, dr, ix, x, y, f, w, bad, fl, mo, m, pt = l.rstrip('\n').split('\t'); kp = kw(w)
    best = None; nl = 0; nb = {'nb': 0, 'other': 0, 'nb_maxnc': None, 'other_maxnc': None, 'hd': []}
    for h in open(f'{W}/P/p{pid}.txt'):
        if not h.startswith('H'): continue
        nl += 1; d = dict(kv.split('=') for kv in h.split()[1:]); v = float(d['nc'])
        same = (int(d['perm']) == int(qi) and int(d['X']) == int(x) and int(d['Y']) == int(y) and int(d['form']) == int(f)
                and kw(d['w']) == kp and (scope == 'direct' or (int(d['dir']) == int(dr) and int(d['ix']) == int(ix))))
        diff = sum(a != b for a, b in zip(d['pt'], pt))
        if same and diff <= (1 if int(bad) >= 0 else 0):
            if best is None or v > best[0]: best = (v, diff)
        elif v >= bsh(NK):
            hd = sum(a != b for a, b in zip(kw(d['w']), kp)); key = 'nb' if hd <= 10 else 'other'; nb[key] += 1; nb['hd'].append(hd)
            nb[key + '_maxnc'] = v if nb[key + '_maxnc'] is None else max(nb[key + '_maxnc'], v)
    c = cell[(mo, float(fl))]
    r = dict(pid=int(pid), scope=scope, f=float(fl), model=mo, bad=int(bad), lines=nl, rec=best is not None,
             nc=best[0] if best else None, p218=bool(best and best[0] >= b218(NK)), psh=bool(best and best[0] >= bsh(NK)),
             cell_p218=c['p218'], cell_psh=c['psh'], trace=nb)
    S['plants'].append(r)
    print(f"plant {pid:>2} {scope:6s} f {fl} {mo} bad {int(bad):3d} lines {nl:5d} rec {int(r['rec'])} NC {r['nc'] if r['nc'] is not None else float('nan'):8.4f} "
          f"218 {'P' if r['p218'] else '-'} SH {'P' if r['psh'] else '-'} (cell {c['p218']:.2f}/{c['psh']:.2f})  other>=barSH: nb<=10 {nb['nb']} other {nb['other']} hd {sorted(set(nb['hd']))[:6]}")
g = sum(p['rec'] for p in S['plants']); g1 = sum(p['rec'] for p in S['plants'] if p['bad'] >= 0)
S['gateP'] = g; print(f"Gate P recovered {g}/20 Wilson {wilson(g,20)} (one-error {g1}/10) -> {'PASS' if g >= 18 else 'FAIL'}")
YRE = re.compile(r'^Y nq=64 n=(\d+) max=(-?[\d.]+)'); FILES = ('direct', 'bank_r10', 'all_r10')
def unit(tag):
    N, mx, per = 0, -99.0, {}
    for f in FILES:
        for l in open(f'{W}/R/{tag}_{f}.txt'):
            mm = YRE.match(l)
            if mm: n, v = int(mm[1]), float(mm[2]); per[f] = (n, v); N += n; mx = max(mx, v) if n else mx
    return N, mx, per
rows = []
for l in open(W + '/nulls240.tsv'):
    seed, st, t, sha = l.rstrip('\n').split('\t'); N, mx, per = unit(f'null{seed}'); R = mx - fit(N)
    rows.append(dict(seed=int(seed), set=st, N=N, max=mx, R=R, p218=N >= 10 and mx >= b218(N), psh=N >= 10 and mx >= bsh(N), per=per))
    print(f"null {seed} {st} N {N:5d} max {mx:8.4f} R {R:+.4f} bar218 {b218(N):.4f} barSH {bsh(N):.4f} {'PASS218' if rows[-1]['p218'] else '-'} {'PASSSH' if rows[-1]['psh'] else '-'}")
k = sum(r['psh'] for r in rows); kA = sum(r['psh'] for r in rows if r['set'] == 'A'); kB = k - kA; k218 = sum(r['p218'] for r in rows)
h3 = 'HOLDS' if k <= 2 else 'REJECTED (too permissive)'; rob = kA <= 1 and kB <= 1
print(f"H3 shifted-bar passes {k}/12 Wilson {wilson(k,12)} (A {kA}/6, B {kB}/6) -> {h3}{' (robust)' if (rob and k <= 2) else ''}; bar218 passes {k218}/12 Wilson {wilson(k218,12)}")
Rn = np.array([r['R'] for r in rows]); R221 = np.array([r['R'] for r in json.load(open(W + '/summary235.json'))['nulls']])
u = mannwhitneyu(Rn, R221, alternative='two-sided', method='exact')
print(f"R_t fresh nulls median {np.median(Rn):+.4f} max {Rn.max():+.4f} | case 221 nulls median {np.median(R221):+.4f} max {R221.max():+.4f} | exact MW U {u.statistic:.1f} p {u.pvalue:.3g}")
print(f"headroom to shifted bar (k_text {KT-SH:.4f}) for best fresh null: {(KT-SH) - Rn.max():+.4f}")
S.update(nulls=rows, H3=dict(k=k, kA=kA, kB=kB, k218=k218, verdict=h3, robust=rob), MW=dict(U=float(u.statistic), p=float(u.pvalue)),
         ladder=dict(verdict=L['verdict'], max_delta=L['max_delta'], f50_S=L['f50_S'], f50_B=L['f50_B']))
json.dump(S, open(W + '/summary240.json', 'w'), indent=1, default=str)
