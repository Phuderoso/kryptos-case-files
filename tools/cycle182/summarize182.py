"""Cycle 182 summary: per text and cell, fits and mod-2 passes from the H lines; overflow / mismatch lines; labels; grid by empirical
rank (I-152); then the I-160 replication (PREREG182 section B).
usage: summarize182.py outdir nulls182.txt i160dir"""
import sys, statistics as st
od, nf, idir = sys.argv[1:4]; nulls = [l.split()[0] for l in open(nf)]
def read(fn):
    H = {}; ok = False; bad = []
    for l in open(fn):
        a = l.split()
        if not a: continue
        if a[0] == "H": H[(int(a[3]), a[5])] = dict(pass2=int(a[11]), fits=int(a[13]))
        elif a[0] == "O" and (a[3] != "0" or a[5] != "0"): bad.append(l.strip())
        elif a[0] == "X": bad.append(l.strip())
        elif a[0] == "END": ok = True
    return H, ok, bad
def cell(H, Ls, key):
    return sum(v[key] for (L, fm), v in H.items() if L in Ls) // (2 if key == "pass2" else 1)
cells = [("L1-5", range(1, 6)), ("L6", [6])]
print("== K4 full set (165,782 perms; 2,703,744 (A, B) pairs per direction x Vig/Beau)")
for d in ("f", "r"):
    H, ok, bad = read(f"{od}/k4.{d}.txt")
    for nm, Ls in cells: print(f"K4 {d} {nm:5s} fits {cell(H, Ls, 'fits')} pass2 {cell(H, Ls, 'pass2')} END {ok} bad {bad}")
for d in ("f", "r"):
    a = [l for l in open(f"{od}/k4.{d}s64.txt") if l.startswith("H ")]; b = [l for l in open(f"{od}/k4.{d}s64safe.txt") if l.startswith("H ")]
    print(f"SAFE audit (method 2, no shortcut) k4 {d} all_s64 H lines identical: {a == b}")
print("== all_s64 (K4 + 19 nulls)")
rows = {}
for lab in ["k4"] + nulls:
    r = {}
    for d in ("f", "r"):
        H, ok, bad = read(f"{od}/{lab}.{d}s64.txt")
        for nm, Ls in cells: r[d + nm] = (cell(H, Ls, "fits"), cell(H, Ls, "pass2"), ok, bad)
    rows[lab] = r
    print(lab, " ".join(f"{k}: fits {v[0]} pass2 {v[1]}{'' if v[2] else ' NO-END'}{' BAD' if v[3] else ''}" for k, v in r.items()))
print("== grid (empirical rank among 20 texts; D1 = q4f mod-2 passes at L 6 (all L <= 6 by nesting), D2 = q4r the same; fit cells scored only if not all-zero)")
F = {k: {lab: rows[lab][k][0] for lab in rows} for k in rows["k4"]}
D = {"D1": {lab: rows[lab]["fL6"][1] for lab in rows}, "D2": {lab: rows[lab]["rL6"][1] for lab in rows}}
ps = []
for nm, v in list(F.items()) + list(D.items()):
    k = v["k4"]; nv = [v[l] for l in nulls]
    if nm in F and all(x == 0 for x in v.values()): print(f"{nm}: all zero (reported, not scored)"); continue
    pp = (1 + sum(x >= k for x in nv)) / 20; pm = (1 + sum(x <= k for x in nv)) / 20; ps.append((pp, pm))
    print(f"{nm}: K4 {k} nulls {min(nv)}-{max(nv)} mean {st.mean(nv):.1f} p+ {pp:.2f} p- {pm:.2f}")
if ps: print(f"grid p+ {min(p for p, _ in ps):.2f} (min over cells) / p- {min(m for _, m in ps):.2f}  [no multiplicity correction; floor 0.05]")
print("== I-160 replication (case 169 D2 = lrk181 M1 one-error mod-2 passes L 1-3, all_s64, sum over L and types; registered K4 value 18,432)")
def d2(fn):
    s = {"q1": 0, "q2": 0, "q3": 0}; end = False
    for l in open(fn):
        a = l.split()
        if a[0] == "H" and a[5] == "vig": s[a[4]] += int(a[11])
        if a[0] == "END": end = True
    assert end; return sum(s.values()), s
labs = [l.split()[0] for l in open(f"{idir}/texts182.txt")]; v = {l: d2(f"{idir}/{l}.txt") for l in labs}
k4, k4s = v["k4"]; print(f"K4 recomputed D2 {k4} {k4s} (registered 18,432: {'same' if k4 == 18432 else 'DIFFERENT'})")
dec = {}
for grp, pre in (("plain fresh shuffles (40)", "f"), ("parity-matched shuffles (20)", "m")):
    g = [l for l in labs if l[0] == pre]; x = [v[l][0] for l in g]; ge = sum(t >= k4 for t in x); pF = (1 + ge) / (len(x) + 1)
    m, sd = st.mean(x), st.stdev(x); dec[pre] = pF
    print(f"{grp}: min {min(x)} max {max(x)} mean {m:.1f} SD {sd:.1f} #>=K4 {ge} p_F {pF:.3f} z {(k4 - m) / sd:+.2f}")
    for t in ("q1", "q2", "q3"):
        y = [v[l][1][t] for l in g]; print(f"   {t}: K4 {k4s[t]} mean {st.mean(y):.1f} SD {st.stdev(y):.1f} #>=K4 {sum(a >= k4s[t] for a in y)}")
print("I-160 DECISION:", "REPLICATED (flag stays open; still not a fit)" if dec["f"] <= 0.05 and dec["m"] <= 0.05 else
      ("NOT REPLICATED (flag closed)" if dec["f"] > 0.05 else "REPLICATED vs plain only; explained by the A-Z parity pattern (matched p_F > 0.05)"))
