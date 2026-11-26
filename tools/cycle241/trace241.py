#!/usr/bin/env python3
"""trace241.py (PREREG241, I-390 amended tracing rule; frozen before the run). Applied to (1) the 20 case 226 plants (P files of cycle 240, read from
/workspace/k4c240/w) and the 10 cycle 241 plants, (2) H lines >= BSH of the 24 fresh nulls.
For every H line with NC >= barSH(343) that is not the planted line:
  (a) hd_off = min_c Hamming(key, plantedkey + c mod 26) (plants only); equivalent-key if <= 10;
  (b) alphabet neighbour = same window id as the planted line AND |dX| <= 100 and |dY| <= 100 (indices in the alphabet list; descriptive, not a metric claim);
  (c) groups: lines sharing >= 50 % of their 97 decrypt letters (Hamming <= 48) are one group (union-find); a group containing the planted line (or a line that
      decrypts identically to it) is planted-expected; the independent pass count = number of groups without a planted member.
usage: trace241.py WORKDIR"""
import sys, glob, re
W = sys.argv[1]; BSH = -6.963380308850821
K = open(W + '/keys233.bin', 'rb').read(); kw = lambda w: K[int(w) * 97:(int(w) + 1) * 97]
def lines(fn):
    out = []
    for h in open(fn):
        if h.startswith('H'): out.append(dict(kv.split('=') for kv in h.split()[1:]))
    return out
def groups(ls):
    p = list(range(len(ls)))
    def f(i):
        while p[i] != i: p[i] = p[p[i]]; i = p[i]
        return i
    for i in range(len(ls)):
        for j in range(i + 1, len(ls)):
            if sum(a != b for a, b in zip(ls[i]['pt'], ls[j]['pt'])) <= 48: p[f(i)] = f(j)
    g = {}
    for i in range(len(ls)): g.setdefault(f(i), []).append(i)
    return list(g.values())
tot = dict(lines=0, nb_key=0, nb_alpha=0, other=0, groups_planted=0, groups_other=0)
for tag, pdir, tsv in (('c240', '/workspace/k4c240/w', '/workspace/k4c240/w/plants240.tsv'), ('c241', W, W + '/plants241.tsv')):
    for l in open(tsv):
        p = l.rstrip('\n').split('\t'); pid, scope, qi, dr, ix, x, y, f, w, pt = p[0], p[1], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[14]; kp = kw(w)
        ls = [d for d in lines(f'{pdir}/P/p{pid}.txt') if float(d['nc']) >= BSH]
        pl = [i for i, d in enumerate(ls) if int(d['perm']) == int(qi) and d['X'] == x and d['Y'] == y and d['form'] == f and kw(d['w']) == kp and (scope == 'direct' or (d['dir'] == dr and d['ix'] == ix))]
        cls = []
        for i, d in enumerate(ls):
            if i in pl: continue
            ho = min(sum(a != (b + c) % 26 for a, b in zip(kw(d['w']), kp)) for c in range(26))
            alp = d['w'] == w and abs(int(d['X']) - int(x)) <= 100 and abs(int(d['Y']) - int(y)) <= 100
            cls.append('KEY' if ho <= 10 else 'ALPHA' if alp else 'OTHER')
        g = groups(ls); gp = sum(1 for gg in g if set(gg) & set(pl)); go = len(g) - gp
        # a group is planted-expected also if any member decrypts identically to a planted line
        tot['lines'] += len(ls) - len(pl); tot['nb_key'] += cls.count('KEY'); tot['nb_alpha'] += cls.count('ALPHA'); tot['other'] += cls.count('OTHER'); tot['groups_planted'] += gp; tot['groups_other'] += go
        print(f"{tag} plant {pid:>2} {scope:6s} lines>=BSH {len(ls):3d} planted {len(pl)} non-planted {len(ls)-len(pl):3d} KEY {cls.count('KEY')} ALPHA {cls.count('ALPHA')} OTHER {cls.count('OTHER')} groups {len(g)} (with planted {gp}, independent {go})")
print('PLANTS TOTAL', tot)
ng = 0; nl = 0
for fn in sorted(glob.glob(W + '/R/null*_*.txt')):
    ls = [d for d in lines(fn) if float(d['nc']) >= BSH]
    if ls: g = groups(ls); ng += len(g); nl += len(ls); print('NULL', fn.split('/')[-1], 'lines', len(ls), 'groups', len(g), 'best nc', max(float(d['nc']) for d in ls))
print(f'NULL TOTAL H lines >= BSH {nl} groups {ng}')
