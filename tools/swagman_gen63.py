"""Cycle 63 planted controls for swagman63.c: English PT with both cribs, random 7x7 Latin key square,
themed alphabet, periodic vig/beau/variant before (A) or after (B) the Swagman layer.
Usage: swagman_gen63.py alpha.bin outdir"""
import random, sys
A=open(sys.argv[1],"rb").read(); al=lambda i:[A[26*i+k] for k in range(26)]; out=sys.argv[2]
filler="THEROOMWASDARKANDTHEAIRWASSTILLXINTHECORNERSTOODANOLDDESKXWECOULDSEETHEBRASSPLATEANDTHEMAPWHEREVERYTHINGPOINTEDTO"
pt=filler[:21]+"EASTNORTHEAST"+filler[21:50]+"BERLINCLOCK"+filler[50:73]; assert len(pt)==97
rng=random.Random(63)
def latin():
    rows=list(range(7)); cols=list(range(7)); sym=list(range(7)); rng.shuffle(rows); rng.shuffle(cols); rng.shuffle(sym)
    return [[sym[(rows[r]+cols[k])%7] for k in range(7)] for r in range(7)]  # L[r][k] = tau_k(r)
def sub(seq,key,mode,alpha,slots):
    idx={c:i for i,c in enumerate(alpha)}; o=[]
    for x,s in zip(seq,slots):
        if s is None: o.append(x); continue
        p=idx[x]; k=key[s%len(key)]
        o.append(alpha[(p+k)%26 if mode=="vig" else (k-p)%26 if mode=="beau" else (p-k)%26])
    return o
def swag(P,L,inv,irregular):
    n=len(P); C=[None]*n
    if irregular:
        for q in range(97):
            r,c=divmod(q,14); k=c%7; v=L[r][k]
            if c==13: m=L[6][6]; C[91+v-(m<v)]=P[q]
            else: C[c*7+v]=P[q]
        return C
    for q in range(98):
        if not inv: r,c=divmod(q,14); C[c*7+L[r][c%7]]=P[q]
        else: c,s=divmod(q,7); C[L[s][c%7]*14+c]=P[q]
    return C
def swagpos(q,L,inv):
    if not inv: r,c=divmod(q,14); return c*7+L[r][c%7]
    c,s=divmod(q,7); return L[s][c%7]*14+c
specs=[(0,"start","end",0,"A","vig",7),(1,"end","start",1,"B","beau",5),(2,"end","end",0,"B","var",4),
       (3,None,None,0,"A","beau",6),(4,"start","start",1,"A","var",3)]
for i,(ai,qpos,npos,inv,case,mode,p) in enumerate(specs):
    alpha=al(ai); key=[rng.randrange(26) for _ in range(p)]; L=latin(); P=[alpha.index(ord(ch)-65) for ch in pt]  # work in letter idx 0..25
    P=[ord(ch)-65 for ch in pt]
    if qpos is None:
        X=sub(P,key,mode,alpha,list(range(97))) if case=="A" else P
        C=swag(X,L,0,1); C=sub(C,key,mode,alpha,list(range(97))) if case=="B" else C
    else:
        X=sub(P,key,mode,alpha,list(range(97))) if case=="A" else P
        null=rng.randrange(26); X=([null]+X) if npos=="start" else (X+[null])
        qi=0 if qpos=="start" else 97
        while True:   # redraw the key square if a crib letter would land on the carved '?' (unrecoverable by design)
            C=swag(X,L,inv,0); off=1 if npos=="start" else 0
            if qi not in [swagpos(q+off,L,inv) for q in list(range(21,34))+list(range(63,74))]: break
            L=latin()
        if case=="B":
            slots=[None if j==qi else (j-1 if qpos=="start" else j) for j in range(98)]
            C=sub(C,key,mode,alpha,slots)
        C=C[:qi]+C[qi+1:]
    open(f"{out}/sctl{i}.txt","w").write("".join(chr(65+c) for c in C)+"\n")
    print(f"sctl{i}: alpha {ai} ?{qpos} null {npos} inverse {inv} case {case} {mode} p={p} key {key} L cols {[''.join(str(L[r][k]+1) for r in range(7)) for k in range(7)]}")
