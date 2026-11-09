"""Cycle 175 summary: per model x p the K4 full-family counts (all / checks >= 4), distinct perms, analytic chance expectation,
K4 and 19 nulls on every 8th perm; Hill n 2-4 K4 full per sub-cell; then the pre-registered 5-cell grid (I-110 z, I-115
zero-variance rule, I-117 two-sided). usage (from the work dir): python3 tools/summarize175.py run/out"""
import sys, math, statistics as st, collections
D = sys.argv[1]; MODELS = ["delx", "insx"]; PM = 26
def rd(f):
    r = {}
    for l in open(f):
        k = l.split()[0] if l.strip() else ""
        if k in ("HIST", "HISTK", "DPERM", "EXPECT", "EXPECTK"): r[k] = {int(a.split(":")[0]): float(a.split(":")[1]) for a in l.split()[1:]}
        if k == "MODEL": r["tests"] = int(l.split("TESTS")[1])
    return r
def rh(f):
    h = collections.defaultdict(lambda: [0, 0, 0, 0, 0.0, 0.0])
    for l in open(f):
        w = l.split()
        if w and w[0] == "H":
            k = (int(w[2]), int(w[3]), w[4], int(w[5]), int(w[6])); x = h[k]
            for i in range(4): x[i] += int(w[7 + i])
            x[4] += float(w[11]); x[5] += float(w[12])
    return h
nulls = [f"null{i}" for i in range(19)]; texts = ["k4s8"] + nulls
F = {(lab, m): rd(f"{D}/{lab}.{m}.txt") for m in MODELS for lab in ["k4full"] + texts}
HL = {lab: rh(f"{D}/{lab}.hill.txt") for lab in ["k4full"] + texts}
print("# Cycle 175 summary (I-111 + I-113)")
print(f"slip175 period-level tests on K4 full: delx {F[('k4full','delx')]['tests']:,} insx {F[('k4full','insx')]['tests']:,}")
print("model p | K4 full configs all / checks>=4 (distinct perms) | chance expectation all / checks>=4 | K4 1/8 all/k | 19 nulls 1/8 all min/med/max | k min/med/max | label")
for m in MODELS:
    for p in range(1, PM + 1):
        k = F[("k4full", m)]; c = int(k["HIST"][p]); ck = int(k["HISTK"][p]); dp = int(k["DPERM"][p]); e = k["EXPECT"][p]; ek = k["EXPECTK"][p]
        s8 = F[("k4s8", m)]; nv = [int(F[(x, m)]["HIST"][p]) for x in nulls]; nk = [int(F[(x, m)]["HISTK"][p]) for x in nulls]
        lab = "EXACT-EXCL" if c == 0 and e < 1 else ("LOW-POWER" if e >= 1 else "CHECK(K4>0 with E<1)")
        print(f"{m} {p} | {c} / {ck} ({dp}) | {e:.3g} / {ek:.3g} | {int(s8['HIST'][p])}/{int(s8['HISTK'][p])} | {min(nv)}/{st.median(nv):g}/{max(nv)} | {min(nk)}/{st.median(nk):g}/{max(nk)} | {lab}")
for m in MODELS:
    k = F[("k4full", m)]; first = next((p for p in range(1, PM + 1) if k["HIST"][p] > 0), PM + 1)
    print(f"BOUND {m}: K4 0 configs at p 1..{first - 1}; chance expectation summed over those p = {sum(k['EXPECT'][p] for p in range(1, first)):.3g}; first K4 hit p {first if first <= PM else '-'}")
print("\nHill (K4 full 165,782 perms): n aff ix | configs consistent invertible consistent(checks>=4) | expectation all / checks>=4")
agg = collections.defaultdict(lambda: [0, 0, 0, 0, 0.0, 0.0])
for k, v in HL["k4full"].items():
    a = agg[(k[0], k[1], k[3])]
    for i in range(6): a[i] += v[i]
for k in sorted(agg): a = agg[k]; print(f"  n{k[0]} aff{k[1]} ix{k[2]} | {a[0]} {a[1]} {a[2]} {a[3]} | {a[4]:.3g} / {a[5]:.3g}")
# ---- grid
def cells(t):
    a = F[(t, "delx")]["HISTK"]; b = F[(t, "insx")]["HISTK"]; h = HL[t]
    return [sum(a[p] for p in range(1, 17)), sum(b[p] for p in range(1, 17)), sum(a[p] for p in range(17, 27)), sum(b[p] for p in range(17, 27)),
            sum(v[3] for k, v in h.items() if k[0] == 4)]
V = {t: cells(t) for t in texts}; names = ["C1 delx p1-16", "C2 insx p1-16", "C3 delx p17-26", "C4 insx p17-26", "C5 Hill n4"]
scored = [j for j in range(5) if len(set(V[x][j] for x in nulls)) > 1]
print("\n== Pre-registered grid (all on 1/8 of the perms; checks >= 4) ==")
for j in range(5):
    nv = [V[x][j] for x in nulls]
    flag = "" if j in scored else ("  [zero null variance: not scored" + ("; K4 differs -> FLAG]" if V["k4s8"][j] != nv[0] else "; K4 equal]"))
    print(f"  {names[j]}: K4 {V['k4s8'][j]:g} | nulls min/median/max {min(nv):g}/{st.median(nv):g}/{max(nv):g}{flag}")
def z(t, j):
    o = [V[u][j] for u in texts if u != t]; m = sum(o) / len(o); sd = st.stdev(o); x = V[t][j]
    if sd == 0: return 0.0 if x == m else (math.inf if x > m else -math.inf)
    return (x - m) / sd
if scored:
    Gp = {t: max(z(t, j) for j in scored) for t in texts}; Gm = {t: min(z(t, j) for j in scored) for t in texts}
    pp = (1 + sum(Gp[t] >= Gp["k4s8"] for t in nulls)) / 20; pm = (1 + sum(Gm[t] <= Gm["k4s8"] for t in nulls)) / 20
    print(f"  scored cells: {[names[j] for j in scored]}")
    print("  z of K4 per scored cell: " + ", ".join(f"{names[j]} {z('k4s8', j):+.2f}" for j in scored))
    print(f"  G+ (K4) = {Gp['k4s8']:+.3f}; grid p+ = {pp:.2f} | G- (K4) = {Gm['k4s8']:+.3f}; grid p- = {pm:.2f} (best attainable 0.05 each)")
    print("  nulls G+: " + " ".join(f"{Gp[t]:+.2f}" for t in nulls))
else:
    print("  no scored cell -> grid not informative")
