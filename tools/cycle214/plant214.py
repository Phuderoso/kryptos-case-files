#!/usr/bin/env python3
"""Cycle 214 plants (PREREG214 part A gate, seed 209225): 10 direct (X, Y from alpha.bin) + 10 behind a random bank/all.bin row
(themed X, Y). Gromark key, primer L 2-10, index ix 0 (plaintext position) or 1 (carved position S[i]). English filler from K1-K3
plaintext pieces. Writes plants214.tsv: id fam row dir X Y form L ix ct pt"""
import random, struct, sys
sys.path.insert(0, ".")
r = random.Random(209225)
A = open("alpha.bin", "rb").read(); NA = len(A) // 26
T = open("themed144.bin", "rb").read(); NT = len(T) // 26
eng = "".join(c for c in open("k123_eng.txt").read().upper() if c.isalpha())
def filler(n):
    s = r.randrange(0, len(eng) - n); return eng[s:s + n]
def row(fn, q):
    with open(fn, "rb") as f: f.seek(q * 194); return list(struct.unpack("<97h", f.read(194)))
out = []
for i in range(20):
    pt = filler(21) + "EASTNORTHEAST" + filler(29) + "BERLINCLOCK" + filler(23); assert len(pt) == 97
    if i < 10: fam, q, d = "direct", -1, 0; S = list(range(97)); xi, yi = r.randrange(NA), r.randrange(NA); src = A
    else:
        fam = r.choice(["bank", "all"]); fn = fam + ".bin"; nr = 165065 if fam == "bank" else 165782
        q = r.randrange(nr); d = r.randrange(2); P = row(fn, q)
        S = P if d == 0 else [P.index(i) for i in range(97)]; xi, yi = r.randrange(NT), r.randrange(NT); src = T
    X = src[xi * 26:xi * 26 + 26]; Y = src[yi * 26:yi * 26 + 26]; xinv = {v: k for k, v in enumerate(X)}
    form = r.randrange(3); L = r.randrange(2, 11); ix = r.randrange(2)
    key = [r.randrange(10) for _ in range(L)]
    while len(key) < 97: key.append((key[-L] + key[-L + 1]) % 10)
    layer = []
    for j, ch in enumerate(pt):
        k = key[j if ix == 0 else S[j]]; x = xinv[ord(ch) - 65]
        y = (x + k) % 26 if form == 0 else (x - k) % 26 if form == 1 else (k - x) % 26
        layer.append(chr(Y[y] + 65))
    ct = [None] * 97
    for j in range(97): ct[S[j]] = layer[j]
    out.append((f"A{i+1:02d}", fam, q, d, xi, yi, form, L, ix, "".join(ct), pt))
with open("plants214.tsv", "w") as f:
    for t in out: f.write("\t".join(map(str, t)) + "\n")
print(len(out), "plants")
