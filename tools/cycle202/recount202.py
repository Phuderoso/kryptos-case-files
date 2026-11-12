"""Cycle 202 gates G4 (regression) and G5 (recount).  Prints counts only.
G5: pure-Python COL_P / PHI_P (separate code path, no numpy) on K4 + 20 C3 plants + 20 C3b plants at the 8 open periods,
    against lib201.col / lib201.phi: 0 mismatches required.
G4: cycle 201's code path and seeds (22000) must reproduce case 188's descriptive q_col for JE C3 at P 8, 13, 23
    (0.003, 0.008, 0.020 of 1,000 plants) exactly."""
import sys, json, os
import numpy as np
import lib202 as M
L = M.L
AZ = L.AZ


def col_py(s, P):
    t = 0
    for f in range(P):
        c = s[f::P]
        for ch in set(c):
            n = c.count(ch); t += n * (n - 1) // 2
    return t


def phi_py(s, P):
    return sum(1 for d in range(P, 49, P) for i in range(len(s) - d) if s[i] == s[i + d])


sup = sys.argv[1]
TXT = L.load_models(sup); U = L.unigram(TXT["JE"]); B = M.bigram(TXT["JE"])
rng = np.random.default_rng([202202, 90])
strings = [L.K4]
for P in (8, 23):
    strings += ["".join(AZ[v] for v in L.plant(rng, TXT["JE"], P, 3, 0, U)[1]) for _ in range(10)]
    strings += ["".join(AZ[v] for v in M.plant_c3b(rng, TXT["JE"], P, B, U)[1]) for _ in range(10)]
mm = 0
for s in strings:
    x = L.enc(s)
    for P in M.OPEN:
        mm += int(L.col(x, P)[0] != col_py(s, P)) + int(L.phi(x, P)[0] != phi_py(s, P))
print("G5 recount mismatches", mm, f"({len(strings)} strings x 8 periods x 2 stats)")

# G4: case 188 regression (cycle 201 seeds 22000, JE = model 0, C3, tag 10/11, K4 own null [22000, 2, P])
R = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cycle201", "results201.json")))
ok = True; got = {}
for P in (8, 13, 23):
    zK = L.own_z(L.enc(L.K4), P, 10000, [22000, 2, P])[1]
    zs = []
    for k in range(1000):
        r = np.random.default_rng([22000, 10, 0, 3, P, k])
        x, y = L.plant(r, TXT["JE"], P, 3, 0.0, U)
        zs.append(L.own_z(y, P, 300, [22000, 11, 0, 3, P, k])[1])
    q = float(np.mean(np.array(zs) <= zK)); exp = R["table"][f"JE_C3_P{P}"]["q_col"]
    got[P] = (q, exp); ok &= (q == exp)
print("G4 case-188 regression q_col JE C3", got, "PASS" if ok else "FAIL")
