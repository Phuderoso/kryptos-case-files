"""Cycle 167 (IDEAS I-082) planted controls, written independently of shift3.c: textbook Quagmire III encryption with ONE
period-7 key shifted by a constant per segment (k | k+d2 | k+d3, shift in keyed-alphabet index space = moving to another
row of the keyed tableau), key letter by index mod 7 (phase from 0), segments [0,b1) | [b1,b2) | [b2,97), every segment
holding >= 1 crib, d2, d3 non-zero and d2 != d3.  Vigenere c = A[A^-1(p)+A^-1(k)+d], Beaufort c = A[A^-1(k)+d-A^-1(p)],
form per segment.  Layers: direct; model Q (key at plaintext index, then transpose by bank perm q, dir d); carved
(transpose first, key at carved index).  Error plants: one carved letter under a crib altered.  Decoys: three
INDEPENDENT keys (model T of cycle 166), which the shift model must reject.  Seeds 16710+.
Output: label CT kind layer q dir alpha b1 b2 forms key d2 d3"""
import sys, random, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "cycle166"))
from plant166 import P, CRIB, AL, alpha, perm, move
def enc(t, A, key, forms, b1, b2, sh, keys3=None):
    out = []
    for i, c in enumerate(t):
        g = 0 if i < b1 else (1 if i < b2 else 2)
        kk = (A.index((keys3[g] if keys3 else key)[i % 7]) + (0 if keys3 else sh[g])) % 26
        out.append(A[(kk - A.index(c)) % 26] if forms[g] else A[(A.index(c) + kk) % 26])
    return "".join(out)
if __name__ == "__main__":
    rng = random.Random(16710)
    rk = lambda: "".join(rng.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(7))
    STRIDE = 4000
    def bounds():
        while True:
            b1 = rng.randrange(14, 80); b2 = rng.randrange(b1 + 1, 96)
            segs = [[x for x in CRIB if x < b1], [x for x in CRIB if b1 <= x < b2], [x for x in CRIB if x >= b2]]
            if all(segs): return b1, b2
    for j in range(18):
        layer = ["direct", "Q", "carved"][j % 3]
        a = [0, 1, None][j % 3]; a = rng.randrange(2, len(AL)) if a is None else a
        q = rng.randrange(0, 165065 // STRIDE) * STRIDE if layer != "direct" else -1
        d = rng.randrange(2) if layer != "direct" else 0
        b1, b2 = bounds(); k = rk()
        d2 = rng.randrange(1, 26)
        while True:
            d3 = rng.randrange(1, 26)
            if d3 != d2: break
        f = [rng.randrange(2) for _ in range(3)] if j % 2 else [j % 4 // 2] * 3
        A = alpha(a); sh = (0, d2, d3)
        if layer == "direct": ct = enc(P, A, k, f, b1, b2, sh)
        elif layer == "Q": ct = move(enc(P, A, k, f, b1, b2, sh), perm(q, d))
        else: ct = enc(move(P, perm(q, d)), A, k, f, b1, b2, sh)
        print(f"p{j} {ct} S {layer} {q} {d} {a} {b1} {b2} {''.join(map(str,f))} {k} {d2} {d3}")
    for j, (a, pos) in enumerate([(1, 28), (0, 66), (30000, 70), (1, 24)]):
        b1, b2 = (30, 66); k = rk(); f = [rng.randrange(2)] * 3; sh = (0, rng.randrange(1, 13), rng.randrange(13, 26))
        c = list(enc(P, alpha(a), k, f, b1, b2, sh)); c[pos] = "A" if c[pos] != "A" else "B"
        print(f"e{j} {''.join(c)} S direct -1 0 {a} {b1} {b2} {''.join(map(str,f))} {k} {sh[1]} {sh[2]} err={pos}")
    for j in range(4):
        a = j % 2; b1, b2 = (28, 68); f = [j // 2] * 3; ks = (rk(), rk(), rk())
        print(f"x{j} {enc(P, alpha(a), None, f, b1, b2, None, ks)} T direct -1 0 {a} {b1} {b2} {''.join(map(str,f))} {','.join(ks)} - -")
