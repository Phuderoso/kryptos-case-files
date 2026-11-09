"""Cycle 159 independent recount on windows: pure-Python checker of tools/cycle155/indep_check.py (all 24 drops, BFS,
no code shared with gromark1e.c) over a primer window; prints counts to compare with gromark1e on the same window.
usage: indep159.py CT L label lo hi   -> 'I label L=.. lo=.. hi=.. strict=.. one=.. pairs=..'"""
import sys,os
src=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','cycle155','indep_check.py')).read()
src=src[:src.rindex('main()')]           # load ok(), AZ, KA, CR without running main
g={}; exec(src,g)
ct,L,lab,lo,hi=sys.argv[1],int(sys.argv[2]),sys.argv[3],int(sys.argv[4]),int(sys.argv[5])
strict=one=pairs=0
for x in range(lo,hi):
    d=[int(c) for c in str(x).zfill(L)]
    while len(d)<74: d.append((d[-L]+d[-L+1])%10)
    for PA in (g['AZ'],g['KA']):
        for f in (0,1):
            eq=[(('c',ct[i]),('o',(i//L)%L),((PA.index(p)+d[i]) if f==0 else (d[i]-PA.index(p)))%26) for i,p in g['CR']]
            if g['ok'](eq): strict+=1; continue
            k=sum(g['ok'](eq[:t]+eq[t+1:]) for t in range(24)); pairs+=k; one+=k>0
print(f"I {lab} L={L} lo={lo} hi={hi} strict={strict} one={one} pairs={pairs}")
