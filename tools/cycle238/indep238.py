"""PREREG238 Part A3 (added as a disclosed extra, see case 224): independent regeneration of the 7 long-stream digit strings of keys217 with plain-integer arithmetic (no mpmath) and
comparison of every keys217 long-stream window (offsets 0..399, shift 0/-1) with the published keys217.bin. Dropped duplicates are skipped by tsv id."""
from math import isqrt
D = 800; S = 10 ** D
def atan_inv(x, S=S):
    s = t = S // x; n = 1; x2 = x * x; sign = 1
    while t:
        t //= x2; n += 2; sign = -sign; s += sign * (t // n)
    return s
pi = 4 * (4 * atan_inv(5) - atan_inv(239))
e = 0; t = S; k = 0
while t: e += t; k += 1; t //= k
sqrt2 = isqrt(2 * S * S); sqrt3 = isqrt(3 * S * S); sqrt5 = isqrt(5 * S * S); phi = (S + sqrt5) // 2
# ln2 = sum_{k>=1} 1/(k 2^k)
ln2 = 0; p = S // 2; k = 1
while p: ln2 += p // k; p //= 2; k += 1
def digs(x): return str(x)[:700]   # integer part digit(s) then decimals, first 700 digits (as keys217: nstr with '.' removed); ln2 < 1 -> leading 0 handled below
dg = {'pi': digs(pi), 'e': digs(e), 'sqrt2': digs(sqrt2), 'sqrt3': digs(sqrt3), 'sqrt5': digs(sqrt5), 'phi': digs(phi), 'ln2': ('0' + str(ln2).zfill(D))[:700]}
for k, v in dg.items(): print(k, v[:20])
b = open('keys217.bin', 'rb').read()
rows = [l.split('\t') for l in open('../repo/data/cycle217/keys217.tsv').read().splitlines()[1:]]
bad = 0; chk = 0
for r in rows:
    i, name, off, s, cyc = int(r[0]), r[1], int(r[2]), int(r[3]), int(r[4])
    if cyc: continue
    d = dg[name]
    exp = bytes((10 * int(d[off + 2 * t]) + int(d[off + 2 * t + 1]) + s) % 26 for t in range(97))
    chk += 1
    if exp != b[i * 97:(i + 1) * 97]: bad += 1
print('long-stream windows checked', chk, 'mismatches', bad)
