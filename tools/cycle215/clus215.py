#!/usr/bin/env python3
"""Cycle 215 (I-291/I-298): cluster-aware recount of survivor lines, rule registered in PREREG214 part C (credit: Voynich desk).
Cells of one text are one cluster iff (a) same family, tm/form (+ X,Y pair when the line has one), L, segE, segB, o1, o2 and
(b) single-linkage on effective maps agreeing on >= 16 of the 24 crib positions; identical maps (inverse twins) always merge.
Effective map: S[i] for crib positions i = 21..33, 63..73, with S = bank/all.bin row (dir 0) or its inverse (dir 1) (wrbank convention).
usage: clus215.py PERMS.bin FILE [FILE...]   -> one JSON line per file and L
       --pairblind   : sensitivity variant, X/Y/ix/iy dropped from the group key"""
import sys, json, re, collections
N = 97; CRIB = list(range(21, 34)) + list(range(63, 74))
args = [a for a in sys.argv[1:] if not a.startswith('--')]; pairblind = '--pairblind' in sys.argv
perms = open(args[0], 'rb').read(); NP = len(perms) // (2 * N)
def row(q):
    b = perms[q * 2 * N:(q + 1) * 2 * N]; return [int.from_bytes(b[2*i:2*i+2], 'little', signed=True) for i in range(N)]
def emap(q, d):
    s = row(q)
    if d == 0: return tuple(s[i] for i in CRIB)
    inv = [0] * N
    for i, v in enumerate(s): inv[v] = i
    return tuple(inv[i] for i in CRIB)
GROUPF = ['tm', 'form', 'X', 'Y', 'pair', 'L', 'segE', 'segB', 'o1', 'o2']
if pairblind: GROUPF = ['tm', 'form', 'L', 'segE', 'segB', 'o1', 'o2']
for fn in args[1:]:
    lines = [l.split() for l in open(fn) if l.startswith('S ')]
    tot = [l for l in open(fn) if l.startswith('T ')]
    byL = collections.defaultdict(list)
    for t in lines:
        d = dict(kv.split('=', 1) for kv in t[1:]); byL[int(d['L'])].append(d)
    for L in sorted(byL):
        groups = collections.defaultdict(set); cells = 0; keys = set()
        for d in byL[L]:
            cells += 1; keys.add(d['key'])
            g = tuple(d.get(f, '') for f in GROUPF)
            groups[g].add(emap(int(d['perm']), int(d['dir'])))
        nmaps = sum(len(v) for v in groups.values()); nclus = 0
        for g, ms in groups.items():
            ms = list(ms); par = list(range(len(ms)))
            def f(x):
                while par[x] != x: par[x] = par[par[x]]; x = par[x]
                return x
            for i in range(len(ms)):
                for j in range(i + 1, len(ms)):
                    if sum(a == b for a, b in zip(ms[i], ms[j])) >= 16: par[f(i)] = f(j)
            nclus += len({f(i) for i in range(len(ms))})
        print(json.dumps({'file': fn.split('/')[-1], 'L': L, 'cells_printed': cells, 'groups': len(groups),
                          'distinct_maps': nmaps, 'clusters': nclus, 'distinct_keys': len(keys), 'pairblind': pairblind,
                          'T': tot[-1].strip() if tot else None}))
