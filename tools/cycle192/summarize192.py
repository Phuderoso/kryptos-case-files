"""Cycle 192 summary (as run): full-power cells (U <= 0.05) with their fits and the printed M lines, low-power totals vs U, bands; grid
(K4 vs 19 shuffles per band); C3/C2t/C2v from agg192 A lines summed over files (cell = model, form, m, n over all tableau pairs; direct runs
are model P only). usage: summarize192.py (in the cycle work dir)"""
import glob, math
def ends(files):
    bad = [f for f in files if not any(l.startswith('END') for l in open(f))]
    return len(files), bad
def cells_H(fn):
    d = {}
    for l in open(fn):
        w = l.split()
        if w[0] == 'H': d[(w[2], w[3], w[4], int(w[5]), int(w[6]))] = [int(w[7]), int(w[8]), int(w[9]), float(w[10])]
    return d
def cells_A(files):
    d = {}
    for fn in files:
        for l in open(fn):
            w = l.split()
            if w[0] == 'A':
                k = (w[1], w[2], int(w[3]), int(w[4])); v = d.setdefault(k, [0, 0, 0, 0.0])
                v[0] += int(w[5]); v[1] += int(w[6]); v[2] += int(w[7]); v[3] += float(w[8])
    return d
def Ms(files): return [l.split() for fn in files for l in open(fn) if l.startswith('M ')]
def bands(files):
    b = {}
    for fn in files:
        for l in open(fn):
            w = l.split()
            if w[0] == 'B': v = b.setdefault(int(w[2]), [0, 0, 0.0]); v[0] += int(w[3]); v[1] += int(w[4]); v[2] += float(w[5])
    return b
def rep(name, d, M, B):
    fp = {k: v for k, v in d.items() if v[3] <= 0.05}; lp = {k: v for k, v in d.items() if v[3] > 0.05}
    print(f"== {name}: cells run {len(d)}, full-power {len(fp)}, low-power (run) {len(lp)}")
    for md in ('P', 'C'):
        ks = [k for k in fp if k[0] == md]
        if not ks and md == 'C': continue
        mn = {(k[-2], k[-1]) for k in ks}
        print(f"   model {md}: full-power cells {len(ks)}; distinct ordered (m,n) {len(mn)}; lcm>26 {sum(1 for a, b in mn if math.lcm(a, b) > 26)}; max lcm {max([math.lcm(a, b) for a, b in mn] or [0])}; U sum {sum(fp[k][3] for k in ks):.3g}; fits {sum(fp[k][1] for k in ks)} (strict {sum(fp[k][2] for k in ks)})")
    fits = {k: v for k, v in fp.items() if v[1] > 0}
    print(f"   full-power cells with K4 fits: {len(fits)}")
    for k, v in sorted(fits.items()):
        pm = [m for m in M if m[6] == str(k[-2]) and m[7] == str(k[-1]) and m[4] == k[-3] and m[5] == k[0] and (len(k) == 4 or m[3] == k[1])]
        print(f"     {k} configs {v[0]} fits {v[1]} strict {v[2]} U {v[3]:.3g} printed {len(pm)}: {[' '.join(m[2:10]) for m in pm[:8]]}")
    print(f"   low-power (run) totals: fits {sum(v[1] for v in lp.values())}, U {sum(v[3] for v in lp.values()):.8g}")
    print("   bands e: configs fits U -> " + "; ".join(f"{b}: {B[b][0]} {B[b][1]} {B[b][2]:.4g}" for b in sorted(B) if b != 25))
n, bad = ends(['run/out/c1_k4_full.txt']); print(f"C1 END check: {n} files, missing END {bad}")
rep("C1 K4, A-Z>KRYPTOS + KRYPTOS>A-Z, all 165,782 routes, pairs_c1 (cell = model, tableau pair, form, m, n)", cells_H('run/out/c1_k4_full.txt'), Ms(['run/out/c1_k4_full.txt']), bands(['run/out/c1_k4_full.txt']))
for s, name in (('c3', 'C3 K4, 572 themed x {A-Z,KRYPTOS} pairs on all_s512, pairs_c3 (cell = model, form, m, n over 572 pairs)'), ('c2t', 'C2t K4 direct, 20,592 themed x themed pairs, pairs_c2t'), ('c2v', 'C2v K4 direct, 75,292 vocabulary x {A-Z,KRYPTOS} pairs, pairs_c2v')):
    fs = sorted(glob.glob(f'run/out/{s}/*.txt'))
    if not fs: print(f"== {name}: NOT RUN"); continue
    n, bad = ends(fs); print(f"{s} END check: {n} files, missing END {len(bad)}")
    rep(name, cells_A(fs), Ms(fs), bands(fs))
# grid
G = {}
for fn in sorted(glob.glob('run/grid/g512_*.txt')):
    lab = fn.split('g512_')[1][:-4]; G[lab] = bands([fn])
if G:
    print(f"== Grid (all_s512, tab2, all 600 pairs): texts {len(G)}")
    for lo in (1, 2, 3, 4):
        f = {lab: sum(v[1] for b, v in B.items() if lo <= b < 25) for lab, B in G.items()}
        nul = [f[x] for x in f if x != 'k4']; k = f.get('k4', -1)
        print(f"   fits in bands >= {lo}: K4 {k}, nulls {min(nul)}-{max(nul)} (mean {sum(nul)/len(nul):.1f}), p+ {(1 + sum(1 for x in nul if x >= k)) / (len(nul) + 1):.2f}, U(K4) {sum(v[2] for b, v in G['k4'].items() if lo <= b < 25):.4g}")
