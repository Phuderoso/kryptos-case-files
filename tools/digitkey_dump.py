"""Cycle 11: dump candidate alphabets for the generator-agnostic small-digit-key test (tools/c/digitwin.c).
Alphabets: cycle-10 set (AZ, KA, ZA, keyed / reversed-keyed / ACA-columnar of every 3-14 letter word in the
Gutenberg vocabulary + plain-sight words) PLUS multi-word keyphrases: every ordered pair of the 89 plain-sight
words (keyed, reversed keyed, ACA columnar).  Writes data/alpha.bin (26 bytes each, A=0) and data/alpha.txt (names).
Optional: control -> also writes data/ct_control.txt (a planted digit-key ciphertext)."""
import sys
sys.path.insert(0, "tools")
from gromark_keyword import vocab, alphabets
from gromark_alphabet import keyed, aca_columnar
from k4_layers import WORDS
A = alphabets(vocab())
seen = set(A.values())
for w1 in WORDS:
    for w2 in WORDS:
        if w1 == w2: continue
        ph = w1 + w2
        for tag, a in (("k2:", keyed(ph)), ("r2:", keyed(ph)[::-1]), ("c2:", aca_columnar(ph))):
            if a not in seen: seen.add(a); A[tag + w1 + "+" + w2] = a
names = list(A)
with open("data/alpha.bin", "wb") as f:
    for n in names: f.write(bytes(ord(c) - 65 for c in A[n]))
open("data/alpha.txt", "w").write("\n".join(names) + "\n")
print("alphabets", len(names))
