"""timing / soundness probe on ONE planted QIV ciphertext (probe seed [209000,1]); K4 not touched."""
import time, sys, numpy as np
sys.path.insert(0, "/workspace/k4c209"); import lib209 as Q, lib201 as L
x = L.enc(L._letters(open("/workspace/k4c209/sup/rk_plain.txt", errors="ignore").read()))
r = np.random.default_rng([209000, 1])
w, ct = Q.qiv_plant(r, x, 8)
t = time.time(); M, st = Q.c4_mask(8, ct); dt = time.time() - t
M3 = Q.c3_mask_for(8, ct)
print(st, "sec", round(dt, 1), "true allowed", int(M[np.arange(97), w].sum()), "subset", bool((M <= M3).all()))
