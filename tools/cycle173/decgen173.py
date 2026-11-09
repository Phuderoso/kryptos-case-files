"""Cycle 173 (IDEAS I-105): K3-law decimation family for a true ciphertext of n = 96, 97, 98 letters.
perm[j] = (a + s*j) mod M, gcd(s,M)=1, every start a, slots >= n empty and skipped (cycle 59 generator, case 57),
both directions (perm and inverse), distinct perms only. M = n..max(112, n+15) (n=97: 97..112 exactly as cycle 59).
out[k] = index in the true ciphertext C' paired with plaintext position k.  Writes dec{n}.bin (int16 x n) + dec{n}.txt."""
import struct, math, sys
def build(n):
    T = {}
    for M in range(n, max(112, n + 15) + 1):
        for s in range(1, M):
            if math.gcd(s, M) != 1: continue
            for a in range(M):
                out = [v for v in ((a + s * j) % M for j in range(M)) if v < n]
                inv = [0] * n
                for k, v in enumerate(out): inv[v] = k
                T.setdefault(tuple(out), f"dec n{n} M{M} s{s} a{a}/dec")
                T.setdefault(tuple(inv), f"dec n{n} M{M} s{s} a{a}/enc")
    return T
if __name__ == "__main__":
    for n in map(int, sys.argv[1:]):
        T = build(n)
        with open(f"dec{n}.bin", "wb") as f:
            for p in T: f.write(struct.pack(f"<{n}h", *p))
        open(f"dec{n}.txt", "w").write("\n".join(T.values()) + "\n")
        print("n", n, "distinct perms", len(T))
