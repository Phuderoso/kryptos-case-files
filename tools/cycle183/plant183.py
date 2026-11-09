"""Cycle 183 planted controls (independent string-level encryptor; shares no code with lrk183.c).
Quagmire IV (plaintext-side alphabet A, ciphertext-side alphabet B), Vig/Beau, affine linear-recurrence key on the plaintext index,
behind perm q of all.bin, then ONE carved letter at a crib slot's carved position changed by a random non-zero shift (one-error plants).
dir f = A themed x B vocabulary, dir r = A vocabulary x B themed.
usage: plant183.py all.bin alpha172.txt alpha_themed180.txt outdir"""
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
R = random.Random(18300); plants = []
def miscarve(ct, q, slots):
    ct = list(ct)
    for s in slots: j = int(P[q][s]); ct[j] = AZ[(AZ.index(ct[j]) + R.randrange(1, 26)) % 26]
    return "".join(ct)
def add(name, dr, L, alab, blab, form, c, d, seed, q, err, kind="pos", key=None):
    A, B = AL[alab], AL[blab]; k = key if key is not None else keystream(c, d, seed)
    if kind == "pos": assert (alab in TH and blab in V) if dr == "f" else (alab in V and blab in TH)
    ct = miscarve(build(PTX, k, A, B, form, q), q, err)
    plants.append(dict(name=name, dir=dr, L=L, alab=alab, blab=blab, form=form, c=c, d=d, seed=seed, q=q, kind=kind, err=err, ct=ct, pt=PTX))
rc = lambda L: [R.randrange(26) for _ in range(L)]
qs = [int(x) for x in R.sample(range(P.shape[0]), 16)]
add("P1_f_L1_vig_KA_x_SHADOW-Z_err25", "f", 1, "KA", "SHADOW/Z", "vig", rc(1), R.randrange(26), rc(1), qs[0], [25])
add("P2_f_L3_beau_PALIMPSEST-K_x_BERLIN-Z_err66", "f", 3, "PALIMPSEST/K", "BERLIN/Z", "beau", rc(3), R.randrange(26), rc(3), qs[1], [66])
add("P3_f_L5_vig_IQLUSION-Z_x_LODESTONE-K_err21seed", "f", 5, "IQLUSION/Z", "LODESTONE/K", "vig", rc(5), R.randrange(26), rc(5), qs[2], [21])
c4 = rc(4); c4[3] = 2 * R.randrange(1, 13)                        # non-unit last weight
add("P4_f_L4_beau_ABSCISSA-Z_x_COMPASS-K_nonunit_err33", "f", 4, "ABSCISSA/Z", "COMPASS/K", "beau", c4, R.randrange(26), rc(4), qs[3], [33])
add("P5_f_L2_vig_SHADOW-K_x_LODESTONE-K_strict", "f", 2, "SHADOW/K", "LODESTONE/K", "vig", rc(2), R.randrange(26), rc(2), qs[4], [])
add("P6_f_L1_vig_BERLINCLOCK-K_x_MAGNETIC-Z_progressive_err73", "f", 1, "BERLINCLOCK/K", "MAGNETIC/Z", "vig", [1], 3, [R.randrange(26)], qs[5], [73])
add("P7_r_L2_beau_MAGNETIC-Z_x_KA_err63", "r", 2, "MAGNETIC/Z", "KA", "beau", rc(2), R.randrange(26), rc(2), qs[6], [63])
add("P8_r_L4_vig_LODESTONE-Z_x_UNDERGRUUND-K_err30", "r", 4, "LODESTONE/Z", "UNDERGRUUND/K", "vig", rc(4), R.randrange(26), rc(4), qs[7], [30])
add("P9_r_L5_beau_CARTER-Z_x_PALIMPSEST-K_err70", "r", 5, "CARTER/Z", "PALIMPSEST/K", "beau", rc(5), R.randrange(26), rc(5), qs[8], [70])
add("P10_r_L1_vig_AZ_x_KA_err22", "r", 1, "AZ", "KA", "vig", rc(1), R.randrange(26), rc(1), qs[9], [22])
# negatives: must NOT be found at their planted perm (either direction, any pair, form, L, slot)
add("N1_f_L3_two_errors_66_70", "f", 3, "PALIMPSEST/K", "BERLIN/Z", "beau", rc(3), R.randrange(26), rc(3), qs[10], [66, 70], kind="neg")
add("N2_f_random_key", "f", 5, "KA", "SHADOW/Z", "vig", None, None, None, qs[11], [], kind="neg", key=[R.randrange(26) for _ in range(97)])
assert "TOMB/Z" not in TH and "SLOWLY/Z" not in TH
add("N3_pair_outside_scope_TOMB-Z_x_SLOWLY-Z_L3_err28", "f", 3, "TOMB/Z", "SLOWLY/Z", "vig", rc(3), R.randrange(26), rc(3), qs[12], [28], kind="neg")
c7 = rc(6); c7[5] = 1
add("N4_r_order6_err68_outside_L_range", "r", 6, "CARTER/Z", "PALIMPSEST/K", "vig", c7, R.randrange(26), rc(6), qs[13], [68], kind="neg")
json.dump(plants, open(f"{out}/plants.json", "w"), indent=1)
for p in plants: print(p["name"], p["kind"], "q", p["q"], "c", p["c"], "d", p["d"], "err", p["err"], p["ct"])
