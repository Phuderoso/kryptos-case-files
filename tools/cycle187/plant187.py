"""Cycle 187 planted controls (independent string-level encryptor; shares no code with lrk186.c).
Quagmire IV (plaintext-side A, ciphertext-side B), Vig/Beau, affine linear-recurrence key on the CARVED index (M1: k[j], j = carved
position, seed at carved positions 0..L-1), behind perm q of all.bin (plaintext i carved at S[i] = P[q][i]).
Direction f = A themed (144) x B vocabulary (18,776); direction r = A vocabulary x B themed.
usage: plant187.py all.bin alpha172.txt alpha_themed180.txt outdir"""
import sys, json, random, os
import numpy as np
P = np.fromfile(sys.argv[1], dtype=np.int16).reshape(-1, 97)
V = dict(reversed(l.split()) for l in open(sys.argv[2])); TH = dict(reversed(l.split()) for l in open(sys.argv[3])); out = sys.argv[4]
os.makedirs(out, exist_ok=True); AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
PTX = "THEIRONDOORFACEDDUEXX" + "EASTNORTHEAST" + "OFTHEFOUNTAINWHERETHEOLDWORLD" + "BERLINCLOCK" + "STRUCKTHEHOURATMIDNIGHT"
assert len(PTX) == 97 and PTX[21:34] == "EASTNORTHEAST" and PTX[63:74] == "BERLINCLOCK"
CI = list(range(21, 34)) + list(range(63, 74))
R = random.Random(18700)
RAND = "".join(R.sample(AZ, 26)); assert RAND not in V.values() and RAND not in TH.values(); AL = {**V, **TH, "RAND1": RAND}
def keystream(c, d, seed):                       # carved index j = 0..96
    k = list(seed)
    while len(k) < 97: k.append((sum(c[j] * k[-1 - j] for j in range(len(c))) + d) % 26)
    return k
def enc(p, k, A, B, form):
    i = A.index(p); return B[(i + k) % 26] if form == "vig" else B[(k - i) % 26]
def build(pt, k, A, B, form, q):
    S = P[q]; C = ["?"] * 97
    for i in range(97): C[S[i]] = enc(pt[i], k[S[i]], A, B, form)
    assert "?" not in C; return "".join(C)
plants = []
def add(name, dr, L, alab, blab, form, c, d, seed, q, kind="pos", key=None, outside=True):
    A, B = AL[alab], AL[blab]; k = key if key is not None else keystream(c, d, seed)
    if kind == "pos":
        if dr == "f": assert alab in TH and blab in V and (blab not in TH or not outside)
        else: assert alab in V and blab in TH and (alab not in TH or not outside)
    plants.append(dict(name=name, dir=dr, L=L, alab=alab, blab=blab, form=form, c=c, d=d, seed=seed, q=q, kind=kind,
                       ct=build(PTX, k, A, B, form, q), pt=PTX))
rc = lambda L: [R.randrange(26) for _ in range(L)]
qs = [int(x) for x in R.sample(range(P.shape[0]), 16)]
seedrows = [q for q in range(P.shape[0]) if min(int(P[q][i]) for i in CI) < 2]     # a crib slot at carved position 0 or 1
sq = R.sample(seedrows, 2)
add("P1_f_L1_vig_KA_x_SAINTLY-K", "f", 1, "KA", "SAINTLY/K", "vig", rc(1), R.randrange(26), rc(1), qs[0])
add("P2_f_L2_beau_PALIMPSEST-Z_x_MERCHANT-Z", "f", 2, "PALIMPSEST/Z", "MERCHANT/Z", "beau", rc(2), R.randrange(26), rc(2), qs[1])
add("P3_f_L3_vig_BERLINCLOCK-Z_x_NOVEMBER-Z_seedslot", "f", 3, "BERLINCLOCK/Z", "NOVEMBER/Z", "vig", rc(3), R.randrange(26), rc(3), sq[0])
c4 = rc(3); c4[2] = 2 * R.randrange(1, 13)
add("P4_f_L3_beau_AZ_x_ITALIAN-K_nonunit", "f", 3, "AZ", "ITALIAN/K", "beau", c4, R.randrange(26), rc(3), qs[2])
add("P5_r_L1_vig_MEDITERRANEAN-Z_x_ABSCISSA-Z", "r", 1, "MEDITERRANEAN/Z", "ABSCISSA/Z", "vig", rc(1), R.randrange(26), rc(1), qs[3])
add("P6_r_L2_beau_OBLIQUE-Z_x_KA", "r", 2, "OBLIQUE/Z", "KA", "beau", rc(2), R.randrange(26), rc(2), qs[4])
add("P7_r_L3_vig_PLIGHT-K_x_PALIMPSEST-Z_seedslot", "r", 3, "PLIGHT/K", "PALIMPSEST/Z", "vig", rc(3), R.randrange(26), rc(3), sq[1])
add("P8_r_L1_vig_MOUTHS-Z_x_SHADOW-K_progressive", "r", 1, "MOUTHS/Z", "SHADOW/K", "vig", [1], 3, [R.randrange(26)], qs[5])
add("P9_f_L2_vig_KA_x_KA_A_eq_B", "f", 2, "KA", "KA", "vig", rc(2), R.randrange(26), rc(2), qs[6], outside=False)
add("P10_f_L1_vig_LAYERTWO-Z_x_TOMB-Z_recount", "f", 1, "LAYERTWO/Z", "TOMB/Z", "vig", rc(1), R.randrange(26), rc(1), qs[7], outside=False)
add("P11_r_L1_beau_SLOWLY-Z_x_EGYPT-Z_recount", "r", 1, "SLOWLY/Z", "EGYPT/Z", "beau", rc(1), R.randrange(26), rc(1), qs[8], outside=False) if "SLOWLY/Z" in V and "EGYPT/Z" in TH else None
# negatives: must NOT be found at the planted perm in either direction (any pair, form, L)
n1 = plants[2]; ct = list(n1["ct"]); S = P[n1["q"]]; j = int(S[30]); ct[j] = AZ[(AZ.index(ct[j]) + 7) % 26]
plants.append(dict(n1, name="N1_P3_one_wrong_carved_letter_slot30", ct="".join(ct), kind="neg"))
add("N2_random_key", "f", 3, "KA", "NOVEMBER/Z", "vig", None, None, None, qs[9], kind="neg", key=[R.randrange(26) for _ in range(97)])
add("N3_alphabet_outside_lists_RAND1_x_MERCHANT-Z_L2", "f", 2, "RAND1", "MERCHANT/Z", "vig", rc(2), R.randrange(26), rc(2), qs[10], kind="neg")
c5 = rc(4); c5[3] = 1
add("N4_order4_outside_L_range", "f", 4, "KA", "PLIGHT/K", "vig", c5, R.randrange(26), rc(4), qs[11], kind="neg")
json.dump(plants, open(f"{out}/plants.json", "w"), indent=1)
for p in plants: print(p["name"], p["kind"], p["dir"], "q", p["q"], "c", p["c"], "d", p["d"], "seed", p["seed"], p["ct"])
