"""PREREG244 T1: case 228 informative count. Re-reads the T lines (cell totals) of data/cycle242/out/<text>/{S1,S2,S3a,S3b}.txt
for K4 and the 12 nulls, sums over scopes (as lowcells242), checks the reproduction of lowcells242.txt, then prints the informative
count, U (unique-max statistics), expected strict wins U/13, observed strict wins, per-statistic mid-rank p and the role-rotation
global rank p of (a) strict wins and (b) mean mid-rank p over informative statistics.  usage: inf244.py REPO > inf244.txt"""
import sys, re
R = sys.argv[1]; D = R + '/data/cycle242/out/'
texts = ['K4'] + ['N%d' % s for s in range(209758, 209770)]
def tot(t):
    T = {}
    for sc in ('S1', 'S2', 'S3a', 'S3b'):
        for ln in open(D + f'{t}/{sc}.txt'):
            a = ln.split()
            if not a or a[0] != 'T' or a[1] == 'pairforms': continue
            key = ' '.join(a[1:3]) if a[1] == 'PER' else ' '.join(a[1:4])
            s, o = int(a[-3]), int(a[-1]); p = T.get(key, (0, 0)); T[key] = (p[0] + s, p[1] + o)
    return T
TT = {t: tot(t) for t in texts}
cells = list(TT['K4'])
assert all(set(TT[t]) == set(cells) for t in texts)
# reproduction of lowcells242.txt
bad = 0; nrow = 0
for ln in open(R + '/data/cycle242/lowcells242.txt'):
    if ln.startswith('#'): continue
    m = re.match(r'(\S+ \S+(?: [01])?)(?: ncons \d+)?\s+n\s*\d+ K4 strict\s+(\d+) one\s+(\d+) \| nulls strict (\d+)-(\d+) one (\d+)-(\d+)', ln)
    if not m: continue
    nrow += 1; key = m.group(1).strip(); v = tuple(map(int, m.groups()[1:]))
    if key not in TT['K4']: bad += 1; print('missing', key); continue
    ns = [TT[t][key][0] for t in texts[1:]]; no = [TT[t][key][1] for t in texts[1:]]
    mine = (TT['K4'][key][0], TT['K4'][key][1], min(ns), max(ns), min(no), max(no))
    if mine != v: bad += 1; print('MISMATCH', key, v, mine)
print(f'# reproduction of lowcells242.txt: {nrow} cells, {bad} mismatches; cells here {len(cells)}, statistics {2*len(cells)}')
stats = [(c, k) for c in cells for k in (0, 1)]
def val(t, s): return TT[t][s[0]][s[1]]
def analyse(me):
    others = [t for t in texts if t != me]
    W = 0; mids = []; inf = 0; U = 0
    for s in stats:
        v = val(me, s); o = [val(t, s) for t in others]; allv = o + [v]
        if max(allv) == 0: continue
        inf += 1
        mx = max(allv); U += allv.count(mx) == 1
        G = sum(1 for x in o if x > v); E = sum(1 for x in o if x == v)
        mids.append((G + 0.5 * (E + 1)) / 13)
        W += v > max(o)
    return dict(W=W, inf=inf, U=U, mean_mid=sum(mids) / len(mids), mids=mids)
A = {t: analyse(t) for t in texts}
k = A['K4']
print(f'statistics 428; informative {k["inf"]} (non-zero in K4 or >= 1 null); all-zero {428 - k["inf"]}')
print(f'unique-max statistics U {k["U"]}; expected strict wins under exchangeability U/13 = {k["U"]/13:.2f}; observed K4 strict wins {k["W"]}')
print(f'old reference 428/13 = {428/13:.2f} (case 228 "~33")')
print(f'K4 mean mid-rank p over informative {k["mean_mid"]:.4f} (exchangeable expectation 0.5)')
n_low = sum(1 for m in k['mids'] if m <= 0.05); print(f'K4 informative statistics with mid-rank p <= 0.05: {n_low}; min mid-rank p {min(k["mids"]):.4f} (floor 0.5/13 = 0.0385)')
print('# role rotation (each text as "K4" vs the other 12)')
for t in texts: print(f'{t:8s} W {A[t]["W"]:3d}  inf {A[t]["inf"]}  U {A[t]["U"]}  mean_mid {A[t]["mean_mid"]:.4f}')
pW = (sum(1 for t in texts if A[t]['W'] >= k['W'])) / 13
pM = (sum(1 for t in texts if A[t]['mean_mid'] <= k['mean_mid'])) / 13
print(f'K4 rank p (strict wins, high) {pW:.3f}; K4 rank p (mean mid-rank p, low = K4 high) {pM:.3f}')
print('LABEL', 'NO-SIGNAL confirmed' if pW >= 0.05 and pM >= 0.05 else 'FLAG')
print('# K4 strict wins (statistic, K4, null max)')
for s in stats:
    v = val('K4', s); o = [val(t, s) for t in texts[1:]]
    if v > max(o): print('  ', s[0], 'strict' if s[1] == 0 else 'one', v, max(o))
