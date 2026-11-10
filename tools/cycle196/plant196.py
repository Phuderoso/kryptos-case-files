"""Cycle 196 planted controls (I-212, one-error audit of case 182; = plant194.py with case 182 inputs). Starts from case 182's literal sandwich plants (plant195.py, seed 19500, KEYED COLUMNAR rows of ctl195.bin,
independent string-level encryptor, shares no code with cmp194.c) and injects ONE wrong carved crib letter (+7 in the carved letter's
tableau index) on a slot of the planted config's 2-core (computed here independently by leaf peeling of the planted residue graph):
a wrong letter on a pendant edge is invisible to any crib test (case 180 §4), so such a plant (PD) must fit STRICTLY and is reported as
'undetectable error', not as a miss. P0 = P1 with no error (strict fit). Negatives: N1 three passes, N2 random key, N3 = P1 with two wrong
letters (slots in different series classes, each in the other's remaining 2-core, unequal shifts; I-195), N4 a case-178 compound key.
usage: plant196.py ctl195.bin plants195.txt outfile   (N5 = case 182 K3-route sandwich negative, kept)"""
import sys
import numpy as np
PERM = np.fromfile(sys.argv[1], dtype=np.int16).reshape(-1, 97)
P = {l.split()[0]: l.split() for l in open(sys.argv[2])}
TAB = {"AZ": "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "KA": "KRYPTOSABCDEFGHIJLMNQUVWXZ"}
CI = list(range(21, 34)) + list(range(63, 74))
def edges(row, md, m, n, skip=()):
    S = [int(v) for v in PERM[row]]
    return {t: ((i if md == "1" else S[i]) % m, ("b", (S[i] if md == "1" else i) % n)) for t, i in enumerate(CI) if t not in skip}
def core(E):
    E = dict(E)
    while True:
        deg = {}
        for u, v in E.values(): deg[u] = deg.get(u, 0) + 1; deg[v] = deg.get(v, 0) + 1
        leaf = [t for t, (u, v) in E.items() if deg[u] == 1 or deg[v] == 1]
        if not leaf: return set(E)
        for t in leaf: E.pop(t)
def wrong(ct, row, tab2, slot, shift):
    T = TAB[tab2]; S = [int(v) for v in PERM[row]]; j = S[CI[slot]]; c = list(ct); c[j] = T[(T.index(c[j]) + shift) % 26]; return "".join(c)
out = open(sys.argv[3], "w")
TARGET = {"P1": 5, "P2": 15, "P3": 23, "P4": 4, "P5": 9, "P6": 19, "P7": 12, "P8": 6, "P9": 0}   # requested slots (as cycle 192), moved up to the next 2-core slot
for name in ["P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8", "P9"]:
    _, row, md, exp, ct = P[name]; tab, form, m, n = exp.split("_"); row = int(row); m = int(m); n = int(n)
    K = sorted(core(edges(row, md, m, n)))
    if not K: out.write(f"#{name} no 2-core at its cell: skipped\n"); continue
    s = next((t for t in K if t >= TARGET[name]), K[0])
    out.write(f"{name} {row} {md} {exp} {s} {wrong(ct, row, tab.split('>')[1], s, 7)}\n")
_, row, md, exp, ct = P["P1"]; row = int(row)
out.write(f"P0 {row} {md} {exp} -1 {ct}\n")
K1 = core(edges(row, md, 7, 11)); pend = [t for t in range(24) if t not in K1]
out.write(f"PD {row} {md} {exp} {pend[0]} {wrong(ct, row, 'KA', pend[0], 7)}\n")
# N3: two wrong letters. s1 in core(G); s2 in core(G - s1) and s1 in core(G - s2); also deleting s1 must not leave s2 outside the core
s1 = min(K1)
for s2 in sorted(core(edges(row, md, 7, 11, (s1,)))):
    if s2 != s1 and s1 in core(edges(row, md, 7, 11, (s2,))): break
out.write(f"N3 {row} {md} two_wrong_letters_slots_{s1}_{s2} -2 {wrong(wrong(ct, row, 'KA', s1, 7), row, 'KA', s2, 11)}\n")
for nm in ["N1", "N2", "N4", "N5"]:
    _, row, md, exp, ct = P[nm]; out.write(f"{nm} {row} {md} {exp} -2 {ct}\n")
out.close()
