"""Cycle 192 planted controls for the one-error audit (independent string-level encryptor, copied from plant191.py; shares no code with
cmp192.c). Positives = case 178's plants with ONE wrong carved crib letter each (slot and shift fixed here, unequal shifts in the carved
letter's tableau), plus P0 = P1 with no error (must fit strictly, slot -1). Negatives: N1 three passes, N2 random key, N3 = P1 with TWO
wrong letters (slots 2 and 17), N4 = P4 with two wrong letters (slots 0 and 23).
usage: plant192.py ctl191.bin outfile   (rows: 0 identity, 1-5 = all.bin rows 12345, 100000, 18944, 165781, 51712)"""
import sys, random
import numpy as np
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"
TAB = {"AZ": AZ, "KA": KA}
PTX = "THEIRONDOORFACEDDUEXX" + "EASTNORTHEAST" + "OFTHEFOUNTAINWHERETHEOLDWORLD" + "BERLINCLOCK" + "STRUCKTHEHOURATMIDNIGHT"
assert len(PTX) == 97 and PTX[21:34] == "EASTNORTHEAST" and PTX[63:74] == "BERLINCLOCK"
CIDX = list(range(21, 34)) + list(range(63, 74))
R = random.Random(19200)
PERM = np.fromfile(sys.argv[1], dtype=np.int16).reshape(-1, 97)
def step(x, k, form): return (x + k) % 26 if form == "vig" else (k - x) % 26 if form == "beau" else (x - k) % 26
def enc(row, model, passes):
    S = [int(v) for v in PERM[row]]; C = ["?"] * 97
    for i in range(97):
        j = S[i]; ch = PTX[i]; pos = i if model == "P" else j
        for tab, key, form in passes:
            T = TAB[tab]; ch = T[step(T.index(ch), key[pos % len(key)], form)]
        C[j] = ch
    assert "?" not in C; return "".join(C)
def corrupt(ct, row, slots_shifts, tab):
    ct = list(ct); T = TAB[tab]
    for slot, sh in slots_shifts:
        j = int(PERM[row][CIDX[slot]]); ct[j] = T[(T.index(ct[j]) + sh) % 26]
    return "".join(ct)
def core(edges, drop):
    """2-core edge set (slot ids) of the residue graph without the slots in drop (pendant trees removed)"""
    E = {t: e for t, e in enumerate(edges) if t not in drop}
    while True:
        deg = {}
        for u, v in E.values(): deg[u] = deg.get(u, 0) + 1; deg[v] = deg.get(v, 0) + 1
        rm = [t for t, (u, v) in E.items() if deg[u] == 1 or deg[v] == 1]
        if not rm: return set(E)
        for t in rm: del E[t]
def resid(row, model, m, n):
    S = [int(v) for v in PERM[row]]
    return [((i if model == "P" else S[i]) % m, m + (i if model == "P" else S[i]) % n) for i in CIDX]
def rk(n): return [R.randrange(26) for _ in range(n)]
def kw(w, tab): return [TAB[tab].index(c) for c in w]
plants = [  # name, row, model, passes, expected cell, wrong (slot, shift) list, last tableau
 ("P0", 1, "P", [("AZ", rk(7), "vig"), ("KA", rk(11), "vig")], "AZ>KA VV 7 11", []),
 ("P1", 1, "P", [("AZ", rk(7), "vig"), ("KA", rk(11), "vig")], "AZ>KA VV 7 11", [(2, 7)]),
 ("P2", 2, "C", [("KA", rk(5), "beau"), ("AZ", rk(13), "vig")], "KA>AZ BV 5 13", [(15, 3)]),
 ("P3", 3, "C", [("AZ", rk(8), "variant"), ("KA", rk(12), "beau")], "AZ>KA VB 8 12", [(23, 11)]),
 ("P4", 4, "P", [("KA", rk(6), "vig"), ("AZ", rk(19), "beau")], "KA>AZ VB 6 19", [(0, 5)]),
 ("P5", 0, "P", [("AZ", kw("PALIMPSEST", "AZ"), "vig"), ("KA", kw("ABSCISSA", "KA"), "vig")], "AZ>KA VV 10 8", [(9, 13)]),
 ("P6", 0, "C", [("KA", kw("KRYPTOS", "KA"), "beau"), ("AZ", kw("BERLINCLOCK", "AZ"), "vig")], "KA>AZ BV 7 11", [(19, 1)]),
 ("P7", 5, "C", [("AZ", rk(3), "variant"), ("AZ", rk(25), "vig")], "AZ>AZ VV 3 25", [(12, 9)]),
 ("P8", 1, "P", [("KA", rk(4), "beau"), ("KA", rk(9), "beau")], "KA>KA BB 4 9", [(6, 20)]),
 ("N1", 1, "P", [("AZ", rk(5), "vig"), ("KA", rk(7), "vig"), ("AZ", rk(11), "vig")], "three passes", []),
 ("N2", 2, "C", [("KA", rk(97), "beau")], "random key", []),
]
# rehearsal fix (before registration): a wrong slot must lie in the 2-core of the planted graph (else the error is invisible); the
# requested slot is kept if so, otherwise the next slot (cyclically) in the core is used. Two-error negatives: the second slot must lie in
# the core of the graph without the first, and vice versa (different series classes, I-195).
out = open(sys.argv[2], "w"); CT = {}
for idx, (name, row, model, passes, exp, wrong) in enumerate(plants):
    if wrong:
        m, n = int(exp.split()[2]), int(exp.split()[3]); c = core(resid(row, model, m, n), set())
        sl = wrong[0][0]
        while sl not in c: sl = (sl + 1) % 24
        wrong = [(sl, wrong[0][1])]; plants[idx] = (name, row, model, passes, exp, wrong)
    ct = enc(row, model, passes); CT[name] = (ct, row, passes)
    if wrong: ct = corrupt(ct, row, wrong, passes[-1][0])
    sl = ",".join(str(s) for s, _ in wrong) or "-1"
    out.write(f"{name} {row} {model} {exp.replace(' ', '_')} {sl} {ct}\n")
def second(row, model, m, n, first, want):
    ed = resid(row, model, m, n); c1 = core(ed, {first}); s2 = want
    while not (s2 != first and s2 in c1 and first in core(ed, {s2})): s2 = (s2 + 1) % 24
    return s2
for nm, src, mn, tab, w1, w2 in (("N3", "P1", (7, 11), "KA", (2, 7), (17, 11)), ("N4", "P4", (6, 19), "AZ", (0, 5), (23, 3))):
    ct, row, passes = CT[src]; md = "P"; c = core(resid(row, md, *mn), set()); f1 = w1[0]
    while f1 not in c: f1 = (f1 + 1) % 24
    f2 = second(row, md, *mn, f1, w2[0])
    out.write(f"{nm} {row} {md} two_wrong_letters_{src} {f1},{f2} {corrupt(ct, row, [(f1, w1[1]), (f2, w2[1])], tab)}\n")
out.close()
