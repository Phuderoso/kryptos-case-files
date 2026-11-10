"""Cycle 198 grid (registered, I-217/I-224 style): per text, the number of distinct clusters (stage, record cluster = 'direct' or perm q,
model, alph/tab, form) with a one-error fit at U_config <= 26^-2, on the direct records + the M = N every-128th banks. K4 vs 19 shuffles
(seeds 19851-19869); p+ = (1 + #nulls >= K4) / 20. Non-degeneracy check (I-224): the statistic must vary across the nulls.
usage: grid198.py run_dir"""
import sys, glob
D = sys.argv[1]; TH = 26.0 ** -2
def stat(files):
    cl = set()
    for fn in files:
        st = fn.split("/")[-1].split("_")[1]
        for l in open(fn):
            w = l.split()
            if w[0] != "M" or float(w[10]) > TH: continue
            cl.add((st, "direct" if w[5] == "D" else w[3], w[5], w[6], w[7]))
    return len(cl)
k4 = stat([f"{D}/k4_dir.txt", f"{D}/grid_M98_K4.txt", f"{D}/grid_M96_K4.txt"])
nulls = [stat([f"{D}/null_dir_{s}.txt", f"{D}/null_M98_{s}.txt", f"{D}/null_M96_{s}.txt"]) for s in range(19851, 19870)]
print("K4", k4, "nulls", nulls, "p+", (1 + sum(x >= k4 for x in nulls)) / 20, "non-degenerate", len(set(nulls)) > 1)
