"""audit238.py (PREREG238, I-382): silent-truncation / degeneracy audit of frozen key-window lists (gn217 .bin: 97 bytes per window, values 0..25).
usage: audit238.py label list.bin [list.tsv] ...   -> one line per flagged window (F lines) + per-list summary (S lines) + cross-list duplicate count (D line)
Flags (all descriptive; thresholds frozen in PREREG238):
  CONST60  : most common value occurs >= 60 times of 97
  DISTINCT3: <= 3 distinct values in the 97
  TAILRUN  : last >= 10 values identical          (size-cap / zero-fill symptom)
  HEADRUN  : first >= 10 values identical
  RUN20    : any run of >= 20 identical consecutive values
  SEATCONST: the 24 crib-seat values (0-based 21..33, 63..73) all equal
  BLOCKCONST: one crib block constant (13 EASTNORTHEAST seats or 11 BERLINCLOCK seats)
  PERIOD12 : exactly periodic with period <= 12 over the 97 values
  ZEROTAIL : last >= 10 values all 0 (subset of TAILRUN, reported separately)
"""
import sys, hashlib, collections
N = 97
EN = list(range(21, 34)); BC = list(range(63, 74)); SEATS = EN + BC
def flags(w):
    f = []
    cnt = collections.Counter(w)
    if cnt.most_common(1)[0][1] >= 60: f.append('CONST60')
    if len(cnt) <= 3: f.append('DISTINCT3')
    t = 1
    while t < N and w[N - 1 - t] == w[N - 1]: t += 1
    if t >= 10: f.append('TAILRUN')
    if t >= 10 and w[N - 1] == 0: f.append('ZEROTAIL')
    h = 1
    while h < N and w[h] == w[0]: h += 1
    if h >= 10: f.append('HEADRUN')
    r = best = 1
    for i in range(1, N):
        r = r + 1 if w[i] == w[i - 1] else 1; best = max(best, r)
    if best >= 20: f.append('RUN20')
    if len({w[i] for i in SEATS}) == 1: f.append('SEATCONST')
    if len({w[i] for i in EN}) == 1 or len({w[i] for i in BC}) == 1: f.append('BLOCKCONST')
    for p in range(1, 13):
        if all(w[i] == w[i - p] for i in range(p, N)): f.append('PERIOD12'); break
    return f
def tag(line):
    for x in line.rstrip('\n').split('\t'):
        if not x.isdigit(): return x
    return '?'
def main(argv):
    seen = {}; dup_cross = 0; dup_in = 0
    i = 0
    while i < len(argv):
        label, binf = argv[i], argv[i + 1]; tsv = None
        i += 2
        if i < len(argv) and argv[i].endswith('.tsv'): tsv = argv[i]; i += 1
        b = open(binf, 'rb').read(); n = len(b) // N; assert n * N == len(b)
        tags = [label] * n
        if tsv:
            L = open(tsv).read().splitlines()
            if len(L) == n + 1: L = L[1:]
            if len(L) == n: tags = [tag(l) for l in L]
        agg = collections.defaultdict(lambda: collections.Counter())
        tot = collections.Counter()
        mine = set()
        for k in range(n):
            w = list(b[k * N:(k + 1) * N]); fl = flags(w)
            tg = tags[k]; tot[tg] += 1
            for x in fl: agg[tg][x] += 1
            if fl: agg[tg]['ANY'] += 1
            h = hashlib.sha1(bytes(w)).digest()
            if h in mine: dup_in += 1
            elif h in seen and seen[h] != label: dup_cross += 1
            mine.add(h)
            if h not in seen: seen[h] = label
            if fl: print('F', label, k, tg, ','.join(fl))
        for tg in sorted(tot):
            a = agg[tg]
            print('S', label, tg, 'windows', tot[tg], 'ANY', a['ANY'], ' '.join(f'{x}={a[x]}' for x in sorted(a) if x != 'ANY'))
        print('L', label, 'windows', n, 'distinct', len(mine), 'sha256', hashlib.sha256(b).hexdigest()[:16])
    print('D within-list duplicate windows', dup_in, 'cross-list duplicates (first occurrence elsewhere)', dup_cross)
main(sys.argv[1:])
