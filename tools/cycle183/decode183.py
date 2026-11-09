"""Cycle 183: string-level replay + decode of lrk183 one-error fits (independent of the C code: rebuilds the keyed tableau from the
alphabet strings, recomputes the key stream from the seed and the listed CRT solutions, checks the 24 crib letters except the wild
slot, decrypts and scores). Wild slot t with value V >= 0: the key at that slot is V (it may be a seed); V = -2: block-2 slot ignored.
usage: decode183.py CT perms.bin quadgrams.json alphafile[,alphafile2] label out.txt M-files...      (also imported by checkctl183.py)"""
import sys, json, itertools
import numpy as np
CRIB = {**{21 + i: c for i, c in enumerate("EASTNORTHEAST")}, **{63 + i: c for i, c in enumerate("BERLINCLOCK")}}
def crt(a2, a13): return (13 * a2 + 14 * a13) % 26
QG = None; ALPHA = {}
def load_qg(fn):
    global QG; QG = json.load(open(fn))
def load_alpha(fns):
    for fn in fns.split(","):
        for l in open(fn):
            a, lb = l.split(); assert ALPHA.get(lb, a) == a; ALPHA[lb] = a
def score(s):
    q, fl = QG["q"], QG["floor"]; v = [q.get(s[i:i + 4], fl) for i in range(len(s) - 3) if all(j not in CRIB for j in range(i, i + 4)) and "?" not in s[i:i + 4]]
    return sum(v) / len(v) if v else -99
def kv(cl, pl, A, B, form): return (B.index(cl) - A.index(pl)) % 26 if form == "vig" else (B.index(cl) + A.index(pl)) % 26
def dec(cl, k, A, B, form):
    j = B.index(cl); return A[(j - k) % 26] if form == "vig" else A[(k - j) % 26]
def replay(ct, S, L, A, B, form, c, d, slot, V):
    k = {i: kv(ct[S[i]], CRIB[i], A, B, form) for i in CRIB}
    if V >= 0: k[slot] = V
    kk = [None] * 97
    for i in range(21, 21 + L): kk[i] = k[i]
    for i in range(21 + L, 97): kk[i] = (sum(c[j] * kk[i - 1 - j] for j in range(L)) + d) % 26
    if any(kk[i] != k[i] for i in CRIB if i != slot): return None
    inv = {a: b for a in range(26) for b in range(26) if a * b % 26 == 1}
    if c[L - 1] in inv:
        for i in range(20, -1, -1): kk[i] = inv[c[L - 1]] * (kk[i + L] - d - sum(c[j] * kk[i + L - 1 - j] for j in range(L - 1))) % 26
    pt = "".join(dec(ct[S[i]], kk[i], A, B, form) if kk[i] is not None else "?" for i in range(97))
    return pt if all(pt[i] == CRIB[i] for i in CRIB if i != slot) else None
def decode_line(ct, P, a):
    L, form, q, alab, blab = int(a[3]), a[5], int(a[6]), a[7], a[8]; slot, V = int(a[12]), int(a[14])
    S = [int(x) for x in P[q]]; A, B = ALPHA[alab], ALPHA[blab]; res = []
    i2, i13 = a.index("S2"), a.index("S13")
    s2 = [list(map(int, x.split(","))) for x in a[i2 + 1:i13]]; s13 = [list(map(int, x.split(","))) for x in a[i13 + 1:]]
    for x2, x13 in itertools.product(s2, s13):
        x = [crt(u, v) for u, v in zip(x2[:L + 1], x13[:L + 1])]; pt = replay(ct, S, L, A, B, form, x[:L], x[L], slot, V)
        if pt: res.append((score(pt), pt, f"c={x[:L]} d={x[L]} slot={slot} V={V}"))
    return sorted(res, reverse=True)
if __name__ == "__main__":
    ct, pf, qf, af, lab, out = sys.argv[1:7]; load_qg(qf); load_alpha(af); P = np.fromfile(pf, dtype=np.int16).reshape(-1, 97)
    with open(out, "w") as o:
        for fn in sys.argv[7:]:
            for l in open(fn):
                a = l.split()
                if not a or a[0] != "M": continue
                r = decode_line(ct, P, a)
                if not r: o.write(f"REPLAYFAIL {l}"); continue
                s, pt, par = r[0]; o.write(f"D {lab} L{a[3]} {a[4]} {a[5]} q{a[6]} {a[7]} {a[8]} t{a[10]} nrep {len(r)} best {s:.3f} {par} {pt}\n")
