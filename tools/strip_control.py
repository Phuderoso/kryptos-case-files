"""Cycle 13 planted control for strip transpositions: English PT with cribs at the official positions,
Quagmire III on the KRYPTOS alphabet with key CLOCK (index = PT position), then cut into strips of 11
(last strip 9 letters) and taped back in the order below. Writes the control CT to stdout."""
import sys; sys.path.insert(0, "tools")
from kryptos_text import KA
pt = ("SLOWLYTHEREMAINSOFPASSAGEDEBRISEASTNORTHEASTWEREREMOVEDWITHTREMBLINGHANDSANDIMADEATINYBERLINCLOCK"
      "BREACHINTHEUPPERLEFTHANDCORNER")
pt = list(pt[:97]); pt[21:34] = "EASTNORTHEAST"; pt[63:74] = "BERLINCLOCK"; pt = "".join(pt)
key = "CLOCK"
mid = "".join(KA[(KA.index(c) + KA.index(key[i % 5])) % 26] for i, c in enumerate(pt))
w = 11; strips = [mid[i:i + w] for i in range(0, 97, w)]
order = [4, 8, 1, 6, 0, 3, 7, 2, 5]          # carved = strips[order[0]] + strips[order[1]] + ...
print("".join(strips[r] for r in order))

# Second control (digit-window test): keyed SHADOW alphabet on both sides, digits of the K2 coordinates as key
# (base 10), then strips of 13 (last strip 6 letters) taped back in the order below.
def keyed(w): return "".join(dict.fromkeys(w + "ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
al = keyed("SHADOW"); dig = [3, 8, 5, 7, 6, 5, 7, 7, 8, 4, 4]
mid2 = "".join(al[(al.index(p) + 11 + dig[i % 11]) % 26] for i, p in enumerate(pt))
s2 = [mid2[i:i + 13] for i in range(0, 97, 13)]
print("".join(s2[r] for r in [3, 7, 0, 5, 1, 6, 2, 4]))
