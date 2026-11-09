"""Cycle 166 (IDEAS I-070) planted controls, written independently of split3.c: textbook Quagmire III encryption
with a period-7 key chosen per segment, key letter by index mod 7 (phase from position 0), segments
[0,b1) | [b1,b2) | [b2,97).  Model T: three independent keys.  Model R: key 1 returns after b2 (same key, same form).
Vigenere c = A[A^-1(p)+A^-1(k)], Beaufort c = A[A^-1(k)-A^-1(p)], chosen per segment (R: segment 3 = segment 1).
Layers: direct; model Q (key at plaintext index, then transpose by bank perm q, dir d); carved (transpose first, key at
carved index).  Error plants: one carved letter under a crib altered (one-error mode must recover with that crib dropped).
Output: label CT model layer q dir alpha b1 b2 forms keys  (one per line).  Seeds 16610+."""
import sys, random, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "cycle127"))
from plant import plain
AL = np.fromfile("/home/box/kryptos_support_backup/alpha.bin", dtype=np.uint8).reshape(-1, 26)
B = np.fromfile("/home/box/kryptos_support_backup/perms97.bin", dtype=np.int16).reshape(-1, 97)
def alpha(i): return "".join(chr(65 + x) for x in AL[i])
def perm(q, d): return [int(x) for x in B[q]] if d == 0 else [int(x) for x in np.argsort(B[q])]
def move(t, s):
    o = [None] * 97
    for i, c in enumerate(t): o[s[i]] = c
    return "".join(o)
def enc(t, A, keys, forms, b1, b2):
    out = []
    for i, c in enumerate(t):
        g = 0 if i < b1 else (1 if i < b2 else 2)
        kk = A.index(keys[g][i % 7])
        out.append(A[(kk - A.index(c)) % 26] if forms[g] else A[(A.index(c) + kk) % 26])
    return "".join(out)
P = plain(); assert P[21:34] == "EASTNORTHEAST" and P[63:74] == "BERLINCLOCK"
CRIB = list(range(21, 34)) + list(range(63, 74))
if __name__ == "__main__":
    rng = random.Random(16610)
    rk = lambda: "".join(rng.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(7))
    STRIDE = 200  # all-alphabet bank sample: q % 200 == 0
    for model in "TR":
        for j in range(10):
            layer = ["direct", "Q", "carved"][j % 3]
            a = rng.choice([0, 1]) if j % 2 == 0 else rng.randrange(2, len(AL))
            q = rng.randrange(0, 165065 // STRIDE) * STRIDE if layer != "direct" else -1
            d = rng.randrange(2) if layer != "direct" else 0
            # boundaries: b1 anywhere 1..80, b2 > b1, at least one crib in the middle, some inside cribs
            while True:
                b1 = rng.randrange(15, 70); b2 = rng.randrange(b1 + 1, 90)
                if any(b1 <= x < b2 for x in CRIB): break
            k1, k2, k3 = rk(), rk(), rk()
            f = [rng.randrange(2) for _ in range(3)]
            if model == "R": k3, f[2] = k1, f[0]
            A = alpha(a); keys = (k1, k2, k3)
            if layer == "direct": ct = enc(P, A, keys, f, b1, b2)
            elif layer == "Q": ct = move(enc(P, A, keys, f, b1, b2), perm(q, d))
            else: ct = enc(move(P, perm(q, d)), A, keys, f, b1, b2)
            print(f"p{model}{j} {ct} {model} {layer} {q} {d} {a} {b1} {b2} {''.join(map(str,f))} {k1},{k2},{k3}")
    # one-error plants: direct, alter the carved letter at a crib position
    for j, (model, a, pos) in enumerate([("R", 1, 28), ("R", 20000, 66), ("T", 0, 70), ("T", 1, 24)]):
        b1, b2 = (30, 60) if model == "R" else (27, 66)
        k1, k2, k3 = rk(), rk(), rk(); f = [rng.randrange(2) for _ in range(3)]
        if model == "R": k3, f[2] = k1, f[0]
        c = list(enc(P, alpha(a), (k1, k2, k3), f, b1, b2)); c[pos] = "A" if c[pos] != "A" else "B"
        print(f"e{model}{j} {''.join(c)} {model} direct -1 0 {a} {b1} {b2} {''.join(map(str,f))} {k1},{k2},{k3} err={pos}")
