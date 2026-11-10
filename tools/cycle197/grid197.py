"""Cycle 197 grid (PREREG197, I-217): per text (K4 + 19 shuffles, same sample banks), distinct clusters (stage, kind, perm or 'direct',
model, alphabet/tableau, form) with a fit at E_config <= 26^-3; raw fit count beside. Rank p = share of the 20 texts with count >= K4's
(floor 1/20 = 0.05, I-216). Also the per-stage full-power fit totals vs E for every text."""
import sys, glob, collections
run = sys.argv[1]; TH = 26.0 ** -3
def stats(files):
    cl, raw = set(), 0
    fp = collections.Counter(); fpe = collections.Counter()
    for f in files:
        st = f.split("/")[-1].split("_")[0] + "_" + f.split("/")[-1].split("_")[1]
        for l in open(f):
            w = l.split()
            if w[0] == "M":
                E = float(w[11]) if w[1] == "A" else float(w[10])
                if E <= TH:
                    raw += 1; cl.add((st, w[1], "direct" if w[5] == "D" else w[3], w[5], w[6], w[7]))
            elif w[0] == "H":
                E = float(w[-1]); fits = int(w[9])
                if E <= 0.05: fp[st] += fits; fpe[st] += E
    return len(cl), raw, sum(fp.values()), sum(fpe.values())
texts = {"K4": glob.glob(f"{run}/grid_*_K4.txt")}
for s in range(19751, 19770): texts[f"n{s}"] = glob.glob(f"{run}/null_*_{s}.txt")
res = {t: stats(fs) for t, fs in texts.items()}
k = res["K4"]
for t, (c, r, f, e) in res.items(): print(f"{t} clusters {c} raw {r} fullpower-fits {f} (E {e:.3g})")
for i, nm in ((0, "clusters"), (1, "raw"), (2, "fullpower-fits")):
    p = sum(1 for v in res.values() if v[i] >= k[i]) / len(res)
    print(f"RANK {nm}: K4 {k[i]}, nulls {min(v[i] for t, v in res.items() if t != 'K4')}-{max(v[i] for t, v in res.items() if t != 'K4')}, p+ {p:.2f} (floor 0.05)")
