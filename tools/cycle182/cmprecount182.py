"""Cycle 182: compare recount182.py F lines with lrk182 M lines on the slice (per text, L, row, A, B, form); L 2 only at the listed
(text, row, A). usage: cmprecount182.py recount.txt texts.txt Cdir L2spec..."""
import sys
rc = sys.argv[1]; labs = [l.split()[0] for l in open(sys.argv[2])]; cd = sys.argv[3]; L2 = {tuple(s.split(":")) for s in sys.argv[4:]}
R = set(); done = set()
for l in open(rc):
    a = l.split()
    if a[0] == "F": R.add(tuple(a[1:]))
    elif a[0] == "DONE": done.add(a[1])
ok = True
for lab in labs:
    C = set()
    for l in open(f"{cd}/c_{lab}.txt"):
        a = l.split()
        if a[0] == "M":
            L, row, A, B, fm = a[3], a[6], a[7], a[8], a[5]
            if L == "1" or (lab, row, A) in L2: C.add((lab, L, row, A, B, fm))
    r = {x for x in R if x[0] == lab}; same = r == C; ok &= same and lab in done
    print(f"{lab}: recount {len(r)} (L1 {sum(x[1]=='1' for x in r)}, L2 {sum(x[1]=='2' for x in r)}) C {len(C)} done {lab in done} identical {same}")
print("RECOUNT", "MATCH" if ok else "MISMATCH")
