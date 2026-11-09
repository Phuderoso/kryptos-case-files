"""Cycle 156 controls (IDEAS I-050): key on both sides of the Hill step.
Encryption: x[t] = p[t] - e[t mod k1]; y_block = E.x_block (blocks from offset o); L[t] = y[t] + f[t mod k2]
<=> decoder (hill2s.c): out_block = D.(L_block - f) + e, D = E^-1.  English control text of cycle 137 (cribs in place).
Frames as hill2s.c: ix=0: L[i]=C[S[i]], PT=out; ix=1: L=C, PT[p]=out[S[p]].  Seed 15600; nulls = K4 shuffled, seeds 15601-15602.
Error controls (direct): ctl7 one corrupted carved letter inside a crib block, ctl8 one wrong crib letter
(strict must FAIL, DROP=1 must recover).
Output: name n k1 k2 src perm dir ix nu o corrupted_carved_pos(-1) wrong_crib_pt_pos(-1) text   (key lines start with '#')"""
import importlib.util, random, os, sys
import numpy as np
here=os.path.dirname(os.path.abspath(__file__))
spec=importlib.util.spec_from_file_location("p141","/tmp/kcf/tools/cycle141/plant.py"); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
R=random.Random(15600)
def rmat(n):
    while True:
        D=[[R.randrange(26) for _ in range(n)] for _ in range(n)]; E=m.inv26(D)
        if E: return D,E
def enc(text,n,k1,k2,o,N,keys):
    D,E=rmat(n); e=[R.randrange(26) for _ in range(k1)]; f=[R.randrange(26) for _ in range(k2)]; keys.append((D,e,f)); t=list(text)
    for b in range(o,97-n+1,n):
        x=[(N.index(text[b+j])-e[(b+j)%k1])%26 for j in range(n)]
        for r in range(n): t[b+r]=N[(sum(E[r][j]*x[j] for j in range(n))+f[(b+r)%k2])%26]
    return "".join(t)
def ctl(P,n,k1,k2,o,nu,ix,S,crib_t,wrong_t,keys):
    N=m.NUMS[nu]; P=list(P)
    if wrong_t is not None: P[wrong_t]=R.choice([x for x in N if x!=P[wrong_t]])
    P="".join(P)
    if ix==0:
        L=enc(P,n,k1,k2,o,N,keys); C=[None]*97
        for i in range(97): C[S[i]]=L[i]
    else:
        out=[None]*97
        for p in range(97): out[S[p]]=P[p]
        C=list(enc("".join(out),n,k1,k2,o,N,keys))
    carved=None if crib_t is None else S[crib_t]
    if carved is not None:
        old=C[carved]; C[carved]=R.choice([x for x in N if x!=old])
    return "".join(C),(-1 if carved is None else carved)
if __name__=="__main__":
    P=m.m.plain(); B=np.fromfile("/home/box/kryptos_support_backup/perms97.bin",dtype=np.int16).reshape(-1,97); I=list(range(97))
    specs=[("ctl1",2,3,5,"-",0,0,0,0,0,None,None),("ctl2",2,5,4,"P",4242,0,0,1,1,None,None),("ctl3",2,3,7,"P",120000,0,1,0,0,None,None),
           ("ctl4",3,2,5,"-",0,0,0,0,1,None,None),("ctl5",3,4,3,"-",0,0,0,1,2,None,None),("ctl6",2,7,3,"-",0,0,0,0,1,None,None),
           ("ctl7",2,3,5,"-",0,0,0,0,1,26,None),("ctl8",3,2,5,"-",0,0,0,0,0,None,66),("ctl9",4,2,3,"-",0,0,0,0,3,None,None),
           ("ctl10",2,5,3,"P",99999,1,1,1,1,None,None)]
    for nm,n,k1,k2,src,q,d,ix,nu,o,ct,wt in specs:
        S=I if src=="-" else (list(B[q]) if d==0 else list(np.argsort(B[q])))
        keys=[]; t,c=ctl(P,n,k1,k2,o,nu,ix,S,ct,wt,keys); print(nm,n,k1,k2,src,q,d,ix,nu,o,c,-1 if wt is None else wt,t)
        D,e,f=keys[0]; print("#",nm,"D="+",".join(str(x%26) for r in D for x in r),"e'="+",".join(str(x%26) for x in e),"f="+",".join(map(str,f)),file=sys.stderr)
    for z in (1,2):
        l=list(m.K4); random.Random(15600+z).shuffle(l); print(f"null{z} 0 0 0 - 0 0 0 0 0 -1 -1","".join(l))
