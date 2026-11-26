"""Gate P plants (PREREG242, seed 209757). 20 plants: ids 0-7 S1 (X = Y from alpha.bin), 8-13 S2 (X, Y from themed144.bin),
14-19 S3 (one of X / Y from alpha.bin, the other AZ or KA = alpha rows 0 / 1). g = id % 2; form random; model by id % 3:
PER (P with >= 8 crib constraints), CA (L 1-24, M random), PA (L in {1..9, 35..47}, M random).
Plaintext: 97-letter K1-K3 English window (k123_eng.txt), cribs written in. Key cells random 0..25 (letters of a key word).
Re-drawn (3,000 texts / keys per alphabet draw, then a new alphabet draw) until no carved cell is 26
(the hypothesis: the extra symbol never appears in the carving).
Odd ids: one-error plants -- the carved letter at one random crib seat replaced by a different letter.
Writes plants242.tsv: id scope x y g f model par M err_pos ct pt"""
import random
from m242 import *
R = random.Random(209757)
AL, TH = rec('alpha.bin'), rec('themed144.bin')
eng = ''.join(ch for ch in open('k123_eng.txt').read().upper() if ch.isalpha())
PERSET = [P for P in list(range(1, 24)) + list(range(35, 48)) if 24 - len({q % P for q in POS}) >= 8]
def attempt(pid, g, f, model, M):
    if pid < 8: scope = 'S1'; x = y = R.randrange(len(AL)); X = Y = AL[x]
    elif pid < 14: scope = 'S2'; x, y = R.randrange(len(TH)), R.randrange(len(TH)); X, Y = TH[x], TH[y]
    else:
        scope = 'S3'
        if R.random() < 0.5: x, y = R.randrange(len(AL)), R.randrange(2)
        else: x, y = R.randrange(2), R.randrange(len(AL))
        X, Y = AL[x], AL[y]
    par = R.choice(PERSET) if model == 'PER' else R.randrange(1, 25) if model == 'CA' else R.choice(list(range(1, 10)) + list(range(35, 48)))
    xi, yi = inv(X), inv(Y); mi = xi if M == 0 else yi
    for tries in range(3000):
        s0 = R.randrange(len(eng) - N); pt = list(eng[s0:s0 + N])
        for j, q in enumerate(POS): pt[q] = CR[j]
        p = [xi[ord(ch) - 65] for ch in pt]
        kk = [R.randrange(26) for _ in range(par)]
        c = []
        for i in range(N):
            if model == 'PER': k = kk[i % par]
            elif model == 'CA': k = kk[i] if i < par else mi[Y[c[i - par]]]
            else: k = kk[i] if i < par else mi[X[p[i - par]]]
            v = enc(g, f, p[i], k)
            if v == 26: break
            c.append(v)
        if len(c) == N: return scope, x, y, X, Y, par, c, pt
    return None
out = []
for pid in range(20):
    g = pid % 2; f = R.randrange(3); model = ['PER', 'CA', 'PA'][pid % 3]; M = R.randrange(2)
    r = None
    while r is None: r = attempt(pid, g, f, model, M)
    scope, x, y, X, Y, par, c, pt = r
    ct = [chr(65 + Y[v]) for v in c]; ep = -1
    if pid % 2 == 1:
        ep = R.choice(POS); ct[ep] = R.choice([ch for ch in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' if ch != ct[ep]])
    out.append((pid, scope, x, y, g, f, model, par, M, ep, ''.join(ct), ''.join(pt)))
with open('plants242.tsv', 'w') as fo:
    for r in out: fo.write('\t'.join(map(str, r)) + '\n')
for r in out: print(' '.join(map(str, r[:10])))
