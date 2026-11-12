"""Cycle 201 driver (I-238).  python3 robust201.py probe|run --sup DIR [--nref 1000] [--nheld 200] [--nown 300] --out FILE
probe: timing on English plants only (never touches K4's letter order).
run  : registered run (PREREG201.md).  Seeds: numpy SeedSequence([SB, tag, ...]), SB = 21000."""
import sys, json, time, argparse
import numpy as np
from multiprocessing import Pool
import lib201 as L

ap = argparse.ArgumentParser()
ap.add_argument("mode")
ap.add_argument("--sup", default="/workspace/k4c201/sup")
ap.add_argument("--nref", type=int, default=1000)
ap.add_argument("--nheld", type=int, default=200)
ap.add_argument("--nown", type=int, default=300)
ap.add_argument("--ndil", type=int, default=300)
ap.add_argument("--seedbase", type=int, default=21000)
ap.add_argument("--procs", type=int, default=7)
ap.add_argument("--out", default=None)
a = ap.parse_args()
SB = a.seedbase
OPEN = [8, 13, 16, 19, 20, 23, 24, 26]
CONF = [8, 13, 23]                      # confirmatory cells (case 187's STAT-DISFAVOURED)
MODELS = ["JE", "CARTER", "K123", "JEX"]
TXT = L.load_models(a.sup)
UNI = {m: L.unigram(t) for m, t in TXT.items()}


def batch(args):
    """args = (tag, mi, cond, P, k0, k1, dilute) -> list of (z_phi, z_col, phi_pt, phi_ct, col_pt, col_ct)"""
    tag, mi, cond, P, k0, k1, dil = args
    txt = TXT[MODELS[mi]]
    res = []
    for k in range(k0, k1):
        rng = np.random.default_rng([SB, tag, mi, cond, P, k])
        x, y = L.plant(rng, txt, P, cond, dil, UNI[MODELS[mi]])
        zp, zc = L.own_z(y, P, a.nown, [SB, tag + 1, mi, cond, P, k])
        res.append((zp, zc, int(L.phi(x, P)[0]), int(L.phi(y, P)[0]), int(L.col(x, P)[0]), int(L.col(y, P)[0]),
                    int(L.consistent(y, P, cond))))
    return res


def run_jobs(jobs, pool):
    chunks = []
    for (tag, mi, cond, P, n, dil) in jobs:
        step = 100
        chunks += [(tag, mi, cond, P, k, min(k + step, n), dil) for k in range(0, n, step)]
    outs = pool.map(batch, chunks)
    res = {}
    for ch, o in zip(chunks, outs):
        res.setdefault(ch[:4] + (ch[6],), []).extend(o)
    return res


t0 = time.time()
out = {"mode": a.mode, "seedbase": SB, "nref": a.nref, "nheld": a.nheld, "nown": a.nown}
pool = Pool(a.procs)

if a.mode == "probe":
    r = run_jobs([(1, mi, c, 8, 50, 0.0) for mi in range(4) for c in range(4)], pool)
    out["probe_seconds_600_plants"] = round(time.time() - t0, 1)
    for key, v in r.items():
        v = np.array(v)
        print(MODELS[key[1]], "C%d" % key[2], "plant z_phi mean %.2f sd %.2f" % (v[:, 0].mean(), v[:, 0].std()),
              "PHI8(pt) mean %.1f" % v[:, 2].mean(), "invariance", bool((v[:, 2] == v[:, 3]).all()), flush=True)
    print(out)
    sys.exit(0)

# ---- K4 (own null 10,000 shuffles, seed [SB, 2]) ----
x4 = L.enc(L.K4)
k4 = {}
for P in OPEN:
    zp, zc = L.own_z(x4, P, 10000, [SB, 2, P])
    k4[P] = dict(z_phi=zp, z_col=zc, phi=int(L.phi(x4, P)[0]), col=int(L.col(x4, P)[0]))
out["K4"] = {str(P): v for P, v in k4.items()}
print("K4", out["K4"], flush=True)

# ---- reference plants: 4 models x 3 conditionings x 8 open periods x nref (tag 10) ----
ref = run_jobs([(10, mi, c, P, a.nref, 0.0) for mi in range(4) for c in range(4) for P in OPEN], pool)
# ---- held-out clean plants (G2, Voynich 'clean item scored as suspect' gate): tag 20, confirmatory cells ----
held = run_jobs([(20, mi, c, P, a.nheld, 0.0) for mi in range(4) for c in range(4) for P in CONF], pool)
# ---- dilution breakpoint (descriptive): JE, C1, share r of non-crib letters uniform; tag 30 ----
DIL = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8]
dil = run_jobs([(30, 0, 1, P, a.ndil, r) for P in CONF for r in DIL], pool)
print("plants done", round(time.time() - t0, 1), flush=True)

inv_ok = all((np.array(v)[:, 2] == np.array(v)[:, 3]).all() and (np.array(v)[:, 4] == np.array(v)[:, 5]).all()
             for d in (ref, held, dil) for v in d.values())
out["G1_invariance"] = bool(inv_ok)
out["G1b_crib_consistency"] = bool(all((np.array(v)[:, 6] == 1).all() for d in (ref, held, dil) for v in d.values()))

tab = {}
for (tag, mi, c, P, dl), v in ref.items():
    v = np.array(v); K = k4[P]
    row = dict(model=MODELS[mi], cond=c, P=P, n=len(v),
               q_rev=float(np.mean(v[:, 0] <= K["z_phi"])), q_raw=float(np.mean(v[:, 2] <= K["phi"])),
               q_col=float(np.mean(v[:, 1] <= K["z_col"])), q_colraw=float(np.mean(v[:, 4] <= K["col"])),
               zphi_mean=float(v[:, 0].mean()), zphi_sd=float(v[:, 0].std()), phi_mean=float(v[:, 2].mean()),
               col_mean=float(v[:, 4].mean()))
    if P in CONF:
        h = np.array(held[(20, mi, c, P, 0.0)])
        qh = np.array([np.mean(v[:, 0] <= z) for z in h[:, 0]])
        row["G2_false_disfavour"] = float(np.mean(qh < 0.05))
    tab[f"{MODELS[mi]}_C{c}_P{P}"] = row
out["table"] = tab

# ---- G3 known negative: K4-multiset shuffles (not H_P) judged against JE C0 references ----
g3 = {}
for P in CONF:
    v = np.array(ref[(10, 0, 0, P, 0.0)])
    S = L.shuffles(np.sort(x4), a.nheld, [SB, 40, P])
    zs = [L.own_z(s, P, a.nown, [SB, 41, P, i])[0] for i, s in enumerate(S)]
    g3[str(P)] = float(np.mean([np.mean(v[:, 0] <= z) < 0.05 for z in zs]))
out["G3_shuffled_K4_disfavour_rate"] = g3

dt = {}
for (tag, mi, c, P, r), v in dil.items():
    v = np.array(v); K = k4[P]
    dt[f"P{P}_r{r}"] = dict(P=P, r=r, q_rev=float(np.mean(v[:, 0] <= K["z_phi"])), q_raw=float(np.mean(v[:, 2] <= K["phi"])),
                           phi_mean=float(v[:, 2].mean()))
out["dilution"] = dt

# ---- verdict (registered): a confirmatory cell stays STAT-DISFAVOURED iff max q_rev over 4 models x C0-C3 < 0.05 ----
ver = {}
for P in CONF:
    qs = {k: r["q_rev"] for k, r in tab.items() if r["P"] == P}
    worst = max(qs, key=qs.get)
    ver[str(P)] = dict(max_q=qs[worst], worst=worst, label="STAT-DISFAVOURED" if qs[worst] < 0.05 else "LOW-POWER (model-sensitive)")
out["verdict"] = ver
g2 = [r["G2_false_disfavour"] for r in tab.values() if "G2_false_disfavour" in r]
out["G2_pooled"] = float(np.mean(g2)); out["G2_max"] = float(max(g2))
out["gates"] = dict(G1=out["G1_invariance"] and out["G1b_crib_consistency"],
                    G2=all(r.get("G2_false_disfavour", 0) <= 0.081 for r in tab.values()),   # as in PREREG201 (FWER ~0.69, I-243)
                    G2b=bool(np.mean(g2) <= 0.0544 and max(g2) < 0.11),                       # PREREG201b: pooled + Bonferroni/48
                    G3=g3["8"] >= 0.25)
out["seconds"] = round(time.time() - t0, 1)
print(json.dumps(dict(verdict=ver, gates=out["gates"], G2_pooled=out["G2_pooled"], G2_max=out["G2_max"], G3=g3, seconds=out["seconds"]), indent=1))
if a.out:
    json.dump(out, open(a.out, "w"), indent=1)
