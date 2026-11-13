"""Cycle 209 run 2 erratum: the PREREG209b boundary-band extension in run209.py drew the 30,000 extra references but scored z on the
plaintext (the run-1 bug survived in the extension branch only).  This script re-does ONLY that step as registered: worst model (JEX),
P 8, tag 10 (must reproduce run 2's q 0.0074993 exactly) + tag 11 (30,000 new), enciphered with the same 256-key pool, z on Y.
Decision rule unchanged (PREREG209 / 209b)."""
import sys, os, json, math, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib209 as Q
import lib204 as M
L = M.L
SB, P, NREF, BAR = 209211, 8, 10000, 0.00625
def rng(*t): return np.random.default_rng([SB, *t])
TXT = M.load(sys.argv[1]); R2 = json.load(open("results209b.json"))
MK, st = Q.c4_mask(P, L.K4)
pool, nsol = Q.key_pool(P, L.K4, [[SB, 3, P, d] for d in range(256)])
mi = M.REG_MODELS.index("JEX"); ch3 = M.model_chain(TXT, "JEX", 3)
ZK = float(M.z_exact(M.K4X[None], P)[0])
def make(tag, n):
    r = rng(tag, mi, P); X = M.ffbs(r, *ch3, MK, n); Y = Q.qiv_encipher_pool(r, X, pool, P)
    assert (L.col(X, P) == L.col(Y, P)).all() and MK[np.arange(M.N), X].all()
    return M.z_exact(Y, P)
z10 = make(10, NREF); q10 = M.mc_q(z10, ZK)
repro = abs(q10 - R2["plants"]["JEX"]["8"]["q_c4"]) < 1e-12
z11 = make(11, 3 * NREF); zz = np.concatenate([z10, z11])
q = M.mc_q(zz, ZK); se = math.sqrt(q * (1 - q) / len(zz))
others = max(R2["plants"][m]["8"]["q_c4"] for m in M.REG_MODELS if m != "JEX")
qd = max(q, others); sed = se if qd == q else math.sqrt(others * (1 - others) / NREF)
label = ("STAT-DISFAVOURED (carries to Quagmire IV at P 8)" if qd <= BAR - 2 * sed else
         "LOW-POWER for Quagmire IV at P 8 (H_8 verdict does not transfer)" if qd >= BAR + 2 * sed else "UNRESOLVED (boundary band)")
out = dict(mask_stats=st, mask_same_as_run2=st == R2["K4"]["8"] if False else None, pool_distinct=len(pool), q_tag10=q10,
           reproduces_run2=bool(repro), q_tag11_only=M.mc_q(z11, ZK), n=len(zz), q_ext=q, se_ext=se, other_models_max=others,
           qstar_decision=qd, se_decision=sed, bar=BAR, label=label if repro else "NO VERDICT (tag-10 reproduction failed)")
json.dump(out, open("results209b_ext.json", "w"), indent=1, default=float); print(out)
