"""Cycle 174 summary: K4 full-family counts per sub-cell (with Hill's analytic expectation), the K4 hits, and the
pre-registered I-110 grid (4 cells, leave-one-out z, max over cells) for K4 vs 19 nulls on all_s4.bin.
usage (from run/): python3 ../tools/summarize174.py"""
import glob, math, collections
def read(f): return [l.split() for l in open(f)]
# ---- K4 full
H = collections.defaultdict(lambda: [0, 0, 0, 0.0]); K = []; RB = []; R = [0, 0, 0]; PXH = collections.defaultdict(lambda: [0, 0]); X = []
for f in sorted(glob.glob("out/*_k4full_*.txt")):
    for w in read(f):
        if w[0] == "H" and f.split("/")[-1].startswith("hill"):
            k = tuple(w[2:7]); h = H[k]; h[0] += int(w[7]); h[1] += int(w[8]); h[2] += int(w[9]); h[3] += float(w[10])
        elif w[0] == "H":
            k = (w[2], w[3], int(w[4])); PXH[k][0] += int(w[5]); PXH[k][1] += int(w[6])
        elif w[0] == "K": K.append(w)
        elif w[0] == "B": RB.append(w)
        elif w[0] == "R": R[0] += int(w[2]); R[1] += int(w[3]); R[2] += int(w[4])
        elif w[0] == "X": X.append(w)
print("== K4, full 165,782 perms ==")
print("Hill: n aff num ix off | configs consistent invertible | chance expectation")
for k in sorted(H): print("  ", *k, "|", *H[k][:3], "| %.3g" % H[k][3])
tot = [sum(H[k][i] for k in H if k[0] == n) for n in "23" for i in range(3)]
print("  totals n2: configs %d consistent %d invertible %d ; n3: configs %d consistent %d invertible %d" % tuple(tot))
print("  sum of chance expectation n2 %.3g n3 %.3g" % (sum(H[k][3] for k in H if k[0] == "2"), sum(H[k][3] for k in H if k[0] == "3")))
print("Hill decodes (K lines):", len(K)); [print("  ", " ".join(w)) for w in K[:20]]
print("Ragbaby: configs %d crib1-fit %d both-fit %d" % tuple(R)); [print("  ", " ".join(w)) for w in RB[:20]]
pc = sum(v[1] for v in PXH.values()); print("Portax: configs %d consistent %d ; informative (pairs>=12) listed %d" % (sum(v[0] for v in PXH.values()), pc, len(X)))
for k in sorted(PXH):
    if PXH[k][1]: print("   consistent at", k, PXH[k][1])
for w in X[:30]: print("  ", " ".join(w))
# ---- grid on all_s4
texts = ["k4s4"] + ["null%d" % i for i in range(19)]
def cell(t):
    c = [0, 0, 0, 0]
    for w in read(f"out/hill_{t}.txt"):
        if w[0] == "H": c[0 if w[2] == "2" else 1] += int(w[8])
    for w in read(f"out/rag_{t}.txt"):
        if w[0] == "R": c[2] += int(w[4])
    for w in read(f"out/portax_{t}.txt"):
        if w[0] == "H": c[3] += int(w[6])
    return c
V = {t: cell(t) for t in texts}
def z(t, j):
    o = [V[u][j] for u in texts if u != t]; m = sum(o) / len(o); sd = (sum((x - m) ** 2 for x in o) / (len(o) - 1)) ** 0.5
    x = V[t][j]
    if sd == 0: return 0.0 if x == m else (math.inf if x > m else -math.inf)
    return (x - m) / sd
G = {t: max(z(t, j) for j in range(4)) for t in texts}
print("\n== Pre-registered I-110 grid (all_s4.bin; cells C1 Hill2-consistent, C2 Hill3-consistent, C3 Ragbaby both-fit, C4 Portax consistent) ==")
for t in texts: print("  %-6s cells %s  G = %s" % (t, V[t], "%.3f" % G[t]))
p = (1 + sum(G[t] >= G["k4s4"] for t in texts[1:])) / 20
print("  K4 grid p = (1 + #nulls with G >= G_K4)/20 = %.2f (best attainable 0.05)" % p)
