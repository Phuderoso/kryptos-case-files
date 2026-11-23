"""Gate P plants (PREREG236, seed 209672): 20 plants, ids 0-7 direct (X, Y from alpha.bin), 8-13 behind bank.bin, 14-19 behind
all.bin (X, Y from themed144.bin, random row and dir). Random window w from keys236.bin, random form, random ix (families).
Plaintext: 97-letter K1-K3 English window with the cribs written in. Odd ids: one carved crib letter replaced by a different letter.
Writes plants236.tsv: id scope ct row dir ix X Y form w corrupted_seat plaintext"""
import random, struct
N = 97; R = random.Random(209672)
def rec(fn, n): b = open(fn, 'rb').read(); return [b[i:i + n] for i in range(0, len(b), n)]
AL, TH, K = rec('alpha.bin', 26), rec('themed144.bin', 26), rec('keys236.bin', N)
eng = ''.join(c for c in open('k123_eng.txt').read().upper() if c.isalpha())
POS = list(range(21, 34)) + list(range(63, 74)); CR = 'EASTNORTHEAST' + 'BERLINCLOCK'
out = []
for pid in range(20):
    scope = 'direct' if pid < 8 else 'bank' if pid < 14 else 'all'
    s0 = R.randrange(len(eng) - N); pt = list(eng[s0:s0 + N])
    for p, c in zip(POS, CR): pt[p] = c
    pt = ''.join(pt)
    w = R.randrange(len(K)); f = R.randrange(3)
    if scope == 'direct':
        A = AL; x, y = R.randrange(len(A)), R.randrange(len(A)); qi, dr, ix = -1, 0, 0; cp = list(range(N))
    else:
        A = TH; x, y = R.randrange(len(A)), R.randrange(len(A))
        pb = open(scope + '.bin', 'rb').read(); nrow = len(pb) // 194; qi = R.randrange(nrow); dr = R.randrange(2); ix = R.randrange(2)
        P = list(struct.unpack('<97h', pb[qi * 194:(qi + 1) * 194])); inv = [0] * N
        for i, v in enumerate(P): inv[v] = i
        cp = P if dr == 0 else inv
    X, Y = A[x], A[y]; xinv = [0] * 26
    for i, v in enumerate(X): xinv[v] = i
    ct = [None] * N
    for i in range(N):
        k = K[w][i] if ix == 0 else K[w][cp[i]]; xx = xinv[ord(pt[i]) - 65]
        yy = (xx + k) % 26 if f == 0 else (xx - k) % 26 if f == 1 else (k - xx) % 26
        ct[cp[i]] = chr(65 + Y[yy])
    seat = -1
    if pid % 2 == 1:
        seat = R.randrange(24); c0 = cp[POS[seat]]; old = ct[c0]
        ct[c0] = R.choice([c for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' if c != old])
    out.append((pid, scope, ''.join(ct), qi, dr, ix, x, y, f, w, seat, pt))
with open('plants236.tsv', 'w') as fh:
    for o in out: fh.write('\t'.join(map(str, o)) + '\n')
print('plants', len(out))
