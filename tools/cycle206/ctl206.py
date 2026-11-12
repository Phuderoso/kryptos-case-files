#!/usr/bin/env python3
"""Cycle 206 controls C1 / C1b (PREREG206 Part A): planted R1 word-restart text behind a bank permutation.
Invented example plaintext (not a K4 guess), cribs at plaintext positions 22-34 / 64-74 (1-indexed)."""
import subprocess, sys, struct
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"
BIN = sys.argv[1]; BANK = sys.argv[2]
W = ["AND", "THE", "GREY", "LIGHT", "TURNED", "EAST", "NORTHEAST", "OVER", "THE", "WALL", "AND", "A", "MAN", "STOOD",
     "BY", "THAT", "BERLIN", "CLOCK", "WAITING", "FOR", "THE", "SIGNAL", "AT", "MIDNIGHT", "IN", "THE", "SQUARE", "NEAR", "HIM"]
def plain():
    s = "".join(W); assert s[21:34] == "EASTNORTHEAST" and s[63:74] == "BERLINCLOCK", (s.find("EASTNORTHEAST"), s.find("BERLINCLOCK"))
    return s
def enc(alph, mode, key):
    out = []
    for w in W:
        for j, p in enumerate(w):
            k = alph.index(key[j % len(key)]); pi = alph.index(p)
            out.append(alph[(pi + k) % 26] if mode == "vig" else alph[(k - pi) % 26])
    return "".join(out)
def perm(q):
    with open(BANK, "rb") as f:
        f.seek(q * 97 * 2); return list(struct.unpack("<97h", f.read(194)))
def carve(layer, q, d):
    s = perm(q)
    S = s if d == 0 else [0] * 97
    if d == 1:
        for i in range(97): S[s[i]] = i
    C = [None] * 97
    for i in range(97): C[S[i]] = layer[i]
    return "".join(C)
P = plain()
print("plaintext", len(P), P)
# pad/trim to 97 with invented tail
for name, alph, mode, key, q, d, tm in (("C1", KA, "vig", "ABSCISSA", 12345, 0, 2), ("C1b", AZ, "beau", "PALIMPSEST", 98765, 1, 1)):
    lay = enc(alph, mode, key)[:97]
    assert len(lay) == 97, len(lay)
    ct = carve(lay, q, d)
    L = len(key)
    out = subprocess.run([BIN, ct, BANK, str(L), str(L), "50"], capture_output=True, text=True).stdout
    S = [l for l in out.splitlines() if l.startswith("S ")]
    hit = [l for l in S if f"perm={q} dir={d} tm={tm} L={L} " in l]
    def kmatch(l):
        k = l.split("key=")[1].strip()
        return len(k) == len(key) and all(a == b or a == "?" for a, b in zip(k, key))   # '?' = index no crib letter reaches
    keyok = any(kmatch(l) for l in hit)
    print(name, "survivors at L", L, ":", len(S), "| true cell found:", bool(hit), "| key recovered:", keyok)
    for l in S[:6]: print("  ", l)
    print("PASS" if hit and keyok else "FAIL", name)
