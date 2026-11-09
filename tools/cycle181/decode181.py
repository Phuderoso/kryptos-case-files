"""Cycle 181: string-level replay + decode of lrk181 fits (independent of the C code: rebuilds the keyed tableau from the alphabet
string, recomputes the key stream from the listed CRT solutions, checks the 23 crib letters other than the wild slot (all 24 for a
strict line, t -1), decrypts and scores). usage: decode181.py CT perms.bin quadgrams.json alphafile label out.txt M-files..."""
import sys, json, itertools
import numpy as np
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
CRIB = {**{21 + i: c for i, c in enumerate("EASTNORTHEAST")}, **{63 + i: c for i, c in enumerate("BERLINCLOCK")}}
CI = sorted(CRIB)
def crt(a2, a13): return (13 * a2 + 14 * a13) % 26
QG = None; ALPHA = {}
def load_qg(fn):
    global QG; QG = json.load(open(fn))
def load_alpha(fn):
    for l in open(fn):
        a, lb = l.split(); ALPHA[lb] = a
def score(s):
    q, fl = QG["q"], QG["floor"]; v = [q.get(s[i:i + 4], fl) for i in range(len(s) - 3) if all(j not in CRIB for j in range(i, i + 4)) and "?" not in s[i:i + 4]]
    return sum(v) / len(v) if v else -99
def tab(alab, ty):
    K = ALPHA[alab]; return {"q1": (K, AZ), "q2": (AZ, K), "q3": (K, K)}[ty]
def kv(cl, pl, A, B, form): return (B.index(cl) - A.index(pl)) % 26 if form == "vig" else (B.index(cl) + A.index(pl)) % 26
def dec(cl, k, A, B, form):
    j = B.index(cl); return A[(j - k) % 26] if form == "vig" else A[(k - j) % 26]
def stream(c, d, seed):
    k = list(seed)
    while len(k) < 97: k.append((sum(c[j] * k[-1 - j] for j in range(len(c))) + d) % 26)
    return k
def ok_cribs(pt, wild): return all(pt[i] == CRIB[i] for i in CRIB if i != wild)
def replay_m0(ct, S, L, A, B, form, c, d, wild, V):
    k = {i: kv(ct[S[i]], CRIB[i], A, B, form) for i in CRIB}
    if wild >= 0 and V >= 0: k[wild] = V
    kk = [None] * 97
    for i in range(21, 34): kk[i] = k[i]
    for i in range(34, 97): kk[i] = (sum(c[j] * kk[i - 1 - j] for j in range(L)) + d) % 26
    if any(kk[i] != k[i] for i in range(63, 74) if i != wild): return None
    inv = {a: b for a in range(26) for b in range(26) if a * b % 26 == 1}
    if c[L - 1] in inv:
        for i in range(20, -1, -1): kk[i] = inv[c[L - 1]] * (kk[i + L] - d - sum(c[j] * kk[i + L - 1 - j] for j in range(L - 1))) % 26
    pt = "".join(dec(ct[S[i]], kk[i], A, B, form) if kk[i] is not None else "?" for i in range(97))
    return pt if ok_cribs(pt, wild) else None
def replay_ix1(ct, S, A, B, form, k, wild):
    pt = "".join(dec(ct[S[i]], k[S[i]], A, B, form) for i in range(97)); return pt if ok_cribs(pt, wild) else None
def decode_line(ct, P, a):
    kind, L, ty, form, q, alab = a[2], int(a[3]), a[4], a[5], int(a[6]), a[7]; S = [int(x) for x in P[q]]; A, B = tab(alab, ty); res = []
    wild = int(a[a.index("slot") + 1]); i2, i13 = a.index("S2"), a.index("S13")
    if kind == "0":
        V = int(a[a.index("V") + 1])
        s2 = [list(map(int, x.split(","))) for x in a[i2 + 1:i13]]; s13 = [list(map(int, x.split(","))) for x in a[i13 + 1:]]
        for x2, x13 in itertools.product(s2, s13):
            x = [crt(u, v) for u, v in zip(x2, x13)]; pt = replay_m0(ct, S, L, A, B, form, x[:L], x[L], wild, V)
            if pt: res.append((score(pt), pt, f"c={x[:L]} d={x[L]} wild={wild} V={V}"))
    else:      # every mod-2 stream whose crib bits match off the wild slot is re-enumerated (the printed one may differ off-crib
               # when c is even mod 2, the cycle-179 decoder lesson); mod 13: the printed weight vector and particular solution
        J = [int(S[i]) for i in CI]; ko = [kv(ct[S[i]], CRIB[i], A, B, form) for i in CI]
        cpart, rest = a[i13 + 1][1:].split("x"); xpart, nul = rest.split("n"); c13 = [int(v) for v in cpart.split(",")]; x13 = [int(v) for v in xpart.split(",")]
        for z in range(1 << (2 * L + 1)):
            c2 = [(z >> j) & 1 for j in range(L)]; sd2 = [(z >> (L + j)) & 1 for j in range(L)]; d2 = (z >> (2 * L)) & 1
            b = list(sd2)
            while len(b) < 97: b.append((sum(c2[j] * b[-1 - j] for j in range(L)) + d2) % 2)
            if any(b[J[u]] != ko[u] % 2 for u in range(24) if CI[u] != wild): continue
            c = [crt(u, v) for u, v in zip(c2, c13)]; seed = [crt(u, v) for u, v in zip(sd2, x13[:L])]; d = crt(d2, x13[L])
            pt = replay_ix1(ct, S, A, B, form, stream(c, d, seed), wild)
            if pt: res.append((score(pt), pt, f"c={c} d={d} seed={seed} null13={nul} wild={wild}"))
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
                s, pt, par = r[0]; o.write(f"D {lab} ix{a[2]} L{a[3]} {a[4]} {a[5]} q{a[6]} {a[7]} t{a[a.index('t')+1]} nrep {len(r)} best {s:.3f} {par} {pt}\n")
