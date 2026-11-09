"""Cycle 190 planted controls for the one-error audit (I-191). Base texts come from the cycle-189 literal two-pass encryptor
(tools/cycle189/plant189.py, seed 18900; shares no code with cmp190.c). Errors are injected here at a crib slot t: the carved letter at
S[CI[t]] is moved by +d in A-Z order (any change of that letter changes the crib key value K_t for every alphabet and form).
usage: plant190.py planted189.txt perms.bin outfile -> lines: name q alab model per slots ct"""
import sys
import numpy as np
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; CI = list(range(21, 34)) + list(range(63, 74))
B = {l.split()[0]: l.split() for l in open(sys.argv[1])}; P = np.fromfile(sys.argv[2], dtype=np.int16).reshape(-1, 97)
def inj(name, slots, d=7):
    nm, q, alab, model, per, ct = B[name]; q = int(q); S = list(range(97)) if q < 0 else [int(v) for v in P[q]]; ct = list(ct)
    for k, t in enumerate(slots): j = S[CI[t]]; ct[j] = AZ[(AZ.index(ct[j]) + (d if k == 0 else 11)) % 26]   # 2nd error +11 (equal shifts on two
    # edges in series cancel on every cycle, which would make a two-error text look clean; found in the rehearsal, fixed before K4).
    # D1 first used slots 5 and 20, which lie in ONE series class {4,5,6,19,20,21} at q 12345 (7 x 11): deleting one class member removes
    # every cycle through both errors, so that text is a one-error text by construction; moved to slots 5 and 10 (different classes).
    return q, alab, model, per, "".join(ct)
spec = [("E1", "P1", [5]), ("E2", "P2", [17]), ("E3", "P5", [0]), ("E4", "P6", [23]), ("E5", "P4", [12]), ("E6", "P7", [9]),
        ("S1", "P3", []), ("D1", "P1", [5, 10]), ("D2", "P6", [2, 15]), ("N1", "N1", []), ("N2", "N2", [])]
with open(sys.argv[3], "w") as o:
    for name, base, slots in spec:
        q, alab, model, per, ct = inj(base, slots)
        o.write(f"{name} {q} {alab} {model} {per} {','.join(map(str, slots)) or '-'} {ct}\n")
