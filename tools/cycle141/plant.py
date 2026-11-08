"""Cycle 141 controls: Hill 5x5 planted on cycle 137's English control plaintext (cribs in place).
Decoder model (hill5.c): ix=0: L[i]=C[S[i]], PT=HillDec(L); ix=1: out=HillDec(C), PT[p]=out[S[p]].
Seed 14100; nulls are shuffled K4 (seeds 14101-14102)."""
import importlib.util, random
import numpy as np
spec=importlib.util.spec_from_file_location("p137","/tmp/kcf/tools/cycle137/plant.py"); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
K4=m.K4; R=random.Random(14100)
NUMS=["ABCDEFGHIJKLMNOPQRSTUVWXYZ","KRYPTOSABCDEFGHIJLMNQUVWXZ"]
def inv26(M):
    n=len(M); A=[list(r)+[int(i==j) for j in range(n)] for i,r in enumerate(M)]
    for c in range(n):
        s=next((i for i in range(c,n) if A[i][c]%2 and A[i][c]%13),None)
        if s is None: return None
        A[c],A[s]=A[s],A[c]; iv=pow(A[c][c],-1,26); A[c]=[x*iv%26 for x in A[c]]
        for i in range(n):
            if i!=c and A[i][c]: f=A[i][c]; A[i]=[(x-f*y)%26 for x,y in zip(A[i],A[c])]
    return [r[n:] for r in A]
def rmat():
    while True:
        D=[[R.randrange(26) for _ in range(5)] for _ in range(5)]; E=inv26(D)
        if E: return D,E
def hill(text,M,o,N):
    t=list(text)
    for b in range(o,97-4,5):
        v=[N.index(c) for c in text[b:b+5]]
        for r in range(5): t[b+r]=N[sum(M[r][j]*v[j] for j in range(5))%26]
    return "".join(t)
def ctl(P,o,nu,ix,S):
    N=NUMS[nu]; D,E=rmat()
    if ix==0:
        L=hill(P,E,o,N); C=[None]*97
        for i in range(97): C[S[i]]=L[i]
        return "".join(C)
    out=[None]*97
    for p in range(97): out[S[p]]=P[p]
    return hill("".join(out),E,o,N)
if __name__=="__main__":
    P=m.plain(); B=np.fromfile("/home/box/kryptos_support_backup/perms97.bin",dtype=np.int16).reshape(-1,97)
    I=list(range(97))
    print("ctl1", ctl(P,3,0,0,I))                      # direct, A-Z, o=3
    print("ctl2", ctl(P,1,1,0,I))                      # direct, KRYPTOS numbering, o=1
    print("ctl3", ctl(P,0,0,0,list(B[4242])))          # model Q, entry 4242 dir 0
    print("ctl4", ctl(P,4,1,1,list(B[160000])))        # carved, entry 160000 dir 0, KRYPTOS
    print("ctl5", ctl(P,2,0,1,list(np.argsort(B[99999]))))  # carved, entry 99999 dir 1
    for z in (1,2):
        l=list(K4); random.Random(14100+z).shuffle(l); print(f"null{z}","".join(l))
