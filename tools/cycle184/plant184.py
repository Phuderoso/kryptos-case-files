"""Cycle 184 planted controls (independent string-level encryptor; shares no code with lrk184.c).
Quagmire IV with BOTH alphabets from the 18,776 vocabulary (I-163): plaintext-side A, ciphertext-side B, Vig/Beau, affine
linear-recurrence key on the plaintext index (M0), behind perm q of all.bin.
usage: plant184.py all.bin alpha172.txt alpha_themed180.txt outdir"""
import sys, json, random, os
import numpy as np
P = np.fromfile(sys.argv[1], dtype=np.int16).reshape(-1, 97)
V = dict(reversed(l.split()) for l in open(sys.argv[2])); TH = dict(reversed(l.split()) for l in open(sys.argv[3])); out = sys.argv[4]
os.makedirs(out, exist_ok=True); AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
PTX = "THEIRONDOORFACEDDUEXX" + "EASTNORTHEAST" + "OFTHEFOUNTAINWHERETHEOLDWORLD" + "BERLINCLOCK" + "STRUCKTHEHOURATMIDNIGHT"
assert len(PTX) == 97 and PTX[21:34] == "EASTNORTHEAST" and PTX[63:74] == "BERLINCLOCK"
R = random.Random(18400)
RAND = "".join(R.sample(AZ, 26)); assert RAND not in V.values(); AL = {**V, "RAND1": RAND}
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
plants = []
def add(name, L, alab, blab, form, c, d, seed, q, kind="pos", key=None, vonly=True):
    A, B = AL[alab], AL[blab]; k = key if key is not None else keystream(c, d, seed)
    if kind == "pos":
        assert alab in V and blab in V
        if vonly: assert alab not in TH and blab not in TH          # genuinely outside case 170's themed x vocabulary scope
    plants.append(dict(name=name, dir="v", L=L, alab=alab, blab=blab, form=form, c=c, d=d, seed=seed, q=q, kind=kind,
                       ct=build(PTX, k, A, B, form, q), pt=PTX))
rc = lambda L: [R.randrange(26) for _ in range(L)]
qs = [int(x) for x in R.sample(range(P.shape[0]), 16)]
add("P1_L1_vig_MEDITERRANEAN-Z_x_SAINTLY-K", 1, "MEDITERRANEAN/Z", "SAINTLY/K", "vig", rc(1), R.randrange(26), rc(1), qs[0])
add("P2_L2_beau_MERCHANT-Z_x_OBLIQUE-Z", 2, "MERCHANT/Z", "OBLIQUE/Z", "beau", rc(2), R.randrange(26), rc(2), qs[1])
add("P3_L3_vig_NOVEMBER-Z_x_PLIGHT-K", 3, "NOVEMBER/Z", "PLIGHT/K", "vig", rc(3), R.randrange(26), rc(3), qs[2])
c4 = rc(4); c4[3] = 2 * R.randrange(1, 13)                        # non-unit last weight
add("P4_L4_beau_ITALIAN-K_x_RATTLING-K_nonunit", 4, "ITALIAN/K", "RATTLING/K", "beau", c4, R.randrange(26), rc(4), qs[3])
add("P5_L4_vig_WHIP-K_x_KNIGHTS-Z", 4, "WHIP/K", "KNIGHTS/Z", "vig", rc(4), R.randrange(26), rc(4), qs[4])
add("P6_L1_vig_MOUTHS-Z_x_HESITATING-K_progressive", 1, "MOUTHS/Z", "HESITATING/K", "vig", [1], 3, [R.randrange(26)], qs[5])
add("P7_L2_vig_SAINTLY-K_x_SAINTLY-K_A_eq_B", 2, "SAINTLY/K", "SAINTLY/K", "vig", rc(2), R.randrange(26), rc(2), qs[6])
add("P8_L1_vig_LAYER-Z_x_TOMB-Z_recount", 1, "LAYER/Z", "TOMB/Z", "vig", rc(1), R.randrange(26), rc(1), qs[7], vonly=False)
add("P9_L2_beau_SLOWLY-Z_x_EGYPT-Z_recount", 2, "SLOWLY/Z", "EGYPT/Z", "beau", rc(2), R.randrange(26), rc(2), qs[8], vonly=False)
add("P10_L1_beau_KA_x_SHADOW-K_recount", 1, "KA", "SHADOW/K", "beau", rc(1), R.randrange(26), rc(1), qs[9], vonly=False)
# negatives: must NOT be found at their planted perm (any pair, form, L)
n1 = plants[2]; ct = list(n1["ct"]); S = P[n1["q"]]; j = int(S[30]); ct[j] = AZ[(AZ.index(ct[j]) + 7) % 26]
plants.append(dict(n1, name="N1_P3_one_wrong_carved_letter_slot30", ct="".join(ct), kind="neg"))
add("N2_random_key", 4, "NOVEMBER/Z", "PLIGHT/K", "vig", None, None, None, qs[10], kind="neg", key=[R.randrange(26) for _ in range(97)])
add("N3_alphabet_outside_vocabulary_RAND1_x_OBLIQUE-Z_L2", 2, "RAND1", "OBLIQUE/Z", "vig", rc(2), R.randrange(26), rc(2), qs[11], kind="neg")
c5 = rc(5); c5[4] = 1
add("N4_order5_outside_L_range", 5, "MERCHANT/Z", "WHIP/K", "vig", c5, R.randrange(26), rc(5), qs[12], kind="neg")
json.dump(plants, open(f"{out}/plants.json", "w"), indent=1)
for p in plants: print(p["name"], p["kind"], "q", p["q"], "c", p["c"], "d", p["d"], p["ct"])
