"""Cycle 11 (3): SMT (z3) satisfiability of structured cipher families under the 24 cribs, with BOTH alphabets unknown.
Unknowns: plain alphabet PA and cipher alphabet CA (two independent permutations of 26 letters), key stream k_i.
Encryption: CA_pos(c_i) = PA_pos(p_i) + k_i (mod 26)   [Vigenere family on mixed alphabets; Beaufort = relabelling]
Families: F1 periodic key period P (Quagmire IV); F2 Gromark base b primer L (key in 0..b-1, lagged Fibonacci);
F3 progressive k_i = a + s*i; F4 plaintext autokey k_i = PA_pos(p_{i-L}) (unknown p outside cribs -> free, so only
crib-internal links constrain); F5 ciphertext autokey k_i = CA_pos(c_{i-L}).
SAT means "not excluded by cribs alone"; UNSAT is a proof of impossibility for that family.
Run: python3 tools/k4_smt.py [control]"""
import sys, time
from z3 import Int, Solver, Distinct, And, Or, sat, IntVal
sys.path.insert(0, "tools")
from kryptos_text import K4
from k4_anneal import AZ, KN
N = 97; CR = sorted(KN.items())
def base(s):
    pa = {c: Int("pa_" + c) for c in AZ}; ca = {c: Int("ca_" + c) for c in AZ}
    for v in list(pa.values()) + list(ca.values()): s.add(v >= 0, v < 26)
    s.add(Distinct(*pa.values())); s.add(Distinct(*ca.values())); s.add(pa["A"] == 0)  # fix rotation symmetry
    return pa, ca
def link(s, ca_pos, pa_pos, k, tag):
    t = Int("t_" + tag); s.add(t >= -2, t <= 2); s.add(ca_pos - pa_pos - k == 26 * t)
def F_periodic(CT, P):
    s = Solver(); pa, ca = base(s); key = [Int(f"k{j}") for j in range(P)]
    for x in key: s.add(x >= 0, x < 26)
    for i, p in CR: link(s, ca[CT[i]], pa[p], key[i % P], str(i))
    return s
def F_gromark(CT, b, L):
    s = Solver(); pa, ca = base(s); k = [Int(f"g{j}") for j in range(N)]
    for j in range(L): s.add(k[j] >= 0, k[j] < b)
    for j in range(L, 74):
        q = Int(f"q{j}"); s.add(q >= 0, q <= 1); s.add(k[j] == k[j - L] + k[j - L + 1] - b * q)
    for i, p in CR: link(s, ca[CT[i]], pa[p], k[i], str(i))
    return s
def F_progressive(CT):
    s = Solver(); pa, ca = base(s); a, st = Int("a"), Int("s"); s.add(a >= 0, a < 26, st >= 0, st < 26)
    for i, p in CR:
        u = Int(f"u{i}"); s.add(u == (a + st * i) - 26 * Int(f"w{i}")); s.add(u >= 0, u < 26)
        link(s, ca[CT[i]], pa[p], u, str(i))
    return s
def F_autokey(CT, L, kind):
    s = Solver(); pa, ca = base(s); n = 0; prim = [Int(f"pr{j}") for j in range(L)]
    for x in prim: s.add(x >= 0, x < 26)
    for i, p in CR:
        j = i - L
        if kind == "pt":
            if j in KN: kk = pa[KN[j]]
            elif j < 0: kk = prim[i]
            else: continue
        else:
            kk = ca[CT[j]] if j >= 0 else prim[i]
        link(s, ca[CT[i]], pa[p], kk, str(i)); n += 1
    return s
def check(s, timeout=60000):
    s.set("timeout", timeout); t = time.time(); r = s.check(); return str(r), round(time.time() - t, 1)
def plant_ct():
    import random
    rng = random.Random(11); PA = "".join(rng.sample(AZ, 26)); CA = "".join(rng.sample(AZ, 26))
    PA = "A" + PA.replace("A", "")
    eng = "WEMETATTHECORNERWHERETHEROADTURNSEASTNORTHEASTANDTHEOLDSTATIONSTOODWAITINGFORTHEBERLINCLOCKTOSTRIKE"[:N]
    pt = list(eng)
    for i, ch in KN.items(): pt[i] = ch
    key = [3, 14, 15, 9, 2, 6, 5]
    return "".join(CA[(PA.index(p) + key[i % 7]) % 26] for i, p in enumerate(pt))
if __name__ == "__main__":
    CT = K4; ctl = len(sys.argv) > 1 and sys.argv[1] == "control"
    if ctl:
        CT = plant_ct(); print("CONTROL: random PA, CA, periodic key P=7 (3,14,15,9,2,6,5)")
    rows = []
    for P in range(1, 27): rows.append((f"F1 Quagmire-IV periodic P={P}", F_periodic(CT, P)))
    if not ctl:
        for b, L in ((10, 5), (10, 4), (5, 5), (8, 5), (26, 2), (26, 3)): rows.append((f"F2 Gromark base {b} primer {L}", F_gromark(CT, b, L)))
        rows.append(("F3 progressive a+s*i", F_progressive(CT)))
        for L in range(1, 15): rows.append((f"F4 PT-autokey lag {L}", F_autokey(CT, L, "pt")))
        for L in range(1, 15): rows.append((f"F5 CT-autokey lag {L}", F_autokey(CT, L, "ct")))
    for name, s in rows:
        r, dt = check(s); print(f"{name}: {r} ({dt}s)", flush=True)
