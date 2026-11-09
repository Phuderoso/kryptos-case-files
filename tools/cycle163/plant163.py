"""Cycle 163 (IDEAS I-069) planted controls: split period-7 Quagmire III key (cycle-162 textbook encryptor, plant162.enc)
behind bank permutations with ONE corrupted carved letter under a crib, plus a two-error decoy.
Output: label CT corrupted-carved-position(s) (one per line)."""
import sys
import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cycle162"))
from plant162 import enc, move, perm, alpha, P
CI = list(range(21, 34)) + list(range(63, 74))
def corrupt(ct, positions):
    c = list(ct)
    for p in positions: c[p] = "A" if c[p] != "A" else "B"
    return "".join(c)
A3, KA, AZ = alpha(3000), alpha(1), alpha(0)
# ctl6: carved index, perm 77777 dir 1, alphabet 3000, Vig QUARTZS | Vig LODESTO, b 55; carved letter under crib 5 altered
s6 = perm(77777, 1); c6 = enc(move(P, s6), A3, "QUARTZS", 0, A3, "LODESTO", 0, 55); e6 = [int(s6[CI[5]])]
# ctl7: model Q, perm 31337 dir 0, KRYPTOS Beau SHADOWF | Vig ORCESAX, b 70 (inside BERLINCLOCK); the letter carrying
#       crib 0 (position 21, the reference member of its residue class) altered
s7 = perm(31337, 0); c7 = move(enc(P, KA, "SHADOWF", 1, KA, "ORCESAX", 0, 70), s7); e7 = [int(s7[CI[0]])]
# ctl8: Z cross, carved index, perm 5000 dir 0, AZ Vig MAGNETI | KA Beau CLUELES, b 35; carved letter under crib 20 altered
s8 = perm(5000, 0); c8 = enc(move(P, s8), AZ, "MAGNETI", 0, KA, "CLUELES", 1, 35); e8 = [int(s8[CI[20]])]
# ctl9: decoy = ctl6 with TWO letters altered (cribs 5 and 17): must NOT be recovered in one-error mode
e9 = [int(s6[CI[5]]), int(s6[CI[17]])]
for lab, c, e in (("ctl6", c6, e6), ("ctl7", c7, e7), ("ctl8", c8, e8), ("ctl9", c6, e9)):
    print(lab, corrupt(c, e), ",".join(map(str, e)))
