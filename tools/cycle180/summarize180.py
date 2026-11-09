"""Cycle 180 summary: per-cell fit counts for K4 and 19 nulls, labels, I-120 grid (leave-one-out Poisson tails).
usage: summarize180.py outdir nulls180.txt"""
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
            L = int(a[3]); R[("fit", L)] += int(a[13]); R[("fit", L, a[4], a[5])] += int(a[13])
            if a[5] == "vig": R[("p2", L)] += int(a[11])          # mod-2 passes are form-independent: count once
        if a[0] == "O": R["ovf"] += int(a[3])
        if a[0] == "X": R["mismatch"] += 1
    return R
F = ("m0", "m1", "m1t", "m0s8", "m1s8")
D = {t: {f: load(t, f) for f in F} for t in T}
g = lambda t, f, k: (D[t][f] or {}).get(k, 0)
def row(name, k4, nv, extra=""):
    lab = "EXACT-EXCL" if k4 == 0 else ("LOW-POWER" if k4 <= max(nv) else "FLAG (above every null)")
    print(f"{name}: K4 {k4} | nulls min/med/max {min(nv)}/{sorted(nv)[9]}/{max(nv)} | {lab}{extra}")
print("== K4 on the full perm set (165,782): fits per L (all types/forms) and mod-2 passes")
for f, Ls in (("m0", range(1, 8)), ("m1", range(1, 4)), ("m1t", (4,))):
    print(f"  {f}: " + "  ".join(f"L{L} fits {g('k4', f, ('fit', L))} pass2 {g('k4', f, ('p2', L))}" for L in Ls))
print("== M0 (key on the plaintext index), vocabulary alphabets, all_s8 (every text)")
for L in range(1, 8): row(f"M0 L{L} (1/8)", g("k4", "m0s8", ("fit", L)), [g(t, "m0s8", ("fit", L)) for t in nulls],
    f" [pass2 K4 {g('k4','m0s8',('p2',L))}, null mean {sum(g(t,'m0s8',('p2',L)) for t in nulls)/19:.0f}]")
print("== M1 (key on the carved index), vocabulary alphabets, all_s8")
for L in range(1, 4): row(f"M1 L{L} (1/8)", g("k4", "m1s8", ("fit", L)), [g(t, "m1s8", ("fit", L)) for t in nulls],
    f" [pass2 K4 {g('k4','m1s8',('p2',L))}, null mean {sum(g(t,'m1s8',('p2',L)) for t in nulls)/19:.1f}]")
print("== M1 L4, themed alphabets (144), full set")
row("M1 L4 themed (full)", g("k4", "m1t", ("fit", 4)), [g(t, "m1t", ("fit", 4)) for t in nulls],
    f" [pass2 K4 {g('k4','m1t',('p2',4))}, null mean {sum(g(t,'m1t',('p2',4)) for t in nulls)/19:.1f}]")
ov = sum(g(t, f, "ovf") for t in T for f in F); mm = sum(g(t, f, "mismatch") for t in T for f in F)
print("overflow count (all texts):", ov, "| table/solve0 mismatch lines:", mm)
cells = {"R1 M0 L1-7 fits (1/8)": lambda t: sum(g(t, "m0s8", ("fit", L)) for L in range(1, 8)),
 "R2 M1 L1-3 fits (1/8)": lambda t: sum(g(t, "m1s8", ("fit", L)) for L in range(1, 4)),
 "R3 M1 L4 themed fits (full)": lambda t: g(t, "m1t", ("fit", 4)),
 "D1 M0 pass2 L6-7 (1/8)": lambda t: sum(g(t, "m0s8", ("p2", L)) for L in (6, 7)),
 "D2 M1 pass2 L1-3 (1/8) + L4 themed": lambda t: sum(g(t, "m1s8", ("p2", L)) for L in range(1, 4)) + g(t, "m1t", ("p2", 4))}
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
