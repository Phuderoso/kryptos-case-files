"""Cycle 171 summary: (1) I-096 Porta one-error behind 165,782 decimations/routes; (2) I-091 one-error named running keys behind
the 165,065-perm bank. Exact binomial (Clopper-Pearson) bounds, 1/(N+1) rank floor, analytic expectation beside each count (I-097).
usage: summarize171.py RUN_DIR"""
import sys, glob, re, os, math
R = sys.argv[1]; os.chdir(R)
def cp_upper(k, n, a=0.05):
    """one-sided exact (Clopper-Pearson) upper bound: largest p with P(X <= k | n, p) >= a, by bisection"""
    if k >= n: return 1.0
    cdf = lambda p: sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(k + 1))
    lo, hi = 0.0, 1.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if cdf(mid) >= a: lo = mid
        else: hi = mid
    return lo
def psumm(f):
    L = open(f).read().split('\n'); s = [l for l in L if l.startswith('SUMMARY')]
    if not s or not any(l.startswith('EXPECT V2B') for l in L): return None
    t = s[0].split()[1:]; d = {t[i]: int(t[i + 1]) for i in range(0, len(t), 2)}
    for l in L:
        if l.startswith(('PERIODIC', 'EXPECT')):
            x = l.split(); d[x[0] + ' ' + x[1]] = [float(v) for v in x[2:]]
    d['fits'] = [l for l in L if l.startswith('FIT')]; return d
def add(a, b):
    for k, v in b.items():
        if k == 'fits': a.setdefault(k, []).extend(v)
        elif isinstance(v, list): a[k] = [x + y for x, y in zip(a.get(k, [0] * 26), v)]
        elif k not in ('masks', 'orderings'): a[k] = a.get(k, 0) + v
    return a
TAGS = ['V1A', 'V1B', 'V2A', 'V2B']
print("# Cycle 171 summary\n\n## 1. I-096 Porta one-error behind 165,782 K3-law decimations + spiral/diagonal routes\n")
K = {}; miss = []
for i in range(16):
    s = psumm(f'out/k4p.c{i}') if os.path.exists(f'out/k4p.c{i}') else None
    if s: add(K, s)
    else: miss.append(i)
print(f"K4 chunks done {16-len(miss)}/16 {miss if miss else ''}")
print(f"K4 perms {K['perms']:,}; dead (>= 2 self-mapped crib pairs) {K['dead_2self']:,}; surviving (perm, ordering): d free {K['surv_ord_free']:,} "
      f"(= cycle 170 strict survivors), d forced {K['surv_ord_forced']:,}")
print(f"running keys one-error on all d-free survivors: {K['rk_ord_free']:,} orderings x 36 texts, fits {K['rk_fits']}")
print("\nPeriodic one-error, K4 observed vs analytic expectation (sum over survivors of chance pass probability; d free = union bound):")
for t in TAGS:
    o, e = K['PERIODIC ' + t], K['EXPECT ' + t]
    print(f"  {t}: " + ' '.join(f"L{L+1}:{int(o[L])}/{e[L]:.2g}" for L in range(26) if o[L] or e[L] >= 1e-3))
    zl = [L + 1 for L in range(26) if o[L] == 0 and e[L] < 0.01]
    print(f"     L with obs 0 and expectation < 0.01: {zl[0]}..{zl[-1] if zl else ''} ({len(zl)} periods) {zl}")
exp_le = {t: sum(K['EXPECT ' + t][:L]) for t in TAGS for L in [23]}
print(f"  fits at L <= 23 (FIT lines): {len(K['fits'])}; total expectation L<=23: " + ', '.join(f"{t} {sum(K['EXPECT '+t][:23]):.2f}" for t in TAGS))
# per-L observed fits L<=23
cnt = {}
for l in K['fits']:
    for part in l.split(' per ')[1].split(' rk ')[0].split():
        tag, Ls = part.split(':')
        for x in Ls.split(','):
            if x and int(x) <= 23: cnt[(tag, int(x))] = cnt.get((tag, int(x)), 0) + 1
print("  per (variant, L<=23) fit counts:", dict(sorted(cnt.items())))
# D: running keys on all survivors, 1/8 slice
D = {}
for f in ['out/k4pall.s16o0', 'out/k4pall.s16o8']:
    s = psumm(f) if os.path.exists(f) else None
    if s: add(D, s)
if D:
    print(f"\nRunning keys one-error on EVERY survivor (d forced too), slice p%8==0: perms {D['perms']:,}, orderings d free {D['rk_ord_free']:,} + d forced {D['rk_ord_forced']:,}, fits {D['rk_fits']}")
    rk = [l for l in D['fits'] if ' rk 0' not in l]; print(f"  RK fit lines: {len(rk)}"); [print('   ', x[:300]) for x in rk[:10]]
# E: nulls on slice p%8==0
k4s = psumm('out/k4p_nork_s8o0'); ns = [psumm(f) for f in sorted(glob.glob('nulls/pnull*.out'))]; ns = [x for x in ns if x]
if k4s and ns:
    N = len(ns); tot = lambda d: d['surv_ord_free'] + d['surv_ord_forced']
    kv = tot(k4s); nv = sorted(tot(x) for x in ns); ge = sum(1 for x in nv if x >= kv); le = sum(1 for x in nv if x <= kv)
    print(f"\nNulls (40 shuffled K4s, slice p%8==0, {k4s['perms']:,} perms): one-error survivors (perm, ordering) K4 {kv}, nulls min/median/max {nv[0]}/{nv[N//2]}/{nv[-1]}")
    print(f"  nulls >= K4 {ge}/{N} -> p(K4 high) = {(ge+1)/(N+1):.3f}; nulls <= K4 {le}/{N} -> p(K4 low) = {(le+1)/(N+1):.3f}; floor 1/(N+1) = {1/(N+1):.3f}")
    for t in TAGS:
        for L in range(1, 27):
            kk = k4s['PERIODIC ' + t][L - 1]; nn = [x['PERIODIC ' + t][L - 1] for x in ns]
            if kk == 0 and max(nn) == 0: continue
            g = sum(1 for x in nn if x >= kk); ek = k4s['EXPECT ' + t][L - 1]; en = sorted(x['EXPECT ' + t][L - 1] for x in ns)[N // 2]
            print(f"  {t} L{L}: K4 {int(kk)} (exp {ek:.2g}); nulls min/med/max {int(min(nn))}/{int(sorted(nn)[N//2])}/{int(max(nn))} (median exp {en:.2g}); nulls >= K4 {g}/{N} p = {(g+1)/(N+1):.3f}")
    a23 = sum(1 for x in ns if any(x['PERIODIC ' + t][L] for t in TAGS for L in range(23)))
    print(f"  nulls with any periodic one-error fit at L <= 23: {a23}/{N} (K4 on slice: {int(any(k4s['PERIODIC '+t][L] for t in TAGS for L in range(23)))})"
          f"; Clopper-Pearson 95% upper bound on that null rate {cp_upper(a23, N):.3f}")
# ---------------- bank
def bsumm(f):
    s = [l for l in open(f) if l.startswith("SUMMARY")]
    if not s: return None
    m = re.search(r"perms=(\d+) configs=(\d+) best=(\d+) best1=(\d+) full=(\d+) fit23=(\d+) hist:(.*) hist1:(.*) bestS=(\d+) histS:(.*)", s[0])
    hs = lambda x: {int(a): int(b) for a, b in (y.split(":") for y in x.split())}
    return dict(perms=int(m[1]), configs=int(m[2]), best=int(m[3]), best1=int(m[4]), full=int(m[5]), fit23=int(m[6]), hist1=hs(m[8]), bestS=int(m[9]))
print("\n## 2. I-091 one-error named running keys (bookrk1e) behind the 165,065-perm bank\n")
tot = dict(perms=0, configs=0, full=0, fit23=0); b1 = 0; bS = 0; h1 = {}; missb = []
for f in sorted(glob.glob('bank_chunk_??')):
    o = f'out/k4b_{f}.out'; s = bsumm(o) if os.path.exists(o) else None
    if not s: missb.append(f); continue
    for k in tot: tot[k] += s[k]
    b1 = max(b1, s['best1']); bS = max(bS, s['bestS'])
    for k, v in s['hist1'].items(): h1[k] = h1.get(k, 0) + v
print(f"K4 bank chunks done {16-len(missb)}/16 {missb if missb else ''}")
if tot['perms']:
    texts = [l.split()[1] for l in open('texts.txt')]; nofs = sum(len(t) - 96 for t in texts)
    pl = tot['configs'] // len(texts) * nofs;  # configs count (perm, model, mode, text); the XOR skip is text-independent
    q = 1 / 26; pr = 24 * q ** 23 * (25 / 26) + q ** 24
    print(f"K4: perms {tot['perms']:,} configs {tot['configs']:,} x {len(texts)} texts ({nofs:,} offsets) = {pl:.3e} placements")
    print(f"K4: FULL {tot['full']} FIT23 {tot['fit23']}; best one-error depth1 {b1}; best strict depth {bS}")
    print(f"  analytic expectation of >= 23/24 chance fits: uniform {pl*pr:.1e}; worst case p=0.127 per letter {pl*(24*0.127**23*0.873+0.127**24):.1e}")
    print("  K4 hist1:", ' '.join(f"{k}:{h1[k]}" for k in sorted(h1)))
    for f in sorted(glob.glob('out/k4b_bank*.out')):
        for l in open(f):
            if l.startswith(('FULL', 'FIT23')): print('   K4 HIT', l.strip())
ks = bsumm('out/k4b_slice.out') if os.path.exists('out/k4b_slice.out') else None
bn = [bsumm(f) for f in sorted(glob.glob('nulls/bnull*.out'))]; bn = [x for x in bn if x]
if ks and bn:
    N = len(bn); v = sorted(x['best1'] for x in bn); nf = sum(1 for x in bn if x['full'] or x['fit23'])
    g = sum(1 for x in v if x >= ks['best1'])
    print(f"\nNull lineup on bankslice.bin (first 250 + last 250 bank perms), {N} shuffled K4s: K4 best1 {ks['best1']} fit23 {ks['fit23']} full {ks['full']}")
    print(f"  nulls best1 min/median/max {v[0]}/{v[N//2]}/{v[-1]}; nulls >= K4 best1 {g}/{N} -> p = {(g+1)/(N+1):.3f} (floor {1/(N+1):.3f})")
    print(f"  nulls with any >= 23/24 fit {nf}/{N}; Clopper-Pearson 95% upper bound on the null fit rate {cp_upper(nf, N):.3f}")
