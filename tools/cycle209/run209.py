"""Cycle 209 registered driver (PREREG209.md, IDEAS I-247).  python3 run209.py SUP OUT.json
Seeds: numpy default_rng([209210, tag, model_index, P]).  Tags: 1 planted QIV soundness plants, 2 K4 key sampling for G1,
10 C4 references, 15 C3 references (paired descriptive), 20 C4 held-out (G2b), 40 shuffled K4 (G3), 11 band extension."""
import sys, os, json, math, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib209 as Q
import lib204 as M
L = M.L
SUP, OUT = sys.argv[1], sys.argv[2]
import os
SMOKE = os.environ.get("SMOKE") == "1"
NREF, NHELD, NG3, NSOUND = (60, 40, 20, 1) if SMOKE else (10000, 2000, 1000, 10)
NPOOL = 40 if SMOKE else 256
M.OPEN = [13] if SMOKE else [8, 13, 23]   # PREREG209b: registered P 8, descriptive 13 / 23
SB = 209211; T0 = time.time(); BAR = 0.00625
def log(*a): print(*a, f"[{time.time()-T0:.1f}s]", flush=True)
def rng(*t): return np.random.default_rng([SB, *t])
R = {"sizes": dict(NREF=NREF, NHELD=NHELD, NG3=NG3, NSOUND=NSOUND), "gates": {}, "seed_block": SB}
TXT = M.load(SUP)

# G0 consistency regression (case 11)
g0 = {P: Q.qiv_status(P, Q.crib_pairs(L.K4), 8, 60)[0] for P in range(1, 27)}
R["gates"]["G0"] = dict(status=g0, pass_=all(g0[P] == "UNSAT" for P in range(1, 8)) and g0[8] == "SAT")
log("G0", R["gates"]["G0"]["pass_"], {P: s for P, s in g0.items() if s != "UNSAT"})

# G4 regression: C3 mask equals case 191's mask, K4 exact z
g4 = all((Q.c3_mask_for(P, L.K4) == M.mask(P)).all() for P in [8, 13, 16, 19, 20, 23, 24, 26])
mu8, sd8 = M.col_moments(M.counts(M.K4X), 8)
ZK = {P: float(M.z_exact(M.K4X[None], P)[0]) for P in [8, 13, 16, 19, 20, 23, 24, 26]}
R["gates"]["G4"] = dict(c3_equal=bool(g4), zK4_P8=ZK[8], pass_=bool(g4 and abs(ZK[8] + 1.3435) < 1e-3))
log("G4", R["gates"]["G4"])

# Gs: soundness on planted QIV ciphertexts (P 8), and certificate check for every SAT answer on one plant
xje = L.enc(TXT["JE"]); sound = []
for i in range(0 if os.environ.get("SKIP_SOUND") == "1" else NSOUND):
    w, ct = Q.qiv_plant(rng(1, i, 8), xje, 8)
    Mk, st = Q.c4_mask(8, ct)
    M3 = Q.c3_mask_for(8, ct)
    sound.append(dict(true_allowed=int(Mk[np.arange(M.N), w].sum()), subset=bool((Mk <= M3).all()), **st))
gs_ok = (os.environ.get("SKIP_SOUND") == "1") or all(s["true_allowed"] == M.N and s["subset"] and s["unknown_query"] == 0 for s in sound)
R["gates"]["Gs"] = dict(plants=sound, pass_=bool(gs_ok)); log("Gs", gs_ok, [(s["true_allowed"], s["extra_bans_positions"]) for s in sound])

# Gx: independent cross-check of 10 UNSAT answers with the full 26-letter model (8 workers, 20 s each); certificates for 20 SAT answers
from ortools.sat.python import cp_model
def full_status(P, pairs, tl=15.0):
    m = cp_model.CpModel()
    f = [m.NewIntVar(0, 25, "") for _ in range(26)]; g = [m.NewIntVar(0, 25, "") for _ in range(26)]; k = [m.NewIntVar(0, 25, "") for _ in range(P)]
    m.AddAllDifferent(f); m.AddAllDifferent(g); m.Add(f[pairs[0][1]] == 0)
    for pos, p, c in pairs:
        b = m.NewIntVar(0, 1, ""); m.Add(g[c] == f[p] + k[pos % P] - 26 * b)
    s = cp_model.CpSolver(); s.parameters.num_workers = 8; s.parameters.max_time_in_seconds = tl
    st = s.Solve(m)
    return "SAT" if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else "UNSAT" if st == cp_model.INFEASIBLE else "UNKNOWN"
if os.environ.get("SKIP_SOUND") == "1":
    R["gates"]["Gx"] = dict(reused="run 1 (seed block 209210), mask code unchanged", pass_=True)
else:
    w, ct = Q.qiv_plant(rng(1, 0, 8), xje, 8); pairs = Q.crib_pairs(ct); M3 = Q.c3_mask_for(8, ct)
    qs = []
    for x in range(M.N):
        if x in L.CRIBPOS: continue
        for p in np.flatnonzero(M3[x]):
            qs.append((x % 8, int(p), M.AZ.index(ct[x])))
    qs = sorted(set(qs)); rr = rng(1, 99, 8); rr.shuffle(qs)
    uns, sats = [], []
    for q in qs:
        st, sol = Q.qiv_status(8, pairs + [q], 1, 20)
        if st == "UNSAT" and len(uns) < (1 if SMOKE else 6): uns.append(q)
        if st == "SAT" and len(sats) < 20: sats.append((q, sol))
        if len(uns) >= (1 if SMOKE else 6) and len(sats) >= 20: break
    agree = [full_status(8, pairs + [q]) for q in uns]
    cert = 0
    for (ph, p, c), sol in sats:
        finv, ginv, k = Q.full_key_from_solution(rng(1, 98, 8), sol, 8)
        okk = all(ginv[cc] == (finv[pp] + k[pos % 8]) % 26 for pos, pp, cc in pairs) and ginv[c] == (finv[p] + k[ph]) % 26
        okk &= len(set(finv)) == 26 and len(set(ginv)) == 26
        cert += bool(okk)
    R["gates"]["Gx"] = dict(unsat_full=agree, sat_certificates=f"{cert}/{len(sats)}",
                            pass_=bool("SAT" not in agree and cert == len(sats)))
log("Gx", R["gates"]["Gx"])

# K4 masks (C4) at every open period
MK = {}; R["K4"] = {}
for P in M.OPEN:
    MK[P], st = Q.c4_mask(P, L.K4)
    R["K4"][P] = dict(zK4=ZK[P], col=int(L.col(M.K4X, P)[0]), **st)
    log("K4 mask", P, st)

# plants (PREREG209b: z on the enciphered plant, as case 191; run 1 computed z on the plaintext = bug)
res = {}; g1 = True; g1b = True; R["key_pool"] = {}
for P in M.OPEN:
    pool, nsol = Q.key_pool(P, L.K4, [[SB, 3, P, d] for d in range(NPOOL)])
    R["key_pool"][P] = dict(draws=NPOOL, solutions=nsol, distinct=len(pool), distinct_k=len({tuple(p[2]) for p in pool}))
    log("key pool", P, R["key_pool"][P])
    forced = [x for x in range(M.N) if x not in L.CRIBPOS and MK[P][x].sum() == 1]
    for mi, name in enumerate(M.REG_MODELS):
        ch3 = M.model_chain(TXT, name, 3)
        def make(tag, n, kind):
            global g1, g1b
            r = rng(tag, mi, P)
            if kind == "C4":
                X = M.ffbs(r, *ch3, MK[P], n); Y = Q.qiv_encipher_pool(r, X, pool, P)
                pos = list(L.CRIBPOS) + forced
                g1b &= bool((Y[:, pos] == M.K4X[pos][None, :]).all() and MK[P][np.arange(M.N), X].all())
            else:
                Mk3 = M.mask(P); X = M.ffbs(r, *ch3, Mk3, n); Y = M.encipher(r, X, P)
                g1b &= bool(M.consistent_rows(Y, P).all() and Mk3[np.arange(M.N), X].all())
            g1 &= bool((L.col(X, P) == L.col(Y, P)).all())
            return M.z_exact(Y, P)
        zr = make(10, NREF, "C4"); zh = make(20, NHELD, "C4"); z3 = make(15, NREF, "C3")
        Sg = rng(40, mi, P).permuted(np.tile(M.K4X, (NG3, 1)), axis=1); zs = M.z_exact(Sg, P)
        qh = np.array([(1 + np.sum(zr <= z)) / (len(zr) + 1) for z in zh])
        qsx = np.array([(1 + np.sum(zr <= z)) / (len(zr) + 1) for z in zs])
        res.setdefault(name, {})[P] = dict(q_c4=M.mc_q(zr, ZK[P]), q_c3_paired=M.mc_q(z3, ZK[P]), mean_c4=float(zr.mean()),
                                           mean_c3=float(z3.mean()), held_false=int((qh < 0.05).sum()),
                                           g3_rate=float((qsx < 0.05).mean()), g3_rate_bar=float((qsx < BAR).mean()))
    log("plants P", P, "done" if SMOKE else {m: (round(res[m][P]["q_c4"], 4), round(res[m][P]["q_c3_paired"], 4)) for m in M.REG_MODELS})
R["plants"] = res; R["gates"]["G1"] = g1; R["gates"]["G1b"] = g1b

def binom_sf(c, n, p):
    return sum(math.exp(math.lgamma(n + 1) - math.lgamma(j + 1) - math.lgamma(n - j + 1) + j * math.log(p) + (n - j) * math.log1p(-p)) for j in range(c, n + 1))
ncfg = len(M.REG_MODELS) * len(M.OPEN)
cfg_bar = next(c for c in range(NHELD + 1) if binom_sf(c, NHELD, 0.05) <= 0.05 / ncfg)
fal = [res[m][P]["held_false"] for m in M.REG_MODELS for P in M.OPEN]
pooled = sum(fal) / (len(fal) * NHELD); pbar = 0.05 + 2 * math.sqrt(0.05 * 0.95 / (len(fal) * NHELD))
R["gates"]["G2b"] = dict(pooled=pooled, pooled_bar=pbar, max_cfg=max(fal), cfg_bar=cfg_bar, pass_=bool(pooled <= pbar and max(fal) < cfg_bar))
P8 = 13 if SMOKE else 8
g3r = {m: res[m][P8]["g3_rate"] for m in M.REG_MODELS}
R["gates"]["G3"] = dict(rates_P8=g3r, pass_=bool(min(g3r.values()) >= 0.15))
C191 = {"JE": 0.0027, "CARTER": 0.0037, "K123MIX": 0.0035, "JEX": 0.0062}
if 8 in M.OPEN:
    g4b = {m: res[m][8]["q_c3_paired"] for m in M.REG_MODELS}
    R["gates"]["G4b"] = dict(q_c3_P8=g4b, case191=C191, pass_=bool(all(abs(g4b[m] - C191[m]) <= 3 * math.sqrt(max(C191[m], 1e-4) * (1 - C191[m]) / NREF) + 1e-12 for m in M.REG_MODELS)))
else:
    R["gates"]["G4b"] = dict(pass_=True, note="smoke")
allpass = all([R["gates"][g]["pass_"] for g in ("G0", "G4", "G4b", "Gs", "Gx", "G2b", "G3")]) and g1 and g1b
R["gates"]["all_pass"] = bool(allpass)

# decision at P 8 (registered), with the boundary band and one x4 extension of the worst model
if SMOKE:
    json.dump(R["gates"], open(OUT, "w"), default=str); log("smoke ok", {k: (v if isinstance(v, bool) else v.get("pass_")) for k, v in R["gates"].items()}); sys.exit(0)
qstar = max(res[m][8]["q_c4"] for m in M.REG_MODELS); worst = max(M.REG_MODELS, key=lambda m: res[m][8]["q_c4"])
se = math.sqrt(qstar * (1 - qstar) / NREF); ext = None
if abs(qstar - BAR) < 2 * se:
    mi = M.REG_MODELS.index(worst); ch3 = M.model_chain(TXT, worst, 3)
    zz = np.concatenate([M.z_exact(M.ffbs(rng(10, mi, 8), *ch3, MK[8], NREF), 8), M.z_exact(M.ffbs(rng(11, mi, 8), *ch3, MK[8], 3 * NREF), 8)])
    q_ext = M.mc_q(zz, ZK[8]); se_ext = math.sqrt(q_ext * (1 - q_ext) / len(zz))
    ext = dict(model=worst, n=len(zz), q=q_ext, se=se_ext)
    qstar_dec = max(q_ext, max(res[m][8]["q_c4"] for m in M.REG_MODELS if m != worst)); se_dec = se_ext if qstar_dec == q_ext else se
else:
    qstar_dec, se_dec = qstar, se
if not allpass: label = "NO VERDICT (gate fail)"
elif qstar_dec <= BAR - 2 * se_dec: label = "STAT-DISFAVOURED (carries to Quagmire IV at P 8)"
elif qstar_dec >= BAR + 2 * se_dec: label = "LOW-POWER for Quagmire IV at P 8 (H_8 verdict does not transfer)"
else: label = "UNRESOLVED (boundary band)"
R["decision"] = dict(qstar=qstar, worst=worst, se=se, extension=ext, qstar_decision=qstar_dec, se_decision=se_dec, bar=BAR, label=label)
qs_all = {P: max(res[m][P]["q_c4"] for m in M.REG_MODELS) for P in M.OPEN}
R["descriptive_holm"] = {P: dict(qstar=qs_all[P], holm=M.holm(qs_all)[P]) for P in M.OPEN}
json.dump(R, open(OUT, "w"), indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
log("gates", {k: (v if isinstance(v, bool) else v.get("pass_")) for k, v in R["gates"].items() if k != "all_pass"}, "all", allpass)
log("decision", "hidden" if SMOKE else R["decision"]); log("wrote", OUT)
