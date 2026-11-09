"""Cycle 189 planted controls (independent string-level encryptor; shares no code with cmp189.c).
Each plant applies the layers literally, letter by letter, as Sanborn would on paper: layer 1 key a (period m), layer 2 key b (period n),
each layer a Vig (x+k), Beau (k-x) or variant (x-k) step on the same tableau alphabet T (index space of T), key at the plaintext index (P)
or at the carved index (C) behind perm q of the given perms file (plaintext i carved at S[i] = P[q][i]).
usage: plant189.py perms.bin alphas.txt outfile -> lines: name q perms model ct"""
import sys, random
import numpy as np
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
PTX = "THEIRONDOORFACEDDUEXX" + "EASTNORTHEAST" + "OFTHEFOUNTAINWHERETHEOLDWORLD" + "BERLINCLOCK" + "STRUCKTHEHOURATMIDNIGHT"
assert len(PTX) == 97 and PTX[21:34] == "EASTNORTHEAST" and PTX[63:74] == "BERLINCLOCK"
AL = dict(reversed(l.split()) for l in open(sys.argv[2]))
R = random.Random(18900)
def step(x, k, form): return (x + k) % 26 if form == "vig" else (k - x) % 26 if form == "beau" else (x - k) % 26
def word(w): return [AZ.index(ch) for ch in w]
def enc(perms, q, alab, model, layers):          # layers = [(key list, form), ...]
    T = AL[alab]; S = list(range(97)) if q < 0 else [int(v) for v in np.fromfile(perms, dtype=np.int16).reshape(-1, 97)[q]]
    C = ["?"] * 97
    for i in range(97):
        j = S[i]; x = T.index(PTX[i]); pos = i if model == "P" else j
        for key, form in layers: x = step(x, key[pos % len(key)], form)
        C[j] = T[x]
    assert "?" not in C; return "".join(C)
out = open(sys.argv[3], "w"); A = sys.argv[1]
def rk(n): return [R.randrange(26) for _ in range(n)]
plants = [
 ("P1", A, 12345, "AZ", "P", [(rk(7), "vig"), (rk(11), "vig")]),
 ("P2", A, 100000, "KA", "C", [(rk(5), "beau"), (rk(13), "beau")]),
 ("P3", A, 512 * 37, "PALIMPSEST/Z", "C", [(rk(8), "vig"), (rk(12), "variant")]),
 ("P4", A, 165781, "KA", "P", [(rk(6), "vig"), (rk(19), "beau")]),
 ("P5", "-", -1, "AZ", "P", [(word("PALIMPSEST"), "vig"), (word("ABSCISSA"), "vig")]),
 ("P6", "-", -1, "KA", "C", [(word("KRYPTOS"), "beau"), (word("BERLINCLOCK"), "vig")]),
 ("P7", A, 512 * 101, "AZ", "C", [(rk(3), "variant"), (rk(25), "vig")]),
 ("N1", A, 12345, "AZ", "P", [(rk(5), "vig"), (rk(7), "vig"), (rk(11), "vig")]),
 ("N2", A, 100000, "KA", "C", [(rk(97), "beau")]),
]
CTS = {}
for name, pf, q, alab, model, layers in plants:
    ct = enc(pf, q, alab, model, layers); CTS[name] = ct
    out.write(f"{name} {q} {alab} {model} {'/'.join(str(len(k)) for k, _ in layers)} {ct}\n")
# N3 = P1 with one carved crib letter changed (slot 5, +7 in the AZ index)
ct = list(CTS["P1"]); j = int(np.fromfile(A, dtype=np.int16).reshape(-1, 97)[12345][26])
ct[j] = AZ[(AZ.index(ct[j]) + 7) % 26]; out.write(f"N3 12345 AZ P 7/11 {''.join(ct)}\n"); out.close()
