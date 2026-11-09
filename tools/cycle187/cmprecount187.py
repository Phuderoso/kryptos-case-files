"""Cycle 187: compare recount187.py F lines with lrk186 (MAIN build, method 1, A = B = recount list, L 1) M lines on the slice, per
(text, row, A, B, form).   usage: cmprecount187.py recount.txt texts.txt Cdir"""
import sys
rc = sys.argv[1]; labs = [l.split()[0] for l in open(sys.argv[2])]; cd = sys.argv[3]
R = set(); done = set()
for l in open(rc):
    a = l.split()
    if a[0] == "F": R.add(tuple(a[1:6]))
    elif a[0] == "DONE": done.add(a[1])
ok = True
for lab in labs:
    C = set(); end = False
    for l in open(f"{cd}/c_{lab}.txt"):
        a = l.split()
        if a[0] == "END": end = True
        if a[0] == "X": ok = False
        if a[0] == "M" and a[3] == "1": C.add((lab, a[6], a[7], a[8], a[5]))
    r = {k for k in R if k[0] == lab}; same = r == C; ok &= same and lab in done and end
    print(f"{lab}: recount fits {len(r)} lrk186 fits {len(C)} done {lab in done} END {end} identical {same}")
print("RECOUNT", "MATCH" if ok else "MISMATCH")
