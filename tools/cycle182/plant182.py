"""Cycle 182 planted controls (independent string-level encryptor; shares no code with lrk182.c).
Quagmire IV: plaintext-side alphabet A and ciphertext-side alphabet B (different keyed alphabets), Vig/Beau, an affine
linear-recurrence key on the plaintext index (M0), behind perm q of all.bin.  dir f = A themed x B vocabulary, dir r = A vocabulary x B themed.
usage: plant182.py all.bin alpha172.txt alpha_themed180.txt outdir"""
import sys, json, random, os
import numpy as np
P = np.fromfile(sys.argv[1], dtype=np.int16).reshape(-1, 97)
V = dict(reversed(l.split()) for l in open(sys.argv[2])); TH = dict(reversed(l.split()) for l in open(sys.argv[3])); out = sys.argv[4]
AL = {**V, **TH}; os.makedirs(out, exist_ok=True); AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
PTX = "THEIRONDOORFACEDDUEXX" + "EASTNORTHEAST" + "OFTHEFOUNTAINWHERETHEOLDWORLD" + "BERLINCLOCK" + "STRUCKTHEHOURATMIDNIGHT"
assert len(PTX) == 97 and PTX[21:34] == "EASTNORTHEAST" and PTX[63:74] == "BERLINCLOCK"
def keystream(c, d, seed):
    k = list(seed)
    while len(k) < 97: k.append((sum(c[j] * k[-1 - j] for j in range(len(c))) + d) % 26)
    return k
def enc(p, k, A, B, form):
    i = A.index(p); return B[(i + k) % 26] if form == "vig" else B[(k - i) % 26]
def build(pt, k, A, B, form, q):
    S = P[q]; C = ["?"] * 97
    for i in range(97): C[S[i]] = enc(pt[i], k[i], A, B, form)
    assert "?" not in C; return "".join(C)
R = random.Random(18200); plants = []
def add(name, dr, L, alab, blab, form, c, d, seed, q, kind="pos", key=None):
    A, B = AL[alab], AL[blab]; k = key if key is not None else keystream(c, d, seed)
    if kind == "pos": assert (alab in TH and blab in V) if dr == "f" else (alab in V and blab in TH)
    plants.append(dict(name=name, dir=dr, L=L, alab=alab, blab=blab, form=form, c=c, d=d, seed=seed, q=q, kind=kind,
                       ct=build(PTX, k, A, B, form, q), pt=PTX))
rc = lambda L: [R.randrange(26) for _ in range(L)]
qs = [int(x) for x in R.sample(range(P.shape[0]), 16)]
add("P1_f_L1_vig_KA_x_SHADOW-Z", "f", 1, "KA", "SHADOW/Z", "vig", rc(1), R.randrange(26), rc(1), qs[0])
add("P2_f_L3_beau_PALIMPSEST-K_x_BERLIN-Z", "f", 3, "PALIMPSEST/K", "BERLIN/Z", "beau", rc(3), R.randrange(26), rc(3), qs[1])
add("P3_f_L5_vig_IQLUSION-Z_x_LODESTONE-K", "f", 5, "IQLUSION/Z", "LODESTONE/K", "vig", rc(5), R.randrange(26), rc(5), qs[2])
c4 = rc(6); c4[5] = 2 * R.randrange(1, 13)                        # non-unit last weight
add("P4_f_L6_beau_ABSCISSA-Z_x_COMPASS-K_nonunit", "f", 6, "ABSCISSA/Z", "COMPASS/K", "beau", c4, R.randrange(26), rc(6), qs[3])
add("P5_f_L2_vig_SHADOW-K_x_LODESTONE-K", "f", 2, "SHADOW/K", "LODESTONE/K", "vig", rc(2), R.randrange(26), rc(2), qs[4])
add("P6_f_L1_vig_BERLINCLOCK-K_x_MAGNETIC-Z_progressive", "f", 1, "BERLINCLOCK/K", "MAGNETIC/Z", "vig", [1], 3, [R.randrange(26)], qs[5])
add("P7_r_L2_beau_MAGNETIC-Z_x_KA", "r", 2, "MAGNETIC/Z", "KA", "beau", rc(2), R.randrange(26), rc(2), qs[6])
add("P8_r_L4_vig_LODESTONE-Z_x_UNDERGRUUND-K", "r", 4, "LODESTONE/Z", "UNDERGRUUND/K", "vig", rc(4), R.randrange(26), rc(4), qs[7])
add("P9_r_L6_beau_CARTER-Z_x_PALIMPSEST-K", "r", 6, "CARTER/Z", "PALIMPSEST/K", "beau", rc(6), R.randrange(26), rc(6), qs[8])
add("P10_r_L1_vig_AZ_x_KA", "r", 1, "AZ", "KA", "vig", rc(1), R.randrange(26), rc(1), qs[9])
# negatives: must NOT be found at their planted perm (either direction, any pair, form, L)
n1 = plants[1]; ct = list(n1["ct"]); S = P[n1["q"]]; j = int(S[30]); ct[j] = AZ[(AZ.index(ct[j]) + 7) % 26]
plants.append(dict(n1, name="N1_P2_one_wrong_carved_letter_slot30", ct="".join(ct), kind="neg"))
add("N2_f_random_key", "f", 6, "KA", "SHADOW/Z", "vig", None, None, None, qs[10], kind="neg", key=[R.randrange(26) for _ in range(97)])
assert "TOMB/Z" not in TH and "SLOWLY/Z" not in TH
add("N3_pair_outside_scope_TOMB-Z_x_SLOWLY-Z_L3", "f", 3, "TOMB/Z", "SLOWLY/Z", "vig", rc(3), R.randrange(26), rc(3), qs[11], kind="neg")
c7 = rc(7); c7[6] = 1
add("N4_r_order7_outside_L_range", "r", 7, "CARTER/Z", "PALIMPSEST/K", "vig", c7, R.randrange(26), rc(7), qs[12], kind="neg")
json.dump(plants, open(f"{out}/plants.json", "w"), indent=1)
for p in plants: print(p["name"], p["kind"], "q", p["q"], "c", p["c"], "d", p["d"], p["ct"])
