"""Cycle 242 (PREREG242, I-399) shared code, written independently of tri242.c (pure Python):
27-cell groups g0 = Z3^3 carry-free (digit-wise base-3 addition), g1 = Z27; forms V c=p+k, R c=p-k, B c=k-p.
Cell of a letter = its index in the keyed alphabet (0..25); cell 26 is the extra symbol (never carved)."""
import json, math
N = 97
C1, C2 = "EASTNORTHEAST", "BERLINCLOCK"
POS = list(range(21, 34)) + list(range(63, 74))
CR = C1 + C2
def tri(a): return [(a // 1) % 3, (a // 3) % 3, (a // 9) % 3]
def untri(t): return t[0] + 3 * t[1] + 9 * t[2]
def add(g, a, b): return untri([(x + y) % 3 for x, y in zip(tri(a), tri(b))]) if g == 0 else (a + b) % 27
def sub(g, a, b): return untri([(x - y) % 3 for x, y in zip(tri(a), tri(b))]) if g == 0 else (a - b) % 27
def enc(g, f, p, k): return add(g, p, k) if f == 0 else sub(g, p, k) if f == 1 else sub(g, k, p)
def dec(g, f, c, k): return sub(g, c, k) if f == 0 else add(g, c, k) if f == 1 else sub(g, k, c)
def keyof(g, f, p, c): return sub(g, c, p) if f == 0 else sub(g, p, c) if f == 1 else add(g, c, p)
def rec(fn): b = open(fn, 'rb').read(); return [list(b[i:i + 26]) for i in range(0, len(b), 26)]
def inv(A):
    r = [0] * 26
    for i, v in enumerate(A): r[v] = i
    return r
QG = None
def nc(pt, skip=set(POS)):
    """mean log10 quadgram (data/support/quadgrams.json) over quadgrams whose 4 positions are known letters and touch no crib seat; returns (nc, nq)"""
    global QG
    if QG is None: QG = json.load(open('quadgrams.json'))
    q, fl = QG['q'], QG['floor']; s = 0.0; n = 0
    for i in range(N - 3):
        w = pt[i:i + 4]
        if any(ch is None or ch == '?' for ch in w) or any(i + d in skip for d in range(4)): continue
        s += q.get(''.join(w), fl); n += 1
    return (s / n if n else float('nan'), n)
def decrypt_line(ct, model, g, f, X, Y, par, M):
    """Full or partial decrypt implied by a survivor line; None = undetermined, '?' = cell 26."""
    xi, yi = inv(X), inv(Y); c = [yi[ord(ch) - 65] for ch in ct]
    Ma = X if M == 0 else Y; mi = xi if M == 0 else yi
    p = [None] * N
    for j, q in enumerate(POS): p[q] = xi[ord(CR[j]) - 65]
    k = {q: keyof(g, f, p[q], c[q]) for q in POS}
    if model == 'PER':
        res = {}
        for q in POS: res.setdefault(q % par, []).append(k[q])
        kr = {r: max(set(v), key=v.count) for r, v in res.items()}
        for i in range(N):
            if p[i] is None and i % par in kr: p[i] = dec(g, f, c[i], kr[i % par])
    elif model == 'CA':
        for i in range(par, N):
            if p[i] is None: p[i] = dec(g, f, c[i], mi[ord(ct[i - par]) - 65])
    elif model == 'PA':
        changed = True
        while changed:
            changed = False
            for i in range(N):
                if p[i] is not None: continue
                if i - par >= 0 and p[i - par] is not None and p[i - par] != 26:
                    kk = mi[X[p[i - par]]]; p[i] = dec(g, f, c[i], kk); changed = True; continue
                if i + par < N and p[i + par] is not None:
                    kk = keyof(g, f, p[i + par], c[i + par])
                    if kk < 26: p[i] = xi[Ma[kk]]; changed = True
    return [None if v is None else '?' if v == 26 else chr(65 + X[v]) for v in p]
