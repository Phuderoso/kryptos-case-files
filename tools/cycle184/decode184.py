"""Cycle 184 (copy of decode182.py, unchanged logic): string-level replay + decode of lrk182 fits (Quagmire IV: A = plaintext-side alphabet, B = ciphertext-side alphabet; adapted from decode180.py) (independent of the C code: rebuilds the keyed tableau from the alphabet
string, recomputes the key stream from the listed CRT solutions, checks all 24 crib letters, decrypts and scores).
usage: decode182.py CT perms.bin quadgrams.json alphafile[,alphafile2] label out.txt M-files...      (also imported by checkctl182.py)"""
import sys, json, itertools
import numpy as np
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
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
def tab(alab, blab):
    return ALPHA[alab], ALPHA[blab]                                              # (A plaintext side, B ciphertext side)
def kv(cl, pl, A, B, form):
    return (B.index(cl) - A.index(pl)) % 26 if form == "vig" else (B.index(cl) + A.index(pl)) % 26
def dec(cl, k, A, B, form):
    j = B.index(cl); return A[(j - k) % 26] if form == "vig" else A[(k - j) % 26]
def stream(c, d, seed):
    k = list(seed)
    while len(k) < 97: k.append((sum(c[j] * k[-1 - j] for j in range(len(c))) + d) % 26)
    return k
def replay_m0(ct, S, L, A, B, form, c, d):
    k = {i: kv(ct[S[i]], CRIB[i], A, B, form) for i in CRIB}; kk = [None] * 97
    for i in range(21, 34): kk[i] = k[i]
    for i in range(34, 97): kk[i] = (sum(c[j] * kk[i - 1 - j] for j in range(L)) + d) % 26
    if any(kk[i] != k[i] for i in range(63, 74)): return None
    inv = {a: b for a in range(26) for b in range(26) if a * b % 26 == 1}
    if c[L - 1] in inv:
        for i in range(20, -1, -1):
            kk[i] = inv[c[L - 1]] * (kk[i + L] - d - sum(c[j] * kk[i + L - 1 - j] for j in range(L - 1))) % 26
    pt = "".join(dec(ct[S[i]], kk[i], A, B, form) if kk[i] is not None else "?" for i in range(97))
    return pt if all(pt[i] == CRIB[i] for i in CRIB) else None
def replay_ix1(ct, S, A, B, form, k):
    pt = "".join(dec(ct[S[i]], k[S[i]], A, B, form) for i in range(97))
    return pt if all(pt[i] == CRIB[i] for i in CRIB) else None
def decode_line(ct, P, a):
    """a = split M line -> list of (score, pt, params) for every replayable CRT combination (cap 32 x 32)"""
    kind, L, ty, form, q, alab, blab = a[2], int(a[3]), a[4], a[5], int(a[6]), a[7], a[8]; S = [int(x) for x in P[q]]; A, B = tab(alab, blab); res = []
    i2, i13 = a.index("S2"), a.index("S13")
    if kind == "0":
        s2 = [list(map(int, x.split(","))) for x in a[i2 + 1:i13]]; s13 = [list(map(int, x.split(","))) for x in a[i13 + 1:]]
        for x2, x13 in itertools.product(s2, s13):
            x = [crt(u, v) for u, v in zip(x2, x13)]; pt = replay_m0(ct, S, L, A, B, form, x[:L], x[L])
            if pt: res.append((score(pt), pt, f"c={x[:L]} d={x[L]}"))
    else:
        s2 = []
        for t in a[i2 + 1:i13]:
            cb, rest = t[1:].split("s"); sb, db = rest.split("d"); s2.append(([int(v) for v in cb], [int(v) for v in sb], int(db)))
        s13 = []
        for t in a[i13 + 1:]:
            cpart, rest = t[1:].split("x"); xpart, nul = rest.split("n"); s13.append(([int(v) for v in cpart.split(",")], [int(v) for v in xpart.split(",")], int(nul)))
        for (c2, sd2, d2), (c13, x13, nul) in itertools.product(s2, s13):
            c = [crt(u, v) for u, v in zip(c2, c13)]; seed = [crt(u, v) for u, v in zip(sd2, x13[:L])]; d = crt(d2, x13[L])
            pt = replay_ix1(ct, S, A, B, form, stream(c, d, seed))
            if pt: res.append((score(pt), pt, f"c={c} d={d} seed={seed} null13={nul}"))
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
                s, pt, par = r[0]; o.write(f"D {lab} ix{a[2]} L{a[3]} {a[4]} {a[5]} q{a[6]} {a[7]} {a[8]} nrep {len(r)} best {s:.3f} {par} {pt}\n")
