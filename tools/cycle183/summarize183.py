"""Cycle 183 summary: per text and cell, one-error fits / strict fits / slot fits and one-error mod-2 passes from the H lines;
overflow / mismatch lines; labels; grid by empirical rank (I-152).
usage: summarize183.py outdir nulls183.txt"""
import sys, statistics as st
od, nf = sys.argv[1:3]; nulls = [l.split()[0] for l in open(nf)]
def read(fn):
    H = {}; ok = False; bad = []
    for l in open(fn):
        a = l.split()
        if not a: continue
        if a[0] == "H": H[(int(a[3]), a[5])] = dict(pass2=int(a[11]), fits=int(a[13]), strict=int(a[15]), slots=int(a[17]))
        elif a[0] == "O" and (a[3] != "0" or a[5] != "0"): bad.append(l.strip())
        elif a[0] == "X": bad.append(l.strip())
        elif a[0] == "END": ok = True
    return H, ok, bad
def cell(H, Ls, key):
    return sum(v[key] for (L, fm), v in H.items() if L in Ls) // (2 if key == "pass2" else 1)
def line(H, Ls):
    return f"fits {cell(H, Ls, 'fits')} (strict {cell(H, Ls, 'strict')}, slot fits {cell(H, Ls, 'slots')}) pass2 {cell(H, Ls, 'pass2')}"
print("== K4 full set (165,782 perms; 2,703,744 (A, B) pairs per direction x Vig/Beau), one error, L 1-4")
for d in ("f", "r"):
    H, ok, bad = read(f"{od}/k4.{d}.txt")
    for nm, Ls in (("L1-3", range(1, 4)), ("L4", [4])): print(f"K4 {d} {nm:5s} {line(H, Ls)} END {ok} bad {bad}")
print("== K4 all_s64 (2,591 perms = 1/64), one error, L 5")
for d in ("f", "r"):
    H, ok, bad = read(f"{od}/k4.{d}s64L5.txt"); print(f"K4 {d} L5    {line(H, [5])} END {ok} bad {bad}")
for d in ("f", "r"):
    a = [l for l in open(f"{od}/k4.{d}s2k.txt") if l.startswith("H ")]; b = [l for l in open(f"{od}/k4.{d}s2ksafe.txt") if l.startswith("H ")]
    print(f"SAFE audit (method 2, no prefilter, 13-value loop on every slot) k4 {d} all_s2048 L 1-5 H lines identical: {a == b}")
print("== all_s64 (K4 + 19 nulls), one error, L 1-4")
rows = {}
for lab in ["k4"] + nulls:
    r = {}
    for d in ("f", "r"):
        H, ok, bad = read(f"{od}/{lab}.{d}s64.txt")
        for nm, Ls in (("L1-3", range(1, 4)), ("L4", [4])): r[d + nm] = (cell(H, Ls, "fits"), cell(H, Ls, "pass2"), ok, bad)
    rows[lab] = r
    print(lab, " ".join(f"{k}: fits {v[0]} pass2 {v[1]}{'' if v[2] else ' NO-END'}{' BAD' if v[3] else ''}" for k, v in r.items()))
print("== grid (empirical rank among 20 texts; D1 = q4f one-error mod-2 passes at L 4 (all L <= 4 by nesting), D2 = q4r the same; fit cells scored only if not all-zero)")
F = {k: {lab: rows[lab][k][0] for lab in rows} for k in rows["k4"]}
D = {"D1": {lab: rows[lab]["fL4"][1] for lab in rows}, "D2": {lab: rows[lab]["rL4"][1] for lab in rows}}
ps = []
for nm, v in list(F.items()) + list(D.items()):
    k = v["k4"]; nv = [v[l] for l in nulls]
    if nm in F and all(x == 0 for x in v.values()): print(f"{nm}: all zero (reported, not scored)"); continue
    pp = (1 + sum(x >= k for x in nv)) / 20; pm = (1 + sum(x <= k for x in nv)) / 20; ps.append((pp, pm))
    print(f"{nm}: K4 {k} nulls {min(nv)}-{max(nv)} mean {st.mean(nv):.1f} p+ {pp:.2f} p- {pm:.2f}")
if ps: print(f"grid p+ {min(p for p, _ in ps):.2f} (min over cells) / p- {min(m for _, m in ps):.2f}  [no multiplicity correction; floor 0.05]")
