"""Cycle 181 summary: per text and cell, fits / strict fits / fitting slots / one-error mod-2 passes from the H lines; overflow and
mismatch lines; labels; grid by EMPIRICAL RANK (I-152: no Poisson tails on overdispersed diagnostic counts).
usage: summarize181.py outdir nulls181.txt"""
import sys, glob, os
od = sys.argv[1]; nulls = [l.split()[0] for l in open(sys.argv[2])]
def read(fn):
    H = {}; ok = False; bad = []
    for l in open(fn):
        a = l.split()
        if not a: continue
        if a[0] == "H":
            k = (int(a[2]), int(a[3]), a[4], a[5]); H[k] = dict(pass2=int(a[11]), fits=int(a[13]), strict=int(a[15]), slots=int(a[17]))
        elif a[0] == "O" and (a[3] != "0" or a[5] != "0"): bad.append(l.strip())
        elif a[0] == "X": bad.append(l.strip())
        elif a[0] == "END": ok = True
    return H, ok, bad
def cell(H, ix, Ls, key):
    return sum(v[key] for (i, L, ty, fm), v in H.items() if i == ix and L in Ls) // (2 if key == "pass2" else 1)   # pass2 is per (L, type), repeated per form
cells = [("M0 L1-5", 0, range(1, 6)), ("M0 L6", 0, [6]), ("M1 L1-2", 1, [1, 2]), ("M1 L3", 1, [3])]
print("== K4 (full set: M0 L1-6, M1 L1-2; all_s8: M1 L3)")
for nm, ix, Ls in cells:
    fn = f"{od}/k4.m0.txt" if ix == 0 else (f"{od}/k4.m1L3s8.txt" if 3 in Ls else f"{od}/k4.m1.txt")
    H, ok, bad = read(fn); print(f"K4 {nm:8s} {'full' if 'L3s8' not in fn else 's8  '} fits {cell(H, ix, Ls, 'fits')} strict {cell(H, ix, Ls, 'strict')} slotfits {cell(H, ix, Ls, 'slots')} pass2 {cell(H, ix, Ls, 'pass2')} END {ok} bad {bad}")
print("== all_s64 (K4 + 19 nulls)")
rows = {}
for lab in ["k4"] + nulls:
    r = {}
    for nm, ix, Ls in cells:
        H, ok, bad = read(f"{od}/{lab}.m{ix}s64.txt"); r[nm] = (cell(H, ix, Ls, "fits"), cell(H, ix, Ls, "pass2"), ok, bad)
    rows[lab] = r
    print(lab, " ".join(f"{nm}: fits {v[0]} pass2 {v[1]}{'' if v[2] else ' NO-END'}{' BAD' if v[3] else ''}" for nm, v in r.items()))
print("== grid (empirical rank among 20 texts; D1 = M0 one-error mod-2 passes L5-6, D2 = M1 one-error mod-2 passes L1-3; fit cells reported, scored only if not all-zero)")
def m0L5(lab):
    H, _, _ = read(f"{od}/{lab}.m0s64.txt"); return cell(H, 0, [5, 6], "pass2")
D = {"D1": {lab: m0L5(lab) for lab in rows}, "D2": {lab: rows[lab]["M1 L1-2"][1] + rows[lab]["M1 L3"][1] for lab in rows}}
F = {nm: {lab: rows[lab][nm][0] for lab in rows} for nm, _, _ in cells}
ps = []
for nm, v in list(F.items()) + list(D.items()):
    k = v["k4"]; nv = [v[l] for l in nulls]
    if nm in F and all(x == 0 for x in v.values()): print(f"{nm}: all zero (reported, not scored)"); continue
    pp = (1 + sum(x >= k for x in nv)) / 20; pm = (1 + sum(x <= k for x in nv)) / 20; ps.append((pp, pm))
    print(f"{nm}: K4 {k} nulls {min(nv)}-{max(nv)} mean {sum(nv)/len(nv):.1f} p+ {pp:.2f} p- {pm:.2f}")
if ps: print(f"grid p+ {min(p for p, _ in ps):.2f} (min over cells) / p- {min(m for _, m in ps):.2f}  [no multiplicity correction; floor 0.05]")
