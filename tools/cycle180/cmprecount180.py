"""Compare recount180 R lines with lrk180 M lines on the same slice/alphabets (M0: count = n2*n13; M1: count = n2 * sum 13^null over
the listed mod-13 weight vectors). usage: cmprecount180.py recount.txt M0L3-labels M1L2-label:q lrk-outputs..."""
import sys
R = {}; C = {}
for l in open(sys.argv[1]):
    a = l.split()
    if a[0] == "R": R[tuple(a[1:8])] = int(a[8])
cover = {(a[0], a[1], a[2]) for a in R}
for fn in sys.argv[4:]:
    for l in open(fn):
        a = l.split()
        if not a or a[0] != "M": continue
        key = (a[1], a[2], a[3], a[4], a[5], a[6], a[7])
        if a[2] == "0": n = int(a[10]) * int(a[12])
        else:
            i13 = a.index("S13"); n = int(a[10]) * sum(13 ** int(t.split("n")[1]) for t in a[i13 + 1:])
        C[key] = n
labs = {k[0] for k in R} | {k[0] for k in C}
# restrict lrk lines to cells the recount covered: M0 L1-2 all texts (L3 where recount has L3 lines' text), M1 L1 all, M1 L2 at the listed q
def covered(k, Rkeys_l3, m1l2):
    lab, ix, L = k[0], k[1], int(k[2])
    if ix == "0": return L <= 2 or (L == 3 and lab in Rkeys_l3)
    return L == 1 or (L == 2 and (lab, k[5]) in m1l2)
l3 = set(sys.argv[2].split(","))
m1l2 = {tuple(x.split(":")) for x in sys.argv[3].split(",")}
Cc = {k: v for k, v in C.items() if covered(k, l3, m1l2)}
keys = sorted(set(R) | set(Cc)); bad = 0
for k in keys:
    a, b = R.get(k), Cc.get(k)
    st = "OK" if a == b else "MISMATCH"; bad += a != b
    print(" ".join(k), "recount", a, "lrk180", b, st)
print(f"lines {len(keys)} mismatches {bad}")
