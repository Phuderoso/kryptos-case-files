#!/usr/bin/env python3
"""Cycle 216 (PREREG216 Part A) scorer: plant gate + K4/null tables + labels exactly as registered. Reads w/AP/*.json, w/A/*.json/txt.
usage: score216.py WORKDIR > summary.json (and a text report on stderr)"""
import sys, json, glob, collections, math, os
W = sys.argv[1]; POS = list(range(21, 34)) + list(range(63, 74)); THR = -6.0; LMAX = 25; out = {}
def log(*a): print(*a, file=sys.stderr)
# --- gate P
plants = [l.rstrip('\n').split('\t') for l in open(f'{W}/plants216.tsv')]; passes = 0; prow = []
for pid, scope, q, d, X, Y, form, model, L, ix, j, dig, p, C in plants:
    rows = json.load(open(f'{W}/AP/p{pid}.json')); found = False; rec = None; hit = []
    for r in rows:
        if (r['perm'], r['dir'], r['X'], r['Y'], r['form']) == (int(q), int(d) if int(q) >= 0 else 0, int(X), int(Y), int(form)):
            found = True; hit = [c for c in r['consistent'] if c['model'] == model and c['L'] == int(L) and c['ix'] == int(ix) and c['drop'] == int(j)]
    ok = bool(hit); mism = None
    if hit and hit[0]['best'] is not None:
        mism = sum(a != b for a, b in zip(hit[0]['best'][1], p)); ok = mism <= 1
    passes += ok; prow.append(dict(pid=int(pid), scope=scope, model=model, L=int(L), ix=int(ix), j=int(j), digit_after=int(dig),
                                   cell_found=found, consistent=bool(hit), nsol=hit[0]['nsol'] if hit else None, pt_mismatch=mism, pass_=ok))
out['gate_P'] = dict(passes=passes, n=len(plants), pass_bar=19, PASS=passes >= 19, rows=prow); log('gate P', passes, '/', len(plants))
# --- clusters (PREREG214 part C rule; direct: map = identity, so clusters = distinct (X,Y,form) cells)
import struct
def emap(fn, q, d):
    if q < 0: return tuple(POS)
    with open(fn, 'rb') as f: f.seek(q * 194); s = list(struct.unpack('<97h', f.read(194)))
    if d == 0: return tuple(s[i] for i in POS)
    inv = [0] * 97
    for i, v in enumerate(s): inv[v] = i
    return tuple(inv[i] for i in POS)
def clusters(rows, perms):
    groups = collections.defaultdict(set)
    for r in rows: groups[(r['X'], r['Y'], r['form'])].add(emap(perms, r['perm'], r['dir']))
    maps = sum(len(v) for v in groups.values()); nc = 0
    for ms in groups.values():
        ms = list(ms); par = list(range(len(ms)))
        def f(x):
            while par[x] != x: par[x] = par[par[x]]; x = par[x]
            return x
        for a in range(len(ms)):
            for b in range(a + 1, len(ms)):
                if sum(u == v for u, v in zip(ms[a], ms[b])) >= 16: par[f(a)] = f(b)
        nc += len({f(a) for a in range(len(ms))})
    return maps, nc
def tline(fn):
    t = [l for l in open(fn) if l.startswith('T ')][-1].split(); return {k: int(v) for k, v in (x.split('=') for x in t[1:])}
def consist(rows):
    """per (model, L): number of lines with >= 1 consistent (drop, ix); and the max best score / any nsol > 1000"""
    c = {}
    for model in ('gromark', 'periodic'):
        for L in range(1, LMAX + 1):
            n = 0; big = 0; best = None; bl = None
            for r in rows:
                h = [x for x in r['consistent'] if x['model'] == model and x['L'] == L]
                if not h: continue
                n += 1; big += any(x['best'] is None for x in h)
                for x in h:
                    if x['best'] and (best is None or x['best'][0] > best): best = x['best'][0]; bl = x['best'][1]
            c[f'{model}:{L}'] = dict(lines=n, nsol_gt1000_lines=big, best_score=best, best_pt=bl)
    return c
P = {'direct': 'x', 'bank': f'{W}/bank.bin', 'all': f'{W}/all.bin'}
for scope in ('direct', 'bank', 'all'):
    k4 = json.load(open(f'{W}/A/k4_{scope}.json')); T = tline(f'{W}/A/k4_{scope}.txt')
    assert all(r['rederive_ok'] for r in k4)
    maps, nc = clusters(k4, P[scope])
    nulls = sorted(glob.glob(f'{W}/A/null_{scope}_*.json'), key=lambda s: int(s.split('_')[-1].split('.')[0]))
    nrows = []; ncells = []; npf = 0; nclus = []
    for fn in nulls:
        rr = json.load(open(fn)); assert all(r['rederive_ok'] for r in rr); nrows += rr; t = tline(fn[:-5] + '.txt'); npf += t['pairforms']
        ncells.append(t['survivors']); nclus.append(clusters(rr, P[scope])[1])
    scale = T['pairforms'] / npf; lam = sum(ncells) * scale
    # Poisson one-sided p of K4 cells given the null-equivalent rate (the registered A1 test)
    pk = 1 - sum(math.exp(-lam) * lam ** i / math.factorial(i) for i in range(T['survivors'])) if T['survivors'] else 1.0
    c4 = consist(k4); cn = consist(nrows); labels = {}
    for key, v in c4.items():
        nl = len(nrows); rate = cn[key]['lines'] / nl if nl else None
        neq = cn[key]['lines'] * scale
        if v['lines'] == 0: lab = 'EXACT-EXCL (one-error scope, discriminating)' if neq <= 1 else f'EXACT-EXCL (one-error scope; zero is exact, low power: null-eq {neq:.1f})'
        elif v['best_score'] is not None and v['best_score'] >= THR: lab = 'CANDIDATE (manual read)'
        elif v['nsol_gt1000_lines'] > 0: lab = 'INSUFFICIENT-DISCRIMINATION'
        else: lab = 'NO-SIGNAL (consistent, gibberish)'
        labels[key] = dict(label=lab, k4_lines=v['lines'], k4_best=v['best_score'], k4_best_pt=v['best_pt'], k4_big=v['nsol_gt1000_lines'],
                           null_rate_per_line=rate, null_lines=cn[key]['lines'], null_eq_lines=round(neq, 2), null_best=cn[key]['best_score'])
    out[scope] = dict(k4=T, k4_maps=maps, k4_clusters=nc, null_cells=ncells, null_clusters=nclus, null_pairforms=npf,
                      null_equiv_cells=round(lam, 2), poisson_p_k4_ge=pk, A1=('SIGNAL-FLAG' if pk < 0.001 else 'NO-SIGNAL (digit level, any stream)'),
                      models=labels)
    log(scope, 'K4', T, 'maps', maps, 'clusters', nc, '| null cells', ncells, 'scaled', round(lam, 1), 'p', round(pk, 4))
    for key, v in labels.items():
        if v['k4_lines'] or v['null_lines']: log('  ', key, v['label'], 'K4', v['k4_lines'], v['k4_best'], '| null', v['null_lines'], '/', len(nrows), v['null_best'])
json.dump(out, sys.stdout, indent=1)
