"""Cycle 193 planted controls (independent string-level encryptor; shares no code with cmp193.c). SANDWICH: pass 1 on tableau T1 with key a,
then the transposition (plaintext i carved at S[i]), then pass 2 on tableau T2 with key b; each pass a Vig (x+k), Beau (k-x) or variant (x-k)
step in that tableau's index space, the letter handed over as a LETTER. Model 1: a at the plaintext index i, b at the carved index S[i];
model 2: a at the carved index, b at the plaintext index. Extra plants: case-178 style compound keys (both keys on one side) and a
three-pass sandwich. Keyword keys use the key letter's index in that tableau.
usage: plant193.py ctl191.bin outfile   (ctl191.bin row 0 = identity, rows 1-5 = all.bin rows 12345, 100000, 18944, 165781, 51712)"""
import sys, random
import numpy as np
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"
TAB = {"AZ": AZ, "KA": KA}
PTX = "THEIRONDOORFACEDDUEXX" + "EASTNORTHEAST" + "OFTHEFOUNTAINWHERETHEOLDWORLD" + "BERLINCLOCK" + "STRUCKTHEHOURATMIDNIGHT"
assert len(PTX) == 97 and PTX[21:34] == "EASTNORTHEAST" and PTX[63:74] == "BERLINCLOCK"
R = random.Random(19300)
PERM = np.fromfile(sys.argv[1], dtype=np.int16).reshape(-1, 97)
def step(x, k, form): return (x + k) % 26 if form == "vig" else (k - x) % 26 if form == "beau" else (x - k) % 26
def enc(row, passes):            # passes = [(tab, key list, form, index 'p' plaintext | 'c' carved), ...] applied in order
    S = [int(v) for v in PERM[row]]; C = ["?"] * 97
    for i in range(97):
        j = S[i]; ch = PTX[i]
        for tab, key, form, ix in passes:
            T = TAB[tab]; pos = i if ix == "p" else j; ch = T[step(T.index(ch), key[pos % len(key)], form)]
        C[j] = ch
    assert "?" not in C; return "".join(C)
def rk(n): return [R.randrange(26) for _ in range(n)]
def kw(w, tab): return [TAB[tab].index(c) for c in w]
plants = [  # name, row, model, passes, expected cell (tabpair, form, m, n)
 ("P1", 1, "1", [("AZ", rk(7), "vig", "p"), ("KA", rk(11), "vig", "c")], "AZ>KA VV 7 11"),
 ("P2", 2, "1", [("KA", rk(5), "beau", "p"), ("AZ", rk(13), "vig", "c")], "KA>AZ BV 5 13"),
 ("P3", 3, "2", [("AZ", rk(8), "variant", "c"), ("KA", rk(12), "beau", "p")], "AZ>KA VB 8 12"),
 ("P4", 4, "1", [("KA", rk(6), "vig", "p"), ("AZ", rk(19), "beau", "c")], "KA>AZ VB 6 19"),
 ("P5", 1, "1", [("AZ", kw("PALIMPSEST", "AZ"), "vig", "p"), ("KA", kw("ABSCISSA", "KA"), "vig", "c")], "AZ>KA VV 10 8"),
 ("P6", 5, "1", [("AZ", rk(3), "variant", "p"), ("AZ", rk(25), "vig", "c")], "AZ>AZ VV 3 25"),
 ("P7", 1, "1", [("KA", rk(4), "beau", "p"), ("KA", rk(9), "beau", "c")], "KA>KA BB 4 9"),
 ("P8", 2, "1", [("AZ", rk(7), "vig", "p"), ("KA", rk(7), "beau", "c")], "AZ>KA VB 7 7"),
 ("P9", 3, "2", [("KA", rk(6), "beau", "c"), ("AZ", rk(10), "beau", "p")], "KA>AZ BB 6 10"),
 ("N1", 1, "1", [("AZ", rk(5), "vig", "p"), ("KA", rk(7), "vig", "c"), ("AZ", rk(11), "vig", "c")], "three passes"),
 ("N2", 2, "1", [("KA", rk(97), "beau", "p")], "random key"),
 ("N4", 1, "1", [("AZ", rk(7), "vig", "p"), ("KA", rk(11), "vig", "p")], "case-178 compound key, both keys on the plaintext index"),
]
out = open(sys.argv[2], "w"); CT = {}
for name, row, model, passes, exp in plants:
    ct = enc(row, passes); CT[name] = ct
    out.write(f"{name} {row} {model} {exp.replace(' ', '_')} {ct}\n")
# N3 = P1 with one carved crib letter changed: slot 3 (plaintext 24), +7 in the KA index (the carved letter's tableau).
# Rehearsal fix (disclosed, I-195): the first choice, slot 2, is a pendant edge of P1's 7 x 11 sandwich graph at row 1 (not in the 2-core),
# so no crib test can see a wrong letter there and P1's cell still fitted; slot 3 is the first 2-core slot >= 2.
ct = list(CT["P1"]); j = int(PERM[1][24]); ct[j] = KA[(KA.index(ct[j]) + 7) % 26]
out.write(f"N3 1 1 AZ>KA_VV_7_11_one_wrong_letter_slot3 {''.join(ct)}\n"); out.close()
