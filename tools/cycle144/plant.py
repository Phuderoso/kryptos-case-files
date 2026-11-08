"""Cycle 144 controls: Hill n x n + additive key of period k on the Hill output stream (decoder:
out[t] = D.c_block + e[t mod k]), planted on cycle 137's English control text.
Seed 14400; nulls: K4 shuffled with seeds 14401-14402."""
import importlib.util, random, os
import numpy as np
here=os.path.dirname(os.path.abspath(__file__))
for cand in (os.path.join(here,"../cycle141/plant.py"),"/workspace/k141/plant.py"):
    if os.path.exists(cand): break
spec=importlib.util.spec_from_file_location("p141",cand); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
R=random.Random(14400); m.R=R
def rmat(n):
    while True:
        D=[[R.randrange(26) for _ in range(n)] for _ in range(n)]; E=m.inv26(D)
        if E: return D,E
def enc(text,n,k,o,N):
    D,E=rmat(n); e=[R.randrange(26) for _ in range(k)]; t=list(text)
    for b in range(o,97-n+1,n):
        v=[(N.index(text[b+r])-e[(b+r)%k])%26 for r in range(n)]
        for r in range(n): t[b+r]=N[sum(E[r][j]*v[j] for j in range(n))%26]
    return "".join(t)
def ctl(P,n,k,o,nu,ix,S):
    N=m.NUMS[nu]
    if ix==0:
        L=enc(P,n,k,o,N); C=[None]*97
        for i in range(97): C[S[i]]=L[i]
        return "".join(C)
    out=[None]*97
    for p in range(97): out[S[p]]=P[p]
    return enc("".join(out),n,k,o,N)
if __name__=="__main__":
    P=m.m.plain(); B=np.fromfile("/home/box/kryptos_support_backup/perms97.bin",dtype=np.int16).reshape(-1,97); I=list(range(97))
    print("ctl1 2 7 - 0", ctl(P,2,7,1,0,0,I))                     # direct n2 k7 o1
    print("ctl2 3 5 P 4242", ctl(P,3,5,2,1,0,list(B[4242])))      # model Q n3 k5 KRYPTOS
    print("ctl3 2 11 P 120000", ctl(P,2,11,0,0,1,list(B[120000]))) # carved n2 k11
    print("ctl4 3 8 P 99999", ctl(P,3,8,1,0,1,list(np.argsort(B[99999])))) # carved n3 k8, dir1
    print("ctl5 4 3 P 77777", ctl(P,4,3,2,0,0,list(B[77777])))    # model Q n4 k3
    print("ctl6 2 13 - 0", ctl(P,2,13,0,1,0,I))                    # direct n2 k13 KRYPTOS
    for z in (1,2):
        l=list(m.K4); random.Random(14400+z).shuffle(l); print(f"null{z} 0 0 - 0","".join(l))
