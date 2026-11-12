"""Probe (English only, never K4): chain fidelity vs real windows under case 189's C3 recipe, FFBS speed. Seed block 204299."""
import sys, time, numpy as np
import lib204 as M
T = M.load(sys.argv[1]); t0 = time.time()
for name in ["JE", "CARTER", "K123MIX", "JEX", "DRAC"]:
    for k in (3, 4):
        Tm, init = M.model_chain(T, name, k)
        rng = np.random.default_rng([204299, k, len(name)])
        P = 8; Mk = M.mask(P)
        X = M.ffbs(rng, Tm, init, Mk, 3000)
        assert Mk[np.arange(M.N), X].all()
        zx = M.z_exact(M.encipher(rng, X, P), P)
        Xc = M.c3_repair(rng, M.forward_sample(rng, Tm, init, 3000), P, M.L.unigram(T["JE" if name == "K123MIX" else name]))
        zc = M.z_exact(M.encipher(rng, Xc, P), P)
        src = T["K123"] if name == "K123MIX" else T[name]
        Xr = M.c3_repair(rng, M.windows(rng, src, 3000), P, M.L.unigram(src))
        zr = M.z_exact(M.encipher(rng, Xr, P), P)
        f = lambda z: f"mean {z.mean():.3f} q05 {np.quantile(z, .05):.3f}"
        print(name, k, "EXACT", f(zx), "| chainC3", f(zc), "| realC3", f(zr), f"[{time.time()-t0:.1f}s]", flush=True)
