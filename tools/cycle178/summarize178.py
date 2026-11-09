"""Cycle 178 summary: per-cell counts for K4 and the 19 nulls, labels, and the pre-registered 7-cell leave-one-out Poisson grid
(I-120 rule).  usage: summarize178.py outdir nulls178.txt"""
import sys, math, collections
od, nf = sys.argv[1], sys.argv[2]; nulls = [l.split()[0] for l in open(nf)]; T = ["k4"] + nulls
def H(fn):
    c = collections.Counter()
    try: lines = open(fn).read().strip().split("\n")
    except FileNotFoundError: return None
    if not lines[-1].startswith("END"): return None
    for l in lines:
        a = l.split()
        if a[0] == "H":
            if a[2] in ("0", "1"): c[("fit", a[2], int(a[3]))] += int(a[11]); c[("pass2", a[2], int(a[3]))] += int(a[9]); c[("sols", a[2], int(a[3]))] += int(a[13]); c[("ovf", a[2], int(a[3]))] += int(a[15])
            else: c[("fit", a[2], int(a[3]))] += int(a[11]); c[("streams", a[2], int(a[3]))] += int(a[7])
        elif a[0] == "O": c[("O", a[2], int(a[3]))] += 1
    return c
R = {t: {k: H(f"{od}/{t}.{k}.txt") for k in ("m0", "m1", "w0", "w1", "m0s8")} for t in T}
K4L9 = H(f"{od}/k4.m0L9.txt")
def g(t, f, key): r = R[t][f]; return None if r is None else r[key]
def row(name, k, nv, extra=""):
    nv = [x for x in nv if x is not None]
    m = sum(nv) / len(nv) if nv else float("nan")
    lab = ("EXACT-EXCL" + (" (null mean < 1: power from the analytic rate)" if m < 1 else "")) if k == 0 else ("FLAG above all nulls" if k > max(nv) else "LOW-POWER")
    print(f"{name}: K4 {k}{extra} | nulls n={len(nv)} min/med/max {min(nv)}/{sorted(nv)[len(nv)//2]}/{max(nv)} mean {m:.2f} -> {lab}")
print("== M0 ix 0 (algebraic), fits per L [mod-2 pass count]  (full perm set; L 9 on 1/8, K4 full in brackets)")
for L in range(1, 9): row(f"M0 L{L}", g("k4", "m0", ("fit", "0", L)), [g(t, "m0", ("fit", "0", L)) for t in nulls], f" [pass2 {g('k4','m0',('pass2','0',L))}, null pass2 mean {sum(g(t,'m0',('pass2','0',L)) for t in nulls)/19:.1f}]")
row("M0 L9 (1/8)", g("k4", "m0s8", ("fit", "0", 9)), [g(t, "m0s8", ("fit", "0", 9)) for t in nulls], f" [K4 full {K4L9[('fit','0',9)]}, pass2 1/8 {g('k4','m0s8',('pass2','0',9))}, null mean {sum(g(t,'m0s8',('pass2','0',9)) for t in nulls)/19:.1f}]")
print("== M1 ix 1 (CRT), fits per L [mod-2 pass]")
for L in range(1, 6): row(f"M1 L{L}", g("k4", "m1", ("fit", "1", L)), [g(t, "m1", ("fit", "1", L)) for t in nulls], f" [pass2 {g('k4','m1',('pass2','1',L))}, null pass2 mean {sum(g(t,'m1',('pass2','1',L)) for t in nulls)/19:.1f}]")
print("== W small weights, vocabulary seeds")
for w, f in (("W0", "w0"), ("W1", "w1")):
    for L in range(6, 11): row(f"{w} L{L}", g("k4", f, ("fit", w, L)), [g(t, f, ("fit", w, L)) for t in nulls], f" [streams {g('k4',f,('streams',w,L))}]")
ov = sum(v for t in T for f in ("m0", "m1", "m0s8") if R[t][f] for k, v in R[t][f].items() if k[0] in ("ovf", "O")) + sum(v for k, v in K4L9.items() if k[0] in ("ovf", "O"))
print("overflow / undetermined lines (all texts):", ov)
cells = {
 "R1 M0 L1-8 fits": lambda t: sum(g(t, "m0", ("fit", "0", L)) for L in range(1, 9)),
 "R2 M0 L9 fits (1/8)": lambda t: g(t, "m0s8", ("fit", "0", 9)),
 "R3 M1 L1-5 fits": lambda t: sum(g(t, "m1", ("fit", "1", L)) for L in range(1, 6)),
 "R4 W0 fits": lambda t: sum(g(t, "w0", ("fit", "W0", L)) for L in range(6, 11)),
 "R5 W1 fits": lambda t: sum(g(t, "w1", ("fit", "W1", L)) for L in range(6, 11)),
 "D1 M0 pass2 L7-8 + L9(1/8)": lambda t: sum(g(t, "m0", ("pass2", "0", L)) for L in (7, 8)) + g(t, "m0s8", ("pass2", "0", 9)),
 "D2 M1 pass2 L1-5": lambda t: sum(g(t, "m1", ("pass2", "1", L)) for L in range(1, 6)),
}
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
