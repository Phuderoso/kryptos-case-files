"""Independent checker (PREREG235, Gate T): for each 'H' line of a gn235 file, re-derive agree8 / agree24 from scratch with the
window's key, decrypt all 97 letters under model Q, recompute NC from quadgrams.json (same table as qg.bin, max |diff| 2.8e-7).
usage: check235.py CT perms.bin|x Xalpha.bin Yalpha.bin keys.bin lines.txt   -> prints '# lines L mismatches M maxdNC D'"""
import sys, json, struct
N = 97
ct = sys.argv[1].strip(); C = [ord(c) - 65 for c in ct]
pf, xf, yf, kf, lf = sys.argv[2:7]
def rec(fn, n): b = open(fn, 'rb').read(); return [b[i:i + n] for i in range(0, len(b), n)]
XA, YA, K = rec(xf, 26), rec(yf, 26), rec(kf, N)
perms = None if pf == 'x' else open(pf, 'rb').read()
Q = json.load(open('quadgrams.json')); q, floor = Q['q'], Q['floor']
CRIB = set(range(21, 34)) | set(range(63, 74)); IDX = [21, 22, 23, 24, 63, 64, 65, 66]
cribs = {21 + j: c for j, c in enumerate('EASTNORTHEAST')}; cribs.update({63 + j: c for j, c in enumerate('BERLINCLOCK')})
def nc(t):
    sc = [q.get(t[i:i + 4], floor) for i in range(N - 3) if not (set(range(i, i + 4)) & CRIB)]
    return sum(sc) / len(sc), len(sc)
L = mm = 0; md = 0.0
for line in open(lf):
    if not line.startswith('H'): continue
    d = dict(kv.split('=') for kv in line.split()[1:])
    qi, dr, ix, x, y, f, w = (int(d[k]) for k in ('perm', 'dir', 'ix', 'X', 'Y', 'form', 'w'))
    if qi < 0: cp = list(range(N))
    else:
        P = list(struct.unpack('<97h', perms[qi * 194:(qi + 1) * 194])); inv = [0] * N
        for i, v in enumerate(P): inv[v] = i
        cp = P if dr == 0 else inv
    X, Y, Kw = XA[x], YA[y], K[w]; yinv = [0] * 26
    for i, v in enumerate(Y): yinv[v] = i
    pt = ''
    for i in range(N):
        k = Kw[i] if ix == 0 else Kw[cp[i]]; yy = yinv[C[cp[i]]]
        xx = (yy - k) % 26 if f == 0 else (yy + k) % 26 if f == 1 else (k - yy) % 26
        pt += chr(65 + X[xx])
    a8 = sum(pt[p] == cribs[p] for p in IDX); a24 = sum(pt[p] == c for p, c in cribs.items()); s, n = nc(pt)
    L += 1; dn = abs(s - float(d['nc'])); md = max(md, dn)
    if a8 != 8 or a24 != int(d['agree24']) or n != 64 or dn > 1e-3 or pt != d['pt']: mm += 1
print(f'# lines {L} mismatches {mm} maxdNC {md:.2e}')
