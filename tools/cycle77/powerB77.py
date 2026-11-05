"""Model-B power: distribution of exact checks over (w, o) for a random sample of 300 family permutations."""
import json, random
import numpy as np
perms = np.fromfile("perms97.bin", dtype=np.int16).reshape(-1, 97)
cpos = list(range(21, 34)) + list(range(63, 74))
rng = random.Random(77); sample = rng.sample(range(1, len(perms)), 300)
byw = {w: [] for w in range(2, 49)}
for pi in sample:
    idx = [int(perms[pi][i]) for i in cpos]
    for w in range(2, 49):
        for o in range(w):
            par = {}
            def f(x):
                while par.setdefault(x, x) != x: x = par[x]
                return x
            ck = 0
            for i in idx:
                q = i + o; u, v = f(("c", q % w)), f(("r", q // w))
                if u == v: ck += 1
                else: par[u] = v
            byw[w].append(ck)
res = {w: dict(median=float(np.median(v)), frac_ge6=float(np.mean(np.array(v) >= 6))) for w, v in byw.items()}
json.dump(res, open("power77_modelB.json", "w"), indent=0)
for w, r in res.items(): print(w, r["median"], round(r["frac_ge6"], 3))
