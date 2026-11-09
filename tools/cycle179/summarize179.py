"""Cycle 179 summary: per-cell one-error fit counts for K4 and 19 nulls, strict fits, labels, I-120 grid.
usage: summarize179.py outdir nulls179.txt"""
import sys, math, collections
od = sys.argv[1]; nulls = [l.split()[0] for l in open(sys.argv[2])]; T = ["k4"] + nulls
def load(t, f):
    R = collections.Counter()
    try: lines = open(f"{od}/{t}.{f}.txt").read().strip().split("\n")
    except FileNotFoundError: return None
    assert lines[-1].startswith("END"), (t, f)
    for l in lines:
        a = l.split()
        if a[0] == "H":
            L = int(a[3]); R[("fit", L)] += int(a[11]); R[("strict", L)] += int(a[13]); R[("p2", L)] += int(a[9]); R[("slots", L)] += int(a[15]); R[("ovf", L)] += int(a[17])
    return R
D = {t: {f: load(t, f) for f in ("m0", "m1", "m1s8")} for t in T}; K4L5 = load("k4", "m1L5")
g = lambda t, f, k: D[t][f][k] if D[t][f] else 0
def row(name, k4, nv, extra=""):
    lab = "EXACT-EXCL" if k4 == 0 else ("LOW-POWER" if k4 <= max(nv) else "FLAG (above every null)")
    print(f"{name}: K4 {k4} | nulls min/med/max {min(nv)}/{sorted(nv)[9]}/{max(nv)} | {lab}{extra}")
print("== M0 one-error (key on the plaintext index), full all.bin")
for L in range(1, 9): row(f"M0 L{L}", g("k4", "m0", ("fit", L)), [g(t, "m0", ("fit", L)) for t in nulls],
    f" [strict K4 {g('k4','m0',('strict',L))}; pass2any K4 {g('k4','m0',('p2',L))}, null mean {sum(g(t,'m0',('p2',L)) for t in nulls)/19:.0f}]")
print("== M1 one-error (key on the carved index), L 1-4 full")
for L in range(1, 5): row(f"M1 L{L}", g("k4", "m1", ("fit", L)), [g(t, "m1", ("fit", L)) for t in nulls],
    f" [pass2any K4 {g('k4','m1',('p2',L))}, null mean {sum(g(t,'m1',('p2',L)) for t in nulls)/19:.0f}]")
row("M1 L5 (all_s8)", g("k4", "m1s8", ("fit", 5)), [g(t, "m1s8", ("fit", 5)) for t in nulls], f" [pass2any K4 {g('k4','m1s8',('p2',5))}]")
print(f"M1 L5 K4 full all.bin: fits {K4L5[('fit',5)]} pass2any {K4L5[('p2',5)]}")
ov = sum(v for t in T for f in ("m0", "m1", "m1s8") if D[t][f] for k, v in D[t][f].items() if k[0] == "ovf") + sum(v for k, v in K4L5.items() if k[0] == "ovf")
print("overflow lines (all texts):", ov)
cells = {"R1 M0 L1-8 fits": lambda t: sum(g(t, "m0", ("fit", L)) for L in range(1, 9)),
 "R2 M1 L1-4 fits": lambda t: sum(g(t, "m1", ("fit", L)) for L in range(1, 5)),
 "R3 M1 L5 fits (1/8)": lambda t: g(t, "m1s8", ("fit", 5)),
 "D1 M0 pass2any L6-8": lambda t: sum(g(t, "m0", ("p2", L)) for L in (6, 7, 8)),
 "D2 M1 pass2any L1-4 + L5(1/8)": lambda t: sum(g(t, "m1", ("p2", L)) for L in range(1, 5)) + g(t, "m1s8", ("p2", 5))}
X = {c: {t: f(t) for t in T} for c, f in cells.items()}
def pmf(i, lam): return math.exp(-lam + i * math.log(lam) - math.lgamma(i + 1)) if lam > 0 else float(i == 0)
def pge(x, lam): return 1.0 if x <= 0 else (0.0 if lam == 0 else max(0.0, 1 - sum(pmf(i, lam) for i in range(x))))
def ple(x, lam): return min(1.0, sum(pmf(i, lam) for i in range(x + 1)))
print("== grid (leave-one-out Poisson tails, I-120)")
Gp = {t: 1.0 for t in T}; Gm = {t: 1.0 for t in T}
for c in cells:
    v = X[c]; scored = any(v[t] for t in T); lam = {t: sum(v[u] for u in T if u != t) / (len(T) - 1) for t in T}
    if scored:
        for t in T: Gp[t] = min(Gp[t], pge(v[t], lam[t])); Gm[t] = min(Gm[t], ple(v[t], lam[t]))
    nv = [v[t] for t in nulls]
    print(f"{c}: K4 {v['k4']} nulls min/med/max {min(nv)}/{sorted(nv)[9]}/{max(nv)} scored={scored} K4 p+ {pge(v['k4'],lam['k4']):.3f} p- {ple(v['k4'],lam['k4']):.3f}")
pp = sum(Gp[t] <= Gp["k4"] for t in T) / len(T); pm = sum(Gm[t] <= Gm["k4"] for t in T) / len(T)
print(f"G+(K4) {Gp['k4']:.3g} grid p+ {pp:.2f} ; G-(K4) {Gm['k4']:.3g} grid p- {pm:.2f} ; best attainable {1/len(T):.2f}")
