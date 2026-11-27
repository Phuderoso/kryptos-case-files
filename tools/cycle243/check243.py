"""Gate T (PREREG243): pure Python re-derivation (shares only group arithmetic m242.keyof and the alphabet readers), independent of rk243.c.
For every printed S line of the named texts: recompute viol / error seat from the running-key text; for the top 5 H lines per scope file:
recompute the score from quadgrams.json. Usage: python3 check243.py NAME=CT ..."""
import sys, json
from m242 import *
AL, TH, AK = rec('alpha.bin'), rec('themed144.bin'), rec('azka.bin')
TX = dict(l.split() for l in open('texts243.txt') if l.strip())
QG = json.load(open('quadgrams.json')); q, fl = QG['q'], QG['floor']
LISTS = {'S1': (AL, AL), 'S2': (TH, TH), 'S3a': (AL, AK), 'S3b': (AK, AL)}
AZ = list(range(26))
def need(ct, X, Y, g, f, M):
    xi, yi = inv(X), inv(Y); Ma = X if M == 0 else Y if M == 1 else AZ
    out = []
    for j, p in enumerate(POS):
        k = keyof(g, f, xi[ord(CR[j]) - 65], yi[ord(ct[p]) - 65]); out.append(None if k == 26 else chr(65 + Ma[k]))
    return out
mis = n = 0
for arg in sys.argv[1:]:
    name, ct = arg.split('=')
    for sc, (XL, YL) in LISTS.items():
        nh = 0
        for l in open(f'out/{name}/{sc}.txt'):
            w = l.split()
            if w[0] == 'S':
                g, f, x, y, M = map(int, w[1:6]); t = TX[w[6]]; o = int(w[7])
                L = need(ct, XL[x], YL[y], g, f, M)
                bad = [j for j, p in enumerate(POS) if L[j] != t[(o + p) % len(t)]]
                v, e = len(bad), (bad[0] if len(bad) == 1 else -1)
                n += 1
                if v != int(w[8]) or e != int(w[9]): mis += 1; print('MISMATCH', name, sc, l.strip(), v, e)
            elif w[0] == 'H' and nh < 5:
                nh += 1; s = float(w[1]); g, f, x, y, M = map(int, w[2:7])
                L = need(ct, XL[x], YL[y], g, f, M)
                if None in L: mis += 1; print('MISMATCH 26', name, l.strip()); continue
                a, b = ''.join(L[:13]), ''.join(L[13:])
                sc2 = (sum(q.get(a[i:i + 4], fl) for i in range(10)) + sum(q.get(b[i:i + 4], fl) for i in range(8))) / 18
                n += 1
                if abs(sc2 - s) > 1e-4 or a != w[7] or b != w[8]: mis += 1; print('MISMATCH H', name, sc, l.strip(), sc2)
print('gate T lines', n, 'mismatches', mis)
