"""Cycle 233 (PREREG233, I-361 arithmetic-sequence keys): key streams from named integer sequences.
Writes keys233.bin (uint8 [W][97]) and keys233.tsv. Windows already in keys217/218/221 files (argv) are dropped, as are duplicates.
Key at plaintext position i (0-based): k_i = (f(o + i) + c) mod 26 ("fwd") or (f(o + 96 - i) + c) mod 26 ("rev"),
o = 0..39, c in {0, 1} (A = 0 or A = 1 reading of the value), for the open sequences S1-S22 (n starts at 1 unless noted).
Finite word-length streams W1-W4 (K1, K2, K3 plaintext, all three joined) are read cyclically, every offset, c in {0, 1}, fwd only.
Open sequences: S1 primes p_n; S2 prime gaps; S3 pi(n); S4 phi(n); S5 d(n); S6 sigma(n); S7 digit sum of n; S8 popcount(n);
S9 Thue-Morse; S10 Collatz total steps; S11 partition numbers p(n); S12 Catalan C_n; S13 Bell B_n; S14 Moebius (-1,0,1);
S15 Recaman; S16 Stern diatomic; S17 Kolakoski; S18 look-and-say length; S19 Josephus J(n) (k=2); S20 letters in the English
name of n; S21 n written in Roman numerals: number of letters; S22 n-th prime's digit sum.
"""
import sys, math
from math import gcd
def primes(m):
    s = bytearray([1]) * (m + 1); s[0:2] = b'\0\0'
    for i in range(2, int(m ** .5) + 1):
        if s[i]: s[i * i::i] = bytearray(len(s[i * i::i]))
    return [i for i, v in enumerate(s) if v]
PR = primes(5000); PS = set(PR); M = 400
def phi(n): return sum(1 for k in range(1, n + 1) if gcd(k, n) == 1)
def divs(n): return [d for d in range(1, n + 1) if n % d == 0]
def collatz(n):
    c = 0
    while n != 1: n = n // 2 if n % 2 == 0 else 3 * n + 1; c += 1
    return c
def partitions(m):
    p = [1] + [0] * m
    for k in range(1, m + 1):
        for j in range(k, m + 1): p[j] += p[j - k]
    return p
def catalan(m): return [math.comb(2 * n, n) // (n + 1) for n in range(m + 1)]
def bell(m):
    row = [1]; out = [1]
    for _ in range(m):
        new = [row[-1]]
        for x in row: new.append(new[-1] + x)
        row = new; out.append(row[0])
    return out
def mobius(n):
    r = 1; m = n; q = 2
    while q * q <= m:
        if m % q == 0:
            m //= q
            if m % q == 0: return 0
            r = -r
        q += 1
    return -r if m > 1 else r
def recaman(m):
    a = [0]; seen = {0}
    for n in range(1, m + 1):
        x = a[-1] - n
        if x < 0 or x in seen: x = a[-1] + n
        a.append(x); seen.add(x)
    return a
def stern(m):
    s = [0, 1]
    for n in range(2, m + 1): s.append(s[n // 2] if n % 2 == 0 else s[n // 2] + s[n // 2 + 1])
    return s
def kolakoski(m):
    k = [1, 2, 2]; i = 2
    while len(k) < m + 2:
        k += [1 if k[-1] == 2 else 2] * k[i]; i += 1
    return k
def las(m):
    s = '1'; out = [1]
    for _ in range(m):
        t = ''; i = 0
        while i < len(s):
            j = i
            while j < len(s) and s[j] == s[i]: j += 1
            t += str(j - i) + s[i]; i = j
        s = t; out.append(len(s))
        if len(s) > 10 ** 5: break
    return out
def josephus(n): return 2 * (n - (1 << (n.bit_length() - 1))) + 1
ONES = 'ONE TWO THREE FOUR FIVE SIX SEVEN EIGHT NINE TEN ELEVEN TWELVE THIRTEEN FOURTEEN FIFTEEN SIXTEEN SEVENTEEN EIGHTEEN NINETEEN'.split()
TENS = 'TWENTY THIRTY FORTY FIFTY SIXTY SEVENTY EIGHTY NINETY'.split()
def name(n):
    if n < 20: return ONES[n - 1]
    if n < 100: return TENS[n // 10 - 2] + (ONES[n % 10 - 1] if n % 10 else '')
    h = ONES[n // 100 - 1] + 'HUNDRED'
    return h + ('AND' + name(n % 100) if n % 100 else '')
def roman(n):
    out = ''
    for v, s in [(1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'), (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'), (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')]:
        while n >= v: out += s; n -= v
    return out
def seq(fn, a=1, b=M): return {n: fn(n) for n in range(a, b + 1)}
P = partitions(M); C = catalan(M); B = bell(M); R = recaman(M); S = stern(M); K = kolakoski(M); L = las(M)
SEQS = {
 'S1_primes': lambda n: PR[n - 1], 'S2_primegap': lambda n: PR[n] - PR[n - 1], 'S3_pi': lambda n: sum(1 for p in PR if p <= n),
 'S4_phi': phi, 'S5_d': lambda n: len(divs(n)), 'S6_sigma': lambda n: sum(divs(n)), 'S7_digsum': lambda n: sum(map(int, str(n))),
 'S8_popcount': lambda n: bin(n).count('1'), 'S9_thuemorse': lambda n: bin(n - 1).count('1') % 2, 'S10_collatz': collatz,
 'S11_partitions': lambda n: P[n], 'S12_catalan': lambda n: C[n], 'S13_bell': lambda n: B[n], 'S14_moebius': mobius,
 'S15_recaman': lambda n: R[n], 'S16_stern': lambda n: S[n], 'S17_kolakoski': lambda n: K[n - 1], 'S18_lookandsay': lambda n: L[n - 1] if n - 1 < len(L) else 0,
 'S19_josephus': josephus, 'S20_engname': lambda n: len(name(n)), 'S21_roman': lambda n: len(roman(n)), 'S22_primedigsum': lambda n: sum(map(int, str(PR[n - 1]))),
}
K1 = 'BETWEEN SUBTLE SHADING AND THE ABSENCE OF LIGHT LIES THE NUANCE OF IQLUSION'
K2 = ('IT WAS TOTALLY INVISIBLE HOWS THAT POSSIBLE THEY USED THE EARTHS MAGNETIC FIELD X THE INFORMATION WAS GATHERED AND TRANSMITTED UNDERGRUUND '
      'TO AN UNKNOWN LOCATION X DOES LANGLEY KNOW ABOUT THIS THEY SHOULD ITS BURIED OUT THERE SOMEWHERE X WHO KNOWS THE EXACT LOCATION ONLY WW '
      'THIS WAS HIS LAST MESSAGE X THIRTY EIGHT DEGREES FIFTY SEVEN MINUTES SIX POINT FIVE SECONDS NORTH SEVEN SEVEN DEGREES EIGHT MINUTES '
      'FORTY FOUR SECONDS WEST X LAYER TWO')
K3 = ('SLOWLY DESPARATLY SLOWLY THE REMAINS OF PASSAGE DEBRIS THAT ENCUMBERED THE LOWER PART OF THE DOORWAY WAS REMOVED WITH TREMBLING HANDS '
      'I MADE A TINY BREACH IN THE UPPER LEFT HAND CORNER AND THEN WIDENING THE HOLE A LITTLE I INSERTED THE CANDLE AND PEERED IN THE HOT AIR '
      'ESCAPING FROM THE CHAMBER CAUSED THE FLAME TO FLICKER BUT PRESENTLY DETAILS OF THE ROOM WITHIN EMERGED FROM THE MIST X CAN YOU SEE ANYTHING Q')
WL = {'W1_K1': K1, 'W2_K2': K2, 'W3_K3': K3, 'W4_K123': K1 + ' ' + K2 + ' ' + K3}
seen = set()
for fn in sys.argv[1:]:
    b = open(fn, 'rb').read()
    for i in range(0, len(b), 97): seen.add(b[i:i + 97])
rows = []
def add(fam, o, c, d, vec):
    t = bytes(v % 26 for v in vec)
    if t in seen: return
    seen.add(t); rows.append((fam, o, c, d, t))
for nm, f in SEQS.items():
    vals = {}
    def g(n):
        if n not in vals: vals[n] = f(n)
        return vals[n]
    for d in ('fwd', 'rev'):
        for o in range(40):
            for c in (0, 1):
                if d == 'fwd': add(nm, o, c, d, [g(1 + o + i) + c for i in range(97)])
                else: add(nm, o, c, d, [g(1 + o + 96 - i) + c for i in range(97)])
for nm, s in WL.items():
    w = [len(x) for x in s.split()]; L_ = len(w)
    for o in range(L_):
        for c in (0, 1): add(nm, o, c, 'fwd', [w[(o + i) % L_] + c for i in range(97)])
open('keys233.bin', 'wb').write(b''.join(r[4] for r in rows))
with open('keys233.tsv', 'w') as fh:
    for r in rows: fh.write(f'{r[0]}\t{r[1]}\t{r[2]}\t{r[3]}\n')
from collections import Counter
print(len(rows), 'windows', dict(Counter(r[0] for r in rows)))
