"""Cycle 71: direct Wheatstone cryptograph with an ARBITRARY outer alphabet (any order of 26 letters + blank on a 27-cell
circle) and an arbitrary inner alphabet (26 cells), clockwise. (Counter-clockwise = reversed outer order, included.)
Exact SMT check (z3) of the crib-consistency conditions used by wheat71.c. Usage: wheat71_sat.py ciphertext_file"""
import sys,z3
ct=open(sys.argv[1]).read().strip()
cribs=[(21,"EASTNORTHEAST"),(63,"BERLINCLOCK")]
s=z3.Solver();s.set("timeout",240000)
pos={c:z3.Int("p_"+c) for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}
for v in pos.values(): s.add(v>=1,v<=26)   # blank fixed at cell 0 (rotation-free)
s.add(z3.Distinct(*pos.values()))
pts=[]  # (T expression, cipher letter)
for ci,(st,w) in enumerate(cribs):
    T=z3.Int(f"r{ci}") ; s.add(T>=0,T<=25)
    for k,ch in enumerate(w):
        if k:
            d=z3.Int(f"s{ci}_{k}"); diff=pos[ch]-pos[w[k-1]]
            s.add(d==z3.If(diff>0,diff,diff+27)); T=T+d
        pts.append((T,ct[st+k]))
for i in range(len(pts)):
    for j in range(i+1,len(pts)):
        same=(pts[i][1]==pts[j][1]); e=(pts[i][0]-pts[j][0])%26==0
        s.add(e if same else z3.Not(e))
r=s.check();print(sys.argv[1],r)
if r==z3.sat:
    m=s.model();print("outer:",sorted(pos,key=lambda c:m[pos[c]].as_long()))
