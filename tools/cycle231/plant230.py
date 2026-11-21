#!/usr/bin/env python3
"""Cycle 230 plants (PREREG230 gate P, seed 209576): 20 plants, bounded-shift keys. Independent textbook encryptor (no import of bsk230).
Ten direct (X, Y from alpha.bin), ten behind a random bank / all.bin row (themed144 X, Y). Key stream i.i.d. over a bounded set:
type 'w' = window of W consecutive shifts at a random offset (W 5-9), type 'd' = D random distinct shifts (D 3-6); the 24 crib seats
are guaranteed to be the full stream (random draws, not forced). English filler from K1-K3 plaintext pieces.
Writes plants230.tsv: id fam row dir X Y form type size ct pt   (usage: plant230.py [seed] > plants230.tsv)"""
import random, struct, sys
seed = int(sys.argv[1]) if len(sys.argv) > 1 else 209576
r = random.Random(seed)
A = open("alpha.bin", "rb").read(); NA = len(A) // 26
T = open("themed144.bin", "rb").read(); NT = len(T) // 26
eng = "".join(c for c in open("k123_eng.txt").read().upper() if c.isalpha())
def filler(n):
    s = r.randrange(0, len(eng) - n); return eng[s:s + n]
def row(fn, q):
    with open(fn, "rb") as f: f.seek(q * 194); return list(struct.unpack("<97h", f.read(194)))
for i in range(20):
    pt = filler(21) + "EASTNORTHEAST" + filler(29) + "BERLINCLOCK" + filler(23); assert len(pt) == 97
    if i < 10: fam, q, d = "direct", -1, 0; S = list(range(97)); xi, yi = r.randrange(NA), r.randrange(NA); src = A
    else:
        fam = r.choice(["bank", "all"]); fn = fam + ".bin"; nr = 165065 if fam == "bank" else 165782
        q = r.randrange(nr); d = r.randrange(2); P = row(fn, q)
        S = P if d == 0 else [P.index(j) for j in range(97)]; xi, yi = r.randrange(NT), r.randrange(NT); src = T
    X = src[xi * 26:xi * 26 + 26]; Y = src[yi * 26:yi * 26 + 26]; xinv = {v: k for k, v in enumerate(X)}
    form = r.randrange(3)
    if i % 2 == 0: typ = "w"; size = r.randint(5, 9); off = r.randrange(26); vals = [(off + t) % 26 for t in range(size)]
    else: typ = "d"; size = r.randint(3, 6); vals = r.sample(range(26), size)
    key = [r.choice(vals) for _ in range(97)]
    layer = []
    for j, ch in enumerate(pt):
        k = key[j]; x = xinv[ord(ch) - 65]
        y = (x + k) % 26 if form == 0 else (x - k) % 26 if form == 1 else (k - x) % 26
        layer.append(chr(Y[y] + 65))
    ct = [None] * 97
    for j in range(97): ct[S[j]] = layer[j]
    print("\t".join(map(str, (f"B{i+1:02d}", fam, q, d, xi, yi, form, typ, size, "".join(ct), pt))))
