"""Cycle 185 planted controls (independent string-level encryptor; shares no code with lrk185.c).
Quagmire IV (plaintext-side alphabet A, ciphertext-side alphabet B), Vig/Beau, affine linear-recurrence key on the plaintext index,
behind perm q of all.bin, then ONE carved letter at a crib slot's carved position changed by a random non-zero shift (one-error plants).
Both alphabets from the 18,776 vocabulary (case 172 scope, I-172); every plant is run on the method-1 (direction r) path, A = B list = vocabulary.
usage: plant185.py all.bin alpha172.txt alpha_themed180.txt outdir   (themed list only used to assert the P1-P7 alphabets are NOT themed)"""
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
R = random.Random(18500); plants = []
RAND = "".join(R.sample(AZ, 26)); assert RAND not in V.values(); AL["RAND1"] = RAND
def miscarve(ct, q, slots):
    ct = list(ct)
    for s in slots: j = int(P[q][s]); ct[j] = AZ[(AZ.index(ct[j]) + R.randrange(1, 26)) % 26]
    return "".join(ct)
def add(name, L, alab, blab, form, c, d, seed, q, err, kind="pos", key=None, notthemed=False):
    A, B = AL[alab], AL[blab]; k = key if key is not None else keystream(c, d, seed)
    if kind == "pos": assert alab in V and blab in V
    if notthemed: assert alab not in TH and blab not in TH
    ct = miscarve(build(PTX, k, A, B, form, q), q, err)
    plants.append(dict(name=name, dir="r", L=L, alab=alab, blab=blab, form=form, c=c, d=d, seed=seed, q=q, kind=kind, err=err, ct=ct, pt=PTX))
rc = lambda L: [R.randrange(26) for _ in range(L)]
qs = [int(x) for x in R.sample(range(P.shape[0]), 16)]
add("P1_L1_vig_MEDITERRANEAN-Z_x_SAINTLY-K_err25", 1, "MEDITERRANEAN/Z", "SAINTLY/K", "vig", rc(1), R.randrange(26), rc(1), qs[0], [25], notthemed=True)
add("P2_L2_beau_MERCHANT-Z_x_OBLIQUE-Z_err66", 2, "MERCHANT/Z", "OBLIQUE/Z", "beau", rc(2), R.randrange(26), rc(2), qs[1], [66], notthemed=True)
add("P3_L3_vig_NOVEMBER-Z_x_PLIGHT-K_err21seed", 3, "NOVEMBER/Z", "PLIGHT/K", "vig", rc(3), R.randrange(26), rc(3), qs[2], [21], notthemed=True)
c3 = rc(3); c3[2] = 2 * R.randrange(1, 13)                        # non-unit last weight
add("P4_L3_beau_ITALIAN-K_x_RATTLING-K_nonunit_err33", 3, "ITALIAN/K", "RATTLING/K", "beau", c3, R.randrange(26), rc(3), qs[3], [33], notthemed=True)
add("P5_L2_vig_WHIP-K_x_KNIGHTS-Z_strict", 2, "WHIP/K", "KNIGHTS/Z", "vig", rc(2), R.randrange(26), rc(2), qs[4], [], notthemed=True)
add("P6_L1_vig_MOUTHS-Z_x_HESITATING-K_progressive_err73", 1, "MOUTHS/Z", "HESITATING/K", "vig", [1], 3, [R.randrange(26)], qs[5], [73], notthemed=True)
add("P7_L2_vig_SAINTLY-K_x_SAINTLY-K_AeqB_err63", 2, "SAINTLY/K", "SAINTLY/K", "vig", rc(2), R.randrange(26), rc(2), qs[6], [63], notthemed=True)
add("P8_L1_vig_LAYER-Z_x_TOMB-Z_err22", 1, "LAYER/Z", "TOMB/Z", "vig", rc(1), R.randrange(26), rc(1), qs[7], [22])
add("P9_L2_beau_SLOWLY-Z_x_EGYPT-Z_err70", 2, "SLOWLY/Z", "EGYPT/Z", "beau", rc(2), R.randrange(26), rc(2), qs[8], [70])
add("P10_L1_beau_KA_x_SHADOW-K_err30", 1, "KA", "SHADOW/K", "beau", rc(1), R.randrange(26), rc(1), qs[9], [30])
# negatives: must NOT be found at their planted perm (any pair, form, L, slot)
add("N1_L2_two_errors_66_70", 2, "MERCHANT/Z", "OBLIQUE/Z", "beau", rc(2), R.randrange(26), rc(2), qs[10], [66, 70], kind="neg")
add("N2_random_key", 3, "MEDITERRANEAN/Z", "SAINTLY/K", "vig", None, None, None, qs[11], [], kind="neg", key=[R.randrange(26) for _ in range(97)])
add("N3_alphabet_outside_vocabulary_RAND1_x_OBLIQUE-Z_L2_err28", 2, "RAND1", "OBLIQUE/Z", "vig", rc(2), R.randrange(26), rc(2), qs[12], [28], kind="neg")
c4 = rc(4); c4[3] = 1
add("N4_order4_err68_outside_L_range", 4, "NOVEMBER/Z", "PLIGHT/K", "vig", c4, R.randrange(26), rc(4), qs[13], [68], kind="neg")
json.dump(plants, open(f"{out}/plants.json", "w"), indent=1)
for p in plants: print(p["name"], p["kind"], "q", p["q"], "c", p["c"], "d", p["d"], "err", p["err"], p["ct"])
