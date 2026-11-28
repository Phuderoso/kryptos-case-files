"""PREREG244 T3: rank-vs-parametric sweep over case files 118-229 (hits of the PREREG244 grep). Parametric p recomputed from the printed
inputs (one-sided normal for z; exact Poisson upper tail for counts); rank p and floor as printed. Prints which scale decided the label."""
from scipy.stats import norm, poisson
rows = [
 # case, statistic, parametric (kind, value), rank p, floor, decided by / outcome
 ('165', 'C2 one-error Gromark ix0 L6, K4 230 vs 19 nulls (LOO mean 191.5)', ('pois', (230, 191.5)), 0.05, 1/20, 'rank: grid p+ 0.05 = floor, not called a signal; replication case 166 NOT REPLICATED (p_F 0.073, p_M 0.143, pooled 60 p 0.082)'),
 ('166', 'C2 replication, fresh 40', ('z', 1.82), 0.073, 1/41, 'rank (pre-registered): NOT REPLICATED'),
 ('166', 'C2 replication, matched 20', ('z', 1.21), 0.143, 1/21, 'rank: NOT REPLICATED'),
 ('168', 'grid upper tail, K4 above all 19', ('text', 'I-120 Poisson tails called meaningless in the case'), 0.05, 1/20, 'rank; fresh 40 p_F 0.122 (z +1.44) -> no signal'),
 ('168', 'fresh 40 shuffles', ('z', 1.44), 0.122, 1/41, 'rank'),
 ('170', 'fresh 40 plain shuffles', ('z', 1.44), 0.073, 1/41, 'rank (concordant)'),
 ('170', 'second set', ('z', 1.19), 0.143, 1/41, 'rank (concordant)'),
 ('174', 'direction r D, K4 3,771 vs 19 nulls', ('z', 2.39), 0.05, 1/20, 'rank flag only; replication case 175 NOT REPLICATED (p_F 0.610, z -0.20)'),
 ('167', 'D1 mod-2 pass count (lower tail)', ('text', 'single Poisson p- 0.012 printed'), 0.25, 1/20, 'rank: K4 5th lowest of 20, diagnostic only'),
 ('184', 'sample bank B 25 vs 17.6', ('z', 1.78), None, None, 'neither: case states Poisson z is no test on heavy-tailed bands; no label from it'),
 ('202', 'stage 1 Poisson p (K4 >=) 0.83 / 1.00 / 0.38', ('text', 'Poisson vs one null-equivalent; tenths overdispersed'), None, None, 'parametric only, all >= 0.38: NO-SIGNAL either way; caveat: anti-conservative under overdispersion, nothing to reverse'),
 ('221', 'H2 Mann-Whitney, 24 nulls R_t vs 20 calibration R_t', ('text', 'normal approx 1.13e-6 vs exact 6.01e-8 (c239)'), 6.01e-8, None, 'exact rank test (corrected in c239); reading unchanged'),
 ('229', 'Part H Hmax, 12 nulls', ('z', -0.52), 0.692, 1/13, 'rank: NO-SIGNAL (concordant)'),
 ('230', 'Part H Hmax, 36 nulls (this cycle, T5)', ('z', -0.33), 0.622, 1/37, 'rank: NO-SIGNAL (concordant)'),
]
print('case | statistic | parametric p (recomputed) | rank p | floor | at floor? | discordant? | decided by')
nfloor = ndisc = nparam = 0
for c, s, (k, v), rp, fl, dec in rows:
    if k == 'z': pp = norm.sf(v); ps = f'z {v:+.2f} -> {pp:.4f}'
    elif k == 'pois': pp = poisson.sf(v[0] - 1, v[1]); ps = f'Poisson P(X>={v[0]}|{v[1]}) = {pp:.4f}'
    else: pp = None; ps = v
    atf = rp is not None and fl is not None and abs(rp - fl) < 1e-9
    disc = pp is not None and rp is not None and ((pp < 0.05) != (rp < 0.05) or atf and pp < fl)
    nfloor += atf; ndisc += bool(disc); nparam += dec.startswith('parametric')
    print(f'{c} | {s} | {ps} | {rp if rp is not None else "-"} | {f"{fl:.3f}" if fl else "-"} | {"FLOOR" if atf else ""} | {"yes" if disc else ""} | {dec}')
print(f'rows {len(rows)}; rank p at floor {nfloor}; parametric/rank discordant {ndisc}; labels that rested on a parametric p with rank at floor: 0 -> no relabel')
