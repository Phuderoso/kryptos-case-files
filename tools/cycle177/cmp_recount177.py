"""Cycle 177: compare recount177.py (numpy) with gm177/pg177 run on the same slice (M lines), as sets of fits.
usage: cmp_recount177.py recount.txt slice_outputs..."""
import sys
R = set(); C = set(); seen = set()
for l in open(sys.argv[1]):
    a = l.split()
    if a[0] == "G": R.add(("G", a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8], a[9]))
    elif a[0] == "P": R.add(("P", a[1], a[2], a[3], a[4], a[5], a[6]))
for f in sys.argv[2:]:
    for l in open(f):
        a = l.split()
        if a and a[0] == "END": seen.add(a[1])
        if not a or a[0] != "M": continue
        if len(a) >= 10: C.add(("G", a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8], a[9]))
        else: C.add(("P", a[1], a[2], a[3], a[4], a[5], a[6]))
labs = sorted({x[1] for x in R | C} | seen)
for lab in labs:
    r = {x for x in R if x[1] == lab}; c = {x for x in C if x[1] == lab}
    print(lab, "numpy", len(r), "C", len(c), "identical" if r == c else f"DIFF only_numpy {sorted(r-c)[:5]} only_C {sorted(c-r)[:5]}")
print("ALL IDENTICAL" if R == C else "MISMATCH", len(R), len(C))
