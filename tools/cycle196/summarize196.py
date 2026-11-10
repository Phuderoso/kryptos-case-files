"""Cycle 196 summary (= summarize194.py with the output prefix as argv[2]: c1 = col1 single keyed columnars, c2 = col2 themed double columnars). Cycle 194 summary: C1a (two-tableau) + C1b chunks (one-tableau) H lines combined per cell (model, tab, form, m, n); full power = cell U
<= 0.05 (one-error bound); fits in full-power cells listed from the M lines; low-power totals vs U per tableau type; grid from B lines.
usage: summarize196.py rundir prefix"""
import sys, glob, collections
d = sys.argv[1]; P = sys.argv[2]
cells = collections.defaultdict(lambda: [0, 0, 0, 0.0]); M = []; ends = []
for fn in [f"{d}/out/{P}a_k4.txt", f"{d}/out/{P}b_k4.txt"]:
    ls = [l.split() for l in open(fn)]
    if not ls or ls[-1][0] != "END": print(f"NOT COMPLETE: {fn}"); continue
    ends.append(" ".join(ls[-1]))
    for w in ls:
        if w[0] == "H":
            c = cells[(w[2], w[3], w[4], int(w[5]), int(w[6]))]; c[0] += int(w[7]); c[1] += int(w[8]); c[2] += int(w[9]); c[3] += float(w[10])
        elif w[0] == "M": M.append(w)
print("runs:", *ends, sep="\n  ")
one = lambda t: t in ("AZ>AZ", "KA>KA")
for typ in ("two-tableau", "one-tableau"):
    fp = {k: v for k, v in cells.items() if (one(k[1]) == (typ == "one-tableau")) and v[3] <= 0.05}
    lp = {k: v for k, v in cells.items() if (one(k[1]) == (typ == "one-tableau")) and v[3] > 0.05}
    print(f"\n{typ}: cells {len(fp) + len(lp)}; FULL POWER {len(fp)} (U sum {sum(v[3] for v in fp.values()):.4g}, fits {sum(v[1] for v in fp.values())}, strict {sum(v[2] for v in fp.values())})"
          f"; pairs per model: " + ", ".join(f"S{md} {len({(k[3], k[4]) for k in fp if k[0] == md})}" for md in "12"))
    print(f"  low-power {len(lp)}: fits {sum(v[1] for v in lp.values())} vs U {sum(v[3] for v in lp.values()):.6g}")
    for md in "12":
        x = [k for k in fp if k[0] == md]; lc = [k[3] * k[4] // __import__('math').gcd(k[3], k[4]) for k in x]
        if x: print(f"  S{md}: full-power cells {len(x)}, max lcm {max(lc)}, lcm > 26: {len({(k[3], k[4]) for k in x if k[3] * k[4] // __import__('math').gcd(k[3], k[4]) > 26})} pairs, m = n: {len({(k[3], k[4]) for k in x if k[3] == k[4]})} pairs")
    for k, v in sorted(fp.items()):
        if v[1]:
            ms = [w for w in M if (w[5], w[3], w[4], int(w[6]), int(w[7])) == k]
            print(f"  FIT in full-power cell {k}: fits {v[1]} (printed {len(ms)}), cell U {v[3]:.4g}: " + "; ".join(f"route {w[2]} U {w[8]} slot {w[9]}" for w in ms))
print("\nstrongest printed fits (lowest config U, any cell):")
for w in sorted(M, key=lambda w: float(w[8]))[:12]:
    k = (w[5], w[3], w[4], int(w[6]), int(w[7])); print(f"  route {w[2]} S{w[5]} {w[3]} {w[4]} {w[6]}x{w[7]} U {w[8]} slot {w[9]} cell U {cells[k][3]:.4g}")
