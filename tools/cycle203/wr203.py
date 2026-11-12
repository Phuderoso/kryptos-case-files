#!/usr/bin/env python3
"""Cycle 203 (I-256): word-restart key family. R1 = key index is the in-word position mod L;
R2 = one key letter per word, advancing per word. AZ / KA tableaux, Vigenere / Beaufort / variant.
Exact crib-consistency check at the carved positions. See PREREG203.md."""
import itertools, json, random, sys
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"
K4 = open(__file__.rsplit('/',3)[0] + "/data/k4.txt").read().split()[0].strip()
CRIBS = [(21, "EASTNORTHEAST"), (63, "BERLINCLOCK")]
SEG_E = {"EASTNORTHEAST": [], "EAST|NORTHEAST": [4], "EASTNORTH|EAST": [9], "EAST|NORTH|EAST": [4, 9]}
SEG_B = {"BERLINCLOCK": [], "BERLIN|CLOCK": [6]}

def kv(c, p, alph, mode):
    ci, pi = alph.index(c), alph.index(p)
    if mode == "vig": return (ci - pi) % 26
    if mode == "beau": return (ci + pi) % 26
    return (pi - ci) % 26           # variant

def enc(p, k, alph, mode):
    pi, ki = alph.index(p), alph.index(k)
    if mode == "vig": return alph[(pi + ki) % 26]
    if mode == "beau": return alph[(ki - pi) % 26]
    return alph[(pi - ki) % 26]

def all_segs(n, minlen=2):
    """boundary sets inside a crib of length n; fully internal words >= minlen letters"""
    out = []
    for r in range(0, n):
        for b in itertools.combinations(range(1, n), r):
            ok = all(b[i+1] - b[i] >= minlen for i in range(len(b)-1))
            if ok: out.append(list(b))
    return out

def r1_map(ct, start, crib, bnds, o, L, alph, mode):
    """dict key-index -> key value, or None on contradiction"""
    m = {}
    for j, p in enumerate(crib):
        prev = [b for b in bnds if b <= j]
        idx = ((j - prev[-1]) if prev else (o + j)) % L
        v = kv(ct[start + j], p, alph, mode)
        if m.setdefault(idx, v) != v: return None
    return m

def r2_map(ct, start, crib, bnds, w0, L, alph, mode):
    m = {}
    for j, p in enumerate(crib):
        idx = (w0 + sum(1 for b in bnds if b <= j)) % L
        v = kv(ct[start + j], p, alph, mode)
        if m.setdefault(idx, v) != v: return None
    return m

def compat(a, b):
    return all(b.get(k, v) == v for k, v in a.items())

def survivors(ct, rule, Ls, segE, segB, configs=None):
    """list of surviving (alph, mode, L, segE, segB, o1, o2) and merged key maps"""
    out = []
    fn = r1_map if rule == "R1" else r2_map
    for an, alph in (("AZ", AZ), ("KA", KA)):
        for mode in ("vig", "beau", "var"):
            for L in Ls:
                m1s = [(sn, o, fn(ct, CRIBS[0][0], CRIBS[0][1], b, o, L, alph, mode))
                       for sn, b in segE.items() for o in range(L)]
                m1s = [x for x in m1s if x[2] is not None]
                if not m1s: continue
                rng2 = range(L)
                m2s = [(sn, o, fn(ct, CRIBS[1][0], CRIBS[1][1], b, o, L, alph, mode))
                       for sn, b in segB.items() for o in rng2]
                m2s = [x for x in m2s if x[2] is not None]
                for a in m1s:
                    for b in m2s:
                        if compat(a[2], b[2]):
                            mm = dict(a[2]); mm.update(b[2])
                            out.append(dict(alph=an, mode=mode, L=L, segE=a[0], segB=b[0], o1=a[1], o2=b[1],
                                            key={k: (AZ if an == "AZ" else KA)[v] for k, v in sorted(mm.items())}))
    return out
