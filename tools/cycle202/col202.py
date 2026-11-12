"""Cycle 202 driver (I-245, PREREG202.md).  python3 col202.py run --sup DIR --out FILE
Confirmatory COL_P reverse test at the 8 SAT-open periods under C3 (4 plaintext models), fresh seeds
SeedSequence([202202, tag, model, P, k]).  Tags: 2 K4 own null; 10 C3 references; 11 their own nulls; 20/21 held-out clean
plants (G2b); 40/41 shuffled-K4 known negative (G3); 50/51 C3b bigram-repair sensitivity (I-246, descriptive)."""
import sys, json, time, argparse, math
import numpy as np
from multiprocessing import Pool
import lib202 as M
L = M.L

ap = argparse.ArgumentParser()
ap.add_argument("mode")
ap.add_argument("--sup", default="/workspace/k4c202/sup")
ap.add_argument("--nref", type=int, default=4000)
ap.add_argument("--nheld", type=int, default=1000)
ap.add_argument("--nb", type=int, default=2000)
ap.add_argument("--ng3", type=int, default=500)
ap.add_argument("--nown", type=int, default=300)
ap.add_argument("--seedbase", type=int, default=202202)
ap.add_argument("--procs", type=int, default=7)
ap.add_argument("--out", default=None)
a = ap.parse_args()
SB = a.seedbase
OPEN, MODELS = M.OPEN, M.MODELS
TXT = L.load_models(a.sup)
UNI = {m: L.unigram(t) for m, t in TXT.items()}
BIG = {m: M.bigram(t) for m, t in TXT.items()}
ALPHA = 0.05


def batch(args):
    """(tag, mi, P, k0, k1, kind) -> rows (z_col, z_phi, col_pt, col_ct, phi_pt, phi_ct, consistent)"""
    tag, mi, P, k0, k1, kind = args
    m = MODELS[mi]; res = []
    for k in range(k0, k1):
        rng = np.random.default_rng([SB, tag, mi, P, k])
        if kind == "C3":
            x, y = L.plant(rng, TXT[m], P, 3, 0.0, UNI[m])
        else:
            x, y = M.plant_c3b(rng, TXT[m], P, BIG[m], UNI[m])
        zp, zc = L.own_z(y, P, a.nown, [SB, tag + 1, mi, P, k])
        res.append((zc, zp, int(L.col(x, P)[0]), int(L.col(y, P)[0]), int(L.phi(x, P)[0]), int(L.phi(y, P)[0]),
                    int(L.consistent(y, P, 3))))
    return res


def run_jobs(jobs, pool):
    chunks = []
    for (tag, mi, P, n, kind) in jobs:
        chunks += [(tag, mi, P, k, min(k + 250, n), kind) for k in range(0, n, 250)]
    outs = pool.map(batch, chunks)
    res = {}
    for ch, o in zip(chunks, outs):
        res.setdefault((ch[0], ch[1], ch[2]), []).extend(o)
    return {k: np.array(v) for k, v in res.items()}


def binom_sf(c, n, p):
    """P(X >= c), X ~ Bin(n, p), exact (log-space)."""
    return sum(math.exp(math.lgamma(n + 1) - math.lgamma(j + 1) - math.lgamma(n - j + 1) + j * math.log(p) + (n - j) * math.log1p(-p))
               for j in range(c, n + 1))


t0 = time.time()
out = {"mode": a.mode, "seedbase": SB, "nref": a.nref, "nheld": a.nheld, "nb": a.nb, "ng3": a.ng3, "nown": a.nown}
pool = Pool(a.procs)

# ---- K4: own null 10,000 shuffles ----
x4 = L.enc(L.K4); k4 = {}
for P in OPEN:
    S = L.shuffles(x4, 10000, [SB, 2, P])
    cs = L.col(S, P); c0 = int(L.col(x4, P)[0])
    zp, zc = L.own_z(x4, P, 10000, [SB, 2, P])
    k4[P] = dict(z_col=zc, z_phi=zp, col=c0, phi=int(L.phi(x4, P)[0]),
                 own_p_lo=float(np.mean(cs <= c0)), own_p_lo_mid=float(np.mean(cs < c0) + 0.5 * np.mean(cs == c0)),
                 own_atom_mass=float(np.mean(cs == c0)), own_mean=float(cs.mean()), own_sd=float(cs.std(ddof=1)))
out["K4"] = {str(P): v for P, v in k4.items()}
print("K4", json.dumps(out["K4"]), flush=True)

ref = run_jobs([(10, mi, P, a.nref, "C3") for mi in range(4) for P in OPEN], pool)
held = run_jobs([(20, mi, P, a.nheld, "C3") for mi in range(4) for P in OPEN], pool)
refb = run_jobs([(50, mi, P, a.nb, "C3b") for mi in range(4) for P in OPEN], pool)
print("plants done", round(time.time() - t0, 1), flush=True)

alld = [ref, held, refb]
out["G1_invariance"] = bool(all((v[:, 2] == v[:, 3]).all() and (v[:, 4] == v[:, 5]).all() for d in alld for v in d.values()))
out["G1b_crib_consistency"] = bool(all((v[:, 6] == 1).all() for d in alld for v in d.values()))

tab = {}; fd = []
for mi, m in enumerate(MODELS):
    for P in OPEN:
        v = ref[(10, mi, P)]; K = k4[P]; h = held[(20, mi, P)]; b = refb[(50, mi, P)]
        zs = v[:, 0]; cr = v[:, 2]
        qh = np.array([M.mc_q(zs, z) for z in h[:, 0]])
        # attainable (next-atom, conservative) size of the raw-count version: largest c with P(col_pt <= c) <= alpha
        cs = sorted(set(cr.tolist())); c_ok = [c for c in cs if np.mean(cr <= c) <= ALPHA]
        c_star = max(c_ok) if c_ok else None
        row = dict(model=m, P=P, n=len(v), q_col=M.mc_q(zs, K["z_col"]), q_col_share=float(np.mean(zs <= K["z_col"])),
                   ties=int(np.sum(zs == K["z_col"])),
                   q_colraw_le=float(np.mean(cr <= K["col"])), q_colraw_mid=float(np.mean(cr < K["col"]) + 0.5 * np.mean(cr == K["col"])),
                   colraw_atom_mass=float(np.mean(cr == K["col"])),
                   raw_next_atom_crit=c_star, raw_next_atom_size=(float(np.mean(cr <= c_star)) if c_star is not None else 0.0),
                   q_phi=M.mc_q(v[:, 1], K["z_phi"]),
                   zcol_mean=float(zs.mean()), zcol_sd=float(zs.std()), zcol_q05=float(np.quantile(zs, 0.05)),
                   col_mean=float(cr.mean()),
                   G2_false_disfavour=float(np.mean(qh < ALPHA)), G2_count=int(np.sum(qh < ALPHA)),
                   G2_false_at_holm_min=float(np.mean(qh <= ALPHA / 8)),
                   q_col_C3b=M.mc_q(b[:, 0], K["z_col"]), zcol_mean_C3b=float(b[:, 0].mean()))
        fd.append(row["G2_count"])
        tab[f"{m}_P{P}"] = row
out["table"] = tab

# ---- G2b (pooled + Bonferroni per configuration), registered bars ----
ncfg = len(fd); npool = ncfg * a.nheld
bar_pool = ALPHA + 2 * math.sqrt(ALPHA * (1 - ALPHA) / npool)
c_bonf = next(c for c in range(a.nheld + 1) if binom_sf(c, a.nheld, ALPHA) <= ALPHA / ncfg)
pooled = sum(fd) / npool
out["G2b"] = dict(pooled=pooled, bar_pooled=bar_pool, max_count=max(fd), bonferroni_fail_if_count_ge=c_bonf,
                  passes=bool(pooled <= bar_pool and max(fd) < c_bonf))

# ---- G3 known negative: shuffles of K4's multiset (not H_P) judged by the same rule, every model, every P ----
g3 = {}
for P in OPEN:
    S = L.shuffles(np.sort(x4), a.ng3, [SB, 40, P])
    zs3 = np.array([L.own_z(s, P, a.nown, [SB, 41, P, i])[1] for i, s in enumerate(S)])
    g3[str(P)] = {m: float(np.mean([M.mc_q(ref[(10, mi, P)][:, 0], z) < ALPHA for z in zs3])) for mi, m in enumerate(MODELS)}
out["G3_shuffled_K4_disfavour_rate"] = g3
out["G3_passes"] = bool(min(g3["8"].values()) >= 0.15)

# ---- verdict: worst case over models per period, Holm over the 8 periods ----
qstar = {P: max(tab[f"{m}_P{P}"]["q_col"] for m in MODELS) for P in OPEN}
worst = {P: max(MODELS, key=lambda m: tab[f"{m}_P{P}"]["q_col"]) for P in OPEN}
H = M.holm(qstar)
qb = {P: max(tab[f"{m}_P{P}"]["q_col_C3b"] for m in MODELS) for P in OPEN}
HB = M.holm(qb)
gates_ok = out["G1_invariance"] and out["G1b_crib_consistency"] and out["G2b"]["passes"] and out["G3_passes"]
ver = {}
for P in OPEN:
    rej = H[P][0] and gates_ok
    ver[str(P)] = dict(q_worst=qstar[P], worst_model=worst[P], holm_threshold=H[P][1], holm_reject=H[P][0],
                       per_model_q={m: tab[f"{m}_P{P}"]["q_col"] for m in MODELS},
                       label=("STAT-DISFAVOURED" if rej else "LOW-POWER"),
                       C3b_q_worst=qb[P], C3b_holm_reject=HB[P][0])
out["verdict"] = ver
out["gates_ok_excluding_recount"] = bool(gates_ok)
out["seconds"] = round(time.time() - t0, 1)
print(json.dumps(dict(verdict=ver, G1=out["G1_invariance"], G1b=out["G1b_crib_consistency"], G2b=out["G2b"], G3=g3,
                      seconds=out["seconds"]), indent=1))
if a.out:
    json.dump(out, open(a.out, "w"), indent=1)
