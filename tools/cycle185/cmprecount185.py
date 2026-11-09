"""Cycle 185: compare recount185.py F lines with lrk185 (MAIN build, method 1, run on the slice with the FULL vocabulary on both sides,
restricted here to pairs with A and B both in the recount list) M lines on the slice, per (text, L, row, A, B, form) on
the SET of fitting slots (-1 = strict); L 2 only at the listed (text, row, A). usage: cmprecount185.py recount.txt texts.txt Cdir alpha_recount.txt L2spec..."""
import sys
from collections import defaultdict
rc = sys.argv[1]; labs = [l.split()[0] for l in open(sys.argv[2])]; cd = sys.argv[3]; RL = {l.split()[1] for l in open(sys.argv[4])}; L2 = {tuple(s.split(":")) for s in sys.argv[5:]}
R = {}; done = set()
for l in open(rc):
    a = l.split()
    if a[0] == "F": R[tuple(a[1:7])] = set(map(int, a[7].split(",")))
    elif a[0] == "DONE": done.add(a[1])
ok = True
for lab in labs:
    C = defaultdict(set); end = False
    for l in open(f"{cd}/c_{lab}.txt"):
        a = l.split()
        if a[0] == "END": end = True
        if a[0] == "X": ok = False
        if a[0] == "M":
            L, row, A, B, fm = a[3], a[6], a[7], a[8], a[5]
            if A not in RL or B not in RL: continue
            if L == "1" or (lab, row, A) in L2: C[(lab, L, row, A, B, fm)].add(int(a[10]))
    r = {k: v for k, v in R.items() if k[0] == lab}; same = r == dict(C); ok &= same and lab in done and end
    print(f"{lab}: recount configs {len(r)} (L1 {sum(k[1]=='1' for k in r)}, L2 {sum(k[1]=='2' for k in r)}; strict {sum(v=={-1} for v in r.values())}) C {len(C)} done {lab in done} END {end} identical {same}")
print("RECOUNT", "MATCH" if ok else "MISMATCH")
