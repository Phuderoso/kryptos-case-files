"""Cycle 178 planted controls (independent string-level encryptor, no code shared with lr178.c).
Writes ctl/plants.json: each plant = carved text, the perm q (row of all.bin) it sits behind, the mode/ix/L it must be found in,
the planted (c, d, seed) and the planted plaintext.  usage: plant178.py all.bin outdir"""
import sys, json, random, os
import numpy as np
P = np.fromfile(sys.argv[1], dtype=np.int16).reshape(-1, 97); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"
PTX = ("SLOWLYDESPARATLYSLOWT" + "EASTNORTHEAST" + "OFTHEOLDTOWERTHESHADOWFELLONX" + "BERLINCLOCK" + "ANDTHEHOURSWERECOUNTEDX")
assert len(PTX) == 97 and PTX[21:34] == "EASTNORTHEAST" and PTX[63:74] == "BERLINCLOCK"
def keystream(c, d, seed):
    k = list(seed)
    while len(k) < 97: k.append((sum(c[j] * k[-1 - j] for j in range(len(c))) + d) % 26)
    return k
def enc(p, k, alph, form):
    i = alph.index(p); return alph[(i + k) % 26] if form == "vig" else alph[(k - i) % 26]
def build(pt, k, alph, form, q, ix):
    S = P[q]; C = ["?"] * 97
    for i in range(97):
        kk = k[i] if ix == 0 else k[S[i]]          # ix 0: key on plaintext index; ix 1: key on carved index
        C[S[i]] = enc(pt[i], kk, alph, form)
    assert "?" not in C; return "".join(C)
R = random.Random(17800); plants = []
def add(name, mode, ix, L, pa, form, c, d, seed, q, pt=PTX, kind="pos", word=None, nb=None, key=None):
    alph = KA if pa == "ka" else AZ
    k = key if key is not None else keystream(c, d, seed)
    ct = build(pt, k, alph, form, q, ix)
    plants.append(dict(name=name, mode=mode, ix=ix, L=L, pa=pa, form=form, c=c, d=d, seed=seed, q=q, ct=ct, pt=pt, kind=kind,
                       word=word, nb=nb))
rc = lambda L: [R.randrange(26) for _ in range(L)]
qs = [int(x) for x in R.sample(range(P.shape[0]), 16)]
add("P1_ix0_L3_az_vig", 0, 0, 3, "az", "vig", rc(3), R.randrange(26), rc(3), qs[0])
add("P2_ix0_L6_ka_beau", 0, 0, 6, "ka", "beau", rc(6), R.randrange(26), rc(6), qs[1])
add("P3_ix0_L8_az_beau", 0, 0, 8, "az", "beau", rc(8), R.randrange(26), rc(8), qs[2])
add("P4_ix0_L9_ka_vig", 0, 0, 9, "ka", "vig", rc(9), R.randrange(26), rc(9), qs[3])
add("P5_ix0_fib_KR_ka_vig", 0, 0, 2, "ka", "vig", [1, 1], 0, [KA.index("K"), KA.index("R")], qs[4])
add("P6_ix1_L2_az_beau", 1, 1, 2, "az", "beau", rc(2), R.randrange(26), rc(2), qs[5])
c7 = rc(4); c7[3] = 2 * R.randrange(13)                       # non-unit last weight
add("P7_ix1_L4_ka_vig_nonunit", 1, 1, 4, "ka", "vig", c7, R.randrange(26), rc(4), qs[6])
add("P8_ix1_L5_az_vig", 1, 1, 5, "az", "vig", rc(5), R.randrange(26), rc(5), qs[7])
add("P9_W1_L7_PALIMPSEST_kaN_ka_beau", 2, 1, 7, "ka", "beau", [1, 0, 1, 1, 0, 0, 1], 5, [KA.index(x) for x in "PALIMPS"], qs[8], word="PALIMPSEST", nb="kaN")
add("P10_W0_L10_BERLINCLOCK_azN_az_vig", 2, 0, 10, "az", "vig", [0, 1, 0, 0, 1, 0, 0, 0, 0, 1], 11, [AZ.index(x) for x in "BERLINCLOC"], qs[9], word="BERLINCLOCK", nb="azN")
add("P11_ix1_L3_ka_beau", 1, 1, 3, "ka", "beau", rc(3), R.randrange(26), rc(3), qs[10])
add("P12_W0_L6_KRYPTOS_kaN_az_beau", 2, 0, 6, "az", "beau", [1, 1, 0, 0, 0, 1], 0, [KA.index(x) for x in "KRYPTO"], qs[11], word="KRYPTOS", nb="kaN")
# negatives: must NOT be found at their planted perm
n1 = plants[0]; ct = list(n1["ct"]); S = P[n1["q"]]; j = int(S[25]); ct[j] = AZ[(AZ.index(ct[j]) + 7) % 26]
plants.append(dict(n1, name="N1_P1_one_wrong_carved_letter", ct="".join(ct), kind="neg"))
add("N2_ix1_random_key", 1, 1, 5, "az", "vig", None, None, None, qs[12], kind="neg", key=[R.randrange(26) for _ in range(97)])
n3 = plants[8]; k = keystream(n3["c"], n3["d"], [KA.index(x) for x in "PALIMPS"]); k = [R.randrange(26)] + k[:96]   # seed shifted by one
add("N3_W1_seed_shifted_by_one", 2, 1, 7, "ka", "beau", n3["c"], n3["d"], n3["seed"], qs[13], kind="neg", key=k, word="PALIMPSEST", nb="kaN")
json.dump(plants, open(f"{out}/plants.json", "w"), indent=1)
for p in plants: print(p["name"], p["kind"], "q", p["q"], "c", p["c"], "d", p["d"], p["ct"])
