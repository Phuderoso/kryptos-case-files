"""Cycle 190 summary: per run file, full-power cells (E <= 0.05) vs low-power; fits; M lines inside full-power cells.
usage: summarize190.py file..."""
import sys, collections
for fn in sys.argv[1:]:
    H = {}; M = collections.defaultdict(list); end = False
    for l in open(fn):
        x = l.split()
        if l.startswith("H "): H[(x[2], x[3], int(x[4]), int(x[5]))] = (int(x[6]), int(x[7]), int(x[8]), float(x[9]))
        elif l.startswith("M "): M[(x[5], x[4], int(x[6]), int(x[7]))].append(x)
        elif l.startswith("END "): end = True
    print(f"## {fn} END={end}")
    cfg = sum(v[0] for v in H.values()); fit = sum(v[1] for v in H.values()); E = sum(v[3] for v in H.values())
    print(f"configs {cfg:,}; total fits {fit:,}; total chance E {E:,.1f}")
    for md in "PC":
        for fm in ("vig", "beau"):
            cells = {k: v for k, v in H.items() if k[0] == md and k[1] == fm}
            fp = {k: v for k, v in cells.items() if v[3] <= 0.05}; lp = {k: v for k, v in cells.items() if v[3] > 0.05}
            print(f"model {md} {fm}: full-power cells {len(fp)} (fits {sum(v[1] for v in fp.values())}, strict {sum(v[2] for v in fp.values())}, sum E {sum(v[3] for v in fp.values()):.3f}); "
                  f"low-power cells {len(lp)} (fits {sum(v[1] for v in lp.values()):,} vs E {sum(v[3] for v in lp.values()):,.1f})")
            for k, v in sorted(fp.items()):
                if v[1]: print("  FULL-POWER FIT cell", k, "fits", v[1], "E", v[3], "printed:", [" ".join(m[1:]) for m in M[k]])
            print("  full-power pairs:", " ".join(f"{k[2]}x{k[3]}" for k in sorted(fp, key=lambda k: (k[2], k[3]))))
