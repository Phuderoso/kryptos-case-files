"""Independent checker (PREREG217): for each 'H' line, re-derive the 24 crib agreements from scratch with the window's key,
decrypt all 97 letters under model Q, and score with quadgrams (mean log10 per quadgram).
usage: check217.py CTfile perms.bin|x Xalpha.bin Yalpha.bin keys.bin lines.txt [out.tsv]"""
import sys, json, math
N = 97
ct = open(sys.argv[1]).read().strip(); C = [ord(c) - 65 for c in ct]
pf, xf, yf, kf, lf = sys.argv[2:7]
def rec(fn, n): b = open(fn, 'rb').read(); return [b[i:i + n] for i in range(0, len(b), n)]
XA, YA, K = rec(xf, 26), rec(yf, 26), rec(kf, N)
perms = None if pf == 'x' else open(pf, 'rb').read()
Q = json.load(open('quadgrams.json')); q, floor = Q['q'], Q['floor']  # same support file and convention as check216.py
def qs(t):
    sc = [q.get(t[i:i + 4], floor) for i in range(len(t) - 3)]; return sum(sc) / len(sc)
cribs = {21 + j: c for j, c in enumerate('EASTNORTHEAST')}; cribs.update({63 + j: c for j, c in enumerate('BERLINCLOCK')})
def row(qi):
    import struct
    return list(struct.unpack('<97h', perms[qi * 194:(qi + 1) * 194]))
out = []
for line in open(lf):
    if not line.startswith('H'): continue
    d = dict(kv.split('=') for kv in line.split()[1:])
    qi, dr, ix, x, y, f, w = (int(d[k]) for k in ('perm', 'dir', 'ix', 'X', 'Y', 'form', 'w'))
    if qi < 0: cp = list(range(N))
    else:
        P = row(qi); inv = [0] * N
        for i, v in enumerate(P): inv[v] = i
        cp = P if dr == 0 else inv
    X, Y, Kw = XA[x], YA[y], K[w]
    yinv = [0] * 26
    for i, v in enumerate(Y): yinv[v] = i
    pt = []
    for i in range(N):
        k = Kw[i] if ix == 0 else Kw[cp[i]]
        yy = yinv[C[cp[i]]]
        xx = (yy - k) % 26 if f == 0 else (yy + k) % 26 if f == 1 else (k - yy) % 26
        pt.append(chr(65 + X[xx]))
    pt = ''.join(pt)
    ag = sum(pt[p] == c for p, c in cribs.items())
    out.append((line.strip(), ag, int(d['agree']), round(qs(pt), 3), pt))
for o in out: print(*o, sep='\t')
mm = sum(1 for o in out if o[1] != o[2])
print(f'# lines {len(out)} agreement mismatches {mm}', file=sys.stderr)
if len(sys.argv) > 7:
    with open(sys.argv[7], 'w') as fh:
        for o in out: fh.write('\t'.join(map(str, o)) + '\n')
