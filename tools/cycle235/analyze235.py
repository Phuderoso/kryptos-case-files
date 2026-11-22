#!/usr/bin/env python3
"""Cycle 235 analysis (PREREG235, I-364 / I-356). Fixed before the run; no tuning after it.
Unit: (text, nq = 64) pooled over the 3 run files (direct full, bank r10, all.bin r10): N = total surrogate decrypts, max = best NC.
Bar (case 218, adopted): bar(nq, N) = fit(nq, N) + 0.879, fit = -6.8417 + 0.0786 ln N + 0.00027 (ln N)^2 - 0.0192 nq (exact betas
from data/cycle232/summary232.json). Per-text pass <=> N >= 10 and max >= bar(64, N).  R_t = max - fit(64, N).
H1 (primary): per-text passes over the 24 fresh nulls; HOLDS if <= 3/24 (P(>=4 | p = 1/21) = 0.025), FAILS (too permissive) if >= 4/24;
   'robust' if each set (A, B) is <= 2/12 (same side).  Wilson 95 % printed.
H2 (secondary): R_t of the 24 nulls vs the 20 case-218 calibration R_t: two-sided Mann-Whitney, Hodges-Lehmann shift with 95 % CI;
   p < 0.05 and shift < 0 -> 'bar conservative in this family by |shift|' (a power note, not a false-pass problem).
Gate P: plant recovered (planted perm/dir/ix/X/Y/form and window key) AND NC >= bar(64, N_K4) for >= 18/20 (one-error 9/10 reported).
Gate T: check235.py mismatches 0 on K4 (all files), the first null of each set (all files) and every plant file.
K4 arm (descriptive): unit N, max, R, rank p vs the 24 nulls = (1 + #nulls with R >= R_K4) / 25; any pass is printed as a lead.
usage: analyze235.py WORKDIR REPO"""
import sys, re, json, math
import numpy as np
from scipy.stats import mannwhitneyu
W, REPO = sys.argv[1], sys.argv[2]
B = json.load(open(REPO + '/data/cycle232/summary232.json'))
beta = B['fit']['beta']; KT = B['bar']['k_text']; RCAL = sorted(B['bar']['Rcal'].values())
def fit(N, q): x = math.log(max(N, 10)); return beta[0] + beta[1] * x + beta[2] * x * x + beta[3] * q
def bar(N, q): return fit(N, q) + KT
def wilson(k, n, z=1.959964):
    if n == 0: return (0.0, 1.0)
    ph = k / n; d = 1 + z * z / n; c = (ph + z * z / (2 * n)) / d; h = z * math.sqrt(ph * (1 - ph) / n + z * z / (4 * n * n)) / d
    return (round(max(0.0, c - h), 4), round(min(1.0, c + h), 4))
YRE = re.compile(r'^Y nq=64 n=(\d+) max=(-?[\d.]+)')
FILES = ('direct', 'bank_r10', 'all_r10')
def unit(tag):
    N, mx, per = 0, -99.0, {}
    for f in FILES:
        for l in open(f'{W}/R/{tag}_{f}.txt'):
            m = YRE.match(l)
            if m: n, v = int(m[1]), float(m[2]); per[f] = (n, v); N += n; mx = max(mx, v) if n else mx
    return N, mx, per
S = {}; nul = [l.split('\t') for l in open(W + '/nulls235.tsv')]
rows = []
for seed, st, t, sha in nul:
    N, mx, per = unit(f'null{seed}'); R = mx - fit(N, 64); ps = N >= 10 and mx >= bar(N, 64)
    rows.append(dict(seed=int(seed), set=st, N=N, max=mx, bar=bar(N, 64), R=R, passed=ps, per=per))
    print(f"null {seed} set {st} N {N:5d} max {mx:8.4f} bar {bar(N,64):8.4f} R {R:+.4f} {'PASS' if ps else '-'}  " +
          '  '.join(f"{f} n {per[f][0]} max {per[f][1]:.4f}" for f in FILES))
kA = sum(r['passed'] for r in rows if r['set'] == 'A'); kB = sum(r['passed'] for r in rows if r['set'] == 'B'); k = kA + kB
h1 = 'HOLDS' if k <= 3 else 'FAILS (too permissive)'; rob = (kA <= 2 and kB <= 2) if k <= 3 else (kA > 2 and kB > 2)
print(f"\nH1 per-text passes {k}/24 Wilson {wilson(k,24)} (A {kA}/12 {wilson(kA,12)}, B {kB}/12 {wilson(kB,12)}) -> {h1}{' (robust: both sets same side)' if rob else ' (FRONTEIRA: sets disagree)'}")
Rn = np.array([r['R'] for r in rows]); Rc = np.array(RCAL)
u = mannwhitneyu(Rn, Rc, alternative='two-sided'); d = np.subtract.outer(Rn, Rc).ravel(); hl = float(np.median(d))
rng = np.random.default_rng(209671); bs = []
for _ in range(2000): bs.append(np.median(np.subtract.outer(rng.choice(Rn, 24), rng.choice(Rc, 20)).ravel()))
ci = (float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5)))
print(f"H2 R_t nulls: median {np.median(Rn):+.4f} max {Rn.max():+.4f} min {Rn.min():+.4f} | case-218 calibration: median {np.median(Rc):+.4f} max {Rc.max():+.4f}")
print(f"   Mann-Whitney U {u.statistic:.1f} p {u.pvalue:.3g}; Hodges-Lehmann shift {hl:+.4f} (bootstrap 95% {ci[0]:+.4f}..{ci[1]:+.4f}, B 2000, seed 209671 reused for resampling only)")
h2 = (f'bar conservative in this family by {-hl:.2f}' if (u.pvalue < 0.05 and hl < 0) else
      f'bar permissive-side shift {hl:+.2f}' if (u.pvalue < 0.05) else 'no family shift detected')
print(f"   -> {h2}; headroom to bar for the best null: {min(r['bar'] - r['max'] for r in rows):+.4f}")
N4, m4, p4 = unit('k4'); R4 = m4 - fit(N4, 64); rk = (1 + sum(r['R'] >= R4 for r in rows)) / 25
print(f"\nK4 unit N {N4} max {m4:.4f} bar {bar(N4,64):.4f} R {R4:+.4f} {'PASS (lead: inspect)' if m4 >= bar(N4,64) else 'no pass'}; rank p {rk:.2f}  " +
      '  '.join(f"{f} n {p4[f][0]} max {p4[f][1]:.4f}" for f in FILES))
# plants
K = open(W + '/keys233.bin', 'rb').read(); PL = []
for l in open(W + '/plants235.tsv'):
    pid, scope, ct, qi, dr, ix, x, y, f, w, bad, pt = l.rstrip('\n').split('\t'); kw = K[int(w) * 97:(int(w) + 1) * 97]
    best = None; nl = 0
    for h in open(f'{W}/P/p{pid}.txt'):
        if not h.startswith('H'): continue
        nl += 1; dd = dict(kv.split('=') for kv in h.split()[1:])
        same = (int(dd['perm']) == int(qi) and int(dd['X']) == int(x) and int(dd['Y']) == int(y) and int(dd['form']) == int(f)
                and K[int(dd['w']) * 97:(int(dd['w']) + 1) * 97] == kw and (scope == 'direct' or (int(dd['dir']) == int(dr) and int(dd['ix']) == int(ix))))
        if same and (best is None or float(dd['nc']) > best[0]): best = (float(dd['nc']), sum(a != b for a, b in zip(dd['pt'], pt)))
    ok = best is not None and best[0] >= bar(N4, 64)
    PL.append(dict(pid=int(pid), bad=int(bad), lines=nl, nc=best[0] if best else None, diff=best[1] if best else None, ok=ok))
    print(f"plant {pid:>2} {scope:6s} bad {int(bad):3d} lines {nl:4d} rec {int(best is not None)} NC {best[0] if best else float('nan'):8.4f} ptdiff {best[1] if best else -1} margin {(best[0]-bar(N4,64)) if best else float('nan'):+.3f} {'PASS' if ok else 'FAIL'}")
gp = sum(p['ok'] for p in PL); g1 = sum(p['ok'] for p in PL if p['bad'] >= 0)
print(f"Gate P {gp}/20 Wilson {wilson(gp,20)} (one-error {g1}/10) -> {'PASS' if gp >= 18 else 'FAIL'}; min margin {min((p['nc'] or -99) - bar(N4,64) for p in PL):+.3f}")
S.update(nulls=rows, H1=dict(k=k, kA=kA, kB=kB, wilson=wilson(k, 24), verdict=h1, robust=rob),
         H2=dict(U=float(u.statistic), p=float(u.pvalue), hl=hl, ci=ci, verdict=h2, Rcal=RCAL),
         K4=dict(N=N4, max=m4, bar=bar(N4, 64), R=R4, rank_p=rk, per=p4), plants=PL, gateP=gp, gateP_oneerror=g1)
json.dump(S, open(W + '/summary235.json', 'w'), indent=1, default=str)
