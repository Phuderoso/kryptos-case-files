"""Cycle 160 (IDEAS I-010) planted controls, written independently of q4v.c:
periodic Quagmire IV (PA = keyed(W1) != CA = keyed(W2)), textbook encryption
c = CA[PA^-1(p) + CA^-1(k)] (Vigenere) or c = CA[CA^-1(k) - PA^-1(p)] (Beaufort),
key at the plaintext index then transpose (model Q) or transpose first then key at the
carved index; plus shuffled-K4 nulls for the bank run (seeds 16001-16004).
Output: label CT  (one per line)."""
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
def quag(text, key, PA, CA, beau):
    out = []
    for i, c in enumerate(text):
        k = CA.index(key[i % len(key)])
        out.append(CA[(k - PA.index(c)) % 26] if beau else CA[(PA.index(c) + k) % 26])
    return "".join(out)
def move(t, s):
    o = [None] * 97
    for i, c in enumerate(t): o[int(s[i])] = c
    return "".join(o)
P = plain(); assert P[21:34] == "EASTNORTHEAST" and P[63:74] == "BERLINCLOCK"
B = np.fromfile("/home/box/kryptos_support_backup/perms97.bin", dtype=np.int16).reshape(-1, 97)
inv = lambda q: np.argsort(B[q])
# ctl1: carved index (transpose first), Vigenere, PA LANTERN, CA HARBOR, key QUARTZ (p 6), perm 4242 dir 0
print("ctl1", quag(move(P, B[4242]), "QUARTZ", keyed("LANTERN"), keyed("HARBOR"), 0))
# ctl2: model Q (key at plaintext index, then transpose), Beaufort, PA VELVET, CA MERIDIAN, key SHADOWS (p 7), inverse of perm 99999 (dir 1)
print("ctl2", move(quag(P, "SHADOWS", keyed("VELVET"), keyed("MERIDIAN"), 1), inv(99999)))
# ctl3: direct (identity), Vigenere, PA MERIDIAN, CA LANTERN, key LODESTAR (p 8)
print("ctl3", quag(P, "LODESTAR", keyed("MERIDIAN"), keyed("LANTERN"), 0))
# ctl4: carved index, Beaufort, PA HARBOR, CA VELVET, key THIRTEENLETTR (p 13), perm 120000 dir 1
print("ctl4", quag(move(P, inv(120000)), "THIRTEENLETTR", keyed("HARBOR"), keyed("VELVET"), 1))
# ctl5 (one error): as ctl3 but PA HARBOR, CA QUARTZ, key COMPASS (p 7), and the carved letter at position 27 (crib 6) altered
c = list(quag(P, "COMPASS", keyed("HARBOR"), keyed("QUARTZ"), 0)); c[27] = AZ[(AZ.index(c[27]) + 5) % 26]
print("ctl5", "".join(c))
for z in range(1, 5):
    l = list(K4); random.Random(16000 + z).shuffle(l); print(f"null{z}", "".join(l))
