"""Cycle 185 summary: per text and cell, one-error fits / strict fits / slot fits and one-error mod-2 passes from the H lines;
overflow / mismatch lines; labels; grid by empirical rank (I-152).
Cells as PREREG185.md. usage: summarize185.py outdir nulls185.txt"""
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
import os
def show(nm, fn, Ls):
    if not os.path.exists(fn): print(f"{nm}: NOT RUN"); return None
    H, ok, bad = read(fn); print(f"{nm}: {line(H, Ls)} END {ok} bad {bad}"); return H, ok, bad
print("== K4, one error, vocabulary x vocabulary (352,538,176 ordered pairs x Vig/Beau), method 1")
show("K4 all_s64 (2,591 perms) L1-3", f"{od}/k4.s64L3.txt", range(1, 4))
show("K4 all_s8 (20,723 perms) L1-2", f"{od}/k4.s8L2.txt", range(1, 3))
tot = dict(fits=0, strict=0, slots=0, pass2=0); nch = 0; perms = 0
for c in range(8):
    fn = f"{od}/k4.fullL1.c{c}.txt"
    if not os.path.exists(fn): print(f"full L1 chunk {c}: NOT RUN"); continue
    H, ok, bad = read(fn)
    if not ok or bad: print(f"full L1 chunk {c}: INVALID END {ok} bad {bad}"); continue
    nch += 1; perms += next(int(l.split()[7]) for l in open(fn) if l.startswith("H "))
    for k in tot: tot[k] += cell(H, [1], k)
print(f"K4 full set L1: chunks complete {nch}/8, perms {perms}: fits {tot['fits']} (strict {tot['strict']}, slot fits {tot['slots']}) pass2 {tot['pass2']}")
a = [l for l in open(f"{od}/k4.s20k.txt") if l.startswith("H ")]; b = [l for l in open(f"{od}/k4.s20ksafe.txt") if l.startswith("H ")]
print(f"SAFE audit (method 2, every pair, no prefilter, 13-value loop on every slot) k4 all_s20000 (9 rows) L 1-3 H lines identical: {a == b}")
print("== all_s2048 (81 perms; K4 + 19 nulls), one error, L 1-3")
rows = {}
for lab in ["k4"] + nulls:
    H, ok, bad = read(f"{od}/{lab}.s2k.txt")
    rows[lab] = dict(F=cell(H, range(1, 4), "fits"), D1=cell(H, [3], "pass2"), ok=ok, bad=bad)
    print(lab, f"fits L1-3 {rows[lab]['F']} pass2 L3 {rows[lab]['D1']}{'' if ok else ' NO-END'}{' BAD' if bad else ''}")
print("== grid (I-152 empirical rank; F = fits L 1-3, scored only if not all-zero; D1 = one-error mod-2 passes at L 3 = every L <= 3 by nesting)")
ps = []
for nm in ("F", "D1"):
    v = {l: rows[l][nm] for l in rows}; k = v["k4"]; nv = [v[l] for l in nulls]
    if nm == "F" and all(x == 0 for x in v.values()): print("F: all zero (reported, not scored)"); continue
    pp = (1 + sum(x >= k for x in nv)) / 20; pm = (1 + sum(x <= k for x in nv)) / 20; ps.append((pp, pm))
    print(f"{nm}: K4 {k} nulls {min(nv)}-{max(nv)} mean {st.mean(nv):.1f} p+ {pp:.2f} p- {pm:.2f}")
if ps: print(f"grid p+ {min(p for p, _ in ps):.2f} / p- {min(m for _, m in ps):.2f}  [no multiplicity correction; floor 0.05]")
