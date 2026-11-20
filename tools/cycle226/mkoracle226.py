"""Cycle 226 (PREREG226): 16 English oracle texts (97 letters, cribs inserted at 21-33 / 63-73), seed 209546.
0-7: windows of K1-K3 plaintext (k123_eng.txt); 8-15: windows of Jane Eyre (Gutenberg #1260, body only, letters A-Z).
usage: mkoracle226.py WORKDIR  -> WORKDIR/oracle226.txt"""
import sys, random
W = sys.argv[1]; R = random.Random(209546); N = 97
POS = list(range(21, 34)) + list(range(63, 74)); CRIB = "EASTNORTHEAST" + "BERLINCLOCK"
k = "".join(c for c in open(W + "/k123_eng.txt").read().upper() if c.isalpha())
je = open(W + "/rk_plain.txt", errors="ignore").read()
je = je[je.index("CHAPTER I"):je.index("END OF THE PROJECT GUTENBERG")]
je = "".join(c for c in je.upper() if "A" <= c <= "Z")
out = []
for src in (k,) * 8 + (je,) * 8:
    s0 = R.randrange(len(src) - N); t = list(src[s0:s0 + N])
    for j, i in enumerate(POS): t[i] = CRIB[j]
    out.append("".join(t))
open(W + "/oracle226.txt", "w").write("\n".join(out) + "\n")
print(len(k), len(je)); print("\n".join(out))
