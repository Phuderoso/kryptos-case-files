"""Cycle 195 summary (as run; adapted from summarize193.py): per bank, cells from cmp193 H lines (cell = model, tableau pair, form, m, n summed
over the bank's rows); full-power cells (E <= 0.05) with fits and printed M lines; low-power totals vs E split two-tableau / one-tableau (I-205);
bands. C3 from agg193 A lines (cell = model, form, m, n over 572 tableau pairs x 184 themed rows).  usage: summarize195.py (in the work dir)"""
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
        for lab, sel in (('two-tableau', lambda k: k[1] not in ONE), ('one-tableau', lambda k: k[1] in ONE)):
            ks = [k for k in fp if k[0] == md and sel(k)]
            if not ks: continue
            mn = {(k[-2], k[-1]) for k in ks}
            print(f"   S{md} {lab}: full-power cells {len(ks)}; distinct (m,n) {len(mn)} (m = n: {sum(1 for a, b in mn if a == b)}; lcm > 26: {sum(1 for a, b in mn if math.lcm(a, b) > 26)}; max lcm {max([math.lcm(a, b) for a, b in mn] or [0])}); E sum {sum(fp[k][3] for k in ks):.4g}; fits {sum(fp[k][1] for k in ks)}")
    fits = {k: v for k, v in fp.items() if v[1] > 0}
    print(f"   full-power cells with K4 fits: {len(fits)}; total full-power E {sum(v[3] for v in fp.values()):.4g}, fits {sum(v[1] for v in fp.values())}")
    for k, v in sorted(fits.items()):
        pm = [m for m in M if m[5] == k[0] and m[4] == k[2] and m[6] == str(k[3]) and m[7] == str(k[4]) and (k[1] == 'ALL' or m[3] == k[1])]
        print(f"     {k} configs {v[0]} fits {v[1]} sols {v[2]:.0f} E {v[3]:.3g} printed {len(pm)}: {[' '.join(m[2:10]) for m in pm[:8]]}")
    for lab, sel in (('two-tableau', lambda k: k[1] not in ONE), ('one-tableau', lambda k: k[1] in ONE)):
        s = {k: v for k, v in lp.items() if sel(k)}
        if s: print(f"   low-power {lab}: cells {len(s)} fits {sum(v[1] for v in s.values())}, sols {sum(v[2] for v in s.values()):.8g}, E {sum(v[3] for v in s.values()):.8g}")
    print("   bands e: configs fits sols E -> " + "; ".join(f"{b[2]}: {b[3]} {b[4]} {b[5]} {b[6]}" for b in B if b[2] != '25'))
    return fp
for nm, fn in (("C1 K4, tab4, 3,674 single keyed columnars (col1)", 'run/out/c1_k4.txt'), ("C2 K4, tab4, 16,928 themed double keyed columnars (col2)", 'run/out/c2_k4.txt')):
    rep(nm, cells_H(fn), lines(fn, 'M'), lines(fn, 'B'))
rep("C3 K4, 572 themed x {A-Z,KRYPTOS} pairs on 184 themed columnar rows (col1_th)", cells_A('run/agg_c3.txt'), lines('run/agg_c3.txt', 'M'), lines('run/agg_c3.txt', 'B'))
