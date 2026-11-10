"""Cycle 195 planted controls (independent string-level encryptor, adapted from plant193.py; shares no code with cmp193.c). SANDWICH with a
KEYWORD COLUMNAR between the passes: pass 1 on tableau T1 with key a, then the transposition (plaintext i carved at S[i]), then pass 2 on T2
with key b; model 1: a at the plaintext index, b at the carved index; model 2 reverse. Rows of ctl195.bin (support/ctl195_index.txt):
 0 KRYPTOS/enc, 1 PALIMPSEST/enc, 2 LODESTONE/inv, 3 ALEXANDERPLATZ/enc (width 14), 4 KRYPTOS+PALIMPSEST/enc (double), 5 all.bin route 12345,
 6 BERLIN/inv. The keyword columnar itself is ALSO re-derived here from the keyword (write by rows, read columns in alphabetical order, ties
 left to right) and asserted equal to the bank row, so the bank generator is checked independently.
usage: plant195.py ctl195.bin outfile"""
import sys, random
import numpy as np
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"
TAB = {"AZ": AZ, "KA": KA}
PTX = "THEIRONDOORFACEDDUEXX" + "EASTNORTHEAST" + "OFTHEFOUNTAINWHERETHEOLDWORLD" + "BERLINCLOCK" + "STRUCKTHEHOURATMIDNIGHT"
assert len(PTX) == 97 and PTX[21:34] == "EASTNORTHEAST" and PTX[63:74] == "BERLINCLOCK"
R = random.Random(19500)
PERM = np.fromfile(sys.argv[1], dtype=np.int16).reshape(-1, 97)
def colperm(word):               # literal keyed columnar: carved position of plaintext letter j
    w = len(word); order = sorted(range(w), key=lambda c: (word[c], c)); pos = {}; k = 0
    for c in order:
        for j in range(c, 97, w): pos[j] = k; k += 1
    return [pos[j] for j in range(97)]
def inv(P): Q = [0] * 97; [Q.__setitem__(j, i) for i, j in enumerate(P)]; return Q
chk = {0: colperm("KRYPTOS"), 1: colperm("PALIMPSEST"), 2: inv(colperm("LODESTONE")), 3: colperm("ALEXANDERPLATZ"),
       4: [colperm("PALIMPSEST")[colperm("KRYPTOS")[i]] for i in range(97)], 6: inv(colperm("BERLIN"))}
for r, P in chk.items(): assert [int(v) for v in PERM[r]] == P, f"bank row {r} differs from the literal columnar"
def step(x, k, form): return (x + k) % 26 if form == "vig" else (k - x) % 26 if form == "beau" else (x - k) % 26
def enc(row, passes):
    S = [int(v) for v in PERM[row]]; C = ["?"] * 97
    for i in range(97):
        j = S[i]; ch = PTX[i]
        for tab, key, form, ix in passes:
            T = TAB[tab]; pos = i if ix == "p" else j; ch = T[step(T.index(ch), key[pos % len(key)], form)]
        C[j] = ch
    assert "?" not in C; return "".join(C)
def rk(n): return [R.randrange(26) for _ in range(n)]
def kw(w, tab): return [TAB[tab].index(c) for c in w]
plants = [
 ("P1", 0, "1", [("AZ", rk(7), "vig", "p"), ("KA", rk(11), "vig", "c")], "AZ>KA VV 7 11"),
 ("P2", 1, "1", [("KA", rk(5), "beau", "p"), ("AZ", rk(13), "vig", "c")], "KA>AZ BV 5 13"),
 ("P3", 2, "2", [("AZ", rk(8), "variant", "c"), ("KA", rk(12), "beau", "p")], "AZ>KA VB 8 12"),
 ("P4", 3, "1", [("KA", rk(6), "vig", "p"), ("AZ", rk(19), "beau", "c")], "KA>AZ VB 6 19"),
 ("P5", 0, "1", [("AZ", kw("PALIMPSEST", "AZ"), "vig", "p"), ("KA", kw("ABSCISSA", "KA"), "vig", "c")], "AZ>KA VV 10 8"),
 ("P6", 4, "1", [("AZ", rk(3), "variant", "p"), ("AZ", rk(25), "vig", "c")], "AZ>AZ VV 3 25"),
 ("P7", 6, "1", [("KA", rk(4), "beau", "p"), ("KA", rk(9), "beau", "c")], "KA>KA BB 4 9"),
 ("P8", 1, "1", [("AZ", rk(7), "vig", "p"), ("KA", rk(7), "beau", "c")], "AZ>KA VB 7 7"),
 ("P9", 2, "2", [("KA", rk(6), "beau", "c"), ("AZ", rk(10), "beau", "p")], "KA>AZ BB 6 10"),
 ("N1", 0, "1", [("AZ", rk(5), "vig", "p"), ("KA", rk(7), "vig", "c"), ("AZ", rk(11), "vig", "c")], "three passes"),
 ("N2", 1, "1", [("KA", rk(97), "beau", "p")], "random key"),
 ("N4", 0, "1", [("AZ", rk(7), "vig", "p"), ("KA", rk(11), "vig", "p")], "case-178 compound key, both keys on the plaintext index"),
 ("N5", 5, "1", [("AZ", rk(7), "vig", "p"), ("KA", rk(11), "vig", "c")], "K3-route sandwich (all.bin 12345): must not fit at any columnar row"),
]
out = open(sys.argv[2], "w"); CT = {}
for name, row, model, passes, exp in plants:
    ct = enc(row, passes); CT[name] = ct
    out.write(f"{name} {row} {model} {exp.replace(' ', '_')} {ct}\n")
SLOT = int(sys.argv[3]) if len(sys.argv) > 3 else 3
ct = list(CT["P1"]); pt = (21 + SLOT) if SLOT < 13 else (63 + SLOT - 13); j = int(PERM[0][pt]); ct[j] = KA[(KA.index(ct[j]) + 7) % 26]
out.write(f"N3 0 1 AZ>KA_VV_7_11_one_wrong_letter_slot{SLOT} {''.join(ct)}\n"); out.close()
