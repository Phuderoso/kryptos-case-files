"""Cycle 173 (IDEAS I-105) planted controls, written independently of anom173.c (string alphabets, no index tables).
A periodic key on a (PA, CA) tableau from {A-Z, KRYPTOS}:  c = CA[(PA.index(p) + k) % 26] (vig) or c = CA[(k - PA.index(p)) % 26] (beau),
k = the numeric key letter (A=0), at the plaintext index (ix pt) or at the true-ciphertext index (ix ct), then a K3-law decimation
of the n-letter true ciphertext C', then ONE anomaly on the copper:
  del: C' has 98 letters, letter d is left off;  ins: C' has 96 letters, an extra letter is carved at carved index d;
  chg: C' has 97 letters, the carved letter under one crib is changed;  swp: carved letters d, d+1 swapped.
Each plant is hidden in a 200-perm slice. Plant 'neg' has a dropped letter AND a changed crib letter (strict del must MISS).
Self-check: each plant is decrypted back through the inverse string operations.
usage: plant173.py outdir seed"""
import sys, random, os, numpy as np
out, seed = sys.argv[1], int(sys.argv[2]); os.makedirs(out, exist_ok=True); R = random.Random(seed)
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"; TAB = {"AZ": AZ, "KA": KA}
CR = {**{21 + i: c for i, c in enumerate("EASTNORTHEAST")}, **{63 + i: c for i, c in enumerate("BERLINCLOCK")}}
BASE = ("ACOLDWINDCAMEOVERTHEW" + "EASTNORTHEAST" + "RIDGEANDTHESURVEYORSFOUNDTHEX" + "BERLINCLOCK" + "STILLRUNNINGBENEATHSNOWX")
def ptext(n):
    s = BASE[:n]; assert len(s) == n and all(s[j] == c for j, c in CR.items()); return s
FAM = {98: "support/dec98.bin", 96: "support/dec96.bin", 97: "support/all.bin"}
KEYS = {5: "LUCID", 7: "COMPASS", 8: "LODESTAR", 11: "UNDERGROUND", 12: "ILLUMINATION", 13: "MAGNETICFIELD", 14: "QUARTZLANTERNS", 19: "THEHIDDENSHADOWLINE"}
#        model  ix   mode   PA   CA   p
plan = [("del", "pt", "vig", "KA", "KA", 7), ("del", "ct", "beau", "AZ", "KA", 11), ("del", "pt", "vig", "AZ", "AZ", 19),
        ("ins", "ct", "vig", "KA", "AZ", 8), ("ins", "pt", "beau", "KA", "KA", 13), ("ins", "ct", "vig", "AZ", "AZ", 19),
        ("chg", "pt", "vig", "KA", "KA", 12), ("chg", "ct", "beau", "AZ", "KA", 5),
        ("swp", "ct", "vig", "KA", "KA", 14), ("swp", "pt", "beau", "KA", "AZ", 8),
        ("neg", "pt", "vig", "KA", "KA", 7)]
def sub(t, key, PA, CA, beau, idx):
    return "".join(CA[((AZ.index(key[idx[i] % len(key)]) - PA.index(c)) if beau else (PA.index(c) + AZ.index(key[idx[i] % len(key)]))) % 26] for i, c in enumerate(t))
def unsub(t, key, PA, CA, beau, idx):
    return "".join(PA[((AZ.index(key[idx[i] % len(key)]) - CA.index(c)) if beau else (CA.index(c) - AZ.index(key[idx[i] % len(key)]))) % 26] for i, c in enumerate(t))
rows = []
for nn, (model, ix, mode, pa, ca, p) in enumerate(plan):
    n = 98 if model in ("del", "neg") else 96 if model == "ins" else 97
    PERM = np.fromfile(FAM[n], dtype=np.int16).reshape(-1, n)
    q = R.randrange(100, len(PERM) - 100); perm = [int(x) for x in PERM[q]]
    P = ptext(n); key = KEYS[p]; PA, CA = TAB[pa], TAB[ca]; beau = mode == "beau"
    if ix == "pt":   # substitute at plaintext index, then C'[perm[j]] = s[j]
        s = sub(P, key, PA, CA, beau, list(range(n))); C = [None] * n
        for j in range(n): C[perm[j]] = s[j]
    else:            # transpose, then substitute at C' index
        T = [None] * n
        for j in range(n): T[perm[j]] = P[j]
        C = list(sub("".join(T), key, PA, CA, beau, list(range(n))))
    C = "".join(C)
    # self-check (inverse operations on C')
    if ix == "pt": back = unsub("".join(C[perm[j]] for j in range(n)), key, PA, CA, beau, list(range(n)))
    else: t2 = unsub(C, key, PA, CA, beau, list(range(n))); back = "".join(t2[perm[j]] for j in range(n))
    assert back == P, nn
    # the anomaly on the copper
    if model in ("del", "neg"):
        d = R.choice([x for x in range(98) if x not in [perm[j] for j in CR]] if model == "neg" else range(98))
        carved = C[:d] + C[d + 1:]
        if model == "neg":   # also change the carved letter under crib plaintext index 26
            u = perm[26]; cpos = u if u < d else u - 1
            carved = carved[:cpos] + chr((ord(carved[cpos]) - 65 + 7) % 26 + 65) + carved[cpos + 1:]
    elif model == "ins":
        d = R.randrange(97); carved = C[:d] + R.choice(AZ) + C[d:]
    elif model == "chg":
        d = R.randrange(24); j = sorted(CR)[d]; u = perm[j]
        carved = C[:u] + chr((ord(C[u]) - 65 + 1 + R.randrange(25)) % 26 + 65) + C[u + 1:]
    else:
        d = R.randrange(96); carved = C[:d] + C[d + 1] + C[d] + C[d + 2:]
    assert len(carved) == 97
    PERM[q - 100:q + 100].tofile(f"{out}/ctl{nn}_slice.bin")
    open(f"{out}/ctl{nn}.txt", "w").write(carved + "\n")
    rows.append(f"ctl{nn} model={model} n={n} q={q} slot=100 d={d} PA={pa} CA={ca} mode={mode} idx={ix} p={p} key={key}" + (" (expect MISS under strict del)" if model == "neg" else ""))
open(f"{out}/plants.txt", "w").write("\n".join(rows) + "\n"); print("\n".join(rows))
