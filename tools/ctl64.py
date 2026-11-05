# Cycle 64 controls: one word sets the columnar order and the mixed tableau; a free periodic key; same geometry as c64.c.
import random
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
def make(w,inv,model,kw,beau,tab=None):
    a=tab or "".join(dict.fromkeys(w+"ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
    P=col(w) if w else list(range(N))
    if inv: Q=[0]*N; [Q.__setitem__(P[i],i) for i in range(N)]; P=Q
    k=[a.index(c) for c in kw]; L=len(k); ct=[None]*N
    enc=lambda p,key: a[(key-a.index(p))%26] if beau else a[(a.index(p)+key)%26]
    for i in range(N):
        if model=='A': ct[P[i]]=enc(PT[i],k[i%L])
        else: ct[i]=enc(PT[P[i]],k[i%L])
    return "".join(ct)
print("CTL1",make("LANTERN",0,'A',"GLOW",False))
print("CTL2",make("UNDERGROUND",1,'B',"SHADOWS",True))
print("CTL3",make("PERIMETER",0,'B',"EGYPTIAN",False))
print("CTL4",make("LUMINOUS",1,'A',"KRYPTOS",False,"KRYPTOSABCDEFGHIJLMNQUVWXZ"))
K4=open('k4.txt').read().strip()
for n in range(2):
    r=random.Random(6400+n); l=list(K4); r.shuffle(l); print("NULL%d"%n,"".join(l))
