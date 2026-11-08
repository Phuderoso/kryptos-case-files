"""Cycle 137 controls: CT-fed autokey with a keyed cipher alphabet and a RANDOM
(arbitrary) plaintext alphabet, independently encrypted in Python; plus
shuffled-K4 nulls (seeds 13701-13702)."""
import sys, random
import numpy as np
sys.path.insert(0, "/tmp/kcf/tools/cycle127")
from plant import plain, K4
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
def keyed(w):
    s = ""
    for c in w + AZ:
        if c not in s: s += c
    return s
KA = keyed("KRYPTOS")
def ct_autokey(text, primer, yalph, zalph, xalph, form):
    # form 0 Vigenere y=x+z, 1 Beaufort y=z-x, 2 variant y=x-z
    L = len(primer); out = []
    for i, p in enumerate(text):
        k = primer[i] if i < L else out[i - L]
        xv, zv = xalph.index(p), zalph.index(k)
        yv = (xv + zv) if form == 0 else (zv - xv) if form == 1 else (xv - zv)
        out.append(yalph[yv % 26])
    return "".join(out)
def move(t, s):
    o = [None] * 97
    for i, c in enumerate(t): o[int(s[i])] = c
    return "".join(o)
if __name__ == "__main__":
    P = plain(); assert P[21:34] == "EASTNORTHEAST" and P[63:74] == "BERLINCLOCK"
    B = np.fromfile("/home/box/kryptos_support_backup/perms97.bin", dtype=np.int16).reshape(-1, 97)
    R = random.Random(13700)
    def rx():
        l = list(AZ); R.shuffle(l); return "".join(l)
    # ctl1 carved, y=z=PALIMPSEST, random x, Vigenere, primer SHADOWS, perm 4242
    print("ctl1", ct_autokey(move(P, B[4242]), "SHADOWS", keyed("PALIMPSEST"), keyed("PALIMPSEST"), rx(), 0))
    # ctl2 carved, y=KRYPTOS z=A-Z, random x, Beaufort, primer L13, inverse of 99999
    print("ctl2", ct_autokey(move(P, np.argsort(B[99999])), "QWERTYUIOPASD", KA, AZ, rx(), 1))
    # ctl3 model Q, y=BERLIN z=KRYPTOS, random x, variant, primer LUCID, perm 160000
    print("ctl3", move(ct_autokey(P, "LUCID", keyed("BERLIN"), KA, rx(), 2), B[160000]))
    # ctl4 carved, y=A-Z z=CLOCK, random x, Vigenere, primer L16, perm 12345
    print("ctl4", ct_autokey(move(P, B[12345]), "ABCDEFGHIJKLMNOP", AZ, keyed("CLOCK"), rx(), 0))
    for zz in (1, 2):
        l = list(K4); random.Random(13700 + zz).shuffle(l); print(f"null{zz}", "".join(l))
