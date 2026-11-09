"""Cycle 174: compare the Python recount (rec/*.py.txt) with the C tools (rec/*.c.txt) on identical ranges.
Hill: per (n, aff, num, ix, off) the consistent and invertible counts (n 2 linear/affine, n 3 linear; n 3 affine not recounted).
Hill invertible in C = configs with a K line. Portax: per (num, ix, p) consistent counts."""
import glob, collections
bad = 0; nh = 0; npx = 0; rows = []
for f in sorted(glob.glob("rec/hill_*.py.txt")):
    c = f.replace(".py.", ".c."); C = {}; Kc = collections.Counter()
    for l in open(c):
        w = l.split()
        if w[0] == "H": C[(w[2], w[3], w[4], w[5], w[6])] = (int(w[7]), int(w[8]))
        if w[0] == "K": Kc[(w[3], w[4], w[5], w[6], w[7])] += 1
    for l in open(f):
        w = l.split(); k = tuple(w[2:7]); py = (int(w[7]), int(w[8]), int(w[9])); cc = (C[k][0], C[k][1], Kc[k]); nh += py[0]
        if py != cc: bad += 1; rows.append(f"MISMATCH {f} {k} py={py} c={cc}")
        elif py[1]: rows.append(f"agree {f.split('/')[-1]} {k} consistent={py[1]} invertible={py[2]}")
for f in sorted(glob.glob("rec/px_*.py.txt")):
    c = f.replace(".py.", ".c."); C = {}
    for l in open(c):
        w = l.split()
        if w[0] == "H": C[(w[2], w[3], w[4])] = (int(w[5]), int(w[6]))
    for l in open(f):
        w = l.split()
        if w[0] != "RP": continue
        k = tuple(w[2:5]); py = (int(w[5]), int(w[6])); npx += py[0]
        if py != C[k]: bad += 1; rows.append(f"MISMATCH {f} {k} py={py} c={C[k]}")
        elif py[1]: rows.append(f"agree {f.split('/')[-1]} {k} consistent={py[1]}")
print("\n".join(rows)); print(f"Hill configs compared {nh}, Portax configs compared {npx}, mismatching sub-cells {bad}")
