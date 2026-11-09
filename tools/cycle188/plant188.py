"""Cycle 188 planted controls (independent string-level encryptor; shares no code with lrk188.c).
Quagmire IV (plaintext-side A, ciphertext-side B), Vig/Beau, affine linear-recurrence key on the CARVED index (M1: k[j], j = carved
position, seed at carved positions 0..L-1), behind perm q of all.bin (plaintext i carved at S[i] = P[q][i]), then ONE carving error:
the carved letter at the carved position of crib slot t is replaced by the letter whose B-index is shifted by delta (delta odd and
not 13: wrong mod 2 and mod 13; delta even: wrong mod 13 only; delta 13: wrong mod 2 only).
Direction f = A themed (144) x B vocabulary (18,776); direction r = A vocabulary x B themed.
usage: plant188.py all.bin alpha172.txt alpha_themed180.txt outdir"""
import sys, json, random, os
import numpy as np
P = np.fromfile(sys.argv[1], dtype=np.int16).reshape(-1, 97)
V = dict(reversed(l.split()) for l in open(sys.argv[2])); TH = dict(reversed(l.split()) for l in open(sys.argv[3])); out = sys.argv[4]
os.makedirs(out, exist_ok=True); AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
PTX = "THEIRONDOORFACEDDUEXX" + "EASTNORTHEAST" + "OFTHEFOUNTAINWHERETHEOLDWORLD" + "BERLINCLOCK" + "STRUCKTHEHOURATMIDNIGHT"
assert len(PTX) == 97 and PTX[21:34] == "EASTNORTHEAST" and PTX[63:74] == "BERLINCLOCK"
CI = list(range(21, 34)) + list(range(63, 74))
R = random.Random(18800)
RAND = "".join(R.sample(AZ, 26)); assert RAND not in V.values() and RAND not in TH.values(); AL = {**V, **TH, "RAND1": RAND}
def keystream(c, d, seed):
    k = list(seed)
    while len(k) < 97: k.append((sum(c[j] * k[-1 - j] for j in range(len(c))) + d) % 26)
    return k
def enc(p, k, A, B, form):
    i = A.index(p); return B[(i + k) % 26] if form == "vig" else B[(k - i) % 26]
def build(pt, k, A, B, form, q, errs):
    S = P[q]; C = ["?"] * 97
    for i in range(97): C[S[i]] = enc(pt[i], k[S[i]], A, B, form)
    for t, dl in errs: j = int(S[CI[t]]); C[j] = B[(B.index(C[j]) + dl) % 26]
    assert "?" not in C; return "".join(C)
plants = []
def add(name, dr, L, alab, blab, form, c, d, seed, q, errs, kind="pos", key=None, outside=True, lmax=2, win=100):
    A, B = AL[alab], AL[blab]; k = key if key is not None else keystream(c, d, seed)
    if kind == "pos":
        if dr == "f": assert alab in TH and blab in V and (blab not in TH or not outside)
        else: assert alab in V and blab in TH and (alab not in TH or not outside)
    plants.append(dict(name=name, dir=dr, L=L, alab=alab, blab=blab, form=form, c=c, d=d, seed=seed, q=q, kind=kind, errs=errs,
                       t=(errs[0][0] if len(errs) == 1 else -1), lmax=lmax, win=win, ct=build(PTX, k, A, B, form, q, errs), pt=PTX))
rc = lambda L: [R.randrange(26) for _ in range(L)]
qs = [int(x) for x in R.sample(range(P.shape[0]), 16)]
seedrows = [q for q in range(P.shape[0]) if min(int(P[q][i]) for i in CI) < 2]
sq = R.sample(seedrows, 2)
def seedslot(q): return min(range(24), key=lambda t: int(P[q][CI[t]]))
add("P1_f_L1_vig_KA_x_SAINTLY-K_err5", "f", 1, "KA", "SAINTLY/K", "vig", rc(1), R.randrange(26), rc(1), qs[0], [(5, 7)])
add("P2_f_L2_beau_PALIMPSEST-Z_x_MERCHANT-Z_err18", "f", 2, "PALIMPSEST/Z", "MERCHANT/Z", "beau", rc(2), R.randrange(26), rc(2), qs[1], [(18, 3)])
add("P3_f_L2_vig_BERLINCLOCK-Z_x_NOVEMBER-Z_err_at_seedslot", "f", 2, "BERLINCLOCK/Z", "NOVEMBER/Z", "vig", rc(2), R.randrange(26), rc(2), sq[0], [(seedslot(sq[0]), 5)])
c4 = rc(3); c4[2] = 2 * R.randrange(1, 13)
add("P4_f_L3_beau_AZ_x_ITALIAN-K_nonunit_err0", "f", 3, "AZ", "ITALIAN/K", "beau", c4, R.randrange(26), rc(3), qs[2], [(0, 11)], lmax=3, win=10)
add("P5_r_L1_vig_MEDITERRANEAN-Z_x_ABSCISSA-Z_err23", "r", 1, "MEDITERRANEAN/Z", "ABSCISSA/Z", "vig", rc(1), R.randrange(26), rc(1), qs[3], [(23, 9)])
add("P6_r_L2_beau_OBLIQUE-Z_x_KA_err12_mod13only", "r", 2, "OBLIQUE/Z", "KA", "beau", rc(2), R.randrange(26), rc(2), qs[4], [(12, 2)])
add("P7_r_L3_vig_PLIGHT-K_x_PALIMPSEST-Z_err14_mod2only", "r", 3, "PLIGHT/K", "PALIMPSEST/Z", "vig", rc(3), R.randrange(26), rc(3), sq[1], [(14, 13)], lmax=3, win=10)
add("P8_r_L1_vig_MOUTHS-Z_x_SHADOW-K_progressive_noerr", "r", 1, "MOUTHS/Z", "SHADOW/K", "vig", [1], 3, [R.randrange(26)], qs[5], [])
add("P9_f_L2_vig_KA_x_KA_err13_mod2only", "f", 2, "KA", "KA", "vig", rc(2), R.randrange(26), rc(2), qs[6], [(13, 13)], outside=False)
add("P10_f_L1_vig_LAYERTWO-Z_x_TOMB-Z_err9_recount", "f", 1, "LAYERTWO/Z", "TOMB/Z", "vig", rc(1), R.randrange(26), rc(1), qs[7], [(9, 4)], outside=False)
add("P11_r_L1_beau_SLOWLY-Z_x_EGYPT-Z_err15_recount", "r", 1, "SLOWLY/Z", "EGYPT/Z", "beau", rc(1), R.randrange(26), rc(1), qs[8], [(15, 6)], outside=False)
# negatives: must NOT be found at the planted perm in either direction (any pair, form, L <= lmax)
add("N1_P2_two_wrong_carved_letters", "f", 2, "PALIMPSEST/Z", "MERCHANT/Z", "beau", plants[1]["c"], plants[1]["d"], plants[1]["seed"], qs[1], [(3, 5), (20, 7)], kind="neg")
add("N2_random_key_one_error", "f", 3, "KA", "NOVEMBER/Z", "vig", None, None, None, qs[9], [(7, 3)], kind="neg", key=[R.randrange(26) for _ in range(97)], lmax=3, win=10)
add("N3_alphabet_outside_lists_RAND1_x_MERCHANT-Z_L2_err4", "f", 2, "RAND1", "MERCHANT/Z", "vig", rc(2), R.randrange(26), rc(2), qs[10], [(4, 3)], kind="neg")
c5 = rc(4); c5[3] = 1
add("N4_order4_outside_L_range_err2", "f", 4, "KA", "PLIGHT/K", "vig", c5, R.randrange(26), rc(4), qs[11], [(2, 3)], kind="neg", lmax=3, win=10)
json.dump(plants, open(f"{out}/plants.json", "w"), indent=1)
for p in plants: print(p["name"], p["kind"], p["dir"], "q", p["q"], "c", p["c"], "d", p["d"], "seed", p["seed"], "errs", p["errs"], p["ct"])
