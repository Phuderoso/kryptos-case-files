"""Cycle 133 controls: model-Q plaintext-autokey independently encrypted in Python
(Quagmire III, or stacked with a repeating keyword on AZ/KA), plus shuffled-K4
nulls (seeds 13301-13302)."""
import sys, os, random
import numpy as np
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(H, "..", "cycle127"))
from plant import plain, K4

AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"

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

def periodic(text, kw, alph, f):
    return "".join(enc_letter(alph, f, c, kw[i % len(kw)]) for i, c in enumerate(text))

def pt_autokey(text, primer, alph, f, key_src=None):
    src = key_src if key_src is not None else text
    L = len(primer)
    out = []
    for i, c in enumerate(text):
        k = primer[i] if i < L else src[i - L]
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
    print("ctl1", move(pt_autokey(P, "BERLIN", keyed("KRYPTOS"), 0), B[12345]))              # QIII vig, KA alphabet
    I1 = periodic(P, "SHADOW", AZ, 2)
    print("ctl2", move(pt_autokey(I1, "CLOCK", AZ, 0, key_src=I1), np.argsort(B[99999])))   # keyword then AK, inverse
    I1 = pt_autokey(P, "EAST", KA, 1)
    print("ctl3", move(periodic(I1, "MIRROR", KA, 0), B[160000]))                           # AK then keyword
    print("ctl4", move(pt_autokey(P, "LAYER", keyed("PALIMPSEST"), 1), B[4242]))            # QIII beau
    for z in (1, 2):
        l = list(K4)
        random.Random(13300 + z).shuffle(l)
        print(f"null{z}", "".join(l))
