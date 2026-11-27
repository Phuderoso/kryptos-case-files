"""PREREG243 analysis: gate E (exact plants), gate H (heuristic plants), K4 vs nulls. Writes summary243.json."""
import json, glob, os, statistics as st
SC = ['S1', 'S2', 'S3a', 'S3b']
def load(name):
    S, H, D, T = [], [], {}, {}
    for sc in SC:
        for l in open(f'out/{name}/{sc}.txt'):
            w = l.split()
            if w[0] == 'S': S.append((sc, int(w[1]), int(w[2]), int(w[3]), int(w[4]), int(w[5]), w[6], int(w[7]), int(w[8]), int(w[9])))
            elif w[0] == 'H': H.append((float(w[1]), sc, int(w[2]), int(w[3]), int(w[4]), int(w[5]), int(w[6]), w[7], w[8]))
            elif w[0] == 'D': D[int(w[1])] = D.get(int(w[1]), 0) + int(w[2])
            elif w[0] == 'T': T[sc] = l.strip()
    H.sort(reverse=True)
    return S, H, D, T
def scope_of(sc): return 'S3' if sc.startswith('S3') else sc
plants = [l.rstrip('\n').split('\t') for l in open('plants243.tsv')]
nulls = [l.split('\t')[0] for l in open('nulls243.tsv')]
res = {'nulls': {}, 'plants': {}}
for s in nulls:
    S, H, D, T = load('N' + s)
    res['nulls'][s] = {'strict': sum(1 for r in S if r[8] == 0), 'one': sum(1 for r in S if r[8] == 1), 'maxdepth': max(D),
                       'Hmax': H[0][0], 'Hmax_scope': {sc: max([h[0] for h in H if scope_of(h[1]) == sc] or [-99]) for sc in ('S1', 'S2', 'S3')}}
nullH = [v['Hmax'] for v in res['nulls'].values()]
gE = gH = 0
for p in plants:
    pid, scope, x, y, g, f, M, src, o, es, ct = p; pid = int(pid); x, y, g, f, M, o, es = map(int, (x, y, g, f, M, o, es))
    S, H, D, T = load(f'P{pid}')
    if pid < 10:
        hit = [r for r in S if scope_of(r[0]) == scope and (r[1], r[2], r[3], r[4], r[5], r[6], r[7]) == (g, f, x, y, M, src, o)]
        ok = any((r[8] == 0) if es < 0 else (r[8] == 1 and r[9] == es) for r in hit)
        cls = 'clean' if es < 0 else ('anchorA' if es < 4 else 'anchorB' if 13 <= es < 17 else 'other')
        res['plants'][pid] = {'gate': 'E', 'pass': ok, 'class': cls, 'lines': len(S), 'strict': sum(1 for r in S if r[8] == 0), 'one': sum(1 for r in S if r[8] == 1)}
        gE += ok
    else:
        rank = None; sc_p = None
        for i, h in enumerate(H):
            if scope_of(h[1]) == scope and (h[2], h[3], h[4], h[5], h[6]) == (g, f, x, y, M): rank = i + 1; sc_p = h[0]; break
        ok = rank == 1 and sc_p is not None and sc_p > max(nullH)
        res['plants'][pid] = {'gate': 'H', 'pass': ok, 'rank': rank, 'score': sc_p, 'top': H[0][0], 'frag': H[0][7] + ' ' + H[0][8] if H else ''}
        gH += ok
S, H, D, T = load('K4')
k4 = {'strict': sum(1 for r in S if r[8] == 0), 'one': sum(1 for r in S if r[8] == 1), 'lines': S, 'maxdepth': max(D), 'depth': D,
      'Hmax': H[0][0], 'top10': [h for h in H[:10]], 'T': T,
      'Hmax_scope': {sc: max([h[0] for h in H if scope_of(h[1]) == sc] or [-99]) for sc in ('S1', 'S2', 'S3')}}
k4['Hrank_p'] = (1 + sum(1 for v in nullH if v >= k4['Hmax'])) / 13
mu, sd = st.mean(nullH), st.stdev(nullH); k4['H_z'] = (k4['Hmax'] - mu) / sd
k4['depth_rank_p'] = (1 + sum(1 for v in res['nulls'].values() if v['maxdepth'] >= k4['maxdepth'])) / 13
res['K4'] = k4; res['gateE'] = f'{gE}/10'; res['gateH'] = f'{gH}/10'
res['null_Hmax'] = sorted(nullH); res['null_Hmax_mean_sd'] = (mu, sd)
json.dump(res, open('summary243.json', 'w'), indent=1, default=str)
print('gate E', gE, '/10; gate H', gH, '/10')
for pid, v in res['plants'].items(): print('P', pid, v)
print('nulls', {s: (v['strict'], v['one'], v['maxdepth'], round(v['Hmax'], 4)) for s, v in res['nulls'].items()})
print('K4 strict', k4['strict'], 'one', k4['one'], 'maxdepth', k4['maxdepth'], 'depth p', round(k4['depth_rank_p'], 3), 'Hmax', round(k4['Hmax'], 4), 'rank p', round(k4['Hrank_p'], 3), 'z', round(k4['H_z'], 2), k4['Hmax_scope'])
for h in k4['top10']: print(' ', h)
for sc, t in T.items(): print(sc, t)
