"""Cycle 190 grid: K4 vs 19 nulls; statistics per run family (g512 = A-Z/KRYPTOS on all_s512, gdir = direct 18,824 alphabets):
fits in full-power cells (cell E <= 0.05), fits with ex_after >= 3 (M lines), all fits. I-152 empirical rank p+ = (1 + #nulls >= K4)/20,
p- = (1 + #nulls <= K4)/20. usage: grid190.py griddir"""
import sys, glob, statistics as st
d = sys.argv[1]
for fam in ("g512", "gdir"):
    R = {}
    for fn in sorted(glob.glob(f"{d}/{fam}_*.txt")):
        lab = fn.split(f"{fam}_")[1][:-4]; fp = 0; allf = 0; ex3 = 0; end = False
        for l in open(fn):
            x = l.split()
            if l.startswith("H "):
                allf += int(x[7])
                if float(x[9]) <= 0.05: fp += int(x[7])
            elif l.startswith("M "): ex3 += 1
            elif l.startswith("END "): end = True
        assert end, fn; R[lab] = (fp, ex3, allf)
    k = R.pop("k4"); N = list(R.values())
    for i, name in enumerate(("fits in full-power cells", "fits with ex_after >= 3", "all fits")):
        v = [n[i] for n in N]
        print(f"{fam} | {name} | K4 {k[i]:,} | nulls {min(v):,}-{max(v):,}, {st.mean(v):,.1f} +- {st.stdev(v):,.1f} | p+ {(1+sum(x>=k[i] for x in v))/20:.2f} / p- {(1+sum(x<=k[i] for x in v))/20:.2f} (n={len(v)})")
