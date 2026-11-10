"""Cycle 196 pooled reference (PREREG196b). Statistic R = one-error fits in bands e >= 3 (two-tableau, col1_s8, all 625 pairs) from the B lines;
statistic D = distinct (row, model, tableau pair, form) among the printed fits with config U <= 26^-2.5 (cluster-aware, I-101: period multiples
and equivalent deletions of one coincidence count once). p_pool = (1 + #{nulls >= K4})/(1 + N) over the 19 registered + 40 fresh nulls; the
binomial SE of the pooled exceedance fraction is printed beside it (I-203). Verdict: p_pool <= 0.01 -> 'REPLICATED rank excess (decode, then a
covariate-matched check before any wording)'; otherwise 'NOT REPLICATED' (flag closed)."""
import sys, glob, math
d = sys.argv[1]; TH = 26 ** -2.5
def stats(fn):
    ls = [l.split() for l in open(fn)]; assert ls and ls[-1][0] == "END", fn
    R = sum(int(w[5]) for w in ls if w[0] == "B" and 3 <= int(w[3]) <= 24)
    D = len({(w[2], w[5], w[3], w[4]) for w in ls if w[0] == "M" and float(w[8]) <= TH})
    return R, D
k = stats(f"{d}/grid/g_k4_tab2.txt")
reg = {fn.split("/g_")[1][:-9]: stats(fn) for fn in glob.glob(f"{d}/grid/g_n*_tab2.txt")}
new = {fn.split("/g_")[1][:-9]: stats(fn) for fn in glob.glob(f"{d}/pool/g_n*_tab2.txt")}
print(f"K4: R {k[0]}, D {k[1]}")
for name, S in (("registered 19", reg), ("fresh 40", new), ("pooled", {**reg, **new})):
    for j, lab in ((0, "R"), (1, "D")):
        v = sorted(x[j] for x in S.values()); n = len(v); ge = sum(x >= k[j] for x in v); p = (1 + ge) / (1 + n)
        mu = sum(v) / n; sd = math.sqrt(sum((x - mu) ** 2 for x in v) / (n - 1))
        print(f"{name} (n {n}) {lab}: range {v[0]}-{v[-1]}, mean {mu:.2f}, SD {sd:.2f}, #>=K4 {ge}, p {p:.3f} (SE of fraction {math.sqrt(max(ge,1)/n*(1-max(ge,1)/n)/n):.3f})")
S = {**reg, **new}; v = [x[0] for x in S.values()]; ge = sum(x >= k[0] for x in v); p = (1 + ge) / (1 + len(v))
print("VERDICT (primary R, pooled):", "REPLICATED rank excess" if p <= 0.01 else "NOT REPLICATED (flag closed)", f"p_pool {p:.3f}")
