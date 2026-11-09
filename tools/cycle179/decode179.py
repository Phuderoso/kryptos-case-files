"""Cycle 179: string-level replay / decode of lr179 fit lines (independent of the C code).
M0 line: key at the crib slots = observed, with slot t replaced by CRT(v2, v13); (c, d) = CRT of listed mod-2 / mod-13 solutions;
seed = k[21..21+L-1]; propagate to 96; decrypt plaintext 21..96 ('?' before 21).
M1 line: (c, seed, d) = CRT of EVERY mod-2 stream matching the crib bits off slot t (re-enumerated here) with the printed
mod-13 solution (null dims set to 0); full 97 letters."""
import json, math, itertools
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"; AL = {"az": AZ, "ka": KA}
CI = list(range(21, 34)) + list(range(63, 74)); PTC = "EASTNORTHEASTBERLINCLOCK"
QG = None
def load_qg(f):
    global QG; QG = json.load(open(f))
def score(pt):
    s, n = 0.0, 0
    for i in range(len(pt) - 3):
        if any(i <= j <= i + 3 for j in CI) or "?" in pt[i:i + 4]: continue
        s += QG["q"].get(pt[i:i + 4], QG["floor"]); n += 1
    return s / n if n else -99
def crt(a2, a13): return next(x for x in range(26) if x % 2 == a2 % 2 and x % 13 == a13 % 13)
def dec(c, k, al, form): i = al.index(c); return al[(i - k) % 26] if form == "vig" else al[(k - i) % 26]
def kobs(ct, S, pa, form):
    al = AL[pa]; ci = [al.index(ct[S[i]]) for i in CI]; pi = [al.index(c) for c in PTC]
    return [(a - b) % 26 if form == "vig" else (a + b) % 26 for a, b in zip(ci, pi)]
def parse_sets(tok):        # ' v0:1,0;0,1; v1:...' -> {v: [[...],...]}
    out = {}
    for part in tok:
        v, sols = part.split(":"); out[int(v[1:])] = [list(map(int, s.split(","))) for s in sols.split(";") if s]
    return out
def decode_line(ct, P, a):
    lab, md, L, pa, form, q = a[1], a[2], int(a[3]), a[4], a[5], int(a[6]); S = P[q]; al = AL[pa]; t = int(a[8]); res = []
    if md == "0":
        i2, i13 = a.index("S2"), a.index("S13"); s2 = parse_sets(a[i2 + 1:i13]); s13 = parse_sets(a[i13 + 1:])
        ko = kobs(ct, S, pa, form)
        for (v2, X2), (v13, X13) in itertools.product(s2.items(), s13.items()):
            for x2, x13 in itertools.product(X2[:6], X13[:4]):
                x = [crt(u, w) for u, w in zip(x2, x13)]; c, d = x[:L], x[L]
                kk = dict(zip(CI, ko)); kk[CI[t]] = crt(v2, v13)
                k = [None] * 97
                for i in range(21, 21 + L): k[i] = kk[i]
                for i in range(21 + L, 97): k[i] = (sum(c[j] * k[i - 1 - j] for j in range(L)) + d) % 26
                pt = "".join("?" if k[i] is None else dec(ct[S[i]], k[i], al, form) for i in range(97))
                res.append((score(pt), pt, f"c{c} d{d} slot{CI[t]} v{kk[CI[t]]}"))
    else:
        i13 = a.index("S13"); s13 = a[i13 + 1]; ko = kobs(ct, S, pa, form); J = [int(S[i]) for i in CI]
        c13 = list(map(int, s13[1:].split("x")[0].split(","))); x13 = list(map(int, s13.split("x")[1].split("n")[0].split(",")))
        for z in range(1 << (2 * L + 1)):     # every mod-2 stream whose crib bits match except possibly at slot t
            cb = [(z >> j) & 1 for j in range(L)]; sb = [(z >> (L + j)) & 1 for j in range(L)]; db = (z >> (2 * L)) & 1
            b = list(sb)
            while len(b) < 97: b.append((sum(cb[j] * b[-1 - j] for j in range(L)) + db) % 2)
            if any(b[J[u]] != ko[u] % 2 for u in range(24) if u != t): continue
            c = [crt(u, w) for u, w in zip(cb, c13)]; seed = [crt(u, w) for u, w in zip(sb, x13[:L])]; d = crt(db, x13[L])
            k = list(seed)
            while len(k) < 97: k.append((sum(c[j] * k[-1 - j] for j in range(L)) + d) % 26)
            pt = "".join(dec(ct[S[i]], k[S[i]], al, form) for i in range(97))
            res.append((score(pt), pt, f"c{c} seed{seed} d{d} slot{CI[t]}"))
    res.sort(key=lambda r: -r[0]); return res
