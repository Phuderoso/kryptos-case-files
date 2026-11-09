"""Cycle 181 planted controls (independent string-level encryptor; shares no code with lrk181.c). Same construction as plant180
(keyed alphabet from the registered list, tableau q1/q2/q3, Vig/Beau, affine linear-recurrence key, behind perm q of all.bin,
key on the plaintext index ix 0 or the carved index ix 1), then ONE (or, for negatives, two) crib slots' carved letters are
changed by a random non-zero shift (a mis-carved letter).
usage: plant181.py all.bin alpha172.txt outdir"""
import sys, json, random, os
import numpy as np
P = np.fromfile(sys.argv[1], dtype=np.int16).reshape(-1, 97); AL = dict(reversed(l.split()) for l in open(sys.argv[2])); out = sys.argv[3]
os.makedirs(out, exist_ok=True); AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
PTX = "THEIRONDOORFACEDDUEXX" + "EASTNORTHEAST" + "OFTHEFOUNTAINWHERETHEOLDWORLD" + "BERLINCLOCK" + "STRUCKTHEHOURATMIDNIGHT"
assert len(PTX) == 97 and PTX[21:34] == "EASTNORTHEAST" and PTX[63:74] == "BERLINCLOCK"
def keystream(c, d, seed):
    k = list(seed)
    while len(k) < 97: k.append((sum(c[j] * k[-1 - j] for j in range(len(c))) + d) % 26)
    return k
def tab(K, ty): return {"q1": (K, AZ), "q2": (AZ, K), "q3": (K, K)}[ty]
def enc(p, k, A, B, form):
    i = A.index(p); return B[(i + k) % 26] if form == "vig" else B[(k - i) % 26]
def build(pt, k, A, B, form, q, ix):
    S = P[q]; C = ["?"] * 97
    for i in range(97):
        kk = k[i] if ix == 0 else k[S[i]]
        C[S[i]] = enc(pt[i], kk, A, B, form)
    assert "?" not in C; return "".join(C)
R = random.Random(18100); plants = []
def add(name, ix, L, alab, ty, form, c, d, seed, q, err=(), kind="pos", key=None, alph=None):
    K = alph if alph else AL[alab]; A, B = tab(K, ty); k = key if key is not None else keystream(c, d, seed)
    ct = list(build(PTX, k, A, B, form, q, ix)); S = P[q]
    for i in err:                                                  # mis-carve the letter at plaintext crib position i
        j = int(S[i]); ct[j] = AZ[(AZ.index(ct[j]) + R.randrange(1, 26)) % 26]
    plants.append(dict(name=name, ix=ix, L=L, alab=alab, alph=K, ty=ty, form=form, c=c, d=d, seed=seed, q=q, kind=kind, err=list(err),
                       ct="".join(ct), pt=PTX))
rc = lambda L: [R.randrange(26) for _ in range(L)]
qs = [int(x) for x in R.sample(range(P.shape[0]), 20)]
add("P1_ix0_L3_q3_vig_SHADOW-Z_err25", 0, 3, "SHADOW/Z", "q3", "vig", rc(3), R.randrange(26), rc(3), qs[0], err=(25,))
add("P2_ix0_L5_q1_beau_BERLIN-K_err66", 0, 5, "BERLIN/K", "q1", "beau", rc(5), R.randrange(26), rc(5), qs[1], err=(66,))
add("P3_ix0_L6_q2_vig_ABSCISSA-Z_err21", 0, 6, "ABSCISSA/Z", "q2", "vig", rc(6), R.randrange(26), rc(6), qs[2], err=(21,))
add("P4_ix0_L2_q3_beau_SHADOW-K_err73", 0, 2, "SHADOW/K", "q3", "beau", rc(2), R.randrange(26), rc(2), qs[3], err=(73,))
add("P5_ix0_L4_q3_vig_PALIMPSEST-K_strict", 0, 4, "PALIMPSEST/K", "q3", "vig", rc(4), R.randrange(26), rc(4), qs[4])
c6 = rc(6); c6[5] = 2 * R.randrange(1, 13)                       # non-unit last weight
add("P6_ix0_L6_q3_beau_KA_nonunit_err33", 0, 6, "KA", "q3", "beau", c6, R.randrange(26), rc(6), qs[5], err=(33,))
add("P7_ix1_L1_q3_vig_COMPASS-Z_err64", 1, 1, "COMPASS/Z", "q3", "vig", rc(1), R.randrange(26), rc(1), qs[6], err=(64,))
add("P8_ix1_L2_q1_beau_LODESTONE-K_err22", 1, 2, "LODESTONE/K", "q1", "beau", rc(2), R.randrange(26), rc(2), qs[7], err=(22,))
add("P9_ix1_L3_q2_vig_MAGNETIC-Z_err29", 1, 3, "MAGNETIC/Z", "q2", "vig", rc(3), R.randrange(26), rc(3), qs[8], err=(29,))
add("P10_ix1_L3_q3_beau_ABSCISSA-K_strict", 1, 3, "ABSCISSA/K", "q3", "beau", rc(3), R.randrange(26), rc(3), qs[9])
add("P11_ix0_L1_q3_vig_KA_progressive_err30", 0, 1, "KA", "q3", "vig", [1], 3, [R.randrange(26)], qs[10], err=(30,))
add("P12_ix1_L3_q1_vig_SHADOW-K_err73", 1, 3, "SHADOW/K", "q1", "vig", rc(3), R.randrange(26), rc(3), qs[11], err=(73,))
# negatives: must NOT be found at their planted perm
add("N1_ix0_L3_q3_vig_SHADOW-Z_two_errors_66_70", 0, 3, "SHADOW/Z", "q3", "vig", rc(3), R.randrange(26), rc(3), qs[12], err=(66, 70), kind="neg")
add("N2_ix1_L2_q1_beau_LODESTONE-K_two_errors_22_68", 1, 2, "LODESTONE/K", "q1", "beau", rc(2), R.randrange(26), rc(2), qs[13], err=(22, 68), kind="neg")
add("N3_ix0_random_key", 0, 6, "SHADOW/Z", "q3", "vig", None, None, None, qs[14], kind="neg", key=[R.randrange(26) for _ in range(97)])
add("N4_ix1_random_key", 1, 3, "MAGNETIC/Z", "q2", "vig", None, None, None, qs[15], kind="neg", key=[R.randrange(26) for _ in range(97)])
rp = list(AZ); R.shuffle(rp); rp = "".join(rp); assert rp not in AL.values()
add("N5_ix0_L3_q3_vig_alphabet_not_in_list_err25", 0, 3, "RANDOM", "q3", "vig", rc(3), R.randrange(26), rc(3), qs[16], err=(25,), kind="neg", alph=rp)
json.dump(plants, open(f"{out}/plants.json", "w"), indent=1)
for p in plants: print(p["name"], p["kind"], "q", p["q"], "c", p["c"], "d", p["d"], "err", p["err"], p["ct"])
