"""Cycle 169 summary: K4 one-error running keys behind decimations/routes, controls, 40 nulls, analytic bound.
usage: summarize169.py RUN_DIR"""
import sys, glob, re, os, math, subprocess
R = sys.argv[1]; os.chdir(R)
def summ(f):
    s = [l for l in open(f) if l.startswith("SUMMARY")]
    if not s: return None
    m = re.search(r"perms=(\d+) configs=(\d+) best=(\d+) best1=(\d+) full=(\d+) fit23=(\d+) hist:(.*) hist1:(.*) bestS=(\d+) histS:(.*)", s[0])
    hs = lambda x: {int(a): int(b) for a, b in (y.split(":") for y in x.split())}
    return dict(perms=int(m[1]), configs=int(m[2]), best=int(m[3]), best1=int(m[4]), full=int(m[5]), fit23=int(m[6]),
                hist=hs(m[7]), hist1=hs(m[8]), bestS=int(m[9]), histS=hs(m[10]))
def strict_summ(f):
    s = [l for l in open(f) if l.startswith("SUMMARY")]; return re.search(r"best=(\d+) full=(\d+)", s[0]).groups() if s else None
print("# Cycle 169 summary (I-087 one-error named running keys behind 165,782 decimations + routes; I-090 masked depths)\n")
tot = dict(perms=0, configs=0, full=0, fit23=0); h1 = {}; hS = {}; best1 = 0; bestS = 0; missing = []
for c in sorted(glob.glob("chunk_??")):
    f = f"out/k4_{c}.out"; s = summ(f) if os.path.exists(f) else None
    if not s: missing.append(c); continue
    for k in tot: tot[k] += s[k]
    best1 = max(best1, s["best1"]); bestS = max(bestS, s["bestS"])
    for k, v in s["hist1"].items(): h1[k] = h1.get(k, 0) + v
    for k, v in s["histS"].items(): hS[k] = hS.get(k, 0) + v
print(f"K4: chunks done {16-len(missing)}/16 {('missing ' + ','.join(missing)) if missing else ''}")
print(f"K4: perms {tot['perms']:,}  configs {tot['configs']:,} (x 48 texts inside each run; one config = perm x model x mode, all texts)")
print(f"K4: FULL {tot['full']}  FIT23 {tot['fit23']}  best one-error depth1 {best1}  best masked strict depth (bookrk configs) {bestS}")
print("K4 hist1 (one-error prefix depth):", " ".join(f"{k}:{h1[k]}" for k in sorted(h1)))
print("K4 histS (masked strict, bookrk's config set):", " ".join(f"{k}:{hS[k]}" for k in sorted(hS)))
cands = []
for f in sorted(glob.glob("out/k4_chunk_*.out")):
    for l in open(f):
        if l.startswith("CAND1") and int(re.search(r"depth1=(\d+)", l)[1]) >= 12: cands.append(f"{f}: {l.strip()}")
print(f"K4 configs with depth1 >= 12: {len(cands)}"); [print("  ", x) for x in cands[:20]]
for f in sorted(glob.glob("out/k4_chunk_*.out")):
    for l in open(f):
        if l.startswith(("FULL", "FIT23")): print("  K4 HIT", f, l.strip())
# nulls
ns = []
for i in range(40):
    f = f"out/null{i}.out"; s = summ(f) if os.path.exists(f) else None
    if s: ns.append(s)
k4s = summ("out/k4_nullslice.out") if os.path.exists("out/k4_nullslice.out") else None
print(f"\nNull lineup on nullslice.bin (first 500 decimations + last 500 routes): K4 best1 {k4s['best1'] if k4s else 'n/a'} fit23 {k4s['fit23'] if k4s else 'n/a'}")
if ns:
    b1 = sorted(x["best1"] for x in ns); nf = sum(1 for x in ns if x["fit23"] or x["full"])
    ub = 1 - 0.05 ** (1 / len(ns)) if nf == 0 else float("nan")
    print(f"nulls done {len(ns)}/40: best1 min/median/max {b1[0]}/{b1[len(b1)//2]}/{b1[-1]}; nulls with any >=23/24 fit: {nf}/{len(ns)}"
          + (f" (exact binomial one-sided 95% upper bound on null fit rate {100*ub:.1f}%)" if nf == 0 else ""))
    if k4s: print(f"nulls with best1 >= K4's {k4s['best1']}: {sum(1 for x in b1 if x >= k4s['best1'])}/{len(ns)}")
# controls
print("\nControls (ctl169/planted.txt):")
pl = {l.split(":")[0]: l.strip() for l in open("ctl169/planted.txt")}
ok = 0; n = 0
for name, line in sorted(pl.items()):
    m = re.search(r"perm (\d+) slice (\d+) model (\w) mode (\d+) text (\S+) offset (\d+)", line); si, model, md, text, o = m[2], m[3], m[4], m[5], m[6]
    f = f"out/ctl_{name}.out"; s = summ(f) if os.path.exists(f) else None
    if not s: print(f"  {name}: not finished"); continue
    hits = [l.strip() for l in open(f) if l.startswith(("FULL", "FIT23"))]
    planted = [h for h in hits if f"perm={si} model={model} mode={md} text={text} offset={o}" in h]
    st = strict_summ(f"out/ctlS_{name}.out") if os.path.exists(f"out/ctlS_{name}.out") else None
    if name[0] == "e":
        exp_miss = re.search(r"expect FIT23 miss=(\d+)", line)[1]
        good = any(h.startswith("FIT23") and h.endswith(f"miss={exp_miss}") for h in planted) and st and st[1] == "0"
    elif name[0] == "n":
        good = any(h.startswith("FULL") for h in planted)
    else:
        good = not planted
    n += 1; ok += good
    print(f"  {name}: {'PASS' if good else 'FAIL'}  planted-config hits {len(planted)}, all hits {len(hits)}, strict bookrk best/full {st}")
print(f"controls PASS {ok}/{n}")
# analytic bound (letter-frequency worst case)
pl_ = 1 / 26
print(f"\nBound: P(>=23 of 24 | random key letter, uniform) = 24*(1/26)^23*(25/26) + (1/26)^24 = {24*pl_**23*(25/26)+pl_**24:.2e}; "
      f"x 3.2e13 placements = {3.2e13*(24*pl_**23*(25/26)+pl_**24):.1e} expected chance fits")
for p in (0.10, 0.127):
    print(f"  worst case every required key letter as common as p={p}: {3.2e13*(24*p**23*(1-p)+p**24):.1e} expected chance fits")
