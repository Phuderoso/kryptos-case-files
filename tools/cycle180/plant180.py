"""Cycle 180 planted controls (independent string-level encryptor; shares no code with lrk180.c).
Each plant: keyed alphabet from the registered list (or, for N4, a random permutation NOT in it), tableau type q1/q2/q3, Vig/Beau,
an affine linear-recurrence key, behind perm q of all.bin, key on the plaintext index (ix 0) or on the carved index (ix 1).
usage: plant180.py all.bin alpha172.txt outdir"""
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
R = random.Random(18000); plants = []
def add(name, ix, L, alab, ty, form, c, d, seed, q, kind="pos", key=None, alph=None, run="vocab"):
    K = alph if alph else AL[alab]; A, B = tab(K, ty); k = key if key is not None else keystream(c, d, seed)
    plants.append(dict(name=name, ix=ix, L=L, alab=alab, alph=K, ty=ty, form=form, c=c, d=d, seed=seed, q=q, kind=kind, run=run,
                       ct=build(PTX, k, A, B, form, q, ix), pt=PTX))
rc = lambda L: [R.randrange(26) for _ in range(L)]
qs = [int(x) for x in R.sample(range(P.shape[0]), 16)]
add("P1_ix0_L3_q3_vig_SHADOW-Z", 0, 3, "SHADOW/Z", "q3", "vig", rc(3), R.randrange(26), rc(3), qs[0])
add("P2_ix0_L5_q1_beau_BERLIN-K", 0, 5, "BERLIN/K", "q1", "beau", rc(5), R.randrange(26), rc(5), qs[1])
add("P3_ix0_L7_q2_vig_ABSCISSA-Z", 0, 7, "ABSCISSA/Z", "q2", "vig", rc(7), R.randrange(26), rc(7), qs[2])
add("P4_ix0_L2_q3_beau_SHADOW-K", 0, 2, "SHADOW/K", "q3", "beau", rc(2), R.randrange(26), rc(2), qs[3])
c5 = rc(6); c5[5] = 2 * R.randrange(1, 13)                       # non-unit last weight
add("P5_ix0_L6_q3_vig_PALIMPSEST-K_nonunit", 0, 6, "PALIMPSEST/K", "q3", "vig", c5, R.randrange(26), rc(6), qs[4])
add("P6_ix1_L1_q3_vig_COMPASS-Z", 1, 1, "COMPASS/Z", "q3", "vig", rc(1), R.randrange(26), rc(1), qs[5])
add("P7_ix1_L2_q1_beau_LODESTONE-K", 1, 2, "LODESTONE/K", "q1", "beau", rc(2), R.randrange(26), rc(2), qs[6])
add("P8_ix1_L3_q2_vig_MAGNETIC-Z", 1, 3, "MAGNETIC/Z", "q2", "vig", rc(3), R.randrange(26), rc(3), qs[7])
add("P9_ix1_L4_q3_beau_ABSCISSA-K_themed", 1, 4, "ABSCISSA/K", "q3", "beau", rc(4), R.randrange(26), rc(4), qs[8], run="themed")
add("P10_ix0_L1_q3_vig_KA_progressive", 0, 1, "KA", "q3", "vig", [1], 3, [R.randrange(26)], qs[9])
# negatives: must NOT be found at their planted perm
n1 = plants[0]; ct = list(n1["ct"]); S = P[n1["q"]]; j = int(S[30]); ct[j] = AZ[(AZ.index(ct[j]) + 7) % 26]
plants.append(dict(n1, name="N1_P1_one_wrong_carved_letter_slot30", ct="".join(ct), kind="neg"))
add("N2_ix0_random_key", 0, 7, "SHADOW/Z", "q3", "vig", None, None, None, qs[10], kind="neg", key=[R.randrange(26) for _ in range(97)])
add("N3_ix1_random_key", 1, 3, "MAGNETIC/Z", "q2", "vig", None, None, None, qs[11], kind="neg", key=[R.randrange(26) for _ in range(97)])
rp = list(AZ); R.shuffle(rp); rp = "".join(rp); assert rp not in AL.values()
add("N4_ix0_L3_q3_vig_alphabet_not_in_list", 0, 3, "RANDOM", "q3", "vig", rc(3), R.randrange(26), rc(3), qs[12], kind="neg", alph=rp)
json.dump(plants, open(f"{out}/plants.json", "w"), indent=1)
for p in plants: print(p["name"], p["kind"], "q", p["q"], "c", p["c"], "d", p["d"], p["ct"])
