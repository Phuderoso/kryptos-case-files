# Cycle 50 controls: planted Nihilist-transposition ciphers (same geometry as nihilist.c) + shuffled-K4 nulls.
import random
KA="KRYPTOSABCDEFGHIJLMNQUVWXZ"
PT="WEWALKEDTOWARDTHEHILL"+"EASTNORTHEAST"+"ANDSAWTHEOLDTOWERWITHTHEGREAT"+"BERLINCLOCK"+"ABOVEUSALLINTHECOLDAIRX"
assert len(PT)==97 and PT[21:34]=="EASTNORTHEAST" and PT[63:74]=="BERLINCLOCK"
def perm(sg,lay,rd):
    pos=[0]*10
    for j in range(10): pos[sg[j]]=j
    occ=[(c<97) if lay==0 else (c>=3) for c in range(100)]
    newocc=[0]*100
    for c in range(100):
        if occ[c]: newocc[pos[c//10]*10+pos[c%10]]=1
    rank={};cnt=0
    for t in range(100):
        cell=t if rd==0 else (t%10)*10+t//10
        if newocc[cell]: rank[cell]=cnt; cnt+=1
    return [rank[pos[(i if lay==0 else i+3)//10]*10+pos[(i if lay==0 else i+3)%10]] for i in range(97)]
def enc(p,key,ka,beau):
    a=KA if ka else "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; x=a.index(p)
    return a[(key-x)%26] if beau else a[(x+key)%26]
def make(sg,lay,rd,inv,model,kw,s,ka,beau):
    P=perm(sg,lay,rd)
    if inv: Q=[0]*97; [Q.__setitem__(P[i],i) for i in range(97)]; P=Q
    a=KA if ka else "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; k=[a.index(c) for c in kw]; L=len(k)
    key=lambda i:(k[i%L]+s*(i//L))%26
    ct=[None]*97
    for i in range(97):
        if model=='A': ct[P[i]]=enc(PT[i],key(i),ka,beau)
        else: ct[i]=enc(PT[P[i]],key(i),ka,beau)
    return "".join(ct)
print("CTL1",make([0,1,2,3,4,5,9,8,7,6],0,1,0,'A',"CLOCK",0,False,False))
print("CTL2",make([0,1,2,3,4,6,5,7,8,9],1,0,0,'B',"SHADOW",3,True,True))
print("CTL3",make([0,1,2,3,5,4,6,7,9,8],0,0,1,'A',"PALIMPSEST",0,True,False))
K4="OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR"
for n in range(3):
    r=random.Random(5000+n); l=list(K4); r.shuffle(l); print("NULL%d"%n,"".join(l))
