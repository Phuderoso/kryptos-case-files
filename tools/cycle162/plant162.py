"""Cycle 162 (IDEAS I-013) planted controls, written independently of split7.c:
textbook split-key Quagmire III encryption.  Key 1 (period 7) on index positions < b, key 2 (period 7) on
positions >= b, key letter chosen by index mod 7 (phase from position 0); Vigenere c = A[A^-1(p) + A^-1(k)] or
Beaufort c = A[A^-1(k) - A^-1(p)], chosen per segment.  Layers: direct; model Q (key at the plaintext index, then
transpose); carved index (transpose first, key at the carved index).  Plus shuffled-K4 nulls (seeds 16201-16204).
Output: label CT (one per line)."""
import sys, random
import numpy as np
sys.path.insert(0, "/tmp/kcf/tools/cycle127")
from plant import plain, K4
AL = np.fromfile("/home/box/kryptos_support_backup/alpha.bin", dtype=np.uint8).reshape(-1, 26)
def alpha(i): return "".join(chr(65 + x) for x in AL[i])
B = np.fromfile("/home/box/kryptos_support_backup/perms97.bin", dtype=np.int16).reshape(-1, 97)
def perm(q, d): return list(B[q]) if d == 0 else list(np.argsort(B[q]))
def move(t, s):
    o = [None] * 97
    for i, c in enumerate(t): o[int(s[i])] = c
    return "".join(o)
def enc(t, A1, k1, beau1, A2, k2, beau2, b):
    out = []
    for i, c in enumerate(t):
        A, k, be = (A1, k1, beau1) if i < b else (A2, k2, beau2)
        kk = A.index(k[i % 7])
        out.append(A[(kk - A.index(c)) % 26] if be else A[(A.index(c) + kk) % 26])
    return "".join(out)
P = plain(); assert P[21:34] == "EASTNORTHEAST" and P[63:74] == "BERLINCLOCK"
if __name__ == "__main__":
    A5, A20, KA, AZ = alpha(5000), alpha(20000), alpha(1), alpha(0)
    # ctl1: carved index, perm 4242 dir 0, alphabet 5000, Vig PALIMPS | Beau SHADOWS, b 50
    print("ctl1", enc(move(P, perm(4242, 0)), A5, "PALIMPS", 0, A5, "SHADOWS", 1, 50))
    # ctl2: model Q, perm 99999 dir 1, KRYPTOS, Beau IQLUSIO | Vig VIRTUAL, b 66 (inside BERLINCLOCK)
    print("ctl2", move(enc(P, KA, "IQLUSIO", 1, KA, "VIRTUAL", 0, 66), perm(99999, 1)))
    # ctl3: direct, alphabet 20000, Vig DESPARA | Vig LAYERTW, b 28 (inside EASTNORTHEAST)
    print("ctl3", enc(P, A20, "DESPARA", 0, A20, "LAYERTW", 0, 28))
    # ctl4: AZ/KA cross, carved index, perm 120000 dir 0, AZ Vig BERLINW | KA Beau CLOCKSX, b 40
    print("ctl4", enc(move(P, perm(120000, 0)), AZ, "BERLINW", 0, KA, "CLOCKSX", 1, 40))
    # ctl5: one error, direct, KRYPTOS, Vig SANBORN | Beau WEBSTER, b 45, carved letter 28 altered
    c = list(enc(P, KA, "SANBORN", 0, KA, "WEBSTER", 1, 45)); c[28] = "A" if c[28] != "A" else "B"
    print("ctl5", "".join(c))
    for s in range(1, 5):
        l = list(K4); random.Random(16200 + s).shuffle(l); print(f"null{s}", "".join(l))
