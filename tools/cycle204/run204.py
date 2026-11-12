"""Cycle 204 registered driver (PREREG204.md, I-252).  python3 run204.py SUP OUT.json [scale]
Seeds: numpy default_rng([204204, tag, model_index, P, k]).  Tags: 10 EXACT-O3 references, 20 EXACT-O3 held-out (G2b),
30 chain-C3 repair recipe, 50 real-window C3 recipe (case 189's, fresh seeds, exact z), 60 EXACT-O4 (descriptive),
40 shuffled K4 (G3), 70 G4 shuffles, 80 G5 FFBS-vs-rejection."""
import sys, json, math, time, itertools
import numpy as np
import lib204 as M
L = M.L
SUP, OUT = sys.argv[1], sys.argv[2]
SC = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
NREF, NHELD, NC3, NREAL, NO4, NG3 = (int(SC * v) for v in (10000, 2000, 10000, 10000, 4000, 1000))
SB = 204204; T0 = time.time()
def log(*a): print(*a, f"[{time.time()-T0:.1f}s]", flush=True)
def rng(*t): return np.random.default_rng([SB, *t])
TXT = M.load(SUP)
MODELS = M.REG_MODELS + M.DESC_MODELS
R = {"sizes": dict(NREF=NREF, NHELD=NHELD, NC3=NC3, NREAL=NREAL, NO4=NO4, NG3=NG3), "gates": {}}

# ---------- G4: exact moments ----------
def brute(x, P):
    vals = [int(L.col(np.array(p), P)[0]) for p in set(itertools.permutations(x))]
    mu, sd = M.col_moments(np.bincount(x, minlength=26)[None], P, len(x))
    return float(np.mean(vals)), float(np.var(vals)), float(mu[0]), float(sd[0] ** 2)
g4 = {"brute": []}; ok4 = True
for x, P in (([0, 0, 1, 1, 1, 2, 3], 3), ([0, 0, 0, 1, 1, 1, 2, 2], 2), ([4, 4, 4, 4, 1, 2, 2, 3], 3)):
    em, ev, xm, xv = brute(x, P); g4["brute"].append([em, ev, xm, xv]); ok4 &= abs(em - xm) < 1e-9 and abs(ev - xv) < 1e-9
mu8, sd8 = M.col_moments(M.counts(M.K4X), 8)
g4["K4_P8_mean_sd"] = [float(mu8[0]), float(sd8[0])]
ok4 &= abs(mu8[0] - 19.48454) < 1e-4 and abs(sd8[0] - 4.08224) < 1e-4
S = rng(70).permuted(np.tile(M.K4X, (200000, 1)), axis=1)
R["K4"] = {}
for P in M.OPEN:
    v = L.col(S, P).astype(float); mu, sd = M.col_moments(M.counts(M.K4X), P)
    dev = (v.mean() - mu[0]) / (sd[0] / math.sqrt(len(v))); rel = v.std(ddof=1) / sd[0] - 1
    ok4 &= abs(dev) <= 4 and abs(rel) <= 0.01
    c0 = int(L.col(M.K4X, P)[0])
    R["K4"][P] = dict(col=c0, exact_mean=float(mu[0]), exact_sd=float(sd[0]), z_exact=float((c0 - mu[0]) / sd[0]),
                      shuf_mean_dev_se=float(dev), shuf_sd_rel=float(rel), p_le_200k=float(np.mean(v <= c0)))
g4["pass"] = bool(ok4); R["gates"]["G4"] = g4; log("G4", g4["pass"], {P: round(R["K4"][P]["z_exact"], 5) for P in M.OPEN})
ZK = {P: R["K4"][P]["z_exact"] for P in M.OPEN}

# ---------- G5: FFBS vs rejection on a mild mask (JE, k = 3) ----------
Tm, init = M.model_chain(TXT, "JE", 3)
Mm = np.ones((M.N, 26), bool); Mm[5] = False; Mm[5, 4] = True
for j in (10, 11, 12): Mm[j, [4, 19, 0]] = False
Mm[40, 4] = False
F = M.forward_sample(rng(80, 0), Tm, init, int(400000 * min(SC, 1) + 2000))
acc = F[Mm[np.arange(M.N), F].all(1)]
Bf = M.ffbs(rng(80, 1), Tm, init, Mm, len(acc))
chi = 0.0; dof = 0
for i in range(46):
    a = np.bincount(acc[:, i], minlength=26); b = np.bincount(Bf[:, i], minlength=26); keep = (a + b) > 0
    a, b = a[keep], b[keep]; tot = a + b; ea = tot * len(acc) / (2 * len(acc))
    chi += float((((a - ea) ** 2) / ea + ((b - ea) ** 2) / ea).sum()); dof += int(keep.sum()) - 1
from math import erfc, sqrt
zchi = (chi - dof) / math.sqrt(2 * dof)        # Wilson-Hilferty-free normal approx (dof ~ 1000)
p5 = 0.5 * erfc(zchi / sqrt(2))
c8a, c8b = L.col(acc, 8).astype(float), L.col(Bf, 8).astype(float)
zc8 = (c8a.mean() - c8b.mean()) / math.sqrt(c8a.var() / len(c8a) + c8b.var() / len(c8b))
R["gates"]["G5"] = dict(n_accepted=int(len(acc)), chi2=chi, dof=dof, p=float(p5), col8_z=float(zc8),
                        mask_ok=bool(Mm[np.arange(M.N), Bf].all()), pass_=bool(p5 > 0.001 and abs(zc8) < 4 and Mm[np.arange(M.N), Bf].all()))
log("G5", R["gates"]["G5"])

# ---------- plants ----------
res = {}; g1 = True; g1b = True; g3 = {}
for mi, name in enumerate(MODELS):
    src = TXT["K123"] if name == "K123MIX" else TXT[name]
    uni = L.unigram(src)
    ch3 = M.model_chain(TXT, name, 3); ch4 = M.model_chain(TXT, name, 4)
    for P in M.OPEN:
        Mk = M.mask(P); out = {}
        def make(kind, tag, n):
            global g1, g1b
            r = rng(tag, mi, P)
            if kind == "EX3": X = M.ffbs(r, *ch3, Mk, n)
            elif kind == "EX4": X = M.ffbs(r, *ch4, Mk, n)
            elif kind == "CH3": X = M.c3_repair(r, M.forward_sample(r, *ch3, n), P, uni)
            else: X = M.c3_repair(r, M.windows(r, src, n), P, uni)
            Y = M.encipher(r, X, P)
            g1 &= bool((L.col(X, P) == L.col(Y, P)).all())
            g1b &= bool(M.consistent_rows(Y, P).all() and Mk[np.arange(M.N), X].all())
            return M.z_exact(Y, P)
        zr = make("EX3", 10, NREF); zh = make("EX3", 20, NHELD)
        zc = make("CH3", 30, NC3); zw = make("RW", 50, NREAL); z4 = make("EX4", 60, NO4)
        Sg = rng(40, mi, P).permuted(np.tile(M.K4X, (NG3, 1)), axis=1)
        zs = M.z_exact(Sg, P)
        thr = np.quantile(zr, 0.05)
        qs_h = np.array([(1 + np.sum(zr <= z)) / (len(zr) + 1) for z in zh])
        qs_s = np.array([(1 + np.sum(zr <= z)) / (len(zr) + 1) for z in zs])
        out = dict(q_exact3=M.mc_q(zr, ZK[P]), q_chainC3=M.mc_q(zc, ZK[P]), q_realC3=M.mc_q(zw, ZK[P]), q_exact4=M.mc_q(z4, ZK[P]),
                   mean=dict(ex3=float(zr.mean()), ch3=float(zc.mean()), real=float(zw.mean()), ex4=float(z4.mean())),
                   q05=dict(ex3=float(thr), ch3=float(np.quantile(zc, .05)), real=float(np.quantile(zw, .05)), ex4=float(np.quantile(z4, .05))),
                   held_false=int((qs_h < 0.05).sum()), held_false_holm=int((qs_h < 0.05 / 8).sum()),
                   g3_rate=float((qs_s < 0.05).mean()), g3_rate_holm=float((qs_s < 0.05 / 8).mean()))
        res.setdefault(name, {})[P] = out
    log(name, {P: (round(res[name][P]["q_exact3"], 4)) for P in M.OPEN} if False else "done")
R["plants"] = res
R["gates"]["G1"] = g1; R["gates"]["G1b"] = g1b

# G2b
def binom_sf(c, n, p):
    return sum(math.exp(math.lgamma(n + 1) - math.lgamma(j + 1) - math.lgamma(n - j + 1) + j * math.log(p) + (n - j) * math.log1p(-p)) for j in range(c, n + 1))
cfg_bar = next(c for c in range(NHELD + 1) if binom_sf(c, NHELD, 0.05) <= 0.05 / 32)
fal = [res[m][P]["held_false"] for m in M.REG_MODELS for P in M.OPEN]
pooled = sum(fal) / (len(fal) * NHELD); pooled_bar = 0.05 + 2 * math.sqrt(0.05 * 0.95 / (len(fal) * NHELD))
R["gates"]["G2b"] = dict(pooled=pooled, pooled_bar=pooled_bar, max_cfg=max(fal), cfg_bar=cfg_bar, pass_=bool(pooled <= pooled_bar and max(fal) < cfg_bar))
# G3
g3r = {m: res[m][8]["g3_rate"] for m in M.REG_MODELS}
R["gates"]["G3"] = dict(rates_P8=g3r, pass_=bool(min(g3r.values()) >= 0.15))
# G6 fidelity
g6 = {m: dict(dmean=res[m][8]["mean"]["ch3"] - res[m][8]["mean"]["real"], dq05=res[m][8]["q05"]["ch3"] - res[m][8]["q05"]["real"]) for m in M.REG_MODELS}
R["gates"]["G6"] = dict(per_model=g6, pass_=bool(all(abs(v["dmean"]) <= 0.20 and abs(v["dq05"]) <= 0.20 for v in g6.values())))
allpass = all([R["gates"]["G1"], R["gates"]["G1b"], R["gates"]["G2b"]["pass_"], R["gates"]["G3"]["pass_"], R["gates"]["G4"]["pass"],
               R["gates"]["G5"]["pass_"], R["gates"]["G6"]["pass_"]])
R["gates"]["all_pass"] = allpass
# decision
qstar = {P: max(res[m][P]["q_exact3"] for m in M.REG_MODELS) for P in M.OPEN}
qreal = {P: max(res[m][P]["q_realC3"] for m in M.REG_MODELS) for P in M.OPEN}
h = M.holm(qstar); hr = M.holm(qreal)
R["min_attainable_q"] = 1 / (NREF + 1)
R["decision"] = {P: dict(qstar_exact3=qstar[P], holm_reject=h[P][0], holm_thr=h[P][1], qstar_realC3=qreal[P], real_holm_reject=hr[P][0],
                         q4_worst=max(res[m][P]["q_exact4"] for m in M.REG_MODELS),
                         label=("STAT-DISFAVOURED" if (allpass and h[P][0] and hr[P][0]) else
                                "STAT-DISFAVOURED (real-window-sensitive)" if (allpass and h[P][0]) else "LOW-POWER" if allpass else "NO VERDICT (gate fail)"))
                 for P in M.OPEN}
json.dump(R, open(OUT, "w"), indent=1, default=float)
log("gates", {k: (v if isinstance(v, bool) else v.get("pass_", v.get("pass"))) for k, v in R["gates"].items()})
log("wrote", OUT)
