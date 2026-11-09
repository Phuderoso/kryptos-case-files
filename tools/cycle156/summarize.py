"""Cycle 156 summary: per (n,k1,k2) and text, strict survivors / underdetermined and one-error (block-drop) survivors, best score.
Also marks whether lcm(k1,n,k2) lies inside case 132's exactly tested period range (n2 k<=14, n3 k<=10, n4 k<=4)."""
import glob, re, sys
from math import lcm
from collections import defaultdict
R=defaultdict(dict); tests=defaultdict(int)
for fn in glob.glob(sys.argv[1]+"/*.txt"):
    for l in open(fn):
        if not l.startswith("C "): continue
        w=dict(x.split("=",1) for x in l.split()[2:]); lab=l.split()[1]; mode="D" if lab.startswith("D") else "B"; lab=lab.lstrip("D") if mode=="D" else lab
        key=(mode,int(w["n"]),int(w["k1"]),int(w["k2"])); r=R[key].setdefault(lab,[0,0,0,0,0,-99.0])
        r[0]+=int(w["tests"]); r[1]+=int(w["survivors"]); r[2]+=int(w["underdet"]); r[3]+=int(w["drop_survivors"]); r[4]+=int(w["drop_underdet"]); r[5]=max(r[5],float(w["best"]))
C132={2:14,3:10,4:4}
print("mode n k1 k2 lcm in132 | K4 tests surv under drop_surv drop_under best | null1 ... | null2 ...")
for key in sorted(R):
    m,n,a,b=key; L=lcm(a,n,b); line=f"{m} {n} {a} {b} {L} {'y' if L<=C132[n] else 'n'} |"
    for lab in ("K4","null1","null2"):
        r=R[key].get(lab); line+=" "+(" ".join(map(str,r[:5]))+f" {r[5]:.3f}" if r else "-")+" |"
    print(line)
