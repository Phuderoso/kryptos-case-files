"""Cycle 191 planted controls (independent string-level encryptor; shares no code with cmp191.c).
Each plant applies the passes literally, letter by letter: pass j on tableau T_j with key k_j (period len(k_j)), as a Vig (x+k),
Beau (k-x) or variant (x-k) step in T_j's index space, the letter handed from one tableau to the next as a LETTER. Key at the plaintext
index (P) or at the carved index (C) behind route row (plaintext i carved at S[i]). Keyword keys use the key letter's index in that tableau.
usage: plant191.py ctl191.bin outfile   (ctl191.bin row 0 = identity, rows 1-5 = all.bin rows 12345, 100000, 18944, 165781, 51712)"""
import sys, random
import numpy as np
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"
TAB = {"AZ": AZ, "KA": KA}
PTX = "THEIRONDOORFACEDDUEXX" + "EASTNORTHEAST" + "OFTHEFOUNTAINWHERETHEOLDWORLD" + "BERLINCLOCK" + "STRUCKTHEHOURATMIDNIGHT"
assert len(PTX) == 97 and PTX[21:34] == "EASTNORTHEAST" and PTX[63:74] == "BERLINCLOCK"
R = random.Random(19100)
PERM = np.fromfile(sys.argv[1], dtype=np.int16).reshape(-1, 97)
def step(x, k, form): return (x + k) % 26 if form == "vig" else (k - x) % 26 if form == "beau" else (x - k) % 26
def enc(row, model, passes):            # passes = [(tab, key list, form), ...]
    S = [int(v) for v in PERM[row]]; C = ["?"] * 97
    for i in range(97):
        j = S[i]; ch = PTX[i]; pos = i if model == "P" else j
        for tab, key, form in passes:
            T = TAB[tab]; ch = T[step(T.index(ch), key[pos % len(key)], form)]
        C[j] = ch
    assert "?" not in C; return "".join(C)
def rk(n): return [R.randrange(26) for _ in range(n)]
def kw(w, tab): return [TAB[tab].index(c) for c in w]
plants = [  # name, row, model, passes, expected cell (tabpair, form, m, n)
 ("P1", 1, "P", [("AZ", rk(7), "vig"), ("KA", rk(11), "vig")], "AZ>KA VV 7 11"),
 ("P2", 2, "C", [("KA", rk(5), "beau"), ("AZ", rk(13), "vig")], "KA>AZ BV 5 13"),
 ("P3", 3, "C", [("AZ", rk(8), "variant"), ("KA", rk(12), "beau")], "AZ>KA VB 8 12"),
 ("P4", 4, "P", [("KA", rk(6), "vig"), ("AZ", rk(19), "beau")], "KA>AZ VB 6 19"),
 ("P5", 0, "P", [("AZ", kw("PALIMPSEST", "AZ"), "vig"), ("KA", kw("ABSCISSA", "KA"), "vig")], "AZ>KA VV 10 8"),
 ("P6", 0, "C", [("KA", kw("KRYPTOS", "KA"), "beau"), ("AZ", kw("BERLINCLOCK", "AZ"), "vig")], "KA>AZ BV 7 11"),
 ("P7", 5, "C", [("AZ", rk(3), "variant"), ("AZ", rk(25), "vig")], "AZ>AZ VV 3 25"),
 ("P8", 1, "P", [("KA", rk(4), "beau"), ("KA", rk(9), "beau")], "KA>KA BB 4 9"),
 ("N1", 1, "P", [("AZ", rk(5), "vig"), ("KA", rk(7), "vig"), ("AZ", rk(11), "vig")], "three passes"),
 ("N2", 2, "C", [("KA", rk(97), "beau")], "random key"),
]
out = open(sys.argv[2], "w"); CT = {}
for name, row, model, passes, exp in plants:
    ct = enc(row, model, passes); CT[name] = ct
    out.write(f"{name} {row} {model} {exp.replace(' ', '_')} {ct}\n")
# N3 = P1 with one carved crib letter changed: slot 2 (plaintext 23), +7 in the KA index (the carved letter's tableau)
ct = list(CT["P1"]); j = int(PERM[1][23]); ct[j] = KA[(KA.index(ct[j]) + 7) % 26]
out.write(f"N3 1 P AZ>KA_VV_7_11_one_wrong_letter_slot2 {''.join(ct)}\n"); out.close()
