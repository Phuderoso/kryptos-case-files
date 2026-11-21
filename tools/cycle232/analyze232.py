#!/usr/bin/env python3
"""Cycle 232 (PREREG232, I-342 + I-350 + distance-to-bar audit). Fixed before the fresh-null run; no tuning after it.
Inputs: WORKDIR/R (fresh nulls + plants from run232.sh), WORKDIR/plants232.tsv, WORKDIR/nulls232.tsv,
        REPO/data/cycle229/R (published K4 + 16 c229 nulls, case 213 family), REPO/data/cycle230|231 logs (count cells, hard-coded below).
Unit (I-342): U = (text, nq) with nq >= 10, pooled over the 8 run files (direct a/b, bank/all Q r10, bank/all V a/b), models and p:
        N_U = sum of Y n, max_U = max of Y max.  Domain: N_U >= 10.
Fit points: calibration units of single texts AND of disjoint groups of calibration texts (g = 2, 5, 10, 20; same nq pooled across
        the group's texts) -> N spans ~10 .. >1e6.  OLS: max = a + b1 x + b2 x^2 + c nq, x = ln N.  No family term.
Bar: bar(nq, N) = fit + k_text, k_text = max over the 20 calibration texts of R_t = max over the text's single-text units of
        (max_U - fit).  Nominal per-text false-pass level 1/21.  Descriptive per-unit bar: fit + k05 (95th pct of single-text residuals).
usage: analyze232.py WORKDIR REPO > analyze232.log ; writes WORKDIR/summary232.json"""
import sys, os, re, json, math, glob
import numpy as np
W, REPO = sys.argv[1], sys.argv[2]
R = W + "/R"; PUB = REPO + "/data/cycle229/R"
CAL = list(range(209609, 209629)); HOLD = list(range(209629, 209641)); PLANT_SEED = 209641; BOOT_SEED = 209642
FILES = ["direct_a", "direct_b", "bank_Q_r10", "all_Q_r10", "bank_V_a", "bank_V_b", "all_V_a", "all_V_b"]
ALPHA = 0.05
YRE = re.compile(r"^Y model=(\w) p=(\d+) nq=(\d+) n=(\d+) pass=(\d+) max=(-?[\d.]+)")
def wilson(k, n, z=1.959964):
    if n == 0: return (0.0, 1.0)
    ph = k / n; d = 1 + z * z / n; c = (ph + z * z / (2 * n)) / d; h = z * math.sqrt(ph * (1 - ph) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))
def units(prefix, d):
    """per nq >= 10: [N, max] pooled over the 8 files of one text"""
    U = {}
    for f in FILES:
        fn = f"{d}/{prefix}_{f}.txt"
        if not os.path.exists(fn): raise SystemExit(f"missing {fn}")
        for l in open(fn):
            m = YRE.match(l)
            if not m: continue
            nq, n, mx = int(m[3]), int(m[4]), float(m[6])
            if nq < 10: continue
            u = U.setdefault(nq, [0, -99.0]); u[0] += n; u[1] = max(u[1], mx)
    return U
def pool(list_of_U):
    P = {}
    for U in list_of_U:
        for q, (n, mx) in U.items():
            u = P.setdefault(q, [0, -99.0]); u[0] += n; u[1] = max(u[1], mx)
    return P
def design(N, q): x = np.log(N); return np.column_stack([np.ones_like(x), x, x * x, q])
def pts(U, lvl):
    return [(q, n, mx, lvl) for q, (n, mx) in U.items() if n >= 10]
S = {}
cal = {s: units(f"null{s}", R) for s in CAL}
hold = {s: units(f"null{s}", R) for s in HOLD}
old = {s: units(f"null{s}", PUB) for s in range(209559, 209575)}
k4 = units("k4", PUB)
# ---- calibration points
P = []
for s in CAL: P += pts(cal[s], 1)
for g in (2, 5, 10, 20):
    for i in range(0, 20, g): P += pts(pool([cal[s] for s in CAL[i:i + g]]), g)
A = np.array([[p[0], p[1], p[2], p[3]] for p in P], dtype=float)
X = design(A[:, 1], A[:, 0]); y = A[:, 2]
beta, *_ = np.linalg.lstsq(X, y, rcond=None)
res = y - X @ beta; r2 = 1 - (res @ res) / ((y - y.mean()) @ (y - y.mean()))
fit = lambda N, q: float((design(np.array([float(N)]), np.array([float(q)])) @ beta)[0])
print("== I-342 fit (calibration nulls %d-%d, %d points, levels 1/2/5/10/20) ==" % (CAL[0], CAL[-1], len(P)))
print("max = %.4f %+.5f ln N %+.6f (ln N)^2 %+.5f nq   R2 %.3f   N range %d .. %d   nq range %d .. %d" %
      (beta[0], beta[1], beta[2], beta[3], r2, A[:, 1].min(), A[:, 1].max(), A[:, 0].min(), A[:, 0].max()))
slope = {N: beta[1] + 2 * beta[2] * math.log(N) for N in (10, 1e3, 1e5, 1e6, 5e6)}
print("local slope b(N) = d max / d ln N: " + "  ".join(f"N={N:.0e}: {v:+.4f}" for N, v in slope.items()))
for lv in (1, 2, 5, 10, 20):
    m = A[:, 3] == lv; print(f"  level {lv:2d}: {m.sum():4d} pts, mean residual {res[m].mean():+.4f}, sd {res[m].std():.4f}, N {A[m,1].min():.0f}..{A[m,1].max():.0f}")
# cluster bootstrap over calibration texts for b1, b2, c and b(N)
rng = np.random.default_rng(BOOT_SEED); BB = []
for b in range(1000):
    pick = [CAL[i] for i in rng.integers(0, 20, 20)]; Pb = []
    for s in pick: Pb += pts(cal[s], 1)
    for g in (2, 5, 10, 20):
        for i in range(0, 20, g): Pb += pts(pool([cal[s] for s in pick[i:i + g]]), g)
    Ab = np.array([[p[0], p[1], p[2]] for p in Pb], dtype=float)
    bb, *_ = np.linalg.lstsq(design(Ab[:, 1], Ab[:, 0]), Ab[:, 2], rcond=None); BB.append(bb)
BB = np.array(BB); ci = lambda v: (float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5)))
print("bootstrap 95%% (B=1000, seed %d, resampling calibration texts): b1 %s  b2 %s  c %s" % (BOOT_SEED, ci(BB[:, 1]), ci(BB[:, 2]), ci(BB[:, 3])))
bslope = {N: ci(BB[:, 1] + 2 * BB[:, 2] * math.log(N)) for N in (10, 1e3, 1e5, 1e6)}
print("b(N) 95%: " + "  ".join(f"N={N:.0e}: [{a:+.4f},{b:+.4f}]" for N, (a, b) in bslope.items()))
S["fit"] = dict(beta=list(map(float, beta)), r2=float(r2), npts=len(P), Nmin=float(A[:, 1].min()), Nmax=float(A[:, 1].max()),
                slope={str(k): float(v) for k, v in slope.items()}, boot=dict(b1=ci(BB[:, 1]), b2=ci(BB[:, 2]), c=ci(BB[:, 3]),
                slope={str(k): v for k, v in bslope.items()}))
# ---- k_text and k05
def Rt(U): return max((mx - fit(n, q)) for q, (n, mx) in U.items() if n >= 10)
Rcal = {s: Rt(cal[s]) for s in CAL}
k_text = max(Rcal.values())
r1 = np.array([mx - fit(n, q) for s in CAL for q, (n, mx) in cal[s].items() if n >= 10]); k05 = float(np.percentile(r1, 95))
bar = lambda N, q: fit(N, q) + k_text
print(f"k_text = {k_text:+.4f} (max of R_t over 20 calibration texts; nominal per-text level 1/21)   k05 (per-unit 95th pct) = {k05:+.4f}")
print("R_t calibration (sorted): " + " ".join(f"{v:+.3f}" for v in sorted(Rcal.values())))
print("bar(nq, N) examples:"); grid = {}
for q in (10, 15, 20, 30, 45, 60):
    row = [bar(N, q) for N in (10, 1e2, 1e3, 1e4, 1e5, 1e6, 5e6)]; grid[q] = row
    print(f"  nq {q:2d}: " + " ".join(f"{v:7.3f}" for v in row) + "   (N = 1e1 1e2 1e3 1e4 1e5 1e6 5e6)")
S["bar"] = dict(k_text=k_text, k05=k05, Rcal={str(k): v for k, v in Rcal.items()}, grid={str(k): v for k, v in grid.items()})
cover = A[:, 1].max() >= 1e6; print(f"Gate C (calibration covers N >= 1e6): max N {A[:,1].max():.0f} -> {'PASS' if cover else 'FAIL'}")
# ---- holdout: per-text rate (I-350) + misfit by decade
def text_pass(U):
    pu = [(q, n, mx, mx - bar(n, q)) for q, (n, mx) in U.items() if n >= 10 and mx >= bar(n, q)]
    return pu
print("\n== Holdout (fresh replicate nulls %d-%d) ==" % (HOLD[0], HOLD[-1]))
Rh = {s: Rt(hold[s]) for s in HOLD}; hp = {s: text_pass(hold[s]) for s in HOLD}
nh = sum(1 for s in HOLD if hp[s]); nu = sum(len(v) for v in hp.values())
print(f"per-text passes {nh}/12 Wilson {wilson(nh,12)}; passing units {nu} -> expected passing units per null text {nu/12:.3f}")
for s in HOLD:
    if hp[s]: print(f"  null {s}: " + "; ".join(f"nq {q} N {n} max {mx:.3f} over bar by {d:+.3f}" for q, n, mx, d in hp[s]))
print("R_t holdout (sorted): " + " ".join(f"{v:+.3f}" for v in sorted(Rh.values())))
HP = []
for s in HOLD: HP += pts(hold[s], 1)
for g in (2, 4, 12):
    for i in range(0, 12, g): HP += pts(pool([hold[s] for s in HOLD[i:i + g]]), g)
Hm = np.array([[p[0], p[1], p[2]] for p in HP], dtype=float); hres = Hm[:, 2] - np.array([fit(n, q) for q, n, mx in Hm])
gateM = True; Mtab = []
print("misfit by decade of N (holdout units, single + pooled g 2/4/12): stratum | units | mean residual | verdict (|mean| <= 0.15 when >= 10 units)")
for lo in (1, 2, 3, 4, 5, 6):
    m = (Hm[:, 1] >= 10 ** lo) & (Hm[:, 1] < 10 ** (lo + 1)); k = int(m.sum()); mr = float(hres[m].mean()) if k else float("nan")
    ok = (k < 10) or abs(mr) <= 0.15; gateM &= ok; Mtab.append((lo, k, mr, ok))
    print(f"  [1e{lo},1e{lo+1}) | {k} | {mr:+.4f} | {'ok' if ok else 'MISFIT'}{' (n<10, not gated)' if k < 10 else ''}")
gateH = nh <= 1
print(f"Gate H (holdout per-text passes <= 1/12): {nh}/12 -> {'PASS' if gateH else 'FAIL'};  Gate M: {'PASS' if gateM else 'FAIL'}")
S["holdout"] = dict(passes=nh, wilson=wilson(nh, 12), units=nu, per_text_units=nu / 12, Rt={str(k): v for k, v in Rh.items()},
                    misfit=Mtab, gateH=gateH, gateM=gateM)
# ---- third null set: the 16 published c229 nulls (not fresh, not in the fit): descriptive
op = {s: text_pass(old[s]) for s in old}; no = sum(1 for s in old if op[s])
print(f"\nc229 published nulls 209559-209574 (descriptive third set): per-text passes {no}/16 Wilson {wilson(no,16)}, units {sum(len(v) for v in op.values())}")
for s in old:
    if op[s]: print(f"  null {s}: " + "; ".join(f"nq {q} N {n} max {mx:.3f} over bar by {d:+.3f}" for q, n, mx, d in op[s]))
# case 215's four -6.0 passes (nq 12/13/13/19) at their unit
for s, q in ((209573, 13), (209568, 13), (209560, 12), (209563, 19)):
    n, mx = old[s][q]; print(f"  case 215 pass null {s} nq {q}: unit N {n} max {mx:.3f} bar {bar(n,q):.3f} -> {'PASS' if mx >= bar(n,q) else 'below'} (by {mx-bar(n,q):+.3f})")
S["old_nulls"] = dict(passes=no, wilson=wilson(no, 16), Rt={str(s): Rt(old[s]) for s in old})
# ---- plants (gate P)
print("\n== Plants (seed %d, Q model, nq bands, odd pid one-error) ==" % PLANT_SEED)
rows = [l.rstrip("\n").split("\t") for l in open(W + "/plants232.tsv")]; hd = rows[0]; PL = []
k4maxN = max(n for n, mx in k4.values())
for r in rows[1:]:
    pl = dict(zip(hd, r)); fn = f"{R}/plant_{pl['pid']}.txt"; key = f"perm={pl['row']} dir={pl['dir']} ix=1 X={pl['X']} Y={pl['Y']} form={pl['form']}"
    tp = int(pl["p"]); divs = {d for d in range(1, tp + 1) if tp % d == 0}   # H lines are printed at the primitive period
    hit = any(l.startswith("H Q " + key + " ") and int(re.search(r" p=(\d+)", l)[1]) in divs for l in open(fn))
    Pm = [l for l in open(fn) if l.startswith("P Q " + key + " ") and f" p={pl['p']} " in l]
    if Pm:
        m = re.search(r"nqnc=(\d+) nc=(-?[\d.]+)", Pm[0]); nq, nc = int(m[1]), float(m[2])
    else: nq, nc = int(pl["n_pred"]), float("nan")
    Nref = k4[nq][0] if nq in k4 else k4maxN
    b_ref, b_1e6, b_5e6 = bar(Nref, nq), bar(1e6, nq), bar(5e6, nq)
    ok = hit and bool(Pm) and nc >= b_ref
    PL.append(dict(pid=int(pl["pid"]), bad=int(pl["bad"]), p=int(pl["p"]), nq=nq, nc=nc, pred_nc=float(pl["nc_pred"]), recovered=hit and bool(Pm),
                   Nref=Nref, bar_ref=b_ref, pass_ref=ok, margin=nc - b_ref, pass_1e6=nc >= b_1e6, pass_5e6=nc >= b_5e6))
    print(f"plant {pl['pid']:>2} bad {pl['bad']:>3} p {pl['p']:>2} nq {nq:2d} NC {nc:7.3f} (pred {float(pl['nc_pred']):.3f}) rec {int(hit and bool(Pm))} | "
          f"N_ref {Nref:6d} bar {b_ref:.3f} {'PASS' if ok else 'FAIL'} margin {nc-b_ref:+.3f} | @1e6 {'P' if nc>=b_1e6 else 'F'} @5e6 {'P' if nc>=b_5e6 else 'F'}")
npass = sum(p["pass_ref"] for p in PL); n1 = sum(p["pass_ref"] for p in PL if p["bad"] >= 0); n0 = sum(1 for p in PL if p["bad"] >= 0)
gateP = npass >= 23
print(f"Gate P: {npass}/24 recovered and over bar(nq, N_ref) Wilson {wilson(npass,24)} -> {'PASS' if gateP else 'FAIL'}; one-error {n1}/{n0} Wilson {wilson(n1,n0)}; "
      f"@1e6 {sum(p['pass_1e6'] for p in PL)}/24, @5e6 {sum(p['pass_5e6'] for p in PL)}/24; min margin {min(p['margin'] for p in PL):+.3f}")
S["plants"] = PL; S["gateP"] = dict(passes=npass, wilson=wilson(npass, 24), one_error=(n1, n0), PASS=gateP)
adopt = gateP and gateH and gateM and cover
print(f"\nDECISION (pre-registered): bar {'ADOPTED from cycle 233 for Y-type families' if adopt else 'NOT adopted'} (P {gateP}, H {gateH}, M {gateM}, C {cover})")
S["adopt"] = adopt
# ---- K4 under the bar (published c229 K4 files = case 215; not re-run)
print("\n== K4 (published data/cycle229/R/k4_*, case 213 family at case 215 scale) ==")
RK = Rt(k4); kp = text_pass(k4)
pc = (1 + sum(1 for v in Rcal.values() if v >= RK)) / 21; ph = (1 + sum(1 for v in Rh.values() if v >= RK)) / 13
po = (1 + sum(1 for s in old if Rt(old[s]) >= RK)) / 17
best = max(((mx - bar(n, q), q, n, mx) for q, (n, mx) in k4.items() if n >= 10))
print(f"K4 R = {RK:+.4f} (k_text {k_text:+.4f}); K4 passing units {len(kp)}; closest unit nq {best[1]} N {best[2]} max {best[3]:.3f} bar {bar(best[2],best[1]):.3f} (gap {best[0]:+.3f})")
print(f"K4 rank p: calibration {pc:.3f} (n 20), holdout {ph:.3f} (n 12), c229 nulls {po:.3f} (n 16, descriptive)")
def dist_label(pvals, passed):
    """agreed distance rule: p -> alpha/p on the signal side, p/alpha on the no-signal side; robust only at >= 2x on every set"""
    if passed:
        d = [ALPHA / p for p in pvals]
        if all(p <= ALPHA for p in pvals): return ("CANDIDATE (robust)" if min(d) >= 2 else "CANDIDATE-FRONTEIRA"), d
        return "NO-SIGNAL-FRONTEIRA (bar pass at a null rate)", d
    d = [p / ALPHA for p in pvals]
    return ("NO-SIGNAL (robust)" if all(p > ALPHA for p in pvals) and min(d) >= 2 else "NO-SIGNAL-FRONTEIRA"), d
lab, d = dist_label([pc, ph], bool(kp))
print(f"K4 label: {lab}; distance p/alpha = {', '.join(f'{v:.2f}' for v in d)} (calibration, holdout)")
S["k4"] = dict(R=RK, passing_units=len(kp), closest=dict(gap=best[0], nq=best[1], N=best[2], max=best[3]), p_cal=pc, p_hold=ph, p_old=po, label=lab, dist=d)
k4u = [(q, n, mx, mx - fit(n, q) - k05) for q, (n, mx) in sorted(k4.items()) if n >= 10 and mx - fit(n, q) >= k05]
print(f"K4 units over the descriptive per-unit bar (fit + k05): {len(k4u)} of {sum(1 for n,m in k4.values() if n>=10)}: " + "; ".join(f"nq {q} N {n} {mx:.3f}" for q, n, mx, _ in k4u))
nullu = [sum(1 for q, (n, mx) in cal[s].items() if n >= 10 and mx - fit(n, q) >= k05) for s in CAL]
print(f"  calibration nulls, units over fit+k05 per text: {nullu} (mean {np.mean(nullu):.2f})")
S["k4"]["units_over_k05"] = len(k4u); S["cal_units_over_k05"] = nullu
# ---- retroactive (descriptive): other families' K4 NC maxima vs the most lenient bar in the domain (N = 10, nq 64)
lenient = min(bar(10, q) for q in range(10, 65))
print(f"\n== Retroactive, descriptive: most lenient bar in domain (N 10, nq 10-64) = {lenient:.3f} ==")
for name, v in (("case 214 Part A (w11 chunk 3) K4 NC max", -7.94), ("case 214 Part B (cases 205/206/211 re-read) K4 NC max", -7.3023),
                ("case 215 K4 best (this K4 data)", best[3])):
    print(f"  {name}: {v:.3f} -> {'below every bar value in the domain' if v < lenient else 'check per unit'}")
S["lenient_bar"] = lenient
# ---- I-350 + distance rule on the case 216 / 217 count cells (descriptive relabelling)
print("\n== I-350 / distance rule on case 216/217 count cells (descriptive; sources data/cycle231/an231.log, data/cycle230/analyze230.log, clus230.log) ==")
C217 = {"direct W9": (3, 5, [0]*8, [0]*8), "direct W10": (47, 5, [0,0,0,1,0,2,0,13], [0,0,0,1,0,1,0,5]),
        "bank W9": (0, 20, [0,2]+[0]*18, [0,1]+[0]*18), "bank W10": (44, 20, [0,3,2,0,4,8,1,3,0,4,6,4,3,2,2,0,1,0,1,0], [0,2,1,0,2,1,1,1,0,2,3,2,2,1,1,0,1,0,1,0]),
        "all W9": (6, 20, [0]*9+[2]+[0]*9+[1], [0]*9+[1]+[0]*9+[1]), "all W10": (48, 20, [2,2,2,2,3,2,2,0,2,4,2,1,2,0,0,0,0,5,5,1], [1,2,1,1,2,1,1,0,1,3,1,1,2,0,0,0,0,4,3,1])}
C216 = {"direct W9": (3, 20, [0,0,2,0,0,2,0,0,0,0], [0,0,1,0,0,1,0,0,0,0]), "direct W10": (47, 20, [0,0,3,0,0,2,0,6,0,0], [0,0,2,0,0,1,0,2,0,0]),
        "bank W9": (0, 20, [0,0,0,0,0,0,4,0,0,10], [0,0,0,0,0,0,1,0,0,1]), "bank W10": (44, 20, [2,1,0,1,3,1,9,3,0,14], [1,1,0,1,2,1,2,2,0,5]),
        "all W9": (6, 20, [0,0,2,0,0,0,0,2,2,0], [0,0,1,0,0,0,0,1,1,0]), "all W10": (48, 20, [1,3,2,3,1,0,5,3,4,7], [1,2,1,2,1,0,3,2,2,5])}
K4CL = {"direct W9": 2, "direct W10": 22, "bank W9": 0, "bank W10": 8, "all W9": 2, "all W10": 20}
def cell(k4raw, scale, raw, cl):
    n = len(raw); lvl = k4raw / scale
    if k4raw == 0:
        h = sum(1 for v in raw if v >= 1); lo, hi = wilson(h, n)
        side = "disc" if hi <= ALPHA else "nondisc" if lo > ALPHA else "mid"
        d = ALPHA / hi if side == "disc" else lo / ALPHA if side == "nondisc" else None
        return dict(kind="K4 0", level=0, hits=h, n=n, wilson=(lo, hi), side=side, d=d, exp_cl=sum(cl) / n * scale)
    h = sum(1 for v in raw if v >= lvl); lo, hi = wilson(h, n)
    side = "excess" if hi <= ALPHA else "nosig" if lo >= ALPHA else "mid"
    d = ALPHA / hi if side == "excess" else lo / ALPHA if side == "nosig" else None
    return dict(kind="K4>0", level=lvl, hits=h, n=n, wilson=(lo, hi), side=side, d=d, exp_cl=sum(cl) / n * scale)
REL = {}
for c in C217:
    a = cell(*C217[c]); b = cell(*C216[c])
    if a["side"] == "mid" or b["side"] == "mid" or a["side"] != b["side"]: lab = ("EXACT-EXCL, " if a["kind"] == "K4 0" else "") + "INSUFFICIENT-DISCRIMINATION-FRONTEIRA"
    else:
        robust = min(a["d"], b["d"]) >= 2
        base = {"disc": "EXACT-EXCL (discriminating)", "nondisc": "EXACT-EXCL (non-discriminating)", "excess": "EXCESS", "nosig": "NO-SIGNAL"}[a["side"]]
        lab = base + ("" if robust else "-FRONTEIRA")
    REL[c] = dict(c217=a, c216=b, label=lab, k4_clusters=K4CL[c])
    f = lambda z: f"{z['hits']}/{z['n']} [{z['wilson'][0]:.3f},{z['wilson'][1]:.3f}] {z['side']}"
    print(f"  {c:10s} K4 raw {C217[c][0]:3d} (cl {K4CL[c]:2d}) | c217 level {a['level']:.2f}: {f(a)}, exp. clusters full scale {a['exp_cl']:.1f} | "
          f"c216 level {b['level']:.2f}: {f(b)}, exp. cl {b['exp_cl']:.1f} | -> {lab}")
S["relabel_counts"] = REL
json.dump(S, open(W + "/summary232.json", "w"), indent=1, default=float)
