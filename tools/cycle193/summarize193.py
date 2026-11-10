"""Cycle 193 summary (as run): C1 cells from cmp193 H lines (cell = model, tableau pair, form, m, n over all routes); full-power cells
(E <= 0.05) with their fits and printed M lines; low-power totals vs E split into two-tableau and one-tableau stacks; bands; and the
descriptive power note (G lines): per model, share of route configs per E_config band in the full-power (m, n) pairs and the
80th-percentile E_config of a planted config (the weak end). C3 from agg193 A lines (cell = model, form, m, n over all 572 pairs).
usage: summarize193.py   (run in the cycle work dir)"""
import math
ONE = {'AZ>AZ', 'KA>KA'}
def cells_H(fn):
    d = {}
    for l in open(fn):
        w = l.split()
        if w[0] == 'H': d[(w[2], w[3], w[4], int(w[5]), int(w[6]))] = [int(w[7]), int(w[8]), float(w[9]), float(w[10])]
    return d
def cells_A(fn):
    d = {}
    for l in open(fn):
        w = l.split()
        if w[0] == 'A': d[(w[1], 'ALL', w[2], int(w[3]), int(w[4]))] = [int(w[5]), int(w[6]), float(w[7]), float(w[8])]
    return d
def lines(fn, k): return [l.split() for l in open(fn) if l.startswith(k + ' ')]
def rep(name, d, M, B):
    fp = {k: v for k, v in d.items() if v[3] <= 0.05}; lp = {k: v for k, v in d.items() if v[3] > 0.05}
    print(f"== {name}: cells {len(d)}, full-power {len(fp)}, low-power {len(lp)}")
    for md in ('1', '2'):
        ks = [k for k in fp if k[0] == md]; mn = {(k[-2], k[-1]) for k in ks}
        print(f"   model S{md}: full-power cells {len(ks)}; distinct (m,n) {len(mn)} (m = n: {sum(1 for a, b in mn if a == b)}; lcm > 26: {sum(1 for a, b in mn if math.lcm(a, b) > 26)}; max lcm {max([math.lcm(a, b) for a, b in mn] or [0])}); E sum {sum(fp[k][3] for k in ks):.4g}; fits {sum(fp[k][1] for k in ks)}")
    fits = {k: v for k, v in fp.items() if v[1] > 0}
    print(f"   full-power cells with K4 fits: {len(fits)}")
    for k, v in sorted(fits.items()):
        pm = [m for m in M if m[5] == k[0] and m[4] == k[2] and m[6] == str(k[3]) and m[7] == str(k[4]) and (k[1] == 'ALL' or m[3] == k[1])]
        print(f"     {k} configs {v[0]} fits {v[1]} sols {v[2]:.0f} E {v[3]:.3g} printed {len(pm)}: {[' '.join(m[2:10]) for m in pm[:8]]}")
    for lab, sel in (('two-tableau', lambda k: k[1] not in ONE), ('one-tableau', lambda k: k[1] in ONE)):
        s = {k: v for k, v in lp.items() if sel(k)}
        if s: print(f"   low-power {lab}: cells {len(s)} fits {sum(v[1] for v in s.values())}, sols {sum(v[2] for v in s.values()):.8g}, E {sum(v[3] for v in s.values()):.8g}")
    print("   bands e: configs fits sols E -> " + "; ".join(f"{b[2]}: {b[3]} {b[4]} {b[5]} {b[6]}" for b in B if b[2] != '25'))
    return fp
fp = rep("C1 K4, tab4 (AZ>KA, KA>AZ, AZ>AZ, KA>KA), all 165,782 routes", cells_H('run/out/c1_k4_full.txt'), lines('run/out/c1_k4_full.txt', 'M'), lines('run/out/c1_k4_full.txt', 'B'))
G = lines('run/out/c1_k4_full.txt', 'G')
print("== Power note (descriptive): planted-config E_config by band in the full-power (m, n) pairs of C1")
for md in ('1', '2'):
    pairs = {(k[3], k[4]) for k in fp if k[0] == md}
    h = {}
    for g in G:
        if g[2] == md and (int(g[3]), int(g[4])) in pairs: h[int(g[5])] = h.get(int(g[5]), 0) + int(g[6])
    tot = sum(h.values())
    if not tot: continue
    cum = 0; p80 = None
    for b in sorted(h):            # weakest first = lowest band (largest E)
        cum += h[b]
        if p80 is None and cum >= 0.2 * tot: p80 = b
    share = ", ".join(f"e{b} {h[b] / tot:.3f}" for b in sorted(h) if h[b] / tot >= 0.005)
    print(f"   S{md}: pairs {len(pairs)}, route configs {tot}; weakest band {min(h)}; 80th-percentile (weak end) band e = {p80} (E_config ~ 26^-{p80}); shares: {share}")
rep("C3 K4, 572 themed x {A-Z,KRYPTOS} pairs on all_s512 (cell = model, form, m, n over all 572 pairs)", cells_A('run/agg_c3.txt'), lines('run/agg_c3.txt', 'M'), lines('run/agg_c3.txt', 'B'))
