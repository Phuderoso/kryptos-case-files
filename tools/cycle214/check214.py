#!/usr/bin/env python3
"""Cycle 214 (I-295) independent checker: re-derives the 24 crib digits of a (perm, dir, X, Y, form) from scratch (no C code),
then decides Gromark chain consistency (primer L 1-40, k_n = k_{n-L} + k_{n-L+1} mod 10) and periodic-digit consistency
(P 1-40) exactly, for key index = plaintext position (ix 0) or carved position S[i] (ix 1). Gromark: elimination mod 2 and mod 5."""
import sys
POS = list(range(21, 34)) + list(range(63, 74)); PT = "EASTNORTHEAST" + "BERLINCLOCK"
def load_alpha(fn):
    d = open(fn, "rb").read(); return [d[i:i + 26] for i in range(0, len(d), 26)]
def perm_row(fn, q):
    import struct
    with open(fn, "rb") as f: f.seek(q * 194); return list(struct.unpack("<97h", f.read(194)))
def digits(ct, S, X, Y, form):
    xi = {v: i for i, v in enumerate(X)}; yi = {v: i for i, v in enumerate(Y)}; out = []
    for j, i in enumerate(POS):
        x = xi[ord(PT[j]) - 65]; y = yi[ord(ct[S[i]]) - 65]
        k = (y - x) % 26 if form == 0 else (x - y) % 26 if form == 1 else (y + x) % 26
        out.append(k)
    return out
_cache = {}
def chain_rows(L):
    if L not in _cache:
        v = [[1 if a == n else 0 for a in range(L)] for n in range(L)]
        for n in range(L, 97): v.append([(v[n - L][a] + v[n - L + 1][a]) for a in range(L)]) if L > 1 else v.append([v[n - 1][0] * 2])
        _cache[L] = v
    return _cache[L]
def solvable(rows, rhs, p):
    M = [[c % p for c in r] + [b % p] for r, b in zip(rows, rhs)]; ncol = len(rows[0]); r = 0
    for c in range(ncol):
        piv = next((i for i in range(r, len(M)) if M[i][c]), None)
        if piv is None: continue
        M[r], M[piv] = M[piv], M[r]; inv = pow(M[r][c], p - 2, p)
        M[r] = [(a * inv) % p for a in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c]:
                f = M[i][c]; M[i] = [(a - f * b) % p for a, b in zip(M[i], M[r])]
        r += 1
    return all(any(row[:-1]) or row[-1] == 0 for row in M)
def gromark_ok(idx, d, L):
    # L=1: k_n = 2 k_{n-1} by the chain rule with k_{n-1}+k_{n} ambiguity; we define L=1 as k_n = k_{n-1}+k_{n-1}
    R = chain_rows(L); rows = [[c % 10 for c in R[i]] for i in idx]
    return solvable(rows, d, 2) and solvable(rows, d, 5)
def periodic_ok(idx, d, P):
    seen = {}
    for i, k in zip(idx, d):
        if seen.setdefault(i % P, k) != k: return False
    return True
def analyse(ct, S, X, Y, form, LMAX=40):
    d = digits(ct, S, X, Y, form)
    if max(d) > 9: return d, None
    res = {}
    for ix in (0, 1):
        idx = POS if ix == 0 else [S[i] for i in POS]
        res[ix] = dict(gromark=[L for L in range(1, LMAX + 1) if gromark_ok(idx, d, L)],
                       periodic=[P for P in range(1, LMAX + 1) if periodic_ok(idx, d, P)])
    return d, res
