"""Timing / distribution probe on English plants only (never K4's letters or order). Seed base 202299 (probe only)."""
import time, sys, numpy as np
import lib202 as M
L = M.L
TXT = L.load_models(sys.argv[1]); U = {m: L.unigram(t) for m, t in TXT.items()}; B = {m: M.bigram(t) for m, t in TXT.items()}
t0 = time.time()
for P in (8, 23):
    for m in ("JE", "JEX"):
        zc = []; zb = []
        for k in range(100):
            r = np.random.default_rng([202299, 1, P, k])
            x, y = L.plant(r, TXT[m], P, 3, 0, U[m]); zc.append(L.own_z(y, P, 300, [202299, 2, P, k])[1])
            x, y = M.plant_c3b(r, TXT[m], P, B[m], U[m]); zb.append(L.own_z(y, P, 300, [202299, 3, P, k])[1])
        print(P, m, "C3 zcol mean %.2f sd %.2f q05 %.2f | C3b mean %.2f q05 %.2f" % (np.mean(zc), np.std(zc), np.quantile(zc, .05), np.mean(zb), np.quantile(zb, .05)))
print("seconds for 800 plants (1 proc)", round(time.time() - t0, 1))
