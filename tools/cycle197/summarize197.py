"""Cycle 197 summary: per output file, full-power cells (exact cell E <= 0.05): count, fits (A) / fits+solutions (B), summed E;
low-power totals vs E; list of fits in full-power cells (cell key -> M lines). usage: summarize197.py files..."""
import sys, collections
for fn in sys.argv[1:]:
    H = {}; Ms = collections.defaultdict(list)
    for line in open(fn):
        w = line.split()
        if w[0] == "H":
            if w[1] == "A": key = ("A", w[3], w[4], w[5], w[6], w[7]); H[key] = (int(w[8]), int(w[9]), 0, float(w[10]))
            else: key = ("B", w[3], w[4], w[5], w[6], w[7]); H[key] = (int(w[8]), int(w[9]), float(w[10]), float(w[11]))
        elif w[0] == "M":
            if w[1] == "A": key = ("A", w[5], "AZ" if w[6] == "AZ" else "KA" if w[6] == "KA" else "OTHER", w[7], w[8], w[9])
            else: key = ("B", w[5], w[6], w[7], w[8], w[9])
            Ms[key].append(line.strip())
    # direct A with a single alphabet file: alphabet class names in H are AZ/KA/OTHER
    fp = {k: v for k, v in H.items() if v[3] <= 0.05}; lp = {k: v for k, v in H.items() if v[3] > 0.05}
    fpf = sum(v[1] for v in fp.values()); fpe = sum(v[3] for v in fp.values()); fps = sum(v[2] for v in fp.values())
    lpf = sum(v[1] for v in lp.values()); lpe = sum(v[3] for v in lp.values()); lps = sum(v[2] for v in lp.values())
    print(f"== {fn.split('/')[-1]}: full-power cells {len(fp)} fits {fpf} (B sols {fps:.0f}) vs E {fpe:.4g} | low-power cells {len(lp)} fits {lpf} (B sols {lps:.4g}) vs E {lpe:.4g}")
    for k, v in sorted(fp.items()):
        if v[1]:
            print("  FP-FIT", " ".join(k), f"configs {v[0]} fits {v[1]} E {v[3]:.3g}", "| printed:", len(Ms.get(k, [])))
            for m in Ms.get(k, [])[:6]: print("     ", m)
