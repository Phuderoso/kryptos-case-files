"""Cycle 135 controls: transposition-first (and one model-Q) periodic Quagmire
independently encrypted in Python, plus shuffled-K4 nulls (seeds 13501-13502).
"""
import sys, os, random
import numpy as np
sys.path.insert(0, "/tmp/kcf/tools/cycle127")
from plant import plain, K4

AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"

def keyed(w):
    s = ""
    for c in w + AZ:
        if c not in s:
            s += c
    return s

def enc_pair(p, k, PA, CA, f):
    a, s_ = PA.index(p), CA.index(k)
    r = (a + s_ if f == 0 else s_ - a if f == 1 else a - s_) % 26
    return CA[r]

def periodic_q(text, kw, PA, CA, f):
    return "".join(enc_pair(c, kw[i % len(kw)], PA, CA, f) for i, c in enumerate(text))

def move(t, s):
    o = [None] * 97
    for i, c in enumerate(t):
        o[int(s[i])] = c
    return "".join(o)

if __name__ == "__main__":
    P = plain()
    assert len(P) == 97 and P[21:34] == "EASTNORTHEAST" and P[63:74] == "BERLINCLOCK"
    B = np.fromfile("/home/box/kryptos_support_backup/perms97.bin", dtype=np.int16).reshape(-1, 97)
    # ctl1 QIII carved: alphabet PALIMPSEST, keyword ABSCISSA, Vigenere, perm 4242
    PA = keyed("PALIMPSEST")
    print("ctl1", periodic_q(move(P, B[4242]), "ABSCISSA", PA, PA, 0))
    # ctl2 QIII carved: alphabet KRYPTOS, keyword SHADOW, Beaufort, inverse of 99999
    PA = keyed("KRYPTOS")
    print("ctl2", periodic_q(move(P, np.argsort(B[99999])), "SHADOW", PA, PA, 1))
    # ctl3 QI carved: plaintext alphabet BERLIN, cipher A-Z, keyword CLOCK, Vigenere, perm 160000
    print("ctl3", periodic_q(move(P, B[160000]), "CLOCK", keyed("BERLIN"), AZ, 0))
    # ctl4 QIII model Q (key at plaintext, then transpose): alphabet NORTHEAST, keyword EAST, Vigenere, perm 12345
    PA = keyed("NORTHEAST")
    print("ctl4", move(periodic_q(P, "EAST", PA, PA, 0), B[12345]))
    for z in (1, 2):
        l = list(K4)
        random.Random(13500 + z).shuffle(l)
        print(f"null{z}", "".join(l))
