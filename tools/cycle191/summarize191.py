"""Cycle 191 summary (as run): full-power cells (E <= 0.05), fits in them with the printed M lines, low-power totals vs E, bands.
C1 cells come from cmp191's H lines (cell = model, tableau pair, form, m, n); C2t/C2v/C3 from agg191's A lines (cell = model, form, m, n
summed over all tableau pairs; on the identity route model C = model P, so direct cells are reported once).
usage: summarize191.py   (run in the cycle work dir: run/out/c1_k4_full.txt, run/agg_c3.txt, run/agg_c2t.txt, run/agg_c2v.txt)"""
import math
def cells_from_H(fn):
    d = {}
    for l in open(fn):
        w = l.split()
        if w[0] == 'H': d[(w[2], w[3], w[4], int(w[5]), int(w[6]))] = [int(w[7]), int(w[8]), float(w[9]), float(w[10])]
    return d
def cells_from_A(fn):
    d = {}
    for l in open(fn):
        w = l.split()
        if w[0] == 'A': d[(w[1], w[2], int(w[3]), int(w[4]))] = [int(w[5]), int(w[6]), float(w[7]), float(w[8])]
    return d
def Ms(fn): return [l.split() for l in open(fn) if l.startswith('M ')]
def bands(fn): return [l.split() for l in open(fn) if l.startswith('B ')]
def rep(name, d, M, B, direct=False):
    if direct: d = {k: v for k, v in d.items() if k[0] == 'P'}
    fp = {k: v for k, v in d.items() if v[3] <= 0.05}; lp = {k: v for k, v in d.items() if v[3] > 0.05}
    print(f"== {name}: cells {len(d)}, full-power {len(fp)}, low-power {len(lp)}")
    for md in ('P',) if direct else ('P', 'C'):
        ks = [k for k in fp if k[0] == md]; mn = {(k[-2], k[-1]) for k in ks}
        print(f"   model {md}: full-power cells {len(ks)}; distinct ordered (m,n) {len(mn)}; with lcm>26 {sum(1 for a, b in mn if math.lcm(a, b) > 26)}; E sum {sum(fp[k][3] for k in ks):.3g}; fits {sum(fp[k][1] for k in ks)}")
    fits = {k: v for k, v in fp.items() if v[1] > 0}
    print(f"   full-power cells with K4 fits: {len(fits)}")
    for k, v in sorted(fits.items()):
        pm = [m for m in M if m[6] == str(k[-2]) and m[7] == str(k[-1]) and m[4] == k[-3] and m[5] == k[0] and (len(k) == 4 or m[3] == k[1])]
        print(f"     {k} configs {v[0]} fits {v[1]} sols {v[2]:.0f} E {v[3]:.3g} printed {len(pm)}: {[' '.join(m[2:10]) for m in pm[:8]]}")
    print(f"   low-power totals: fits {sum(v[1] for v in lp.values())}, sols {sum(v[2] for v in lp.values()):.8g}, E {sum(v[3] for v in lp.values()):.8g}")
    print("   bands e: configs fits sols E -> " + "; ".join(f"{b[2]}: {b[3]} {b[4]} {b[5]} {b[6]}" for b in B if b[2] != '25'))
rep("C1 K4, A-Z>KRYPTOS + KRYPTOS>A-Z, all 165,782 routes (cell = model, tableau pair, form, m, n)", cells_from_H('run/out/c1_k4_full.txt'), Ms('run/out/c1_k4_full.txt'), bands('run/out/c1_k4_full.txt'))
for s, name, direct in (('c3', 'C3 K4, 572 themed x {A-Z,KRYPTOS} pairs on all_s512 (cell = model, form, m, n over all 572 pairs)', False), ('c2t', 'C2t K4 direct, 20,592 themed x themed pairs (cell = form, m, n)', True), ('c2v', 'C2v K4 direct, 75,292 vocabulary x {A-Z,KRYPTOS} pairs (cell = form, m, n)', True)):
    rep(name, cells_from_A(f'run/agg_{s}.txt'), Ms(f'run/agg_{s}.txt'), bands(f'run/agg_{s}.txt'), direct)
