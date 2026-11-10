"""Aggregate meter197.sh output: per stage (D direct / T sample banks) x solver x cell-E band, observed vs exact E (Poisson z).
Solver A: fits vs E (exact pass probability). Solver B: solutions vs E (E_config = exact expected solution count; fits <= solutions).
Fits cluster (one coincidence repeats across overlapping records and across nested pairs, e.g. 2x25 inside 10x25), so z overstates
significance; 'max1' = the largest single-text contribution, and z_wo = z without that text."""
import sys, math, collections
acc = collections.defaultdict(lambda: [0, 0.0, 0, collections.Counter()])
for line in open(sys.argv[1]):
    w = line.split()
    if len(w) < 3 or w[1] != "H": continue
    st, sv, txt = w[0], w[2], w[3]
    o, E = (int(w[-2]), float(w[-1])) if sv == "A" else (float(w[-2]), float(w[-1]))
    band = "fp<=0.05" if E <= 0.05 else "0.05-1" if E <= 1 else "1-10" if E <= 10 else ">10"
    a = acc[(st, sv, band)]; a[0] += o; a[1] += E; a[2] += 1; a[3][txt] += o
for k in sorted(acc):
    o, E, c, per = acc[k]; z = (o - E) / math.sqrt(E) if E > 0 else 0
    t1, m1 = per.most_common(1)[0]; ntx = len(per)
    zw = (o - m1 - E * (ntx - 1) / ntx) / math.sqrt(E * (ntx - 1) / ntx) if E > 0 else 0
    print(*k, f"cells {c} obs {o:.0f} E {E:.4g} z {z:+.2f} | texts-with-obs {sum(1 for v in per.values() if v)} max1 {m1:.0f} ({t1}) z_wo {zw:+.2f}")
