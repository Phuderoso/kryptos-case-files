#!/usr/bin/env python3
"""Cycle 241 analysis (PREREG241, I-389 + I-377(b)). Frozen before the run. Adapted from analyze240.py: ladder removed, plants 10 full-English (gate P >= 9/10),
24 fresh nulls (sets C 209731-42, D 209743-54); BSH adoption rule k <= 3/24 and each set <= 2/12; I-377(b) multiplicity reading: exact MW of the fresh
R_t vs the 20 case 218 calibration nq-64 single-unit residuals (consistent if p >= 0.05 and |HL| <= 0.15) and vs the 20 calibration R_t; one-unit bar OU0 = fit + 0.4902982 (max R_t of the 36 earlier nulls, cases 221 + 240): passes k/24, HOLDS if <= 2.
Original header follows (240).
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
usage: analyze241.py WORKDIR REPO"""
import sys, re, json, math
import numpy as np
from scipy.stats import mannwhitneyu
W = sys.argv[1]; REPO0 = sys.argv[2]
B = json.load(open(W + '/summary232.json')); beta = B['fit']['beta']; KT = B['bar']['k_text']; SH = 0.23881117221901338
def fit(N, q=64): x = math.log(max(N, 10)); return beta[0] + beta[1] * x + beta[2] * x * x + beta[3] * q
def b218(N): return fit(N) + KT
def bsh(N): return b218(N) - SH
def wilson(k, n, z=1.959964):
    if n == 0: return (0.0, 1.0)
    ph = k / n; d = 1 + z * z / n; c = (ph + z * z / (2 * n)) / d; h = z * math.sqrt(ph * (1 - ph) / n + z * z / (4 * n * n)) / d
    return (round(max(0.0, c - h), 4), round(min(1.0, c + h), 4))
K = open(W + '/keys233.bin', 'rb').read(); kw = lambda w: K[int(w) * 97:(int(w) + 1) * 97]
S = {'plants': []}; NK = 343
print(f'bar218(343) {b218(NK):.5f}  barSH(343) {bsh(NK):.5f}')
for l in open(W + '/plants241.tsv'):
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
    r = dict(pid=int(pid), scope=scope, f=float(fl), model=mo, bad=int(bad), lines=nl, rec=best is not None,
             nc=best[0] if best else None, p218=bool(best and best[0] >= b218(NK)), psh=bool(best and best[0] >= bsh(NK)),
             trace=nb)
    S['plants'].append(r)
    print(f"plant {pid:>2} {scope:6s} f {fl} {mo} bad {int(bad):3d} lines {nl:5d} rec {int(r['rec'])} NC {r['nc'] if r['nc'] is not None else float('nan'):8.4f} "
          f"218 {'P' if r['p218'] else '-'} SH {'P' if r['psh'] else '-'}  other>=barSH: nb<=10 {nb['nb']} other {nb['other']} hd {sorted(set(nb['hd']))[:6]}")
g = sum(p['rec'] for p in S['plants']); g1 = sum(p['rec'] for p in S['plants'] if p['bad'] >= 0)
S['gateP'] = g; print(f"Gate P recovered {g}/10 Wilson {wilson(g,10)} (one-error {g1}/5) -> {'PASS' if g >= 9 else 'FAIL'}")
YRE = re.compile(r'^Y nq=64 n=(\d+) max=(-?[\d.]+)'); FILES = ('direct', 'bank_r10', 'all_r10')
def unit(tag):
    N, mx, per = 0, -99.0, {}
    for f in FILES:
        for l in open(f'{W}/R/{tag}_{f}.txt'):
            mm = YRE.match(l)
            if mm: n, v = int(mm[1]), float(mm[2]); per[f] = (n, v); N += n; mx = max(mx, v) if n else mx
    return N, mx, per
rows = []
for l in open(W + '/nulls241.tsv'):
    seed, st, t, sha = l.rstrip('\n').split('\t'); N, mx, per = unit(f'null{seed}'); R = mx - fit(N)
    rows.append(dict(seed=int(seed), set=st, N=N, max=mx, R=R, p218=N >= 10 and mx >= b218(N), psh=N >= 10 and mx >= bsh(N), per=per))
    print(f"null {seed} {st} N {N:5d} max {mx:8.4f} R {R:+.4f} bar218 {b218(N):.4f} barSH {bsh(N):.4f} {'PASS218' if rows[-1]['p218'] else '-'} {'PASSSH' if rows[-1]['psh'] else '-'}")
k = sum(r['psh'] for r in rows); kC = sum(r['psh'] for r in rows if r['set'] == 'C'); kD = k - kC; k218 = sum(r['p218'] for r in rows)
OU0 = 0.4902982394620903; kou = sum(1 for r in rows if r['R'] >= OU0)
adopt = k <= 3 and kC <= 2 and kD <= 2
print(f"H3 shifted-bar passes {k}/24 Wilson {wilson(k,24)} (C {kC}/12, D {kD}/12) -> {'ADOPT BSH for gn217 decrypts from 241' if adopt else 'NOT ADOPTED'}; bar218 passes {k218}/24 Wilson {wilson(k218,24)}")
print(f"OU0 (one-unit bar, fit + {OU0:.4f}) passes {kou}/24 Wilson {wilson(kou,24)} -> {'HOLDS' if kou <= 2 else 'REJECTED'}")
Rn = np.array([r['R'] for r in rows]); R221 = np.array([r['R'] for r in json.load(open(W + '/summary235.json'))['nulls']]); R240 = np.array([r['R'] for r in json.load(open(W + '/summary240.json'))['nulls']])
print(f"R_t fresh 24: median {np.median(Rn):+.4f} max {Rn.max():+.4f} | case 221 (24) median {np.median(R221):+.4f} | case 240 (12) median {np.median(R240):+.4f}")
import re as _re, os
REPO = sys.argv[2]
YR = _re.compile(r"^Y model=(\w) p=(\d+) nq=(\d+) n=(\d+) pass=(\d+) max=(-?[\d.]+)")
cal = {}
for sd in range(209609, 209629):
    U = {}
    for fn in ("direct_a","direct_b","bank_Q_r10","all_Q_r10","bank_V_a","bank_V_b","all_V_a","all_V_b"):
        for l in open(f"{REPO}/data/cycle232/R/null{sd}_{fn}.txt"):
            m = YR.match(l)
            if m and int(m[3]) >= 10: u = U.setdefault(int(m[3]), [0, -99.]); u[0] += int(m[4]); u[1] = max(u[1], float(m[6]))
    cal[sd] = {q: mx - fit(n, q) for q, (n, mx) in U.items() if n >= 10}
c64 = np.array([cal[s][64] for s in cal]); Rcal = np.array([max(v.values()) for v in cal.values()])
u64 = mannwhitneyu(Rn, c64, alternative='two-sided', method='exact'); hl64 = float(np.median([a - b for a in Rn for b in c64]))
ucal = mannwhitneyu(Rn, Rcal, alternative='two-sided', method='exact'); hlc = float(np.median([a - b for a in Rn for b in Rcal]))
mult = u64.pvalue >= 0.05 and abs(hl64) <= 0.15
print(f"I-377(b) fresh R_t vs cal nq-64 single-unit residuals: exact MW p {u64.pvalue:.3g} HL {hl64:+.3f} -> {'CONSISTENT (shift = multiplicity of units, not family)' if mult else 'NOT consistent'}")
print(f"        fresh R_t vs cal R_t (max over ~52 units): exact MW p {ucal.pvalue:.3g} HL {hlc:+.3f} (case 221 got p 6.0e-8, HL -0.239)")
print(f"headroom to BSH (k_text-SH {KT-SH:.4f}) for best fresh null: {(KT-SH) - Rn.max():+.4f}")
S.update(nulls=rows, H3=dict(k=k, kC=kC, kD=kD, k218=k218, adopt=adopt, kou=kou), MW64=dict(p=float(u64.pvalue), HL=hl64, consistent=bool(mult)), MWcal=dict(p=float(ucal.pvalue), HL=hlc))
json.dump(S, open(W + '/summary241.json', 'w'), indent=1, default=str)
