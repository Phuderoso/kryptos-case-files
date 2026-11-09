"""Cycle 189 per-offset alignment controls for the I-184 add-on (answers the Voynich C096 offer): a case-174 direction-r plant
(Quagmire IV, A vocabulary x B themed, affine linear-recurrence key on the CARVED index, string-level encryptor copied from plant187)
placed at a global row q = 8k + r of all.bin; lrk186 run on the class file all_r{r}s8.bin must report it at LOCAL index k, and the same
text run on the other class file must not (misalignment negative).
usage: i184plant189.py all.bin alpha172.txt alpha_themed180.txt -> lines: name q r k ct"""
import sys, random
import numpy as np
P = np.fromfile(sys.argv[1], dtype=np.int16).reshape(-1, 97)
V = dict(reversed(l.split()) for l in open(sys.argv[2])); TH = dict(reversed(l.split()) for l in open(sys.argv[3]))
PTX = "THEIRONDOORFACEDDUEXX" + "EASTNORTHEAST" + "OFTHEFOUNTAINWHERETHEOLDWORLD" + "BERLINCLOCK" + "STRUCKTHEHOURATMIDNIGHT"
R = random.Random(18950)
def keystream(c, d, seed):
    k = list(seed)
    while len(k) < 97: k.append((sum(c[j] * k[-1 - j] for j in range(len(c))) + d) % 26)
    return k
def build(k, A, B, form, q):
    S = P[q]; C = ["?"] * 97
    for i in range(97):
        x = A.index(PTX[i]); C[S[i]] = B[(x + k[S[i]]) % 26] if form == "vig" else B[(k[S[i]] - x) % 26]
    return "".join(C)
for name, r, k, alab, blab, form, L in (("A6", 6, 1000, "MEDITERRANEAN/Z", "ABSCISSA/Z", "vig", 2), ("A7", 7, 15000, "OBLIQUE/Z", "KA", "beau", 3)):
    assert alab in V and blab in TH
    q = 8 * k + r; key = keystream([R.randrange(26) for _ in range(L)], R.randrange(26), [R.randrange(26) for _ in range(L)])
    print(name, q, r, k, alab, blab, form, L, build(key, V[alab], TH[blab], form, q))
