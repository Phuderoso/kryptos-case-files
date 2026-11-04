"""Cycle 11 controls for tools/c/digitwin.c: plant a base-10 digit key (digits of pi, i.e. NOT Gromark-generated)
with PA = keyed(LANTERN), CA = keyed(SHADOW+BERLIN) (a two-word keyphrase), rotation s=7; vig and beau versions.
Prints the two control ciphertexts."""
import sys
sys.path.insert(0, "tools")
from gromark_alphabet import keyed
from k4_anneal import KN
eng = "WEMETATTHECORNERWHERETHEROADTURNSEASTNORTHEASTANDTHEOLDSTATIONSTOODWAITINGFORTHEBERLINCLOCKTOSTRIKE"[:97]
pt = list(eng)
for i, ch in KN.items(): pt[i] = ch
PI = "31415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679"
PA, CA, s = keyed("LANTERN"), keyed("SHADOWBERLIN"), 7
vig = "".join(CA[(PA.index(p) + s + int(PI[i])) % 26] for i, p in enumerate(pt))
beau = "".join(CA[(s + int(PI[i]) - PA.index(p)) % 26] for i, p in enumerate(pt))
print(vig); print(beau)
# third control: a true Gromark key (primer 27182, base 10, L=5) for the lagged-Fibonacci follow-up
from gromark_alphabet import keys
prim, K = keys(); kk = K[27182]
print("".join(CA[(PA.index(p) + s + int(kk[i])) % 26] for i, p in enumerate(pt)))
