"""Cycle 177 summary: per (model, ix, L) counts for K4 and the 19 nulls (one-error-only fits for G1/PG1, strict fits for GB),
labels, and the pre-registered 6-cell leave-one-out Poisson grid (I-120 rule).   usage: summarize177.py outdir nulls177.txt"""
import sys, math, collections
od, nf = sys.argv[1], sys.argv[2]
nulls = [l.split()[0] for l in open(nf)]
def H(fn):
    c = collections.Counter()
    try: lines = open(fn).read().split("\n")
    except FileNotFoundError: return None
    if not any(l.startswith("END") or l.startswith("ALLEND") for l in lines[-3:]): return None
    for l in lines:
        a = l.split()
        if not a or a[0] != "H": continue
        if len(a) == 12:                                  # gm177: H lab ix L pa form base err nprim cfg strict onlyone
            ix, L, b, err = int(a[2]), int(a[3]), int(a[6]), int(a[7]); c[(ix, L, b)] += int(a[11]) if err else int(a[10])
            if err: c[("strict", ix, L, b)] += int(a[10])
        else: c[("pg", int(a[2]))] += int(a[7]); c[("pgstrict", int(a[2]))] += int(a[6])
    return c
def tot(c, keys): return None if c is None else sum(v for k, v in c.items() if k in keys)
T = ["k4"] + nulls; R = {}
for t in T:
    s8 = "k4s8" if t == "k4" else t
    R[t] = dict(g0=H(f"{od}/{t}.g0e.txt"), g1=H(f"{od}/{s8}.g1e.txt"), w0=H(f"{od}/{t}.w0e.txt"), w1=H(f"{od}/{s8}.w1e.txt"),
                pg0=H(f"{od}/{t}.pg0e.txt"), pg1=H(f"{od}/{t}.pg1e.txt"), b0=H(f"{od}/{t}.b0.txt"), b1=H(f"{od}/{s8}.b1.txt"))
K4F = dict(g1=H(f"{od}/k4.g1e.txt"), w1=H(f"{od}/k4.w1e.txt"), b1=H(f"{od}/k4.b1.txt"))
def row(name, k, nv, extra=""):
    nv = [x for x in nv if x is not None]
    if not nv: print(name, "K4", k, "no nulls"); return
    m = sum(nv) / len(nv)
    lab = ("EXACT-EXCL" + (" (weak power)" if m < 1 else "")) if k == 0 else ("FLAG above all nulls" if k > max(nv) else "LOW-POWER")
    print(f"{name}: K4 {k}{extra} nulls n={len(nv)} min/med/max {min(nv)}/{sorted(nv)[len(nv)//2]}/{max(nv)} mean {m:.2f} ge_K4 {sum(x>=k for x in nv)} -> {lab}")
print("== G1 one-error-only, ix 0 (full perms)   [strict fits in brackets]")
for L in range(2, 7):
    row(f"G1 ix0 L{L}", tot(R["k4"]["g0"], {(0, L, 10)}), [tot(R[t]["g0"], {(0, L, 10)}) for t in nulls], f" [strict {tot(R['k4']['g0'], {('strict', 0, L, 10)})}]")
print("== G1 one-error-only, ix 1 (1/8 perms; K4 full in brackets)")
for L in range(2, 6):
    row(f"G1 ix1 L{L}", tot(R["k4"]["g1"], {(1, L, 10)}), [tot(R[t]["g1"], {(1, L, 10)}) for t in nulls], f" [K4 full {tot(K4F['g1'], {(1, L, 10)})}]")
print("== named primers, one-error-only")
row("W ix0 (full)", tot(R["k4"]["w0"], {(0, -1, 10)}), [tot(R[t]["w0"], {(0, -1, 10)}) for t in nulls])
row("W ix1 (1/8)", tot(R["k4"]["w1"], {(1, -1, 10)}), [tot(R[t]["w1"], {(1, -1, 10)}) for t in nulls], f" [K4 full {tot(K4F['w1'], {(1, -1, 10)})}]")
print("== PG1 one-error-only (>= 23/24, not 24)")
for ix in (0, 1): row(f"PG1 ix{ix}", tot(R["k4"][f"pg{ix}"], {("pg", ix)}), [tot(R[t][f"pg{ix}"], {("pg", ix)}) for t in nulls])
print("== GB strict, bases 5-9")
for b in range(5, 10):
    for L in range(2, 8):
        row(f"GB b{b} ix0 L{L}", tot(R["k4"]["b0"], {(0, L, b)}), [tot(R[t]["b0"], {(0, L, b)}) for t in nulls])
    for L in range(2, 5):
        row(f"GB b{b} ix1 L{L} (1/8)", tot(R["k4"]["b1"], {(1, L, b)}), [tot(R[t]["b1"], {(1, L, b)}) for t in nulls], f" [K4 full {tot(K4F['b1'], {(1, L, b)})}]")
cells = {
 "C1 G1 ix0 L2-5": lambda r: tot(r["g0"], {(0, L, 10) for L in range(2, 6)}),
 "C2 G1 ix0 L6": lambda r: tot(r["g0"], {(0, 6, 10)}),
 "C3 G1 ix1 L2-5 (1/8)": lambda r: tot(r["g1"], {(1, L, 10) for L in range(2, 6)}),
 "C4 named G1 ix0+ix1(1/8)": lambda r: None if r["w0"] is None or r["w1"] is None else tot(r["w0"], {(0, -1, 10)}) + tot(r["w1"], {(1, -1, 10)}),
 "C5 PG1 both ix": lambda r: None if r["pg0"] is None or r["pg1"] is None else tot(r["pg0"], {("pg", 0)}) + tot(r["pg1"], {("pg", 1)}),
 "C6 GB ix0 L2-7 + ix1 L2-4 (1/8)": lambda r: None if r["b0"] is None or r["b1"] is None else tot(r["b0"], {(0, L, b) for L in range(2, 8) for b in range(5, 10)}) + tot(r["b1"], {(1, L, b) for L in range(2, 5) for b in range(5, 10)}),
}
X = {c: {t: f(R[t]) for t in T} for c, f in cells.items()}
def pmf(i, lam): return math.exp(-lam + i * math.log(lam) - math.lgamma(i + 1)) if lam > 0 else float(i == 0)
def pois_ge(x, lam):
    if x <= 0: return 1.0
    if lam == 0: return 0.0
    return max(0.0, 1 - sum(pmf(i, lam) for i in range(x)))
def pois_le(x, lam): return min(1.0, sum(pmf(i, lam) for i in range(x + 1)))
print("== grid (leave-one-out Poisson tails, I-120)")
Gp = {t: 1.0 for t in T}; Gm = {t: 1.0 for t in T}
for c in cells:
    v = X[c]
    if not all(v[t] is not None for t in T): print(c, "INCOMPLETE", v); continue
    scored = any(v[t] for t in T)
    lam = {t: sum(v[u] for u in T if u != t) / (len(T) - 1) for t in T}
    if scored:
        for t in T: Gp[t] = min(Gp[t], pois_ge(v[t], lam[t])); Gm[t] = min(Gm[t], pois_le(v[t], lam[t]))
    nv = [v[t] for t in nulls]
    print(f"{c}: K4 {v['k4']} nulls min/med/max {min(nv)}/{sorted(nv)[9]}/{max(nv)} scored={scored} K4 p+ {pois_ge(v['k4'],lam['k4']):.3f} p- {pois_le(v['k4'],lam['k4']):.3f}")
pp = sum(Gp[t] <= Gp["k4"] for t in T) / len(T); pm = sum(Gm[t] <= Gm["k4"] for t in T) / len(T)
print(f"G+(K4) {Gp['k4']:.3g} grid p+ {pp:.2f} ; G-(K4) {Gm['k4']:.3g} grid p- {pm:.2f} ; best attainable {1/len(T):.2f}")
