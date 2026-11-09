"""Cycle 176 summary: per (model, ix, L) counts for K4 and the 19 nulls, labels, and the pre-registered 5-cell Poisson grid.
usage: summarize176.py outdir nulls176.txt"""
import sys, glob, math, collections
od, nf = sys.argv[1], sys.argv[2]
nulls = [l.split()[0] for l in open(nf)]
def H(fn):
    c = collections.Counter(); 
    try: lines = open(fn).read().split("\n")
    except FileNotFoundError: return None
    if not any(l.startswith("END") for l in lines): return None
    for l in lines:
        a = l.split()
        if not a or a[0] != "H": continue
        if len(a) == 9: c[(int(a[2]), int(a[3]))] += int(a[8])            # gm176: H lab ix L pa form nprim cfg fits
        else: c[(int(a[2]), a[3])] += int(a[6])                             # pg176: H lab ix form nc tests fits
    return c
def tot(c, keys): return None if c is None else sum(v for k, v in c.items() if k in keys)
T = ["k4"] + nulls
R = {}
for t in T:
    g0 = H(f"{od}/{t}.g0.txt"); g0L8 = H(f"{od}/{t}.g0L8.txt") if t != "k4" else g0
    g1 = H(f"{od}/{'k4s8' if t=='k4' else t}.g1.txt"); w0 = H(f"{od}/{t}.w0.txt"); w1 = H(f"{od}/{'k4s8' if t=='k4' else t}.w1.txt")
    pg0 = H(f"{od}/{t}.pg0.txt"); pg1 = H(f"{od}/{t}.pg1.txt")
    R[t] = dict(g0=g0, g0L8=g0L8, g1=g1, w0=w0, w1=w1, pg0=pg0, pg1=pg1)
print("== per-L counts, model G ix 0 (full perms; L 8: K4 + first 9 nulls)")
for L in range(2, 9):
    k = tot(R["k4"]["g0"], {(0, L)}); src = "g0L8" if L == 8 else "g0"
    nv = [tot(R[t][src], {(0, L)}) for t in nulls]; nv = [x for x in nv if x is not None]
    print(f"L{L} K4 {k} nulls n={len(nv)} min/med/max {min(nv) if nv else '-'}/{sorted(nv)[len(nv)//2] if nv else '-'}/{max(nv) if nv else '-'} mean {sum(nv)/max(1,len(nv)):.2f} ge_K4 {sum(x>=k for x in nv)}")
print("== model G ix 1 (1/8 perms; K4 full in brackets)")
k4full = H(f"{od}/k4.g1.txt")
for L in range(2, 6):
    k = tot(R["k4"]["g1"], {(1, L)}); nv = [tot(R[t]["g1"], {(1, L)}) for t in nulls]; nv = [x for x in nv if x is not None]
    print(f"L{L} K4s8 {k} [K4 full {tot(k4full,{(1,L)})}] nulls n={len(nv)} min/med/max {min(nv)}/{sorted(nv)[len(nv)//2]}/{max(nv)} mean {sum(nv)/len(nv):.2f}")
cells = {
 "C1 G ix0 L2-6": lambda r: tot(r["g0"], {(0, L) for L in range(2, 7)}),
 "C2 G ix0 L7": lambda r: tot(r["g0"], {(0, 7)}),
 "C3 G ix1 L2-5 (1/8)": lambda r: tot(r["g1"], {(1, L) for L in range(2, 6)}),
 "C4 named primers ix0+ix1(1/8)": lambda r: None if r["w0"] is None or r["w1"] is None else tot(r["w0"], {(0, -1)}) + tot(r["w1"], {(1, -1)}),
 "C5 PG both ix": lambda r: None if r["pg0"] is None or r["pg1"] is None else sum(r["pg0"].values()) + sum(r["pg1"].values()),
}
X = {c: {t: f(R[t]) for t in T} for c, f in cells.items()}
def pois_ge(x, lam):
    if x <= 0: return 1.0
    if lam == 0: return 0.0
    return max(0.0, 1 - sum(math.exp(-lam) * lam ** i / math.factorial(i) for i in range(x)))
def pois_le(x, lam): return min(1.0, sum(math.exp(-lam) * lam ** i / math.factorial(i) for i in range(x + 1)))
print("== grid (leave-one-out Poisson tails)")
Gp = {t: 1.0 for t in T}; Gm = {t: 1.0 for t in T}
for c in cells:
    v = X[c]; ok = all(v[t] is not None for t in T)
    if not ok: print(c, "INCOMPLETE", v); continue
    scored = any(v[t] for t in T)
    lam = {t: sum(v[u] for u in T if u != t) / (len(T) - 1) for t in T}
    if scored:
        for t in T: Gp[t] = min(Gp[t], pois_ge(v[t], lam[t])); Gm[t] = min(Gm[t], pois_le(v[t], lam[t]))
    nv = [v[t] for t in nulls]
    print(f"{c}: K4 {v['k4']} nulls min/med/max {min(nv)}/{sorted(nv)[9]}/{max(nv)} scored={scored} K4 p+ {pois_ge(v['k4'],lam['k4']):.3f} p- {pois_le(v['k4'],lam['k4']):.3f}")
pp = sum(Gp[t] <= Gp["k4"] for t in T) / len(T); pm = sum(Gm[t] <= Gm["k4"] for t in T) / len(T)
print(f"G+(K4) {Gp['k4']:.3g} grid p+ {pp:.2f} ; G-(K4) {Gm['k4']:.3g} grid p- {pm:.2f} ; best attainable {1/len(T):.2f}")
