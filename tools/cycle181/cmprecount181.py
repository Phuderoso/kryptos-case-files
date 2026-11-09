"""Compare recount181 R lines with lrk181 M lines on the same slice / alphabets: per (text, ix, L, type, form, row, alphabet) the
set of fitting slots ('strict' for a t -1 line) must be identical. usage: cmprecount181.py recount.txt M0L2-lab:row M1L2-lab:row lrk-outputs..."""
import sys
R = {}; C = {}
for l in open(sys.argv[1]):
    a = l.split()
    if a[0] == "R": R[tuple(a[1:8])] = a[8]
m0l2 = {tuple(x.split(":")) for x in sys.argv[2].split(",")}; m1l2 = {tuple(x.split(":")) for x in sys.argv[3].split(",")}   # (label, row, alphabet)
for fn in sys.argv[4:]:
    for l in open(fn):
        a = l.split()
        if not a or a[0] != "M": continue
        k = tuple(a[1:8]); sl = int(a[a.index("slot") + 1]); C.setdefault(k, set()).add("strict" if sl < 0 else sl)
def covered(k):
    lab, ix, L, row, al = k[0], k[1], int(k[2]), k[5], k[6]
    return L == 1 or (L == 2 and (lab, row, al) in (m0l2 if ix == "0" else m1l2))
fmt = lambda s: "strict" if "strict" in s else ",".join(str(x) for x in sorted(s))
Cc = {k: fmt(v) for k, v in C.items() if covered(k)}; bad = 0
for k in sorted(set(R) | set(Cc)):
    a, b = R.get(k), Cc.get(k); bad += a != b; print(" ".join(k), "recount", a, "lrk181", b, "OK" if a == b else "MISMATCH")
print(f"lines {len(set(R) | set(Cc))} mismatches {bad}")
