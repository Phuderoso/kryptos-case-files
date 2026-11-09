"""Summarize cycle 170 runs: K4 chunks (out/k4.c*), 40 full-family nulls (nulls/null*.out), RK nulls (nulls/rk_null*.out)."""
import glob, re, sys, math
from math import comb
def cp_upper(x, n, a=0.05):
    lo, hi = 0.0, 1.0
    for _ in range(60):
        m = (lo + hi) / 2; cdf = sum(comb(n, i) * m**i * (1-m)**(n-i) for i in range(x+1))
        lo, hi = (m, hi) if cdf > a else (lo, m)
    return hi
def read(files):
    S = {}; per = {t: [0]*26 for t in ('V1A', 'V1B', 'V2A', 'V2B')}; rk = 0; surv = 0
    for fn in files:
        for l in open(fn):
            if l.startswith('SUMMARY'):
                f = l.split()
                for i in range(1, len(f) - 1, 2): S[f[i]] = int(f[i+1]) if f[i] in ('masks', 'orderings') else S.get(f[i], 0) + int(f[i+1])
            elif l.startswith('PERIODIC'):
                f = l.split(); per[f[1]] = [a + int(b) for a, b in zip(per[f[1]], f[2:])]
            elif l.startswith('SURV'):
                surv += 1; rk += int(re.search(r' rk (\d+)', l).group(1))
    return S, per, rk, surv
W = sys.argv[1] if len(sys.argv) > 1 else '.'
k = read(sorted(glob.glob(f'{W}/out/k4.c*')))
print('K4 (full family, 16 chunks):', k[0]); print('K4 survivors (perm, ordering):', k[3], ' running-key full fits:', k[2])
for t, v in k[1].items(): print(f'K4 periodic {t} L1..26:', v)
nulls = [read([fn]) for fn in sorted(glob.glob(f'{W}/nulls/null*.out'), key=lambda s: int(re.findall(r'\d+', s.split('/')[-1])[0]))]
sv = sorted(n[3] for n in nulls); ge = sum(n[3] <= k[3] for n in nulls)
print(f'nulls: {len(nulls)}; survivors min/median/max {sv[0]}/{sv[len(sv)//2]}/{sv[-1]}; nulls with <= K4 survivors {ge}/{len(nulls)}  -> rank p (K4 as few as or fewer) = {(ge+1)/(len(nulls)+1):.3f}, floor 1/(N+1) = {1/(len(nulls)+1):.3f}')
for t in ('V1A', 'V1B', 'V2A', 'V2B'):
    for L in range(1, 27):
        vals = [n[1][t][L-1] for n in nulls]
        if max(vals) or k[1][t][L-1]:
            ge = sum(x >= k[1][t][L-1] for x in vals)
            print(f'  {t} L{L}: K4 {k[1][t][L-1]}  nulls min/median/max {min(vals)}/{sorted(vals)[len(vals)//2]}/{max(vals)}  nulls >= K4 {ge}/{len(nulls)}  p = {(ge+1)/(len(nulls)+1):.3f}')
    z = [L for L in range(1, 27) if k[1][t][L-1] == 0 and all(n[1][t][L-1] == 0 for n in nulls)]
    print(f'  {t}: K4 and all nulls 0 at L {z[0]}..{z[-1] if z else None} (contiguous from 1: {all(L in z for L in range(1, (z[-1] if z else 0)+1))})')
nz = sum(any(n[1][t][L-1] for t in n[1] for L in range(1, 24)) for n in nulls)
ub = cp_upper(nz, len(nulls))
print(f'nulls with any periodic fit at L <= 23: {nz}/{len(nulls)} (one-sided 95% Clopper-Pearson upper bound on the null rate {ub:.3f})')
rkn = [read([fn]) for fn in sorted(glob.glob(f'{W}/nulls/rk_null*.out'))]
print('RK nulls (chunk c0 = 1/16 of family):', [(n[3], n[2]) for n in rkn])
kc0 = read([f'{W}/out/k4.c0']); print('K4 chunk c0: survivors', kc0[3], 'rk', kc0[2])
