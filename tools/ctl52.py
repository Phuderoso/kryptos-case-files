# Cycle 52 controls: planted double keyed columnar + periodic/progressive key (same geometry as dcol.c) + shuffled-K4 nulls.
import random
KA="KRYPTOSABCDEFGHIJLMNQUVWXZ"
PT="WEWALKEDTOWARDTHEHILL"+"EASTNORTHEAST"+"ANDSAWTHEOLDTOWERWITHTHEGREAT"+"BERLINCLOCK"+"ABOVEUSALLINTHECOLDAIRX"
assert len(PT)==97 and PT[21:34]=="EASTNORTHEAST" and PT[63:74]=="BERLINCLOCK"
N=97
def col(w):
    o=sorted(range(len(w)),key=lambda i:(w[i],i)); P=[0]*N; k=0; rows=(N+len(w)-1)//len(w)
    for c in o:
        for r in range(rows):
            i=r*len(w)+c
            if i<N: P[i]=k; k+=1
    return P
def enc(p,key,ka,beau):
    a=KA if ka else "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; x=a.index(p)
    return a[(key-x)%26] if beau else a[(x+key)%26]
def make(w1,w2,inv,model,kw,s,ka,beau):
    P1=col(w1); P2=col(w2) if w2 else list(range(N)); P=[P2[P1[i]] for i in range(N)]
    if inv: Q=[0]*N; [Q.__setitem__(P[i],i) for i in range(N)]; P=Q
    a=KA if ka else "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; k=[a.index(c) for c in kw]; L=len(k)
    key=lambda i:(k[i%L]+s*(i//L))%26
    ct=[None]*N
    for i in range(N):
        if model=='A': ct[P[i]]=enc(PT[i],key(i),ka,beau)
        else: ct[i]=enc(PT[P[i]],key(i),ka,beau)
    return "".join(ct)
print("CTL1",make("KRYPTOS","PALIMPSEST",0,'A',"LAYER",0,False,False))
print("CTL2",make("SHADOW","BERLIN",1,'B',"ABSCISSA",2,True,True))
print("CTL3",make("THOUGHT","PALIMPSEST",0,'B',"CLOCK",0,True,False))
K4="OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR"
for n in range(2):
    r=random.Random(5200+n); l=list(K4); r.shuffle(l); print("NULL%d"%n,"".join(l))
