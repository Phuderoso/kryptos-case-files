"""PREREG242 analysis. Reads out/<text>/{S1,S2,S3a,S3b}.txt (tri242 output), plants242.tsv, nulls242.tsv.
Primary (registered) cells: strict = PER with >= 6 crib constraints, CA every L 1-48 (>= 11 constraints), PA with >= 6;
one-error = the same models with >= 9 constraints. Plants: recovered iff the planted (scope x y g f model par M) line is printed with viol <= 1
(viol 0 required for clean plants). Every primary K4 / null survivor is decrypted (m242.decrypt_line) and scored (NC, nq);
trace trigger: nq >= 40 and NC >= -6.9634 (BSH(343) borrowed from the gn217 family, descriptive here)."""
import os, sys, json
from m242 import *
AL, TH, AK = rec('alpha.bin'), rec('themed144.bin'), rec('azka.bin')
ALPH = {'S1': (AL, AL), 'S2': (TH, TH), 'S3a': (AL, AK), 'S3b': (AK, AL)}
NP = {P: 24 - len({q % P for q in POS}) for P in range(1, 49)}
NPA = {L: sum(1 for q in POS if q - L in POS) for L in range(1, 61)}
BSH = -6.9634
def ncons(model, par, nc):
    return NP[par] if model == 'PER' else NPA[par] if model == 'PA' else int(nc)
def lines(name):
    out = []; T = {}
    for sc in ALPH:
        fn = f'out/{name}/{sc}.txt'
        for ln in open(fn):
            a = ln.split()
            if a[0] == 'S':
                model, g, f, x, y, par, M, v, nc = a[1], int(a[2]), int(a[3]), int(a[4]), int(a[5]), int(a[6]), a[7], int(a[8]), a[9]
                n = ncons(model, par, nc if nc != '-' else 0)
                prim = (n >= 6) if v == 0 else (n >= 9)
                out.append(dict(sc=sc, model=model, g=g, f=f, x=x, y=y, par=par, M=M, v=v, n=n, prim=prim))
            elif a[0] == 'T' and a[1] != 'pairforms':
                key = tuple(a[1:-4]) if a[1] != 'PER' else (a[1], a[2])
                s, o = int(a[-3]), int(a[-1]); T[key] = (T.get(key, (0, 0))[0] + s, T.get(key, (0, 0))[1] + o)
            elif a[0] == 'T': T['pf'] = T.get('pf', 0) + int(a[2])
    return out, T
def score(ct, L):
    X, Y = ALPH[L['sc']][0][L['x']], ALPH[L['sc']][1][L['y']]
    pt = decrypt_line(ct, L['model'], L['g'], L['f'], X, Y, L['par'], 0 if L['M'] in ('-', '0') else 1)
    v, nq = nc(pt)
    return ''.join(ch if ch else '.' for ch in pt), v, nq
res = {'plants': [], 'texts': {}}
# plants
for r in open('plants242.tsv'):
    pid, sc, x, y, g, f, mo, par, M, ep, ct, pt = r.rstrip('\n').split('\t'); pid, x, y, g, f, par, M, ep = map(int, (pid, x, y, g, f, par, M, ep))
    L, T = lines(f'P{pid}')
    scs = [sc] if sc != 'S3' else (['S3a'] if y < 2 and x >= 2 else ['S3b'] if x < 2 and y >= 2 else ['S3a', 'S3b'])
    hit = None
    for l in L:
        if l['sc'] not in scs or l['model'] != mo or l['g'] != g or l['f'] != f or l['par'] != par: continue
        xx, yy = (x, y)
        if l['x'] != xx or l['y'] != yy: continue
        if mo != 'PER' and int(l['M']) != M: continue
        if ep < 0 and l['v'] != 0: continue
        hit = l; break
    d = dict(pid=pid, scope=sc, model=mo, g=g, f=f, par=par, M=M, err=ep, rec=hit is not None, lines=len(L), prim=sum(l['prim'] for l in L))
    if hit:
        dec, v, nq = score(ct, hit); d.update(v=hit['v'], nc=round(v, 4), nq=nq, agree=sum(1 for a, b in zip(dec, pt) if a == b), known=sum(1 for a in dec if a != '.'))
    res['plants'].append(d)
    print('plant', d)
rp = sum(d['rec'] for d in res['plants']); print(f'GATE P {rp}/20')
texts = ['K4'] + ['N' + r.split('\t')[0] for r in open('nulls242.tsv')]
cts = {'K4': open('k4.txt').read().strip()}; cts.update({'N' + r.split('\t')[0]: r.split('\t')[1].strip() for r in open('nulls242.tsv')})
for t in texts:
    if not os.path.exists(f'out/{t}/S3b.txt'): print('missing', t); continue
    L, T = lines(t); P = [l for l in L if l['prim']]
    cell = {}
    for l in P: k = (l['model'], l['par'], l['v']); cell[k] = cell.get(k, 0) + 1
    sc = []
    for l in P:
        dec, v, nq = score(cts[t], l); trig = nq >= 40 and v >= BSH
        sc.append(dict(l, nc=round(v, 4), nq=nq, trig=trig, dec=dec))
    res['texts'][t] = dict(pf=T['pf'], nprim=len(P), strict=sum(1 for l in P if l['v'] == 0), one=sum(1 for l in P if l['v'] == 1),
                           trig=sum(s['trig'] for s in sc), cells={f'{a}{b}v{c}': n for (a, b, c), n in sorted(cell.items())}, lines=sc,
                           totals={' '.join(k) if isinstance(k, tuple) else k: v for k, v in T.items()})
    print(t, 'pairforms', T['pf'], 'primary', len(P), 'strict', res['texts'][t]['strict'], 'one', res['texts'][t]['one'], 'trig', res['texts'][t]['trig'], res['texts'][t]['cells'])
    for s in sorted(sc, key=lambda s: -s['nc'] if s['nc'] == s['nc'] else 9)[:5]:
        print('   ', s['sc'], s['model'], s['g'], s['f'], s['x'], s['y'], s['par'], s['M'], 'v', s['v'], 'n', s['n'], 'NC', s['nc'], 'nq', s['nq'], s['dec'])
json.dump(res, open('summary242.json', 'w'), indent=1)
