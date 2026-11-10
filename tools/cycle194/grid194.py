"""Cycle 194 grid: K4 + 19 shuffles, tab2 + tab1s on all_s2048, all 625 pairs: one-error fits in bands >= e (e = 1..4; band 25 = no cycle
excluded), per tableau type and pooled; p+ = (1 + #nulls >= K4)/20 (rank only)."""
import sys, glob
d = sys.argv[1]; T = {}
for fn in glob.glob(f"{d}/grid/g_*_tab*.txt"):
    lab, tab = fn.split("/g_")[1].rsplit("_", 1); tab = tab[:-4]
    ls = [l.split() for l in open(fn)]; assert ls[-1][0] == "END", fn
    for w in ls:
        if w[0] == "B" and 1 <= int(w[3]) <= 24: bb = T.setdefault(lab, {}).setdefault(tab, {}); bb[int(w[3])] = bb.get(int(w[3]), 0) + int(w[5])
for typ in ("tab2", "tab1s", "pooled"):
    for e in (1, 2, 3, 4):
        f = lambda lab: sum(v for tb, bb in T[lab].items() if typ in (tb, "pooled") for b, v in bb.items() if b >= e)
        k = f("k4"); nl = sorted(f(l) for l in T if l != "k4")
        print(f"{typ} e>={e}: K4 {k}, nulls {nl[0]}-{nl[-1]} (median {nl[len(nl)//2]}), p+ {(1 + sum(x >= k for x in nl)) / 20:.2f}")
