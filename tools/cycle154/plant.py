"""Cycle 154 controls (IDEAS I-012): Hill first, then a period-k Vigenere on the Hill output (key on the ciphertext side):
L_block = E.p_block + f[(bs+j) mod k]  <=>  decoder p_block = D.(L_block - f).  English control text of cycle 137.
Frames as hillcs.c: ix=0: L[i]=C[S[i]], PT=out; ix=1: L=C, PT[p]=out[S[p]]. Seed 15400; nulls = K4 shuffled, seeds 15401-15402.
Two error controls (direct): ctl7 one corrupted carved letter inside a crib block (strict must FAIL, DROP=1 must recover),
ctl8 one wrong crib letter (strict must FAIL, DROP=1 must recover).
Output: name n k src perm dir ix nu o corrupted_carved_pos(-1) wrong_crib_pt_pos(-1) text"""
import importlib.util, random, os
import numpy as np
here=os.path.dirname(os.path.abspath(__file__))
spec=importlib.util.spec_from_file_location("p141",os.path.join(here,"../cycle141/plant.py")); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
R=random.Random(15400)
def rmat(n):
    while True:
        D=[[R.randrange(26) for _ in range(n)] for _ in range(n)]; E=m.inv26(D)
        if E: return D,E
def enc(text,n,k,o,N):
    D,E=rmat(n); f=[R.randrange(26) for _ in range(k)]; t=list(text)
    for b in range(o,97-n+1,n):
        v=[N.index(text[b+j]) for j in range(n)]
        for r in range(n): t[b+r]=N[(sum(E[r][j]*v[j] for j in range(n))+f[(b+r)%k])%26]
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
    specs=[("ctl1",2,9,"-",0,0,0,0,1,None,None),("ctl2",3,4,"P",4242,0,0,1,2,None,None),("ctl3",2,13,"P",120000,0,1,0,0,None,None),
           ("ctl4",3,7,"P",99999,1,1,0,1,None,None),("ctl5",4,3,"P",77777,0,0,0,3,None,None),("ctl6",2,19,"-",0,0,0,1,0,None,None),
           ("ctl7",3,5,"-",0,0,0,0,2,26,None),("ctl8",2,11,"-",0,0,0,0,1,None,66),("ctl9",4,5,"P",31337,0,0,0,1,None,None),
           ("ctl10",3,8,"P",150000,1,0,1,0,None,None)]
    for nm,n,k,src,q,d,ix,nu,o,ct,wt in specs:
        S=I if src=="-" else (list(B[q]) if d==0 else list(np.argsort(B[q])))
        t,c=ctl(P,n,k,o,nu,ix,S,ct,wt); print(nm,n,k,src,q,d,ix,nu,o,c,-1 if wt is None else wt,t)
    for z in (1,2):
        l=list(m.K4); random.Random(15400+z).shuffle(l); print(f"null{z} 0 0 - 0 0 0 0 0 -1 -1","".join(l))
