"""Model-A power: number of independent exact checks for each (w, o) (text-independent)."""
import json
cpos = list(range(21, 34)) + list(range(63, 74))
res = {}
for w in range(2, 49):
    for o in range(w):
        par = {}
        def f(x):
            while par.setdefault(x, x) != x: x = par[x]
            return x
        ck = 0
        for i in cpos:
            q = i + o; u, v = f(("c", q % w)), f(("r", q // w))
            if u == v: ck += 1
            else: par[u] = v
        res[f"{w},{o}"] = ck
json.dump(res, open("power77_modelA.json", "w"))
for w in range(2, 49):
    v = [res[f"{w},{o}"] for o in range(w)]
    print(w, min(v), max(v))
