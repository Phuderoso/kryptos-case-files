"""Cycle 228 shared decrypt / NC reader for col1e / col1e4 hit lines (I-312 chunk 3 and the I-331 re-read).
Conventions copied from tools/cycle225/analyze225.py (reading_order, S_of, PAIRS, CRP / CRS); the only changes are the two house
rules of PREREG227: (b) a residue class whose crib-seat key values tie for the top multiplicity reads '?' (tie='?'),
(a) NC = mean log10 quadgram (qg.bin, float32, 26^4 little-endian, index ((a*26+b)*26+c)*26+d) over quadgrams with no '?' and no
crib position (21-33, 63-73); candidate iff known >= 49 and nq >= 10 and NC >= -6.0.
Hit tuple: (w, mode, dir, al, be, model, p, excess, bad, pi)."""
import collections, math
import numpy as np
KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"; AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; PAIRS = [(AZ, AZ), (KA, KA), (AZ, KA), (KA, AZ)]
CRP = list(range(21, 34)) + list(range(63, 74)); CRS = "EASTNORTHEASTBERLINCLOCK"; CRSET = set(CRP)
BAR, KMIN, QMIN = -6.0, 49, 10
_qg = None
def load_qg(path):
    global _qg; _qg = np.fromfile(path, dtype=np.float32); assert _qg.size == 26**4
def reading_order(w, pi, mode):
    rows = (97 + w - 1) // w; col_at = sorted(range(w), key=lambda c: pi[c])
    if mode == 1: return [r*w + c for c in col_at for r in range(rows) if r*w + c < 97]
    return [r*w + c for r in range(rows) for c in col_at if r*w + c < 97]
def S_of(w, pi, mode, dir_):
    sig = [0]*97
    for m, cell in enumerate(reading_order(w, pi, mode)): sig[cell] = m
    if dir_ == 0: return sig
    inv = [0]*97
    for i in range(97): inv[sig[i]] = i
    return inv
def decrypt(ct, h, tie="?"):
    """tie='?': tied top class reads '?'; tie='first': first seat's value (old kb226 / analyze225 rule, audit only)."""
    w, mode, dir_, al, be, model, p, e, bad, pi = h
    CA, PA = PAIRS[al]; S = S_of(w, list(pi), mode, dir_)
    cls = lambda i: (i if model == 0 else S[i]) % p
    votes = collections.defaultdict(collections.Counter)
    for t, i in enumerate(CRP):
        c = CA.index(ct[S[i]]); x = PA.index(CRS[t]); votes[cls(i)][(c + x) % 26 if be else (c - x) % 26] += 1
    key = {}
    for r, v in votes.items():
        mc = v.most_common()
        if tie == "?" and len(mc) > 1 and mc[1][1] == mc[0][1]: continue
        key[r] = mc[0][0]
    P = []
    for i in range(97):
        r = cls(i)
        if r not in key: P.append("?"); continue
        c = CA.index(ct[S[i]]); P.append(PA[(key[r] - c) % 26] if be else PA[(c - key[r]) % 26])
    return "".join(P), key, S, cls
def nc(P):
    q = [float(_qg[((ord(P[i])-65)*26 + ord(P[i+1])-65)*676 + (ord(P[i+2])-65)*26 + ord(P[i+3])-65]) for i in range(94)
         if "?" not in P[i:i+4] and not (CRSET & {i, i+1, i+2, i+3})]
    return (sum(q)/len(q) if q else float("nan")), len(q)
def read(ct, h, tie="?"):
    P, key, S, cls = decrypt(ct, h, tie); s, n = nc(P); known = 97 - P.count("?")
    return {"pt": P, "known": known, "nq": n, "nc": s, "barred": known >= KMIN and n >= QMIN, "pass": known >= KMIN and n >= QMIN and s >= BAR}
def d2sig(h):
    S = S_of(h[0], list(h[9]), h[1], h[2]); return h[:7] + tuple(S[i] for i in CRP)
def wilson(k, n, z=1.959964):
    if n == 0: return (float("nan"), float("nan"))
    ph = k/n; d = 1 + z*z/n; c = (ph + z*z/(2*n))/d; hw = z*math.sqrt(ph*(1-ph)/n + z*z/(4*n*n))/d
    return (max(0.0, c-hw), min(1.0, c+hw))
def parse_H(line, has_label=True):
    a = line.split(); a = a[2:] if has_label else a[1:]
    v = [int(x) for x in a[:9]]; return tuple(v) + (tuple(int(x) for x in a[9:]),)
