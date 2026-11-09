"""Cycle 179 planted controls (independent string-level encryptor; no code shared with lr179.c).
Each plant: a linear-recurrence key (cycle-178 family) behind a perm q of all.bin, then ONE carved letter changed at the carved
position of crib slot `err` (the mis-carving the one-error test must tolerate), or two letters (negatives).
usage: plant179.py all.bin outdir   -> outdir/plants.json"""
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
def build(k, alph, form, q, ix):
    S = P[q]; C = ["?"] * 97
    for i in range(97): C[S[i]] = enc(PTX[i], k[i] if ix == 0 else k[S[i]], alph, form)
    return "".join(C)
R = random.Random(17900); plants = []
rc = lambda L: [R.randrange(26) for _ in range(L)]
qs = [int(x) for x in R.sample(range(P.shape[0]), 16)]
def add(name, ix, L, pa, form, errs, q, kind="pos", c=None, d=None, seed=None, key=None):
    alph = KA if pa == "ka" else AZ
    if key is None:
        while True:                      # keep plants whose recurrence is non-degenerate at its order (c_L != 0)
            c = c or rc(L); d = R.randrange(26) if d is None else d; seed = seed or rc(L)
            if c[-1] % 26: break
            c = None
        key = keystream(c, d, seed)
    ct = list(build(key, alph, form, q, ix)); S = P[q]
    for e in errs:                       # e = crib plaintext index; change its carved letter by a non-zero shift
        j = int(S[e]); ct[j] = AZ[(AZ.index(ct[j]) + R.randrange(1, 26)) % 26]
    plants.append(dict(name=name, ix=ix, L=L, pa=pa, form=form, c=c, d=d, seed=seed, q=q, ct="".join(ct), pt=PTX, kind=kind,
                       errs=errs, slot_t=([21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73].index(errs[0]) if errs else None)))
add("P1_ix0_L3_az_vig_err25", 0, 3, "az", "vig", [25], qs[0])          # cycle-178 N1 situation: must now be FOUND at L 3
add("P2_ix0_L6_ka_beau_err21", 0, 6, "ka", "beau", [21], qs[1])         # error in the seed window, first slot
add("P3_ix0_L8_az_beau_err70", 0, 8, "az", "beau", [70], qs[2])         # error in BERLINCLOCK
add("P4_ix0_L5_ka_vig_err33", 0, 5, "ka", "vig", [33], qs[3])           # error at the last block-1 slot (start of the gap propagation)
add("P5_ix0_L7_az_vig_strict", 0, 7, "az", "vig", [], qs[4])            # no error: strict fit must still be reported
add("P6_ix0_fib_ka_beau_err63", 0, 2, "ka", "beau", [63], qs[5], c=[1, 1], d=0, seed=[KA.index("K"), KA.index("R")])
add("P7_ix1_L2_az_beau_err64", 1, 2, "az", "beau", [64], qs[6])
add("P8_ix1_L4_ka_vig_err22", 1, 4, "ka", "vig", [22], qs[7])
add("P9_ix1_L3_ka_beau_strict", 1, 3, "ka", "beau", [], qs[8])
add("P10_ix1_L5_az_vig_err29", 1, 5, "az", "vig", [29], qs[9])
add("P11_ix1_L1_az_vig_err73", 1, 1, "az", "vig", [73], qs[10])
# negatives (must be missed at the planted q at every L listed in the controls job)
add("N1_ix0_L3_two_errors", 0, 3, "az", "vig", [25, 66], qs[11], kind="neg")
add("N2_ix1_random_key", 1, 5, "az", "vig", [], qs[12], kind="neg", key=[R.randrange(26) for _ in range(97)])
add("N3_ix1_L4_two_errors", 1, 4, "ka", "beau", [24, 70], qs[13], kind="neg")
add("N4_ix0_random_key", 0, 6, "ka", "vig", [], qs[14], kind="neg", key=[R.randrange(26) for _ in range(97)])
json.dump(plants, open(f"{out}/plants.json", "w"), indent=1)
for p in plants: print(p["name"], p["kind"], "q", p["q"], "c", p["c"], "d", p["d"], "seed", p["seed"], "errs", p["errs"])
