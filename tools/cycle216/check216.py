#!/usr/bin/env python3
"""Cycle 216 (PREREG216 Part A, I-297) stage 2: for every gron216 survivor line, re-derive the 24 crib digits from scratch, drop the
failing crib position (bad=j; for bad=-1 lines test the full 24 and each leave-one-out), and decide EXACTLY whether a Gromark chain
(primer L 1-25, k_n = k_{n-L} + k_{n-L+1} mod 10; elimination mod 2 and mod 5) or a periodic digit key (P 1-25) generates the remaining
23 digits, key index = plaintext position (ix 0) or carved position S[i] (ix 1). For each consistent (line, model) the solution set
is counted; if it has <= 1000 members every member is decrypted over all 97 positions and the best quadgram score (mean log10 per
quadgram, data/quadgrams.json of the repo support set) is kept. usage: check216.py CT perms.bin|x alphabets.bin FILE [FILE...] > json"""
import sys, json, struct, itertools
POS = list(range(21, 34)) + list(range(63, 74)); PT = "EASTNORTHEAST" + "BERLINCLOCK"; LMAX = 25
ct = sys.argv[1]; pf = sys.argv[2]; A = open(sys.argv[3], 'rb').read()
Q = json.load(open('quadgrams.json')); QG, FL = Q['q'], Q['floor']
def qscore(s): return sum(QG.get(s[i:i + 4], FL) for i in range(len(s) - 3)) / (len(s) - 3)
def alpha(a): return A[a * 26:(a + 1) * 26]
def perm(q):
    with open(pf, 'rb') as f: f.seek(q * 194); return list(struct.unpack('<97h', f.read(194)))
def Smap(q, d):
    if q < 0: return list(range(97))
    s = perm(q)
    if d == 0: return s
    inv = [0] * 97
    for i, v in enumerate(s): inv[v] = i
    return inv
def kf(f, y, x): return (y - x) % 26 if f == 0 else (x - y) % 26 if f == 1 else (y + x) % 26
_cache = {}
def chain(L):
    if L not in _cache:
        v = [[1 if a == n else 0 for a in range(L)] for n in range(L)]
        for n in range(L, 97):
            v.append([(v[n - L][a] + v[n - L + 1][a]) for a in range(L)] if L > 1 else [v[n - 1][0] * 2])
        _cache[L] = v
    return _cache[L]
def solve(rows, rhs, p):
    """Gaussian elimination mod p: None if inconsistent, else (particular solution, nullspace basis)."""
    n = len(rows[0]); M = [[c % p for c in r] + [b % p] for r, b in zip(rows, rhs)]; piv = []; r = 0
    for c in range(n):
        k = next((i for i in range(r, len(M)) if M[i][c]), None)
        if k is None: continue
        M[r], M[k] = M[k], M[r]; iv = pow(M[r][c], p - 2, p); M[r] = [(a * iv) % p for a in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c]:
                fct = M[i][c]; M[i] = [(a - fct * b) % p for a, b in zip(M[i], M[r])]
        piv.append(c); r += 1
    if any(not any(row[:-1]) and row[-1] for row in M): return None
    x0 = [0] * n
    for i, c in enumerate(piv): x0[c] = M[i][-1]
    free = [c for c in range(n) if c not in piv]; basis = []
    for fc in free:
        v = [0] * n; v[fc] = 1
        for i, c in enumerate(piv): v[c] = (-M[i][fc]) % p
        basis.append(v)
    return x0, basis
def gromark_solutions(idx, d, L, cap=1000):
    R = chain(L); rows = [[c % 10 for c in R[i]] for i in idx]
    s2 = solve(rows, d, 2); s5 = solve(rows, d, 5)
    if s2 is None or s5 is None: return 0, []
    n = 2 ** len(s2[1]) * 5 ** len(s5[1])
    if n > cap: return n, None
    out = []
    for c2 in itertools.product(range(2), repeat=len(s2[1])):
        a = [(s2[0][i] + sum(c * b[i] for c, b in zip(c2, s2[1]))) % 2 for i in range(L)]
        for c5 in itertools.product(range(5), repeat=len(s5[1])):
            b5 = [(s5[0][i] + sum(c * b[i] for c, b in zip(c5, s5[1]))) % 5 for i in range(L)]
            primer = [next(v for v in range(10) if v % 2 == a[i] and v % 5 == b5[i]) for i in range(L)]
            out.append([sum(r * pp for r, pp in zip(R[t], primer)) % 10 for t in range(97)])
    return n, out
def periodic_solutions(idx, d, P, cap=1000):
    seen = {}
    for i, k in zip(idx, d):
        if seen.setdefault(i % P, k) != k: return 0, []
    free = [r for r in range(P) if r not in seen]; n = 10 ** len(free)
    if n > cap: return n, None
    out = []
    for c in itertools.product(range(10), repeat=len(free)):
        kk = dict(seen); kk.update(zip(free, c)); out.append([kk[t % P] for t in range(97)])
    return n, out
def decrypt(S, X, Y, f, key, ix):
    xi = X; yi = {v: i for i, v in enumerate(Y)}; p = []
    for i in range(97):
        y = yi[ord(ct[S[i]]) - 65]; k = key[i] if ix == 0 else key[S[i]]
        x = (y - k) % 26 if f == 0 else (y + k) % 26 if f == 1 else (k - y) % 26
        p.append(chr(65 + xi[x]))
    return ''.join(p)
def analyse(q, dr, Xa, Ya, f):
    S = Smap(q, dr); X = alpha(Xa); Y = alpha(Ya); xi = {v: i for i, v in enumerate(X)}; yi = {v: i for i, v in enumerate(Y)}
    d = [kf(f, yi[ord(ct[S[i]]) - 65], xi[ord(PT[j]) - 65]) for j, i in enumerate(POS)]
    badl = [j for j in range(24) if d[j] > 9]
    drops = badl if badl else [None] + list(range(24))
    res = []
    for drop in drops:
        keep = [j for j in range(24) if j != drop]; dd = [d[j] for j in keep]
        for ix in (0, 1):
            idx = [POS[j] if ix == 0 else S[POS[j]] for j in keep]
            for kind, fn in (('gromark', gromark_solutions), ('periodic', periodic_solutions)):
                for L in range(1, LMAX + 1):
                    n, sols = fn(idx, dd, L)
                    if n == 0: continue
                    best = None
                    if sols is not None:
                        for key in sols:
                            pt = decrypt(S, X, Y, f, key, ix); sc = qscore(pt)
                            if best is None or sc > best[0]: best = (round(sc, 3), pt)
                    res.append(dict(drop=drop, ix=ix, model=kind, L=L, nsol=n, best=best))
    return d, badl, res
out = []
for fn in sys.argv[4:]:
    for l in open(fn):
        if not l.startswith('S '): continue
        kv = dict(t.split('=', 1) for t in l.split()[1:])
        q, dr, Xa, Ya, f = int(kv['perm']), int(kv['dir']), int(kv['X']), int(kv['Y']), int(kv['form'])
        d, badl, res = analyse(q, dr, Xa, Ya, f)
        ok = (len(badl) <= 1) and (badl == [] or badl[0] == int(kv['bad'])) and ','.join(map(str, d)) == kv['k']
        out.append(dict(file=fn.split('/')[-1], perm=q, dir=dr, X=Xa, Y=Ya, form=f, digits=d, bad=badl, rederive_ok=ok, consistent=res))
json.dump(out, sys.stdout); print()
