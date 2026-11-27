"""Gate plants (PREREG243, seed 209770). 20 plants, plaintext = 97-letter K1-K3 English window (k123_eng.txt) with cribs written in.
Scopes by id % 10: 0-3 S1 (X = Y from alpha.bin), 4-6 S2 (X, Y from themed144.bin), 7-9 S3 (one of X / Y from alpha.bin,
the other AZ or KA). g = id % 2, form random, map M random among the maps rk243 keeps (S1: X or A-Z).
ids 0-9  (gate E, exact): key = a running key from texts243.txt (random text, random offset, cyclic).
          ids 1,3,5,7,9 carry one wrong carved letter at a crib seat: id 1 in anchor A (seats 0-3), id 3 in anchor B
          (seats 13-16), id 5 elsewhere in EASTNORTHEAST (seats 4-12), id 7 elsewhere in BERLINCLOCK (17-23), id 9 any seat.
ids 10-19 (gate H, heuristic): key = H. G. Wells, The Time Machine (Gutenberg #35, letters only; not in the exact list)
          at a random offset; no error.
Re-drawn (text window + offset) until no carved cell is 26. Writes plants243.tsv:
id scope x y g f M keysrc offset errseat ct"""
import random
from m242 import *
R = random.Random(209770)
AL, TH = rec('alpha.bin'), rec('themed144.bin')
eng = ''.join(ch for ch in open('k123_eng.txt').read().upper() if ch.isalpha())
TXT = [l.split() for l in open('texts243.txt') if l.strip()]
TM = open('tm35_letters.txt').read().strip()
AZ = list(range(26))
def keep_maps(X, Y, s1):
    ms = [0] if s1 else [0, 1]
    if not s1 and Y == X: ms = [0]
    if AZ != X and AZ != Y: ms.append(2)
    return ms
out = []
for pid in range(20):
    r10 = pid % 10; g = pid % 2; f = R.randrange(3)
    while True:
        if r10 < 4: scope = 'S1'; x = y = R.randrange(len(AL)); X = Y = AL[x]
        elif r10 < 7: scope = 'S2'; x, y = R.randrange(len(TH)), R.randrange(len(TH)); X, Y = TH[x], TH[y]
        else:
            scope = 'S3'
            if R.random() < 0.5: x, y = R.randrange(len(AL)), R.randrange(2)
            else: x, y = R.randrange(2), R.randrange(len(AL))
            X, Y = AL[x], AL[y]
        M = R.choice(keep_maps(X, Y, scope == 'S1'))
        Ma = X if M == 0 else Y if M == 1 else AZ
        mi = inv(Ma)                      # key letter -> cell
        xi = inv(X)
        if pid < 10: name, T = R.choice(TXT)
        else: name, T = 'timemachine35', TM
        ok = False
        for tries in range(3000):
            o = R.randrange(len(T)); s0 = R.randrange(len(eng) - N); pt = list(eng[s0:s0 + N])
            for j, q in enumerate(POS): pt[q] = CR[j]
            c = []
            for i in range(N):
                v = enc(g, f, xi[ord(pt[i]) - 65], mi[ord(T[(o + i) % len(T)]) - 65])
                if v == 26: break
                c.append(v)
            if len(c) == N: ok = True; break
        if ok: break
    ct = [chr(65 + Y[v]) for v in c]; es = -1
    if pid < 10 and pid % 2 == 1:
        es = {1: R.randrange(0, 4), 3: R.randrange(13, 17), 5: R.randrange(4, 13), 7: R.randrange(17, 24), 9: R.randrange(24)}[pid]
        q = POS[es]; ct[q] = R.choice([ch for ch in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' if ch != ct[q]])
    out.append((pid, scope, x, y, g, f, M, name, o, es, ''.join(ct)))
with open('plants243.tsv', 'w') as fo:
    for r in out: fo.write('\t'.join(map(str, r)) + '\n')
for r in out: print(' '.join(map(str, r[:10])))
