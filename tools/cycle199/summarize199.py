"""Cycle 199 summary: per-cell fits vs E for chunk 1 (registered PREREG199 classification) and the grid statistic."""
import glob, os, sys
O = sys.argv[1] if len(sys.argv) > 1 else "/workspace/k4c199/work/run"
FAC = {"del": 166142 / 24000, "ins": 165786 / 24000}
for kind in ("del", "ins"):
    fn = f"{O}/k4_B_{kind}_c1.txt"; H = []; M = []
    for l in open(fn):
        p = l.split()
        if l.startswith("H B"): H.append((p[3], p[4], p[5], int(p[6]), int(p[7]), int(p[9]), float(p[11])))
        elif l.startswith("M B"): M.append(p)
    bank = [h for h in H if h[6] * FAC[kind] <= 0.05]; chunk = [h for h in H if h[6] <= 0.05 and h not in bank]; low = [h for h in H if h[6] > 0.05]
    for nm, S in (("full-power (bank)", bank), ("full-power (chunk only)", chunk), ("LOW-POWER", low)):
        print(f"{kind} {nm}: cells {len(S)} fits {sum(h[5] for h in S)} vs E {sum(h[6] for h in S):.3f}")
    fp = {(h[0], h[1], h[2], h[3], h[4]) for h in bank + chunk}
    print(f"{kind} printed fits (E_config<=0.002): {len(M)}; in full-power cells:")
    for p in M:
        if (p[5], p[6], p[7], int(p[8]), int(p[9])) in fp: print("  ", " ".join(p))
    M.sort(key=lambda p: float(p[10])); print(f"{kind} strongest 20:"); [print("  ", " ".join(p)) for p in M[:20]]
def grid(lab):
    n = 0
    for kind in ("del", "ins"):
        cl = set()
        for l in open(f"{O}/g_{kind}_{lab}.txt"):
            if l.startswith("M B") and float(l.split()[10]) <= 26 ** -3:
                p = l.split(); cl.add((p[3], p[5], p[6], p[7]))
        n += len(cl)
    return n
g = {s: grid(s) for s in ["K4"] + [str(x) for x in range(19951, 19970)]}
k = g.pop("K4"); vals = sorted(g.values())
print("grid K4", k, "nulls", vals, "p+ (rank of K4 >= ) =", (1 + sum(v >= k for v in vals)) / 20, "p- =", (1 + sum(v <= k for v in vals)) / 20)
