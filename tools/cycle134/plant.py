"""Cycle 134 controls: model-Q phrase-primer autokey independently encrypted
in Python (Quagmire III PT/CT and keyword stacks), plus shuffled-K4 nulls
(seeds 13401-13402)."""
import sys, os, random
import numpy as np
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(H if os.path.isdir(H) else "/tmp/kcf/tools/cycle134", "..", "cycle127"))
# When run from /workspace/k134 the cycle127 plant is at /tmp/kcf/tools/cycle127
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
    # ctl1 Q-PT: alphabet PALIMPSEST, primer NORTHEAST+BERLIN (L=16), Beaufort, perm 4242
    print("ctl1", move(pt_autokey(P, "NORTHEASTBERLIN", keyed("PALIMPSEST"), 1), B[4242]))
    # ctl2 KA-PT: keyword SHADOW (AZ, variant) then PT-autokey primer CLOCK+KRYPTOS (L=12, AZ vig), inverse of 99999
    I1 = periodic(P, "SHADOW", AZ, 2)
    print("ctl2", move(pt_autokey(I1, "CLOCKKRYPTOS", AZ, 0, key_src=I1), np.argsort(B[99999])))
    # ctl3 AK-PT: PT-autokey primer EAST+BERLIN+CLOCK (L=15, KA Beau) then keyword LAYER (KA vig), perm 160000
    I1 = pt_autokey(P, "EASTBERLINCLOCK", KA, 1)
    print("ctl3", move(periodic(I1, "LAYER", KA, 0), B[160000]))
    # ctl4 Q-CT: alphabet KRYPTOS, primer ALEXANDERPLATZ+NORTHEAST (L=23), Vigenere, perm 12345
    print("ctl4", move(ct_autokey(P, "ALEXANDERPLATZNORTHEAST", keyed("KRYPTOS"), 0), B[12345]))
    for z in (1, 2):
        l = list(K4)
        random.Random(13400 + z).shuffle(l)
        print(f"null{z}", "".join(l))
