"""Cycle 158 controls (IDEAS I-056): key on both sides of Hill, both keys vocabulary words (phase 0).
Relation (hillw.c): sum_j D[r][j]*(L[bs+j] + sf*F[(bs+j)%k2]) = P[t] + se*E[t%k1]  (mod 26), D = H^-1.
Encryption here: x = P + se*E ; y_block = H.x_block (blocks from offset o) ; L = y - sf*F.  Letters outside full blocks unchanged.
Frames: ix=0: C[S[i]] = L[i] (crib at plaintext index); ix=1: stream out[S[p]] = P[p], C = L.  Seed 15800.
Error controls: one corrupted carved letter inside a crib block (ctl7), one wrong crib letter (ctl8): strict must FAIL, DROP=1 recover.
Nulls: K4 shuffled (seeds 15801, 15802) and two cycle-157 profile-matched nulls (mnull01, mnull02).
Output lines: name n f sf e se src perm dir ix nu o carved_err wrong_crib text"""
import random, sys, numpy as np
sys.path.insert(0,"/tmp/kcf/tools/cycle127")
from plant import plain, K4
NUMS=["ABCDEFGHIJKLMNOPQRSTUVWXYZ","KRYPTOSABCDEFGHIJLMNQUVWXZ"]
R=random.Random(15800)
def inv26(M):
    n=len(M); A=[list(r)+[int(i==j) for j in range(n)] for i,r in enumerate(M)]
    for c in range(n):
        s=next((i for i in range(c,n) if A[i][c]%2 and A[i][c]%13),None)
        if s is None: return None
        A[c],A[s]=A[s],A[c]; iv=pow(A[c][c],-1,26); A[c]=[x*iv%26 for x in A[c]]
        for i in range(n):
            if i!=c and A[i][c]: f=A[i][c]; A[i]=[(x-f*y)%26 for x,y in zip(A[i],A[c])]
    return [r[n:] for r in A]
def rmat(n):
    while True:
        H=[[R.randrange(26) for _ in range(n)] for _ in range(n)]
        if inv26(H): return H
def enc(text,n,F,sf,E,se,o,N):
    H=rmat(n); t=list(text); fv=[N.index(c) for c in F]; ev=[N.index(c) for c in E]
    for b in range(o,97-n+1,n):
        x=[(N.index(text[b+j])+se*ev[(b+j)%len(ev)])%26 for j in range(n)]
        for r in range(n): t[b+r]=N[(sum(H[r][j]*x[j] for j in range(n))-sf*fv[(b+r)%len(fv)])%26]
    return "".join(t),H
if __name__=="__main__":
    P0=plain(); assert P0[21:34]=="EASTNORTHEAST" and P0[63:74]=="BERLINCLOCK"
    B=np.fromfile("/home/box/kryptos_support_backup/perms97.bin",dtype=np.int16).reshape(-1,97)
    W=open("/workspace/k4c158/all.txt").read().split()
    specs=[("ctl1",2,"PALIMPSEST",1,"KRYPTOS",1,"-",0,0,0,0,0,None,None),
           ("ctl2",2,"ABSCISSA",-1,"SHADOWFORCES",-1,"-",0,0,0,1,1,None,None),
           ("ctl3",3,"EASTNORTHEAST",1,"LAYERTWO",-1,"-",0,0,0,0,2,None,None),
           ("ctl4",4,"BERLINCLOCK",-1,"KRYPTOS",1,"-",0,0,0,0,1,None,None),
           ("ctl5",2,"KRYPTOS",1,"PALIMPSEST",-1,"P",4242,0,0,1,1,None,None),
           ("ctl6",3,"IQLUSION",-1,"UNDERGROUND",1,"P",120000,1,1,0,0,None,None),
           ("ctl7",2,"PALIMPSEST",1,"ABSCISSA",1,"-",0,0,0,0,0,26,None),
           ("ctl8",3,"SANBORN",-1,"WEBSTER",-1,"-",0,0,0,1,1,None,66),
           ("ctl9",2,W[5000],1,W[8000],-1,"-",0,0,0,1,0,None,None),
           ("ctl10",3,"SHADOW",1,"CLOCK",1,"P",99999,1,0,0,2,None,None)]
    for (nm,n,F,sf,E,se,src,perm,d,ix,nu,o,cerr,werr) in specs:
        N=NUMS[nu]; P=list(P0)
        if werr is not None: P[werr]=R.choice([x for x in N if x!=P[werr]])
        P="".join(P)
        S=list(range(97)) if src=="-" else [int(x) for x in B[perm]]
        if d: T=[0]*97; [T.__setitem__(S[i],i) for i in range(97)]; S=T
        if ix==0:
            L,H=enc(P,n,F,sf,E,se,o,N); C=[None]*97
            for i in range(97): C[S[i]]=L[i]
        else:
            out=[None]*97
            for p in range(97): out[S[p]]=P[p]
            L,H=enc("".join(out),n,F,sf,E,se,o,N); C=list(L)
        ce=-1
        if cerr is not None: ce=cerr; C[ce]=R.choice([x for x in N if x!=C[ce]])
        print(nm,n,F,sf,E,se,src,perm,d,ix,nu,o,ce,-1 if werr is None else werr,"".join(C))
        print("#",nm,"H=",H)
    for i,sd in enumerate((15801,15802)):
        r=random.Random(sd); x=list(K4); r.shuffle(x); print("null%d"%(i+1),0,"-",0,"-",0,"-",0,0,0,0,0,-1,-1,"".join(x))
    for l in open("/workspace/k4c158/repo/data/cycle157/nulls.txt"):
        a=l.split()
        if a[0] in("mnull01","mnull02"): print(a[0],0,"-",0,"-",0,"-",0,0,0,0,0,-1,-1,a[1])
