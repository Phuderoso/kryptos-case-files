"""Cycle 158 independent recount (pure Python/numpy, different algorithm from hillw.c's null-space checks):
for every direct configuration (numbering, alignment o, f word, sf, e word, se) and every row r of D and field p in {2, 13},
decide by brute force over all p^n row vectors whether some D-row satisfies all crib equations of that row mod p.
Prints totals in the same order as hillw's VC line: cons13 per row, cons2 per row, all (rows x fields consistent).
usage: indep158.py TEXT label n wordfile"""
import sys, itertools, numpy as np
NUMS=["ABCDEFGHIJKLMNOPQRSTUVWXYZ","KRYPTOSABCDEFGHIJLMNQUVWXZ"]; CRIB="EASTNORTHEASTBERLINCLOCK"
CP=list(range(21,34))+list(range(63,74))
T,lab,n,wf=sys.argv[1],sys.argv[2],int(sys.argv[3]),sys.argv[4]
W=[w for w in open(wf).read().split() if len(w)<=15]
c13=[0]*4; c2=[0]*4; allc=0
for nu in (0,1):
    N=NUMS[nu]; L=[N.index(c) for c in T]; Wv=[[N.index(c) for c in w] for w in W]
    for o in range(n):
        nb=(97-o)//n; eqs=[(t,(t-o)%n,o+((t-o)//n)*n,N.index(CRIB[k])) for k,t in enumerate(CP) if o<=t<o+nb*n]
        for F in Wv:
            for sf in (1,-1):
                V=[(L[t]+sf*F[t%len(F)])%26 for t in range(97)]
                ok={}  # (p,r) -> bool array over (e word, se)
                for p in (13,2):
                    cand=np.array(list(itertools.product(range(p),repeat=n)),dtype=np.int64)
                    for r in range(n):
                        er=[(t,bs,pv) for (t,rr,bs,pv) in eqs if rr==r]
                        Vm=np.array([[V[bs+j] for j in range(n)] for (t,bs,pv) in er]).T % p
                        outs=set(map(bytes,((cand@Vm)%p).astype(np.uint8)))
                        res=[]
                        for E in Wv:
                            for se in (1,-1):
                                rhs=bytes([(pv+se*E[t%len(E)])%26%p for (t,bs,pv) in er]); res.append(rhs in outs)
                        res=np.array(res); ok[(p,r)]=res
                        (c13 if p==13 else c2)[r]+=int(res.sum())
                a=np.ones(len(W)*2,bool)
                for v in ok.values(): a&=v
                allc+=int(a.sum())
print("VC %s n=%d cons13=%s cons2=%s all=%d"%(lab,n,",".join(map(str,c13)),",".join(map(str,c2)),allc))
