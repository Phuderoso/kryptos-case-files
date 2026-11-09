"""Cycle 173 summary: per model x p the K4 full-family count, distinct perms, analytic chance expectation, and K4 / 19 nulls
on every 4th perm; then the pre-registered I-107 grid statistic (min over 104 cells of the upper-tail cell p) and K4's rank.
usage: summarize173.py run/out"""
import sys, statistics as st
D = sys.argv[1]; MODELS = ["del", "ins", "chg", "swp"]; PM = 26
def rd(f):
    r = {}
    for l in open(f):
        if l[:4] in ("HIST", "DPER", "EXPE"):
            k = l.split()[0]; r[k] = {int(a.split(":")[0]): float(a.split(":")[1]) for a in l.split()[1:]}
        if l.startswith("MODEL"): r["tests"] = int(l.split("TESTS")[1])
    return r
nulls = [f"null{i}" for i in range(19)]; texts = ["k4s4"] + nulls
F = {(lab, m): rd(f"{D}/{lab}.{m}.txt") for m in MODELS for lab in ["k4full"] + texts}
print("# Cycle 173 summary (I-105): one-letter anomaly behind K3-law decimations, A-Z/KRYPTOS tableaux, Vig/Beau, both frames")
tests = sum(F[("k4full", m)]["tests"] for m in MODELS); print(f"K4 full-family period-level tests: {tests:,}")
print("model p | K4 full configs (distinct perms) | chance expectation | K4 on 1/4 | 19 nulls on 1/4 min/median/max | label")
for m in MODELS:
    for p in range(1, PM + 1):
        k = F[("k4full", m)]; c = int(k["HIST"][p]); dp = int(k["DPERM"][p]); e = k["EXPECT"][p]
        s4 = int(F[("k4s4", m)]["HIST"][p]); nv = [int(F[(x, m)]["HIST"][p]) for x in nulls]
        lab = "EXACT-EXCL" if c == 0 and e < 1 else ("LOW-POWER" if e >= 1 else "CHECK")
        print(f"{m} {p} | {c} ({dp}) | {e:.3g} | {s4} | {min(nv)}/{st.median(nv):g}/{max(nv)} | {lab}")
# cumulative exact bound per model
for m in MODELS:
    k = F[("k4full", m)]; first = next((p for p in range(1, PM + 1) if k["HIST"][p] > 0), None)
    print(f"BOUND {m}: K4 0 configs at p 1..{first - 1}; sum of chance expectation over those p = {sum(k['EXPECT'][p] for p in range(1, first)):.3g}; first K4 hit p {first}")
# I-107 grid statistic
cells = [(m, p) for m in MODELS for p in range(1, PM + 1)]
cnt = {x: [F[(x, m)]["HIST"][p] for m, p in cells] for x in texts}
def pc(x, i): return sum(1 for y in texts if cnt[y][i] >= cnt[x][i]) / len(texts)
Tm = {x: min(pc(x, i) for i in range(len(cells))) for x in texts}
argk = min(range(len(cells)), key=lambda i: pc("k4s4", i))
rank = sum(1 for y in texts if Tm[y] <= Tm["k4s4"]) / len(texts)
print(f"I-107 GRID: 104 cells; T(K4) = min cell p = {Tm['k4s4']:.3f} at {cells[argk]} ; nulls' T: " + " ".join(f"{Tm[x]:.2f}" for x in nulls))
print(f"I-107 GRID RANK of K4 = {rank:.3f} (#texts with T <= T(K4) / 20; floor 0.05)")
# also the low tail (K4 unusually LOW in some cell), same rule, reported for completeness
def pl(x, i): return sum(1 for y in texts if cnt[y][i] <= cnt[x][i]) / len(texts)
Tl = {x: min(pl(x, i) for i in range(len(cells))) for x in texts}
print(f"I-107 GRID low tail: T_low(K4) = {Tl['k4s4']:.3f}, rank {sum(1 for y in texts if Tl[y] <= Tl['k4s4']) / len(texts):.3f}")
