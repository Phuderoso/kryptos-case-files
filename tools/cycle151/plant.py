"""Cycle 151 controls: Hill n x n (n 2-4) planted on cycle 137's English control text, then ONE carved letter
corrupted (a carving error) so that the strict 24-crib test must fail and the one-error test must recover it.
Decoder frames as hill1e.c: ix=0: L[i]=C[S[i]]; ix=1: out=Hill(C), PT[p]=out[S[p]].
Seed 15100; nulls = K4 shuffled, seeds 15101-15102. Output: name n src perm corrupted_carved_pos text"""
import importlib.util, random, os
import numpy as np
here=os.path.dirname(os.path.abspath(__file__))
spec=importlib.util.spec_from_file_location("p141",os.path.join(here,"../cycle141/plant.py")); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
R=random.Random(15100)
def rmat(n):
    while True:
        D=[[R.randrange(26) for _ in range(n)] for _ in range(n)]; E=m.inv26(D)
        if E: return D,E
def hill(text,M,o,N,n):
    t=list(text)
    for b in range(o,97-n+1,n):
        v=[N.index(c) for c in text[b:b+n]]
        for r in range(n): t[b+r]=N[sum(M[r][j]*v[j] for j in range(n))%26]
    return "".join(t)
def ctl(P,n,o,nu,ix,S,crib_t):
    """crib_t: plaintext crib index whose Hill block gets one corrupted carved letter (None = no corruption)"""
    N=m.NUMS[nu]; D,E=rmat(n)
    if ix==0:
        L=hill(P,E,o,N,n); C=[None]*97
        for i in range(97): C[S[i]]=L[i]
        hpos=crib_t; carved=None if crib_t is None else S[hpos]
    else:
        out=[None]*97
        for p in range(97): out[S[p]]=P[p]
        C=list(hill("".join(out),E,o,N,n)); carved=None if crib_t is None else S[crib_t]
    C=list(C)
    if carved is not None:
        old=C[carved]; C[carved]=R.choice([x for x in N if x!=old])
    return "".join(C), (-1 if carved is None else carved)
if __name__=="__main__":
    P=m.m.plain(); B=np.fromfile("/home/box/kryptos_support_backup/perms97.bin",dtype=np.int16).reshape(-1,97); I=list(range(97))
    specs=[("ctl1",2,1,0,0,"-",0,25),("ctl2",3,2,1,0,"-",0,66),("ctl3",2,0,0,0,"P",4242,30),("ctl4",3,1,0,1,"Pinv",120000,70),
           ("ctl5",4,2,0,0,"P",77777,24),("ctl6",4,0,0,0,"-",0,64),("ctl7",3,0,0,0,"-",0,None),("ctl8",2,1,1,1,"P",99999,None)]
    for nm,n,o,nu,ix,src,q,ct in specs:
        S=I if src=="-" else (list(B[q]) if src=="P" else list(np.argsort(B[q])))
        t,c=ctl(P,n,o,nu,ix,S,ct); print(nm,n,"-" if src=="-" else "P",q,c,t)
    for z in (1,2):
        l=list(m.K4); random.Random(15100+z).shuffle(l); print(f"null{z} 0 - 0 -1","".join(l))
