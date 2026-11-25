"""Gate P / tier-2 plants (PREREG240, seed 209717): plant235.py with partial-English plaintexts.
20 plants, ids 0-7 direct (X, Y from alpha.bin), 8-13 behind bank.bin, 14-19 behind all.bin (themed144.bin, random row and dir),
random window w from keys233.bin, random form, random ix (families) -- same draws as plant235 for the cipher side.
Plaintext: 97-letter K1-K3 English window, cribs written in, then partial240.partial(f, model):
  f = [1.0, 0.7, 0.5, 0.3, 1.0][id // 4]; model = S for id % 4 in {0, 1}, B for {2, 3}.
Odd ids: one carved letter at a random NON-crib plaintext position replaced by a different letter (one-error plants).
Writes plants240.tsv: id scope ct row dir ix X Y form w corrupted_pos f model m plaintext"""
import random, struct
from partial240 import *
R = random.Random(209717)
def rec(fn, n): b = open(fn, 'rb').read(); return [b[i:i + n] for i in range(0, len(b), n)]
AL, TH, K = rec('alpha.bin', 26), rec('themed144.bin', 26), rec('keys233.bin', N)
eng = eng_text(); out = []
for pid in range(20):
    scope = 'direct' if pid < 8 else 'bank' if pid < 14 else 'all'
    f = [1.0, 0.7, 0.5, 0.3, 1.0][pid // 4]; model = 'S' if pid % 4 in (0, 1) else 'B'
    pt, m = partial(base_pt(eng, R), f, model, R)
    w = R.randrange(len(K)); fm = R.randrange(3)
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
        yy = (xx + k) % 26 if fm == 0 else (xx - k) % 26 if fm == 1 else (k - xx) % 26
        ct[cp[i]] = chr(65 + Y[yy])
    bad = -1
    if pid % 2 == 1:
        bad = R.choice(NONCRIB); c0 = cp[bad]; old = ct[c0]
        ct[c0] = R.choice([c for c in AZ if c != old])
    out.append((pid, scope, ''.join(ct), qi, dr, ix, x, y, fm, w, bad, f, model, m, pt))
with open('plants240.tsv', 'w') as fh:
    for o in out: fh.write('\t'.join(map(str, o)) + '\n')
print('plants', len(out))
