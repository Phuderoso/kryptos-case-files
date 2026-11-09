"""Cycle 188 summary: C1/C2/C3 totals, audit, grid ranks (I-152), I-183 verdict (PREREG188 B).  usage: summarize188.py rundir"""
import sys, glob, os, statistics as st
d = sys.argv[1]
def rd(fn):
    r = {}; t = open(fn).read(); end = "\nEND" in t; x = t.count("\nX ")
    for l in t.split("\n"):
        a = l.split()
        if a and a[0] == "H": r[(int(a[3]), a[5])] = [int(a[7]), int(a[11]), int(a[13])] + ([int(a[15]), int(a[17])] if len(a) > 15 else [])
    return r, end, x
def tot(fns):
    t = {}; ends = 0; xs = 0
    for fn in fns:
        if not os.path.exists(fn): continue
        r, e, x = rd(fn); ends += e; xs += x
        if not e: continue
        for k, v in r.items(): t[k] = [a + b for a, b in zip(t.get(k, [0] * len(v)), v)]
    return t, ends, xs
cells = (("C1 K4 f full L1-2", [f"{d}/out/k4.f.full.c{c}.txt" for c in range(8)]), ("C2 K4 r full L1-2", [f"{d}/out/k4.r.full.c{c}.txt" for c in range(8)]),
         ("C3 K4 f all_s512 L1-3", [f"{d}/out/k4.f.s512L3.txt"]), ("C3 K4 r all_s512 L1-3", [f"{d}/out/k4.r.s512L3.txt"]))
for name, fns in cells:
    t, e, x = tot(fns); print(f"{name} (chunks with END {e}/{len(fns)}, X {x}):", "; ".join(f"L{L} {fm}: perms {v[0]} pass2 {v[1]} fits {v[2]} strict {v[3]} slot {v[4]}" for (L, fm), v in sorted(t.items())))
for dr in ("f", "r"):
    a, b = rd(f"{d}/out/k4.{dr}.s20k.txt"), rd(f"{d}/out/k4.{dr}.s20ksafe.txt")
    print(f"audit {dr}: main == SAFE {a[0] == b[0]} END {a[1] and b[1]} X {a[2] + b[2]}")
labs = [l.split()[0] for l in open(f"{d}/nulls188.txt")]
for dr in ("f", "r"):
    for stat in ("F", "D"):
        def val(lab):
            r = rd(f"{d}/out/{lab}.{dr}.s512.txt")[0]
            return sum(v[2] for v in r.values()) if stat == "F" else r[(2, "vig")][1]
        k = val("k4"); ns = [val(l) for l in labs]
        if stat == "F" and k == 0 and not any(ns): print(f"grid {dr} F: all zero (not scored)"); continue
        pp = (1 + sum(n >= k for n in ns)) / 20; pm = (1 + sum(n <= k for n in ns)) / 20
        print(f"grid {dr} {stat}: K4 {k} nulls {min(ns)}-{max(ns)} mean {st.mean(ns):.1f} SD {st.stdev(ns):.1f} p+ {pp:.2f} p- {pm:.2f} z {(k-st.mean(ns))/st.stdev(ns):+.2f}")
I = {}
for fn in glob.glob(f"{d}/i183/*.txt"):
    lab = fn.split("/")[-1][:-4]; t = open(fn).read()
    if "\nEND" not in t: continue
    for l in t.split("\n"):
        a = l.split()
        if a and a[0] == "H" and a[3] == "3" and a[5] == "vig": I[lab] = int(a[11])
if I:
    K4 = open(f"{d}/k4.txt").read().strip(); TX = dict(l.split() for l in open(f"{d}/i183_texts188.txt"))
    k = I["k4"]; m = [v for l, v in I.items() if l[0] == "m"]; f = [v for l, v in I.items() if l[0] == "f"]
    agree = {l: sum((ord(a) - 65) % 2 == (ord(b) - 65) % 2 for a, b in zip(TX[l], K4)) for l in TX if l[0] == "f"}
    med = st.median(agree.values()); filt = [I[l] for l in agree if agree[l] >= med and l in I]
    pF = (1 + sum(v >= k for v in m)) / (len(m) + 1)
    print(f"I-183 D (r, L3 mod-2 passes, all.bin[256::512]) K4 {k}; matched n {len(m)} {min(m)}-{max(m)} mean {st.mean(m):.1f} SD {st.stdev(m):.1f} #>=K4 {sum(v>=k for v in m)} pF {pF:.3f} z {(k-st.mean(m))/st.stdev(m):+.2f}")
    print(f"   plain n {len(f)} {min(f)}-{max(f)} mean {st.mean(f):.1f} SD {st.stdev(f):.1f} #>=K4 {sum(v>=k for v in f)}; filtered (parity agreement >= median {med}) n {len(filt)} mean {st.mean(filt):.1f}; inflation (filtered - matched) {st.mean(filt)-st.mean(m):+.1f}")
    print("   verdict:", "REPLICATED" if pF <= 0.05 and len(m) == 40 else ("NOT REPLICATED" if len(m) == 40 else f"INCOMPLETE ({len(m)}/40 matched)"))
else: print("I-183: not run")
