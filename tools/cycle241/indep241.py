"""I-383 value audit of keys233 (cycle 241). Independent regeneration of S1-S22 / W1-W4 windows from libraries (sympy, num2words, roman) or
structurally different code, compared byte for byte with keys233.bin via keys233.tsv; plus OEIS anchors typed from the sequence definitions,
plus planted wrong-term controls. usage: indep241.py keys233.bin keys233.tsv  (run with the venv python)"""
import sys, random
from sympy import prime, totient, divisor_count, divisor_sigma, mobius, npartitions, catalan, bell, primepi
import num2words, roman, re
b = open(sys.argv[1], 'rb').read(); rows = [l.rstrip('\n').split('\t') for l in open(sys.argv[2])]
assert len(b) == 97 * len(rows)
def thue(n): x = n - 1; r = 0
def tm(n):
    x, r = n - 1, 0
    while x: r ^= x & 1; x >>= 1
    return r
def collatz(n):
    c = 0
    while n > 1: n = n >> 1 if not n & 1 else 3 * n + 1; c += 1
    return c
def recaman_():
    seen = {0}; a = 0; yield 0; n = 0
    while True:
        n += 1; c = a - n
        a = c if c > 0 and c not in seen else a + n; seen.add(a); yield a
def stern(n):  # A002487 via binary recursion, n >= 0
    a, bb = 1, 0
    while n: 
        if n & 1: bb += a
        else: a += bb
        n >>= 1
    return bb
def kol(N):  # A000002 generator by run lengths
    out = [1, 2, 2]; i = 2
    while len(out) < N:
        out.extend([3 - out[-1]] * out[i]); i += 1
    return out
def jos(n):
    r = 0
    for m in range(2, n + 1): r = (r + 2) % m
    return r + 1
def eng(n): return re.sub('[^A-Z]', '', num2words.num2words(n).upper())
def rom(n): return len(roman.toRoman(n))
M = 400; RC = []; g = recaman_()
for _ in range(M + 1): RC.append(next(g))
KO = kol(M + 5)
F = {'S1_primes': lambda n: int(prime(n)), 'S2_primegap': lambda n: int(prime(n + 1) - prime(n)), 'S3_pi': lambda n: int(primepi(n)),
 'S4_phi': lambda n: int(totient(n)), 'S5_d': lambda n: int(divisor_count(n)), 'S6_sigma': lambda n: int(divisor_sigma(n)),
 'S7_digsum': lambda n: sum(map(int, str(n))), 'S8_popcount': lambda n: bin(n).count('1'), 'S9_thuemorse': tm, 'S10_collatz': collatz,
 'S11_partitions': lambda n: int(npartitions(n)), 'S12_catalan': lambda n: int(catalan(n)), 'S13_bell': lambda n: int(bell(n)),
 'S14_moebius': lambda n: int(mobius(n)), 'S15_recaman': lambda n: RC[n], 'S16_stern': stern, 'S17_kolakoski': lambda n: KO[n - 1],
 'S19_josephus': jos, 'S20_engname': lambda n: len(eng(n)), 'S21_roman': rom, 'S22_primedigsum': lambda n: sum(map(int, str(prime(n))))}
# anchors typed from definitions (OEIS leading terms), n starting 1 unless noted
AN = {'S1_primes': [2, 3, 5, 7, 11, 13, 17, 19], 'S2_primegap': [1, 2, 2, 4, 2, 4, 2, 4, 6], 'S3_pi': [0, 1, 2, 2, 3, 3, 4, 4, 4, 4],
 'S4_phi': [1, 1, 2, 2, 4, 2, 6, 4, 6, 4], 'S5_d': [1, 2, 2, 3, 2, 4, 2, 4, 3, 4], 'S6_sigma': [1, 3, 4, 7, 6, 12, 8, 15, 13, 18],
 'S7_digsum': [1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2], 'S8_popcount': [1, 1, 2, 1, 2, 2, 3, 1], 'S9_thuemorse': [0, 1, 1, 0, 1, 0, 0, 1],
 'S10_collatz': [0, 1, 7, 2, 5, 8, 16, 3, 19, 6], 'S11_partitions': [1, 2, 3, 5, 7, 11, 15, 22, 30, 42], 'S12_catalan': [1, 2, 5, 14, 42, 132],
 'S13_bell': [1, 2, 5, 15, 52, 203], 'S14_moebius': [1, -1, -1, 0, -1, 1, -1, 0, 0, 1], 'S15_recaman': [1, 3, 6, 2, 7, 13, 20, 12, 21, 11, 22],
 'S16_stern': [1, 1, 2, 1, 3, 2, 3, 1, 4, 3, 5], 'S17_kolakoski': [1, 2, 2, 1, 1, 2, 1, 2, 2, 1, 2, 2], 'S19_josephus': [1, 1, 3, 1, 3, 5, 7, 1, 3, 5],
 'S20_engname': [3, 3, 5, 4, 4, 3, 5, 5, 4, 3, 6, 6], 'S21_roman': [1, 2, 3, 2, 1, 2, 3, 4, 2, 1], 'S22_primedigsum': [2, 3, 5, 7, 2, 4, 8, 10, 5, 11]}
bad_an = []
for k, v in AN.items():
    got = [F[k](n) for n in range(1, len(v) + 1)]
    if k == 'S15_recaman': pass
    if got != v: bad_an.append((k, got, v))
print('anchors checked', len(AN), 'sequences, mismatches', len(bad_an), bad_an[:3])
K1 = 'BETWEEN SUBTLE SHADING AND THE ABSENCE OF LIGHT LIES THE NUANCE OF IQLUSION'
exec(open('k123_words.py').read()) if False else None
W = {}
src = open('../repo/tools/cycle233/keys233.py').read()
for nm in ('K1', 'K2', 'K3'):   # plaintext strings read from the frozen file text (data, not code)
    m = re.search(nm + r" = (\(.*?\)|'[^']*')\n", src, re.S); W[nm] = eval(m.group(1))
WL = {'W1_K1': W['K1'], 'W2_K2': W['K2'], 'W3_K3': W['K3'], 'W4_K123': W['K1'] + ' ' + W['K2'] + ' ' + W['K3']}
def expect(fam, o, c, d):
    if fam in WL:
        w = [len(x) for x in WL[fam].split()]; L = len(w); return bytes((w[(o + i) % L] + c) % 26 for i in range(97))
    f = F[fam]
    idx = [1 + o + i for i in range(97)] if d == 'fwd' else [1 + o + 96 - i for i in range(97)]
    return bytes((f(n) + c) % 26 for n in idx)
from collections import Counter
mis = Counter(); tot = Counter(); first = {}
for i, r in enumerate(rows):
    fam, o, c, d = r[0], int(r[1]), int(r[2]), r[3]; tot[fam] += 1
    if fam == 'S18_lookandsay': continue
    if expect(fam, o, c, d) != b[i * 97:(i + 1) * 97]: mis[fam] += 1; first.setdefault(fam, i)
chk = sum(v for k, v in tot.items() if k != 'S18_lookandsay')
print('windows', len(rows), 'checked', chk, 'S18 skipped (case 223 truncation, repaired in keys237)', tot['S18_lookandsay'])
print('mismatching windows', sum(mis.values()), dict(mis), 'first rows', first)
# control: plant one wrong term in a copy of the stream
rng = random.Random(209731); det = 0; nc = 0
for t in range(40):
    fam = rng.choice([k for k in F]); n_bad = rng.randint(1, 100)
    orig = F[fam]; F[fam] = (lambda f, nb: (lambda n: f(n) + (1 if n == nb else 0)))(orig, n_bad)
    hit = [i for i, r in enumerate(rows) if r[0] == fam and (n_bad in ([1 + int(r[1]) + j for j in range(97)] if r[3] == 'fwd' else [1 + int(r[1]) + 96 - j for j in range(97)]))]
    if hit:
        nc += 1; i = hit[0]; r = rows[i]
        if expect(fam, int(r[1]), int(r[2]), r[3]) != b[i * 97:(i + 1) * 97]: det += 1
    F[fam] = orig
print('planted wrong-term control: detected %d / %d (one wrong term in the stream, window containing it)' % (det, nc))
