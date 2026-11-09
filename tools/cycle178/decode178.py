"""Cycle 178: string-level replay + decode of lr178 fits (independent of the C code: recomputes the key stream from the listed
solutions, checks all 24 crib letters, decrypts every determined position and scores it).
usage: decode178.py CT perms.bin quadgrams.json label out.txt M-files...      (also imported by checkctl178.py)"""
import sys, json, itertools
import numpy as np
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"; CRIB = {**{21 + i: c for i, c in enumerate("EASTNORTHEAST")}, **{63 + i: c for i, c in enumerate("BERLINCLOCK")}}
def crt(a2, a13): return (13 * a2 + 14 * a13) % 26
QG = None
def score(s):
    q, fl = QG["q"], QG["floor"]; v = [q.get(s[i:i + 4], fl) for i in range(len(s) - 3) if all(j not in CRIB for j in range(i, i + 4)) and "?" not in s[i:i + 4]]
    return sum(v) / len(v) if v else -99
def dec(cl, k, alph, form):
    i = alph.index(cl); return alph[(i - k) % 26] if form == "vig" else alph[(k - i) % 26]
def replay_m0(ct, S, L, pa, form, c, d):
    alph = KA if pa == "ka" else AZ; k = {}
    for i in CRIB:
        ci, pi = alph.index(ct[S[i]]), alph.index(CRIB[i]); k[i] = (ci - pi) % 26 if form == "vig" else (ci + pi) % 26
    kk = [None] * 97
    for i in range(21, 34): kk[i] = k[i]
    for i in range(34, 97): kk[i] = (sum(c[j] * kk[i - 1 - j] for j in range(L)) + d) % 26
    if any(kk[i] != k[i] for i in range(63, 74)): return None
    inv = {a: b for a in range(26) for b in range(26) if a * b % 26 == 1}
    if c[L - 1] in inv:
        for i in range(20, -1, -1):
            kk[i] = inv[c[L - 1]] * (kk[i + L] - d - sum(c[j] * kk[i + L - 1 - j] for j in range(L - 1))) % 26
    return "".join(dec(ct[S[i]], kk[i], alph, form) if kk[i] is not None else "?" for i in range(97))
def stream(c, d, seed):
    k = list(seed)
    while len(k) < 97: k.append((sum(c[j] * k[-1 - j] for j in range(len(c))) + d) % 26)
    return k
def replay_ix1(ct, S, pa, form, k):
    alph = KA if pa == "ka" else AZ
    pt = "".join(dec(ct[S[i]], k[S[i]], alph, form) for i in range(97))
    return pt if all(pt[i] == CRIB[i] for i in CRIB) else None
def replay_ix0_stream(ct, S, pa, form, k):
    alph = KA if pa == "ka" else AZ
    pt = "".join(dec(ct[S[i]], k[i], alph, form) for i in range(97))
    return pt if all(pt[i] == CRIB[i] for i in CRIB) else None
def decode_line(ct, P, a):
    """a = split M line; returns list of (score, pt, params) for every replayable solution combination (cap 32x32)"""
    lab, kind, L, pa, form, q = a[1], a[2], int(a[3]), a[4], a[5], int(a[6]); S = [int(x) for x in P[q]]; res = []
    if kind == "0":
        i2, i13 = a.index("S2"), a.index("S13")
        s2 = [list(map(int, x.split(","))) for x in a[i2 + 1:i13]]; s13 = [list(map(int, x.split(","))) for x in a[i13 + 1:]]
        for x2, x13 in itertools.product(s2, s13):
            x = [crt(u, v) for u, v in zip(x2, x13)]; pt = replay_m0(ct, S, L, pa, form, x[:L], x[L])
            if pt: res.append((score(pt), pt, f"c={x[:L]} d={x[L]}"))
    elif kind == "1":
        i2, i13 = a.index("S2"), a.index("S13")
        s2 = []
        for t in a[i2 + 1:i13]:
            cb, rest = t[1:].split("s"); sb, db = rest.split("d"); s2.append(([int(v) for v in cb], [int(v) for v in sb], int(db)))
        s13 = []
        for t in a[i13 + 1:]:
            cpart, rest = t[1:].split("x"); xpart, nul = rest.split("n"); s13.append(([int(v) for v in cpart.split(",")], [int(v) for v in xpart.split(",")], int(nul)))
        for (c2, sd2, d2), (c13, x13, nul) in itertools.product(s2, s13):
            c = [crt(u, v) for u, v in zip(c2, c13)]; seed = [crt(u, v) for u, v in zip(sd2, x13[:L])]; d = crt(d2, x13[L])
            pt = replay_ix1(ct, S, pa, form, stream(c, d, seed))
            if pt: res.append((score(pt), pt, f"c={c} d={d} seed={seed} null13={nul}"))
    else:
        word, nb, cm, d = a[7], a[8], int(a[9][1:]), int(a[10][1:]); al = KA if nb == "kaN" else AZ
        c = [(cm >> j) & 1 for j in range(L)]; k = stream(c, d, [al.index(x) for x in word[:L]])
        pt = (replay_ix0_stream if kind == "W0" else replay_ix1)(ct, S, pa, form, k)
        if pt: res.append((score(pt), pt, f"word={word} {nb} c={c} d={d}"))
    return sorted(res, reverse=True)
def load_qg(fn):
    global QG; QG = json.load(open(fn))
if __name__ == "__main__":
    ct, pf, qf, lab, out = sys.argv[1:6]; load_qg(qf); P = np.fromfile(pf, dtype=np.int16).reshape(-1, 97)
    with open(out, "w") as o:
        for fn in sys.argv[6:]:
            for l in open(fn):
                a = l.split()
                if not a or a[0] != "M": continue
                r = decode_line(ct, P, a)
                if not r: o.write(f"REPLAYFAIL {l}"); continue
                s, pt, par = r[0]; o.write(f"D {lab} {a[2]} L{a[3]} {a[4]} {a[5]} q{a[6]} nrep {len(r)} best {s:.3f} {par} {pt}\n")
