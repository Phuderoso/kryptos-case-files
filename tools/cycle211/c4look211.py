"""Cycle 211 add-on (IDEAS I-279, PREREG211 part B): worst-model (JEX) C4 conditioning at P 8 with the exact 85-ban mask
(case 196 addendum, cycle 210), large looks with FRESH seeds.  python3 c4look211.py SUP OUT.json
Gates: M (mask counts 1,517 / 1,513, forced {35,41,43,46,61,78}); R1 (81-ban, seed 209211 -> case 196 JEX tag-10 q 0.0074993 exactly);
R2 (85-ban, seed 209212 -> cycle 210 JEX tag-10 q 0.0056994 exactly).
Main: seed block 209216, fresh 256-key pool, JEX, 85-ban mask, chunks of 160,000 plants (tags 20..35).
Looks (I-265 x4): n = 640,000 (tags 20-23), 2,560,000 (tags 20-35); stop at the first look with |q - 0.00625| >= 2 SE.
q <= bar - 2SE -> STAT-DISFAVOURED (Quagmire IV at P 8, JEX worst model); >= bar + 2SE -> LOW-POWER; inside after 2 looks -> UNRESOLVED.
(The 10k other-model q's of cycle 210 are all below JEX, so only JEX is re-looked; registered.)"""
import sys, os, json, math, time
import numpy as np
REPO = os.environ.get("REPO", "/workspace/k4c211/repo")
sys.path.insert(0, os.path.join(REPO, "tools", "cycle209")); sys.path.insert(0, os.path.join(REPO, "tools", "cycle204"))
import lib209 as Q
import lib204 as M
L = M.L; P = 8; BAR = 0.00625; T0 = time.time()
def log(*a): print(*a, f"[{time.time()-T0:.1f}s]", flush=True)
SUP, OUT = sys.argv[1], sys.argv[2]
R = {}; AZ = L.AZ
M3 = Q.c3_mask_for(P, L.K4)
mk = json.load(open(os.path.join(REPO, "tools", "cycle209", "mask209_P8.json")))["8"]
ban81 = [(x, AZ.index(ch)) for x, ch in mk["extra_bans"]]
ban4 = [(x, AZ.index(ch)) for x, ch in [(37, "T"), (50, "C"), (50, "E"), (50, "T")]]
M81 = M3.copy(); M85 = M3.copy()
for x, p in ban81: M81[x, p] = False; M85[x, p] = False
for x, p in ban4: M85[x, p] = False
forced = sorted(x for x in range(97) if x not in L.CRIBPOS and M85[x].sum() == 1)
gm = int(M81.sum()) == 1517 and int(M85.sum()) == 1513 and forced == [35, 41, 43, 46, 61, 78]
R["gate_M"] = dict(pass_=bool(gm), allowed81=int(M81.sum()), allowed85=int(M85.sum()), forced85=forced); log("M", R["gate_M"])
TXT = M.load(SUP); ZK = float(M.z_exact(M.K4X[None], P)[0])
mJ = M.REG_MODELS.index("JEX")
def zplants(seedblock, tag, mi, mask, pool, n):
    r = np.random.default_rng([seedblock, tag, mi, P]); ch3 = M.model_chain(TXT, M.REG_MODELS[mi], 3)
    X = M.ffbs(r, *ch3, mask, n); Y = Q.qiv_encipher_pool(r, X, pool, P)
    assert (L.col(X, P) == L.col(Y, P)).all() and mask[np.arange(M.N), X].all()
    assert (Y[:, list(L.CRIBPOS)] == M.K4X[list(L.CRIBPOS)][None, :]).all()
    return M.z_exact(Y, P)
pool9, _ = Q.key_pool(P, L.K4, [[209211, 3, P, d] for d in range(256)])
q1 = M.mc_q(zplants(209211, 10, mJ, M81, pool9, 10000), ZK)
pool12, _ = Q.key_pool(P, L.K4, [[209212, 3, P, d] for d in range(256)])
q2 = M.mc_q(zplants(209212, 10, mJ, M85, pool12, 10000), ZK)
R["gate_R1"] = dict(q=q1, case196=0.007499250074992501, pass_=bool(abs(q1 - 0.007499250074992501) < 1e-12))
R["gate_R2"] = dict(q=q2, cycle210=0.005699430056994301, pass_=bool(abs(q2 - 0.005699430056994301) < 1e-12)); log("R", R["gate_R1"], R["gate_R2"])
if not (gm and R["gate_R1"]["pass_"] and R["gate_R2"]["pass_"]):
    R["label"] = "NO VERDICT (gate fail)"; json.dump(R, open(OUT, "w"), indent=1, default=str); log("stop"); sys.exit(0)
SB = 209216
pool, nsol = Q.key_pool(P, L.K4, [[SB, 3, P, d] for d in range(256)]); R["pool"] = dict(solutions=nsol, distinct=len(pool))
zs = []; looks = []; WALL = float(os.environ.get("WALL", "330"))
for tag in range(20, 36):
    if time.time() - T0 > WALL: R["wall_stop"] = f"stopped before tag {tag} (wall {WALL}s)"; break
    zs.append(zplants(SB, tag, mJ, M85, pool, 160000)); log("chunk", tag)
    if tag in (23, 35):
        zz = np.concatenate(zs); qq = M.mc_q(zz, ZK); se = math.sqrt(qq * (1 - qq) / len(zz))
        looks.append(dict(n=len(zz), q=qq, se=se)); log("look", looks[-1])
        if abs(qq - BAR) >= 2 * se: break
if not looks or (looks[-1]["n"] < 640000):
    zz = np.concatenate(zs) if zs else np.zeros(0); R["label"] = "NO VERDICT (wall before first look)"
else:
    lk = looks[-1]
    R["label"] = ("STAT-DISFAVOURED (Quagmire IV at P 8, worst model JEX)" if lk["q"] <= BAR - 2 * lk["se"] else
                  "LOW-POWER for Quagmire IV at P 8" if lk["q"] >= BAR + 2 * lk["se"] else "UNRESOLVED (boundary band)")
    if lk["n"] < 2560000 and abs(lk["q"] - BAR) < 2 * lk["se"]: R["label"] = "UNRESOLVED (boundary band; look 2 not reached: wall)"
R["decision"] = dict(model="JEX", seed_block=SB, looks=looks, bar=BAR)
json.dump(R, open(OUT, "w"), indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o)); log("decision", R["label"], looks)
