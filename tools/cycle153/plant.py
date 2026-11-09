"""Cycle 153 controls: Hill n x n + additive key of period k (k = 0: plain Hill, n = 5) planted on cycle 137's English
control text, then ONE carved letter corrupted inside a crib-bearing Hill block (a carving error), so the strict test
must fail and hillk1e's block-drop + exact repair must recover it. Also one uncorrupted control (strict must pass) and
one control with ONE WRONG CRIB LETTER (the plaintext differs from the published crib at one position).
Decoder frames as hillk1e.c: ix=0: L[i]=C[S[i]], out[t]=D.L_block+e[t mod k], PT=out; ix=1: out from C, PT[p]=out[S[p]].
Seed 15300; nulls = K4 shuffled, seeds 15301-15302.
Output: name n k src perm dir ix nu o corrupted_carved_pos(-1) wrong_crib_pt_pos(-1) text"""
import importlib.util, random, os
import numpy as np
here=os.path.dirname(os.path.abspath(__file__))
spec=importlib.util.spec_from_file_location("p141",os.path.join(here,"../cycle141/plant.py")); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
R=random.Random(15300)
def rmat(n):
    while True:
        D=[[R.randrange(26) for _ in range(n)] for _ in range(n)]; E=m.inv26(D)
        if E: return D,E
def enc(text,n,k,o,N):
    """inverse of out[t]=D.c_block+e[t mod k]: c_block = E.(p_block - e)"""
    D,E=rmat(n); e=[R.randrange(26) for _ in range(k)] if k else []; t=list(text)
    for b in range(o,97-n+1,n):
        v=[(N.index(text[b+r])-(e[(b+r)%k] if k else 0))%26 for r in range(n)]
        for r in range(n): t[b+r]=N[sum(E[r][j]*v[j] for j in range(n))%26]
    return "".join(t)
def ctl(P,n,k,o,nu,ix,S,crib_t,wrong_t):
    N=m.NUMS[nu]; P=list(P)
    if wrong_t is not None: P[wrong_t]=R.choice([x for x in N if x!=P[wrong_t]])
    P="".join(P)
    if ix==0:
        L=enc(P,n,k,o,N); C=[None]*97
        for i in range(97): C[S[i]]=L[i]
    else:
        out=[None]*97
        for p in range(97): out[S[p]]=P[p]
        C=list(enc("".join(out),n,k,o,N))
    carved=None if crib_t is None else S[crib_t]
    if carved is not None:
        old=C[carved]; C[carved]=R.choice([x for x in N if x!=old])
    return "".join(C),(-1 if carved is None else carved)
if __name__=="__main__":
    P=m.m.plain(); B=np.fromfile("/home/box/kryptos_support_backup/perms97.bin",dtype=np.int16).reshape(-1,97); I=list(range(97))
    # name n k src perm dir ix nu o crib_t(corrupt block) wrong_crib_t
    specs=[("ctl1",2,7,"-",0,0,0,0,1,25,None),("ctl2",3,5,"P",4242,0,0,1,2,66,None),("ctl3",2,11,"P",120000,0,1,0,0,30,None),
           ("ctl4",3,10,"P",99999,1,1,0,1,70,None),("ctl5",4,3,"P",77777,0,0,0,2,24,None),("ctl6",4,4,"-",0,0,0,1,0,64,None),
           ("ctl7",2,14,"-",0,0,0,0,0,72,None),("ctl8",5,0,"-",0,0,0,0,3,28,None),("ctl9",5,0,"-",0,0,0,1,1,67,None),
           ("ctl10",3,6,"-",0,0,0,0,2,None,None),("ctl11",3,4,"P",54321,0,0,0,0,None,29)]
    for nm,n,k,src,q,d,ix,nu,o,ct,wt in specs:
        S=I if src=="-" else (list(B[q]) if d==0 else list(np.argsort(B[q])))
        t,c=ctl(P,n,k,o,nu,ix,S,ct,wt); print(nm,n,k,src,q,d,ix,nu,o,c,-1 if wt is None else wt,t)
    for z in (1,2):
        l=list(m.K4); random.Random(15300+z).shuffle(l); print(f"null{z} 0 0 - 0 0 0 0 0 -1 -1","".join(l))
