"""Cycle 172 (IDEAS I-095) planted controls, written independently of q4d172.c (string alphabets, no tables):
textbook Quagmire IV  c = CA[PA.index(p) + CA.index(k)] (Vigenere) or c = CA[CA.index(k) - PA.index(p)] (Beaufort),
PA != CA taken from support/alpha172.txt, keyword key of period L, placed behind a random entry of all.bin:
  ix 0: substitute at the plaintext index, then carved[perm[j]] = s[j]
  ix 1: transpose first (T[perm[j]] = P[j]), then substitute at the carved index.
Each plant is hidden in a 200-perm slice around its perm. Plant 8 has one carved letter under a crib altered
(strict test must MISS it at its slot). Self-check: every plant is decrypted back by the inverse string operations.
usage: plant172.py outdir seed"""
import sys, random, numpy as np, os
out, seed = sys.argv[1], int(sys.argv[2]); os.makedirs(out, exist_ok=True); R = random.Random(seed)
P = ("ACOLDWINDCAMEOVERTHEW" + "EASTNORTHEAST" + "RIDGEANDTHESURVEYORSFOUNDTHEX" + "BERLINCLOCK" + "STILLRUNNINGBENEATHSNOW")
assert len(P) == 97 and P[21:34] == "EASTNORTHEAST" and P[63:74] == "BERLINCLOCK"
AL = [l.split() for l in open("support/alpha172.txt")]
PERM = np.fromfile("support/all.bin", dtype=np.int16).reshape(-1, 97)
KEYS = ["LUCID", "SHADOW", "COMPASS", "LODESTAR", "MERIDIANS", "UNDERGROUND", "ILLUMINATION", "MAGNETICFIELD", "QUARTZLANTERNS"]
plan = [(0,"vig",5),(1,"beau",6),(0,"beau",7),(1,"vig",8),(0,"vig",11),(1,"beau",12),(0,"vig",13),(1,"vig",14),(1,"vig",7)]
def enc(t, key, PA, CA, beau):
    return "".join(CA[(CA.index(key[i % len(key)]) - PA.index(c)) % 26] if beau else CA[(PA.index(c) + CA.index(key[i % len(key)])) % 26] for i, c in enumerate(t))
def dec(t, key, PA, CA, beau):
    return "".join(PA[(CA.index(key[i % len(key)]) - CA.index(c)) % 26] if beau else PA[(CA.index(c) - CA.index(key[i % len(key)])) % 26] for i, c in enumerate(t))
rows = []
for n, (ix, mode, L) in enumerate(plan):
    key = [k for k in KEYS if len(k) == L][0] if any(len(k) == L for k in KEYS) else KEYS[0]
    a, b = R.sample(range(len(AL)), 2); PA, la = AL[a]; CA, lb = AL[b]
    q = R.randrange(100, len(PERM) - 100); perm = [int(x) for x in PERM[q]]; beau = mode == "beau"
    if ix == 0:
        s = enc(P, key, PA, CA, beau); c = [None] * 97
        for j in range(97): c[perm[j]] = s[j]
    else:
        T = [None] * 97
        for j in range(97): T[perm[j]] = P[j]
        c = list(enc("".join(T), key, PA, CA, beau))
    c = "".join(c)
    # self-check by inverse operations
    if ix == 0: back = dec("".join(c[perm[j]] for j in range(97)), key, PA, CA, beau)
    else: t2 = dec(c, key, PA, CA, beau); back = "".join(t2[perm[j]] for j in range(97))
    assert back == P, n
    if n == 8:  # one carved letter under crib 5 (plaintext index 26) altered
        pos = perm[26]; c = c[:pos] + chr((ord(c[pos]) - 65 + 7) % 26 + 65) + c[pos + 1:]
    PERM[q - 100:q + 100].tofile(f"{out}/ctl{n}_slice.bin")
    open(f"{out}/ctl{n}.txt", "w").write(c + "\n")
    rows.append(f"ctl{n} q={q} slot=100 ix={ix} mode={mode} p={len(key)} key={key} PA={la} CA={lb} {'ALTERED carved pos %d (expect MISS)' % perm[26] if n == 8 else ''}")
open(f"{out}/plants.txt", "w").write("\n".join(rows) + "\n"); print("\n".join(rows))
