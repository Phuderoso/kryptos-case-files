"""Cycle 136 controls: transposition-first (and one model-Q) Quagmire III autokey
independently encrypted in Python, plus shuffled-K4 nulls (seeds 13601-13602).
"""
import sys, os, random
import numpy as np
sys.path.insert(0, "/tmp/kcf/tools/cycle127")
from plant import plain, K4

AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def keyed(w):
    s = ""
    for c in w + AZ:
        if c not in s:
            s += c
    return s

def enc_letter(alph, f, p, k):
    a, s_ = alph.index(p), alph.index(k)
    r = (a + s_ if f == 0 else s_ - a if f == 1 else a - s_) % 26
    return alph[r]

def pt_autokey(text, primer, alph, f):
    L = len(primer)
    out = []
    for i, c in enumerate(text):
        k = primer[i] if i < L else text[i - L]
        out.append(enc_letter(alph, f, c, k))
    return "".join(out)

def ct_autokey(text, primer, alph, f):
    L = len(primer)
    out = []
    for i, c in enumerate(text):
        k = primer[i] if i < L else out[i - L]
        out.append(enc_letter(alph, f, c, k))
    return "".join(out)

def move(t, s):
    o = [None] * 97
    for i, c in enumerate(t):
        o[int(s[i])] = c
    return "".join(o)

if __name__ == "__main__":
    P = plain()
    assert len(P) == 97 and P[21:34] == "EASTNORTHEAST" and P[63:74] == "BERLINCLOCK"
    B = np.fromfile("/home/box/kryptos_support_backup/perms97.bin", dtype=np.int16).reshape(-1, 97)
    # ctl1 QIII carved PT-autokey: alphabet PALIMPSEST, primer ABSCISSA, Vigenere, perm 4242
    print("ctl1", pt_autokey(move(P, B[4242]), "ABSCISSA", keyed("PALIMPSEST"), 0))
    # ctl2 QIII carved CT-autokey: alphabet KRYPTOS, primer SHADOW, Beaufort, inverse of 99999
    print("ctl2", ct_autokey(move(P, np.argsort(B[99999])), "SHADOW", keyed("KRYPTOS"), 1))
    # ctl3 QIII carved PT-autokey: alphabet BERLIN, primer CLOCK, variant Beaufort, perm 160000
    print("ctl3", pt_autokey(move(P, B[160000]), "CLOCK", keyed("BERLIN"), 2))
    # ctl4 QIII model Q PT-autokey (key at plaintext, then transpose): alphabet NORTHEAST, primer EAST, Vigenere, perm 12345
    print("ctl4", move(pt_autokey(P, "EAST", keyed("NORTHEAST"), 0), B[12345]))
    for z in (1, 2):
        l = list(K4)
        random.Random(13600 + z).shuffle(l)
        print(f"null{z}", "".join(l))
