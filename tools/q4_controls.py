"""Cycle 28 controls: plant Quagmire IV texts behind family transpositions and shuffled-K4 nulls.
Writes ct strings to q4_cases.txt as name ct."""
import random, numpy as np
from kryptos_text import K4
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
names = open("q4_alpha_names.txt").read().split("\n")
A = np.fromfile("q4_alpha.bin", dtype=np.uint8).reshape(-1, 26)
P = np.fromfile("perms97.bin", dtype=np.int16).reshape(-1, 97)
PT = ("THESHADOWCROSSEDTHEYAR" [:21] + "EASTNORTHEAST" + "OFTHEPOOLWHEREITURNEDTOSEETHE"[:29]
      + "BERLINCLOCK" + "ANDTHENIGHTWASVERYSTILL"[:23])
PT = PT[:97]; assert PT[21:34] == "EASTNORTHEAST" and PT[63:74] == "BERLINCLOCK", (PT[21:34], PT[63:74])
def alpha(n): return "".join(chr(65 + x) for x in A[names.index(n)])
def enc(pa, ca, key, mode, ix, t):
    perm = P[t]; out = [""] * 97
    for j, ch in enumerate(PT):
        k = AZ.index(key[(perm[j] if ix == "carved" else j) % len(key)])
        pv = pa.index(ch)
        out[perm[j]] = ca[(pv + k) % 26] if mode == "vig" else ca[(k - pv) % 26]
    return "".join(out)
cases = [("control1_PALIMPSEST_SHADOW_vig_pt_CLOCK_t5000", enc(alpha("PALIMPSEST"), alpha("SHADOW"), "CLOCK", "vig", "pt", 5000)),
         ("control2_BERLIN_rev_KRYPTOS_beau_carved_LAYERTWO_t120000", enc(alpha("BERLIN_rev"), alpha("KRYPTOS"), "LAYERTWO", "beau", "carved", 120000)),
         ("control3_LUCID_ABSCISSA_vig_carved_IQLUSION_t0identity", enc(alpha("LUCID"), alpha("ABSCISSA"), "IQLUSION", "vig", "carved", 0))]
for s in (1, 2, 3):
    l = list(K4); random.Random(s).shuffle(l); cases.append((f"null{s}", "".join(l)))
cases.insert(0, ("K4", K4))
open("q4_cases.txt", "w").write("\n".join(f"{n} {c}" for n, c in cases) + "\n")
print(open("q4_cases.txt").read())
