"""Cycle 187 independent decoder for lrk186 M lines (string level; no lrk186 code): CRT-combine the listed mod-2 and mod-13 solutions
(weights c, seed at carved positions 0..L-1, constant d), regenerate the carved-index key mod 26, decrypt all 97 letters through perm q
with (A, B, form), and return the plaintexts whose 24 crib letters all match (one per listed solution pair, up to 32 x 32)."""
import numpy as np
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; CI = list(range(21, 34)) + list(range(63, 74)); CR = "EASTNORTHEASTBERLINCLOCK"
AL = {}
def load_alpha(*fns):
    for fn in fns:
        for l in open(fn): a, b = l.split(); AL[b] = a
def crt(a2, a13): return next(x for x in range(26) if x % 2 == a2 and x % 13 == a13)
def parse(a):
    L = int(a[3]); i2, i13 = a.index("S2"), a.index("S13"); s2, s13 = [], []
    for t in a[i2 + 1:i13]:
        cb, rest = t[1:].split("s"); sb, db = rest.split("d"); s2.append(([int(x) for x in cb], [int(x) for x in sb], int(db)))
    for t in a[i13 + 1:]:
        cs, rest = t[1:].split("x"); xs, nl = rest.split("n"); c = [int(x) for x in cs.split(",")]; x = [int(v) for v in xs.split(",")]
        s13.append((c, x[:L], x[L], int(nl)))
    return L, s2, s13
def decode_line(ct, P, a):
    L, s2, s13 = parse(a); form, q, A, B = a[5], int(a[6]), AL[a[7]], AL[a[8]]; S = P[q]; res = []
    for c2, sd2, d2 in s2:
        for c13, sd13, d13, nl in s13:
            c = [crt(c2[i], c13[i]) for i in range(L)]; k = [crt(sd2[i], sd13[i]) for i in range(L)]; d = crt(d2, d13)
            while len(k) < 97: k.append((sum(c[j] * k[-1 - j] for j in range(L)) + d) % 26)
            pt = "".join(A[(B.index(ct[S[i]]) - k[S[i]]) % 26] if form == "vig" else A[(k[S[i]] - B.index(ct[S[i]])) % 26] for i in range(97))
            if all(pt[i] == CR[t] for t, i in enumerate(CI)): res.append((c, d, k[:L], pt))
    return res
