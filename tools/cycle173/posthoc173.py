"""Cycle 173, POST-HOC (not pre-registered, descriptive only): finer grid statistic than the pre-registered min cell-p, which
saturates with 20 texts. Per text and cell with chance expectation E >= 1 (each text's own analytic E on the 1/4 subset):
z = (count - E) / sqrt(E); statistic = max over cells; K4's rank among the 20 texts (K4 + 19 nulls). usage: posthoc173.py run/out"""
import sys, math
D = sys.argv[1]; MODELS = ["del", "ins", "chg", "swp"]
def rd(f):
    r = {}
    for l in open(f):
        if l[:4] in ("HIST", "EXPE"): r[l.split()[0]] = {int(a.split(":")[0]): float(a.split(":")[1]) for a in l.split()[1:]}
    return r
texts = ["k4s4"] + [f"null{i}" for i in range(19)]; S = {}; arg = {}
for x in texts:
    best = -1e9
    for m in MODELS:
        r = rd(f"{D}/{x}.{m}.txt")
        for p in range(1, 27):
            E = r["EXPECT"][p]
            if E >= 1:
                z = (r["HIST"][p] - E) / math.sqrt(E)
                if z > best: best = z; arg[x] = (m, p, int(r["HIST"][p]), round(E, 1))
    S[x] = best
rank = sum(1 for y in texts if S[y] >= S["k4s4"]) / len(texts)
print("POST-HOC max-z over cells with E>=1 (own expectation, 1/4 subset):")
for x in texts: print(f"  {x}: max z {S[x]:.1f} at {arg[x]}")
print(f"K4 rank (#texts with max z >= K4's / 20) = {rank:.2f}")
