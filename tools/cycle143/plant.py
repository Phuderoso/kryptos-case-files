"""Cycle 143 controls: affine Hill (p = D c + e per block, i.e. Hill plus a period-n additive key)
planted on cycle 137's English control plaintext. Decoder model as cycle 141 (ix=0 model Q, ix=1 carved).
Seed 14300; nulls: shuffled K4 seeds 14301-14302."""
import importlib.util, random
import numpy as np
spec=importlib.util.spec_from_file_location("p141",__import__("os").path.join(__import__("os").path.dirname(__file__),"../cycle141/plant.py")); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
R=random.Random(14300); m.R=R
def rmat(n):
    while True:
        D=[[R.randrange(26) for _ in range(n)] for _ in range(n)]; E=m.inv26(D)
        if E: return D,E
def ahill(text,n,o,N):
    D,E=rmat(n); e=[R.randrange(26) for _ in range(n)]; t=list(text)
    for b in range(o,97-n+1,n):
        v=[(N.index(c)-e[r])%26 for r,c in enumerate(text[b:b+n])]
        for r in range(n): t[b+r]=N[sum(E[r][j]*v[j] for j in range(n))%26]
    return "".join(t)
def ctl(P,n,o,nu,ix,S):
    N=m.NUMS[nu]
    if ix==0:
        L=ahill(P,n,o,N); C=[None]*97
        for i in range(97): C[S[i]]=L[i]
        return "".join(C)
    out=[None]*97
    for p in range(97): out[S[p]]=P[p]
    return ahill("".join(out),n,o,N)
if __name__=="__main__":
    P=m.m.plain(); B=np.fromfile("/home/box/kryptos_support_backup/perms97.bin",dtype=np.int16).reshape(-1,97); I=list(range(97))
    print("ctl1 4", ctl(P,4,1,0,0,I))                           # direct n4 o1 A-Z
    print("ctl2 3", ctl(P,3,2,1,0,list(B[4242])))               # model Q n3 KRYPTOS, entry 4242 dir0
    print("ctl3 4", ctl(P,4,3,0,1,list(B[160000])))             # carved n4, entry 160000 dir0
    print("ctl4 2", ctl(P,2,0,1,1,list(np.argsort(B[99999]))))  # carved n2 KRYPTOS, entry 99999 dir1
    print("ctl5 5", ctl(P,5,2,0,0,I))                           # direct n5 o2
    print("ctl6 4", ctl(P,4,0,1,1,list(B[50000])))              # carved n4 KRYPTOS, entry 50000 dir0
    print("ctl7 3", ctl(P,3,1,0,1,list(B[120000])))             # carved n3, entry 120000 dir0
    print("ctl8 4", ctl(P,4,2,0,0,list(B[77777])))              # model Q n4, entry 77777 dir0
    for z in (1,2):
        l=list(m.K4); random.Random(14300+z).shuffle(l); print(f"null{z} 0","".join(l))
