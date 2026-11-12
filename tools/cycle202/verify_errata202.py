"""Cycle 202: own cheap verification of the Voynich agent's audit of case 187 (errata 1-3).  Uses only K4's letter
multiset (sorted) and English plants; seeds SeedSequence([202202, 9xx, ...]), outside every earlier block and Voynich's 7001-7800.
(1) Zmax alpha-0.05 critical value: case 187's Meter moments (seeds 20001/20002, as rhythm200), 100,000 fresh held-out shuffles.
(2) exact null size of case 187's targeted 'z(PHI_P) >= crit95' rule: crit95 mapped back to the raw-count atom with case 187's
    meter moments; size P(raw >= atom) and next-atom size P(raw >= atom + 1), 200,000 fresh shuffles.
(3) P4b (Vig p 7 then columnar w 7) family power with case 187's own procedure (own null 300 shuffles, crit 3.863), fresh plants."""
import os, sys, json, math, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "cycle200"))
import plant200
from lib200 import enc, K4, panel, shuffles, names, Meter

sup = sys.argv[1]; npl = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
outf = sys.argv[3] if len(sys.argv) > 3 else None
t0 = time.time(); out = {}
x = np.sort(enc(K4)); NM = names()
M = Meter(x, 10000, 20001, 10000, 20002)
crit = M.crit_hi(0.05)
zmx = np.concatenate([M.z(panel(shuffles(x, 10000, [202202, 901, b]))).max(1) for b in range(10)])
tail = float(np.mean(zmx >= crit))
out["E1_zmax"] = dict(crit_case187=crit, n_fresh=int(len(zmx)), fresh_crit95=float(np.quantile(zmx, 0.95)),
                      size_of_case187_crit=tail, size_se=math.sqrt(tail * (1 - tail) / len(zmx)))
print("E1", out["E1_zmax"], round(time.time() - t0, 1), flush=True)

R = json.load(open(os.path.join(HERE, "..", "cycle200", "results200.json")))["targeted"]
E2 = {}
def phi(X, P):
    return sum((X[:, :-d] == X[:, d:]).sum(1) for d in range(P, 49, P))
for P in (8, 13, 16, 19, 20, 23, 24, 26):
    i = NM.index(f"PHI{P}")
    raw = M.mu[i] + R[str(P)]["crit95"] * M.sd[i]
    atom = int(round(raw)) if abs(raw - round(raw)) < 1e-6 else int(math.ceil(raw))
    v = np.concatenate([phi(shuffles(x, 50000, [202202, 902, P, b]).astype(np.int8), P) for b in range(4)])
    E2[str(P)] = dict(crit_raw=float(raw), reject_if_raw_ge=atom, size=float(np.mean(v >= atom)),
                      size_next_atom=float(np.mean(v >= atom + 1)), atom_mass=float(np.mean(v == atom)),
                      midp_size=float(np.mean(v > atom) + 0.5 * np.mean(v == atom)))
    print("E2", P, E2[str(P)], flush=True)
out["E2_targeted_size"] = E2

txt = plant200.corpus(f"{sup}/rk_plain.txt")
z = []
for k in range(npl):
    rng = np.random.default_rng([202202, 903, k])
    s, _ = plant200.family("P4b_vig7_col7", rng, txt)
    xs = enc(s)
    P0 = panel(shuffles(xs, 300, [202202, 904, k])).astype(float)
    mu, sd = P0.mean(0), P0.std(0, ddof=1); sd[sd == 0] = 1
    z.append(((panel(xs[None, :])[0] - mu) / sd).max())
z = np.array(z); pw = float(np.mean(z >= 3.863))
out["E3_P4b_power"] = dict(n=npl, power_at_3863=pw, se=math.sqrt(pw * (1 - pw) / npl),
                           power_at_fresh_crit=float(np.mean(z >= out["E1_zmax"]["fresh_crit95"])))
print("E3", out["E3_P4b_power"], flush=True)
out["seconds"] = round(time.time() - t0, 1)
print("seconds", out["seconds"])
if outf:
    json.dump(out, open(outf, "w"), indent=1)
