"""degen241.py (PREREG241, I-383 / I-382 extension): Voynich's degeneracy criteria as DESCRIPTIVE per-family counts (credit: Voynich audit criteria,
case 224 reply). Limits frozen in PREREG241 before the run.
Per 97-value window: P4 = exactly periodic with minimal period <= 4 (key[i] == key[i+p] for all i, p in 1..4);
 ENT = Shannon entropy of the 97 values < 2.0 bits OR the most common value > 50 % of the window (>= 49 of 97);
 AP = key[i] == (a + d*i) mod 26 for all i with d != 0 (arithmetic progression mod 26; d = 0 is constant and falls under P4);
 TAIL = last >= 20 values identical;  DUP = window bytes identical to a window of ANOTHER family (any list in the audited set).
 usage: degen241.py [--gate]   (reads bins from W_DIR below)"""
import sys, math, collections, random, os
D = '/workspace/k4c241/w/lists'; R = '/workspace/k4c241/repo'
N = 97
def fl(w):
    f = set()
    if any(all(w[i] == w[i + p] for i in range(N - p)) for p in range(1, 5)): f.add('P4')
    c = collections.Counter(w); H = -sum(v / N * math.log2(v / N) for v in c.values())
    if H < 2.0 or c.most_common(1)[0][1] > N / 2: f.add('ENT')
    d = (w[1] - w[0]) % 26
    if d and all((w[0] + d * i) % 26 == w[i] for i in range(N)): f.add('AP')
    t = 1
    while t < N and w[N - 1 - t] == w[N - 1]: t += 1
    if t >= 20: f.add('TAIL')
    return f
if '--gate' in sys.argv:
    rng = random.Random(209756); neg = sum(bool(fl(bytes(rng.randrange(26) for _ in range(N)))) for _ in range(20000))
    pos = {'P4': 0, 'ENT': 0, 'AP': 0, 'TAIL': 0}
    for _ in range(100):
        p = rng.randint(1, 4); b = [rng.randrange(26) for _ in range(p)]; pos['P4'] += 'P4' in fl(bytes(b[i % p] for i in range(N)))
        v = [rng.randrange(26) for _ in range(N)]
        for i in rng.sample(range(N), 49): v[i] = 7
        pos['ENT'] += 'ENT' in fl(bytes(v))
        a, d = rng.randrange(26), rng.randrange(1, 26); pos['AP'] += 'AP' in fl(bytes((a + d * i) % 26 for i in range(N)))
        v = [rng.randrange(26) for _ in range(N)]; v[N - 20:] = [v[N - 1]] * 20; pos['TAIL'] += 'TAIL' in fl(bytes(v))
    print(f'gate N: random windows flagged {neg}/20000; gate P (100 planted each): {pos}'); sys.exit()
# lists: (label, bin, tsv, family column index, header lines)
L = [('keys217', 'keys217.bin', R + '/data/cycle217/keys217.tsv', 1, 1), ('keys218', 'keys218.bin', R + '/data/cycle218/keys218.tsv', 1, 1),
     ('keys221a', 'keys221a.bin', R + '/data/cycle221/keys221a.tsv', 2, 1), ('keys233', 'keys233.bin', R + '/tools/cycle233/keys233.tsv', 0, 0),
     ('keys234', 'keys234.bin', R + '/tools/cycle234/keys234.tsv', 1, 0), ('keys236', 'keys236.bin', R + '/tools/cycle236/keys236.tsv', 0, 0),
     ('keys237', 'keys237.bin', R + '/tools/cycle237/keys237.tsv', 1, 0), ('keys239', 'keys239.bin', R + '/tools/cycle239/keys239.tsv', 0, 0),
     ('keys222b', 'keys222b.bin', None, None, 0)]
W = []; skipped = []
for lab, bn, tsv, col, hd in L:
    b = open(f'{D}/{bn}', 'rb').read(); n = len(b) // N
    if tsv:
        rows = open(tsv).read().splitlines()[hd:]
        if len(rows) != n: skipped.append((lab, n, len(rows))); continue
        fam = [r.split('\t')[col] for r in rows]
    else: fam = ['all'] * n
    for i in range(n): W.append((lab, lab + ':' + fam[i], b[i * N:(i + 1) * N]))
first = {}
for lab, fa, w in W: first.setdefault(w, set()).add(fa)
cnt = collections.defaultdict(lambda: collections.Counter())
for lab, fa, w in W:
    f = fl(w); c = cnt[fa]; c['n'] += 1
    for x in f: c[x] += 1
    if len(first[w]) > 1: c['DUP'] += 1
print('lists skipped (row count mismatch):', skipped, '| windows', len(W), '| families', len(cnt))
print('family\tn\tP4\tENT\tAP\tTAIL\tDUP\tany')
anyc = {}
tot = collections.Counter()
for fa, c in sorted(cnt.items()):
    print(f"{fa}\t{c['n']}\t{c['P4']}\t{c['ENT']}\t{c['AP']}\t{c['TAIL']}\t{c['DUP']}\t-"); tot.update(c)
print('TOTAL', dict(tot))
