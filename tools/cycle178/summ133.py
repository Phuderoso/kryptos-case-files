"""I-133 summary (pre-registered rule in PREREG178.md). usage: summ133.py i133dir fresh133.txt matched133.txt"""
import sys, statistics as st
d = sys.argv[1]
def v(lab):
    L = open(f"{d}/{lab}.txt").read().strip().split("\n"); assert L[-1].startswith("END")
    return sum(int(a.split()[11]) for a in L if a.startswith("H ") and a.split()[3] == "6")
k = v("k4"); F = [(l.split()[0], v(l.split()[0])) for l in open(sys.argv[2])]; M = [(l.split()[0], v(l.split()[0]), l.split()[2]) for l in open(sys.argv[3])]
fv = [x for _, x in F]; mv = [x for _, x, _ in M]
pF = (1 + sum(x >= k for x in fv)) / (1 + len(fv)); pM = (1 + sum(x >= k for x in mv)) / (1 + len(mv)); pP = (1 + sum(x >= k for x in fv + mv)) / (1 + len(fv) + len(mv))
print(f"K4 (rerun) one-error-only fits, G1 ix0 L6: {k} (case 165: 230)")
for nm, vals in (("fresh F (40, seeds 17841-17880)", fv), ("matched M (20, mean eq-pairs within 0.02 of K4)", mv), ("pooled (60)", fv + mv)):
    m, s = st.mean(vals), st.stdev(vals)
    print(f"{nm}: min/med/max {min(vals)}/{st.median(vals)}/{max(vals)} mean {m:.1f} sd {s:.1f}; #>=K4 {sum(x >= k for x in vals)}; z(K4) {(k - m) / s:+.2f}")
print(f"p_F {pF:.3f}  p_M {pM:.3f}  pooled p {pP:.3f}")
dec = "REPLICATED" if pF <= 0.05 and pM <= 0.05 else ("NOT REPLICATED" if pP > 0.05 else "WEAK / INCONCLUSIVE")
print("decision (pre-registered):", dec)
print("fresh:", " ".join(f"{a}:{b}" for a, b in F)); print("matched:", " ".join(f"{a}:{b}({e})" for a, b, e in M))
