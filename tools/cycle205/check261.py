"""Cycle 205, I-261 check of the Voynich desk's 10M-plant P 8 tail: 2,000,000 fresh JEX plants (seed block [205205, 3, c]),
same lib204 law (order-3 chain, FFBS on the C3 mask, exact-moment z). Independent seed, not independent code."""
import sys, json, math, time, numpy as np
sys.path.insert(0, '/workspace/k4c205/repo/tools/cycle204'); import lib204 as M
L = M.L; T0 = time.time(); TXT = M.load('/workspace/k4c205/sup'); Mk = M.mask(8); P = 8
ZK = float(M.z_exact(M.K4X[None], 8)[0]); assert abs(ZK + 1.3435124989412075) < 1e-12
ch = M.model_chain(TXT, 'JEX', 3); CH = 200_000; hits = 0; nn = 0; bl = []
for c in range(10):
    r = np.random.default_rng([205205, 3, c]); X = M.ffbs(r, *ch, Mk, CH); Y = M.encipher(r, X, P)
    if c == 0: assert (L.col(X, P) == L.col(Y, P)).all() and M.consistent_rows(Y, P).all()
    z = M.z_exact(Y, P); h = int((z <= ZK).sum()); hits += h; nn += CH; bl.append(h / CH)
    print(c, h, f'{time.time()-T0:.0f}s', flush=True)
p = hits / nn; se = math.sqrt(p*(1-p)/nn)
out = dict(model='JEX', n=nn, hits=hits, p=p, se=se, voynich_p=0.0054776, diff_in_se=(p-0.0054776)/math.sqrt(se**2+2.334e-5**2),
           margin_to_holm_in_se=(0.00625-p)/se, secs=time.time()-T0)
print(out); json.dump(out, open('check261.json','w'), indent=1)
