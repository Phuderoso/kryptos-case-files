# Cycle 53 controls: planted disrupted columnar (+ optional keyword columnar) + periodic/progressive key, same
# geometry as disr_gen.py / disr.c, and shuffled-K4 nulls.
import random
from disr_gen import perm
KA="KRYPTOSABCDEFGHIJLMNQUVWXZ"; AZ="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
PT="WEWALKEDTOWARDTHEHILL"+"EASTNORTHEAST"+"ANDSAWTHEOLDTOWERWITHTHEGREAT"+"BERLINCLOCK"+"ABOVEUSALLINTHECOLDAIRX"
N=97
def order(w): return tuple(sorted(range(len(w)),key=lambda i:(w[i],i)))
def col(w):
    o=order(w); P=[0]*N; k=0; rows=(N+len(w)-1)//len(w)
    for c in o:
        for r in range(rows):
            i=r*len(w)+c
            if i<N: P[i]=k; k+=1
    return P
def make(D,C,dfirst,inv,model,kw,s,ka,beau):
    if C is None: P=D
    elif dfirst: P=[C[D[i]] for i in range(N)]
    else: P=[D[C[i]] for i in range(N)]
    if inv: Q=[0]*N; [Q.__setitem__(P[i],i) for i in range(N)]; P=Q
    a=KA if ka else AZ; k=[a.index(c) for c in kw]; L=len(k)
    key=lambda i:(k[i%L]+s*(i//L))%26
    enc=lambda p,kk: a[(kk-a.index(p))%26] if beau else a[(a.index(p)+kk)%26]
    ct=[None]*N
    for i in range(N):
        if model=='A': ct[P[i]]=enc(PT[i],key(i))
        else: ct[i]=enc(PT[P[i]],key(i))
    return "".join(ct)
print("CTL1",make(perm(7,order("KRYPTOS"),1),None,1,0,'A',"LAYER",0,False,False))
print("CTL2",make(perm(6,(4,1,5,0,3,2),2),None,1,1,'B',"ABSCISSA",2,True,True))
print("CTL3",make(perm(10,order("PALIMPSEST"),1),col("BERLIN"),1,0,'B',"CLOCK",0,True,False))
print("CTL4",make(perm(6,order("SHADOW"),2),col("THOUGHT"),0,0,'A',"EGYPT",0,False,True))
K4=open('k4.txt').read().strip()
for n in range(2):
    r=random.Random(5300+n); l=list(K4); r.shuffle(l); print("NULL%d"%n,"".join(l))
