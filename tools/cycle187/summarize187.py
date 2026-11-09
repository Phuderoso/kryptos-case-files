"""Cycle 187 summary: C1/C2 totals, grid ranks (I-152), I-176 verdict (PREREG187 B).  usage: summarize187.py rundir"""
import sys, glob, statistics as st
d = sys.argv[1]
def H(fn):
    r = {}
    for l in open(fn):
        a = l.split()
        if a[0] == "H": r[(int(a[3]), a[5])] = (int(a[7]), int(a[11]), int(a[13]))
    return r
def tot(fns):
    t = {}
    for fn in fns:
        for k, v in H(fn).items(): t[k] = tuple(x + y for x, y in zip(t.get(k, (0, 0, 0)), v))
    return t
for name, fns in (("C1 K4 f full", sorted(glob.glob(f"{d}/out/k4.f.full.c*.txt"))), ("C2 K4 r all_s8", [f"{d}/out/k4.r.s8.txt"])):
    t = tot(fns); print(name, "; ".join(f"L{L} {fm}: perms {v[0]} pass2 {v[1]} fits {v[2]}" for (L, fm), v in sorted(t.items())))
labs = [l.split()[0] for l in open(f"{d}/nulls187.txt")]
for dr in ("f", "r"):
    for stat, idx in (("F", 2), ("D", 1)):
        val = lambda lab: (sum(v[2] for v in H(f"{d}/out/{lab}.{dr}.s512.txt").values()) if idx == 2 else H(f"{d}/out/{lab}.{dr}.s512.txt")[(3, "vig")][1])
        k = val("k4"); ns = [val(l) for l in labs]
        if stat == "F" and k == 0 and not any(ns): print(f"grid {dr} F: all zero (not scored)"); continue
        pp = (1 + sum(n >= k for n in ns)) / 20; pm = (1 + sum(n <= k for n in ns)) / 20
        print(f"grid {dr} {stat}: K4 {k} nulls {min(ns)}-{max(ns)} mean {st.mean(ns):.1f} SD {st.stdev(ns):.1f} p+ {pp:.2f} p- {pm:.2f}")
I = {}
for fn in glob.glob(f"{d}/i176/*.txt"):
    lab = fn.split("/")[-1][:-4]; t = open(fn).read()
    if "\nEND" not in t: continue
    for l in t.split("\n"):
        a = l.split()
        if a and a[0] == "H" and a[3] == "3" and a[5] == "vig": I[lab] = int(a[11])
if I:
    K4 = open(f"{d}/k4.txt").read().strip(); TX = dict(l.split() for l in open(f"{d}/i176_texts187.txt"))
    k = I["k4"]; m = [v for l, v in I.items() if l[0] == "m"]; f = [v for l, v in I.items() if l[0] == "f"]
    agree = {l: sum((ord(a) - 65) % 2 == (ord(b) - 65) % 2 for a, b in zip(TX[l], K4)) for l in TX if l[0] == "f"}
    med = st.median(agree.values()); filt = [I[l] for l in agree if agree[l] >= med]
    pF = (1 + sum(v >= k for v in m)) / (len(m) + 1)
    print(f"I-176 D1 K4 {k}; matched n {len(m)} {min(m)}-{max(m)} mean {st.mean(m):.1f} SD {st.stdev(m):.1f} #>=K4 {sum(v>=k for v in m)} pF {pF:.3f} z {(k-st.mean(m))/st.stdev(m):+.2f}")
    print(f"   plain n {len(f)} {min(f)}-{max(f)} mean {st.mean(f):.1f} SD {st.stdev(f):.1f} #>=K4 {sum(v>=k for v in f)}; filtered (parity agreement >= median {med}) n {len(filt)} mean {st.mean(filt):.1f}; inflation (filtered - matched) {st.mean(filt)-st.mean(m):+.1f}")
    print("   verdict:", "REPLICATED" if pF <= 0.05 else "NOT REPLICATED")
