"""Cycle 201 gates G4/G5.  G5: pure-Python recount of PHI_P / COL_P (separate code path) on K4 + 20 plants, and
lib201.phi vs cycle 200's lib200 panel on 50 strings.  G4: regression — cycle 200's own code and seeds must give case
187's q_rev exactly (7/300, 5/300, 11/300 at P 8, 13, 23).  Prints counts only."""
import sys, os
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cycle200"))
import lib201 as L
import lib200, plant200

AZ = L.AZ


def phi_py(s, P):
    return sum(1 for d in range(P, 49, P) for i in range(len(s) - d) if s[i] == s[i + d])


def col_py(s, P):
    t = 0
    for f in range(P):
        c = s[f::P]
        for ch in set(c):
            n = c.count(ch); t += n * (n - 1) // 2
    return t


sup = sys.argv[1] if len(sys.argv) > 1 else "/workspace/k4c201/sup"
TXT = L.load_models(sup)
rng = np.random.default_rng([21000, 90])
strings = [L.K4] + ["".join(AZ[v] for v in L.plant(rng, TXT["JE"], 8, 3, 0, L.unigram(TXT["JE"]))[1]) for _ in range(20)]
mm = 0
for s in strings:
    x = L.enc(s)
    for P in (8, 13, 16, 19, 20, 23, 24, 26):
        mm += int(L.phi(x, P)[0] != phi_py(s, P)) + int(L.col(x, P)[0] != col_py(s, P))
NM = lib200.names()
X = rng.integers(0, 26, (50, 97))
pan = lib200.panel(X)
for P in (8, 13, 16, 19, 20, 23, 24, 26):
    mm += int((pan[:, NM.index(f"PHI{P}")] != L.phi(X, P)).sum())
print("G5 recount mismatches", mm, "(21 strings x 8 periods x 2 stats + 50 x 8 vs lib200)")

# G4 regression of case 187 (cycle 200 code path, seeds of PREREG200)
SB = 20000
x4 = lib200.enc(lib200.K4)
M = lib200.Meter(np.sort(x4), 10000, SB + 1, 10000, SB + 2)
z4 = M.z(lib200.panel(x4[None, :]))[0]
txt = plant200.corpus(f"{sup}/rk_plain.txt")
counts = {}
for P in (8, 13, 23):
    r = np.random.default_rng(SB + 300 + P); iP = NM.index(f"PHI{P}"); c = 0
    for k in range(300):
        s = plant200.arbitrary_periodic(r, plant200.with_cribs(plant200.window(r, txt)), P)
        x = lib200.enc(s)
        P0 = lib200.panel(lib200.shuffles(x, 300, SB + 50000 + P * 1000 + k)).astype(float)
        mu, sd = P0.mean(0), P0.std(0, ddof=1); sd[sd == 0] = 1
        z = (lib200.panel(x[None, :])[0] - mu) / sd
        c += int(z[iP] <= z4[iP])
    counts[P] = c
ok = counts == {8: 7, 13: 5, 23: 11}
print("G4 case-187 regression counts", counts, "expected {8: 7, 13: 5, 23: 11}", "PASS" if ok else "FAIL")
