"""Cycle 210 — case 196 addendum (IDEAS I-279 prerequisite, Voynich desk C4 check sha e06ce501...):
rerun the case-196 C4 plants and q at P 8 with the EXACT 85-ban C4 mask (81 CP-SAT bans + the 4 cells CP-SAT left UNKNOWN:
(37,T), (50,C), (50,E), (50,T)), each of the 4 named and independently decided here by Z3 (no time limit).
python3 c4add210.py SUP OUT.json   [REPRO_ONLY=1 runs only gates Z and R]
Gates: Z (Z3: 4 timeouts UNSAT; 6 sampled CP-SAT bans UNSAT; pos 43: only T SAT; 6 sampled allowed cells SAT with checked witness),
M (mask counts 1,517 / 1,513, forced {35,41,43,46,61,78}), R (I-283: 81-ban mask + seed 209211 reproduces case 196's JEX tag-10 q 0.0074993 exactly).
Main (seed block 209212): 4 registered models x 10,000 C4 references at P 8 (tag 10), 85-ban mask; paired 81-ban run on identical seeds
(descriptive mask effect).  Decision (I-281 band, I-265 extension): worst model, looks n = 10k, 40k, 160k (tags 10, 11, 12), stop at the
first look outside |q - 0.00625| < 2 SE; after 3 looks still inside -> UNRESOLVED.  STAT-DISFAVOURED if q <= bar - 2SE, LOW-POWER if >= bar + 2SE."""
import sys, os, json, math, time
import numpy as np
H = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get("REPO", "/workspace/k4c210/repo")
sys.path.insert(0, os.path.join(REPO, "tools", "cycle209")); sys.path.insert(0, os.path.join(REPO, "tools", "cycle204"))
import lib209 as Q
import lib204 as M
import z3
L = M.L; P = 8; BAR = 0.00625; T0 = time.time()
def log(*a): print(*a, f"[{time.time()-T0:.1f}s]", flush=True)
SUP, OUT = sys.argv[1], sys.argv[2]
R = {}
AZ = L.AZ; pairs = Q.crib_pairs(L.K4)

def z3_status(extra):
    s = z3.Solver(); f = [z3.Int(f"f{i}") for i in range(26)]; g = [z3.Int(f"g{i}") for i in range(26)]; k = [z3.Int(f"k{i}") for i in range(P)]
    for v in f + g + k: s.add(v >= 0, v <= 25)
    s.add(z3.Distinct(f)); s.add(z3.Distinct(g)); s.add(f[pairs[0][1]] == 0)
    allp = pairs + extra
    for pos, p, c in allp:
        b = z3.Int(f"b{pos}_{p}_{c}"); s.add(b >= 0, b <= 1); s.add(g[c] == f[p] + k[pos % P] - 26 * b)
    r = s.check()
    if r == z3.sat:
        m = s.model(); fv = [m[v].as_long() for v in f]; gv = [m[v].as_long() for v in g]; kv = [m[v].as_long() for v in k]
        ok = len(set(fv)) == 26 and len(set(gv)) == 26 and all(gv[c] == (fv[p] + kv[pos % P]) % 26 for pos, p, c in allp)
        return "SAT", ok
    return ("UNSAT" if r == z3.unsat else "UNKNOWN"), None

M3 = Q.c3_mask_for(P, L.K4)
mk = json.load(open(os.path.join(REPO, "tools", "cycle209", "mask209_P8.json")))["8"]
ban81 = [(x, AZ.index(ch)) for x, ch in mk["extra_bans"]]
TIMEOUTS = [(37, "T"), (50, "C"), (50, "E"), (50, "T")]
ban4 = [(x, AZ.index(ch)) for x, ch in TIMEOUTS]
M81 = M3.copy(); M85 = M3.copy()
for x, p in ban81: M81[x, p] = False; M85[x, p] = False
for x, p in ban4: assert M81[x, p]; M85[x, p] = False
q = lambda x, p: (x, p, AZ.index(L.K4[x]))
zr = {}
zr["timeouts"] = {f"{x}{AZ[p]}": z3_status([q(x, p)])[0] for x, p in ban4}
rr = np.random.default_rng([209212, 99])
samp_ban = [ban81[i] for i in rr.choice(len(ban81), 6, replace=False)]
zr["sampled_bans"] = {f"{x}{AZ[p]}": z3_status([q(x, p)])[0] for x, p in samp_ban}
zr["pos43"] = {AZ[p]: z3_status([q(43, p)])[0] for p in np.flatnonzero(M3[43])}
allowed = [(x, p) for x in range(97) if x not in L.CRIBPOS for p in np.flatnonzero(M85[x]) if M85[x].sum() > 1]
samp_ok = [allowed[i] for i in rr.choice(len(allowed), 6, replace=False)]
zr["sampled_allowed"] = {f"{x}{AZ[p]}": z3_status([q(x, p)]) for x, p in samp_ok}
gz = (all(v == "UNSAT" for v in zr["timeouts"].values()) and all(v == "UNSAT" for v in zr["sampled_bans"].values())
      and [a for a, v in zr["pos43"].items() if v == "SAT"] == ["T"] and all(v == ("SAT", True) for v in zr["sampled_allowed"].values()))
R["gate_Z"] = dict(pass_=bool(gz), **zr); log("Z", gz, zr)
forced = sorted(x for x in range(97) if x not in L.CRIBPOS and M85[x].sum() == 1)
gm = int(M81.sum()) == 1517 and int(M85.sum()) == 1513 and forced == [35, 41, 43, 46, 61, 78]
R["gate_M"] = dict(pass_=bool(gm), allowed81=int(M81.sum()), allowed85=int(M85.sum()), forced85=forced); log("M", R["gate_M"])

TXT = M.load(SUP); ZK = float(M.z_exact(M.K4X[None], P)[0])
def zplants(seedblock, tag, mi, mask, pool, n):
    r = np.random.default_rng([seedblock, tag, mi, P]); ch3 = M.model_chain(TXT, M.REG_MODELS[mi], 3)
    X = M.ffbs(r, *ch3, mask, n); Y = Q.qiv_encipher_pool(r, X, pool, P)
    assert (L.col(X, P) == L.col(Y, P)).all() and mask[np.arange(M.N), X].all()
    fpos = list(L.CRIBPOS) + [x for x in forced]
    assert (Y[:, list(L.CRIBPOS)] == M.K4X[list(L.CRIBPOS)][None, :]).all()
    return M.z_exact(Y, P)
# gate R (I-283)
pool9, _ = Q.key_pool(P, L.K4, [[209211, 3, P, d] for d in range(256)])
mJ = M.REG_MODELS.index("JEX")
qr = M.mc_q(zplants(209211, 10, mJ, M81, pool9, 10000), ZK)
R["gate_R"] = dict(q=qr, case196=0.007499250074992501, pass_=bool(abs(qr - 0.007499250074992501) < 1e-12)); log("R", R["gate_R"])
if os.environ.get("REPRO_ONLY") == "1" or not (gz and gm and R["gate_R"]["pass_"]):
    R["label"] = "gates only" if os.environ.get("REPRO_ONLY") == "1" else "NO VERDICT (gate fail)"
    json.dump(R, open(OUT, "w"), indent=1, default=str); log("stop", R["label"]); sys.exit(0)
SB = 209212
pool, nsol = Q.key_pool(P, L.K4, [[SB, 3, P, d] for d in range(256)]); R["pool"] = dict(solutions=nsol, distinct=len(pool))
res = {}
for mi, name in enumerate(M.REG_MODELS):
    z85 = zplants(SB, 10, mi, M85, pool, 10000); z81 = zplants(SB, 10, mi, M81, pool, 10000)
    res[name] = dict(q85=M.mc_q(z85, ZK), q81_paired=M.mc_q(z81, ZK), mean85=float(z85.mean()), mean81=float(z81.mean()))
    log("model", name, res[name])
R["models"] = res
worst = max(res, key=lambda m: res[m]["q85"]); mi = M.REG_MODELS.index(worst)
zz = zplants(SB, 10, mi, M85, pool, 10000); looks = []
for look, (tag, add) in enumerate([(None, 0), (11, 30000), (12, 120000)]):
    if tag is not None: zz = np.concatenate([zz, zplants(SB, tag, mi, M85, pool, add)])
    qq = M.mc_q(zz, ZK); others = max(res[m]["q85"] for m in res if m != worst)
    se = math.sqrt(qq * (1 - qq) / len(zz)); qd = max(qq, others); sed = se if qd == qq else math.sqrt(others * (1 - others) / 10000)
    looks.append(dict(n=len(zz), q=qq, se=se, qd=qd, sed=sed)); log("look", looks[-1])
    if abs(qd - BAR) >= 2 * sed: break
lk = looks[-1]
label = ("STAT-DISFAVOURED (carries to Quagmire IV at P 8)" if lk["qd"] <= BAR - 2 * lk["sed"] else
         "LOW-POWER for Quagmire IV at P 8" if lk["qd"] >= BAR + 2 * lk["sed"] else "UNRESOLVED (boundary band)")
R["decision"] = dict(worst=worst, looks=looks, bar=BAR, label=label)
json.dump(R, open(OUT, "w"), indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o)); log("decision", R["decision"])
