"""PREREG244 T4 (I-407): (a) reversal pairs in alpha.bin / themed144.bin; (b) brute-force check of the Z27 reversal identity
(g1, V, Y^R, M1) == (g1, B, Y, M1) on the 24 implied key letters (S3b: X in {AZ, KA}, every Y whose reverse is listed) for K4 and
the 12 case-229 nulls, plus non-identity analogues (g0; M0; form R; X reversed too = S1-type); (c) class-rank re-score of gate H
on the 10 case-229 H plants.  usage: twin244.py REPO > twin244.txt"""
import sys, json, numpy as np
R = sys.argv[1]
A = np.fromfile('alpha.bin', dtype=np.uint8).reshape(-1, 26); TH = np.fromfile('themed144.bin', dtype=np.uint8).reshape(-1, 26)
def pairs(L):
    idx = {bytes(r): i for i, r in enumerate(L)}
    return [(i, idx[bytes(r[::-1])]) for i, r in enumerate(L) if bytes(r[::-1]) in idx]
pa, pt = pairs(A), pairs(TH)
print(f'(a) alpha.bin: {len(A)} rows, {len(pa)} rows whose reverse is listed ({sum(1 for i, j in pa if abs(j - i) == 2)} of them at distance 2: '
      f'{sum(1 for i, j in pa if j - i == 2)} with the reverse at +2, {sum(1 for i, j in pa if i - j == 2)} at -2; palindromes impossible); themed144: {len(pt)} rows whose reverse is listed')
POS = list(range(21, 34)) + list(range(63, 74)); PT = [ord(c) - 65 for c in 'EASTNORTHEAST' + 'BERLINCLOCK']
ADD = np.zeros((2, 27, 27), int); SUB = np.zeros((2, 27, 27), int)
for a in range(27):
    for b in range(27):
        s = d = 0; m = 1
        for t in range(3):
            da, db = (a // m) % 3, (b // m) % 3; s += ((da + db) % 3) * m; d += ((da - db) % 3) * m; m *= 3
        ADD[0, a, b], SUB[0, a, b] = s, d; ADD[1, a, b], SUB[1, a, b] = (a + b) % 27, (a - b) % 27
def keyof(g, f, p, c): return SUB[g][c, p] if f == 0 else SUB[g][p, c] if f == 1 else ADD[g][c, p]
def inv(L):
    I = np.zeros_like(L)
    for i in range(26): I[np.arange(len(L)), L[:, i]] = i
    return I
AI = inv(A); AZ = np.arange(26, dtype=np.uint8)
def letters(ct, X, Y, YI, g, f, M):
    """X: one alphabet (26,), Y: (n,26). returns (n,24) letters, 255 for cell 26."""
    C = np.array([ord(ch) - 65 for ch in ct]); xi = np.argsort(X)
    p = xi[PT]; c = YI[:, C[POS]]                       # (24,), (n,24)
    k = keyof(g, f, p[None, :], c)                      # (n,24) cells 0..26
    Ma = X[None, :].repeat(len(Y), 0) if M == 0 else Y if M == 1 else AZ[None, :].repeat(len(Y), 0)
    Ma27 = np.concatenate([Ma, np.full((len(Y), 1), 255, np.uint8)], 1)
    return np.take_along_axis(Ma27, k, 1)
k4 = open('k4.txt').read().strip(); nulls = [l.split('\t')[1].strip() for l in open('nulls243.tsv')]
I0 = np.array([i for i, j in pa]); J0 = np.array([j for i, j in pa])
res = {}
tests = {'g1 V(Y^R) vs B(Y), M1 [identity]': (1, 0, 2, 1), 'g1 B(Y^R) vs V(Y), M1 [identity]': (1, 2, 0, 1),
         'g0 V(Y^R) vs B(Y), M1': (0, 0, 2, 1), 'g1 V(Y^R) vs B(Y), M0': (1, 0, 2, 0), 'g1 R(Y^R) vs R(Y), M1': (1, 1, 1, 1)}
for name, (g, fa, fb, M) in tests.items():
    exc = tot = 0
    for ct in [k4] + nulls:
        for X in (A[0], A[1]):
            La = letters(ct, X, A[J0], AI[J0], g, fa, M); Lb = letters(ct, X, A[I0], AI[I0], g, fb, M)
            exc += int((La != Lb).any(1).sum()); tot += len(I0)
    res[name] = (exc, tot); print(f'(b) {name}: {exc} of {tot} (text, X, Y) triples differ')
# S1-type: X = Y reversed together (eq scope). Expected identity: (g1, V, Y^R, M2) == (g1, R, Y, M2) and (g1, R, Y^R, M2) == (g1, V, Y, M2)
# (p' = 25 - p, c' = 25 - c => c' - p' = p - c); not with M0 / M1 (letters reflected) nor in g0.
def s1(ct, i, j, g, fa, fb, M):
    La = letters(ct, A[j], A[j:j+1], AI[j:j+1], g, fa, M); Lb = letters(ct, A[i], A[i:i+1], AI[i:i+1], g, fb, M)
    return int((La != Lb).any())
s1t = {'S1 g1 V(Y^R) vs R(Y), M2 [identity]': (1, 0, 1, 2), 'S1 g1 R(Y^R) vs V(Y), M2 [identity]': (1, 1, 0, 2),
       'S1 g1 V(Y^R) vs R(Y), M1': (1, 0, 1, 1), 'S1 g0 V(Y^R) vs R(Y), M2': (0, 0, 1, 2), 'S1 g1 V(Y^R) vs B(Y), M1': (1, 0, 2, 1)}
for name, (g, fa, fb, M) in s1t.items():
    exc = tot = 0
    for ct in [k4] + nulls:
        for i, j in pa[::12]:
            exc += s1(ct, i, j, g, fa, fb, M); tot += 1
    print(f'(b) {name} (every 12th pair): {exc} of {tot} differ')
# (c) class rank on gate H plants
old = json.load(open(R + '/data/cycle243/summary243.json')); nullmax = max(old['null_Hmax'])
plants = [l.rstrip('\n').split('\t') for l in open(R + '/tools/cycle243/plants243.tsv') if l[0].isdigit()] if False else None
P = [l.rstrip('\n').split('\t') for l in open('plants243.tsv')]
gH = 0
for p in P:
    pid = int(p[0])
    if pid < 10: continue
    scope, x, y, g, f, M = p[1], int(p[2]), int(p[3]), int(p[4]), int(p[5]), int(p[6])
    H = []
    for sc in ('S1', 'S2', 'S3a', 'S3b'):
        for ln in open(R + f'/data/cycle243/out/P{pid}/{sc}.txt'):
            a = ln.split()
            if a[0] == 'H': H.append((float(a[1]), sc, int(a[2]), int(a[3]), int(a[4]), int(a[5]), int(a[6]), a[7] + a[8]))
    H.sort(key=lambda h: -h[0])
    classes = []
    for h in H:
        key = (round(h[0], 5), h[7])
        if key not in classes: classes.append(key)
    me = [h for h in H if (h[1][:2] == scope[:2]) and (h[2], h[3], h[4], h[5], h[6]) == (g, f, x, y, M)]
    crank = classes.index((round(me[0][0], 5), me[0][7])) + 1 if me else None
    lrank = H.index(me[0]) + 1 if me else None
    ok = crank == 1 and me[0][0] > nullmax
    gH += ok; tw = [h for h in H if (round(h[0], 5), h[7]) == classes[0]]
    print(f'(c) plant {pid}: line rank {lrank}, class rank {crank}, top class size {len(tw)} {"PASS" if ok else "FAIL"}' + (f'  members {[(h[1], h[2], h[3], h[4], h[5], h[6]) for h in tw]}' if len(tw) > 1 else ''))
print(f'(c) gate H by class: {gH}/10 (post hoc for case 229; registered for later Part H gates)')
