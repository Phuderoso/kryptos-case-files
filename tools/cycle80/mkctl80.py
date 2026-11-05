import random, json, numpy as np
from kryptos_text import K4, KA
AZ="ABCDEFGHIJKLMNOPQRSTUVWXYZ"; rng=random.Random(8001)
perms=np.fromfile("perms97.bin",dtype=np.int16).reshape(-1,97); NP=len(perms)
cpos=list(range(21,34))+list(range(63,74)); crib="EASTNORTHEASTBERLINCLOCK"; src=open("eng.txt").read()
def make(T,mode,c,d,seed,pi):
    L=len(c); k=list(seed)
    while len(k)<97: k.append((sum(c[j]*k[-1-j] for j in range(L))+d)%26)
    o=rng.randrange(len(src)-100); pt=list(src[o:o+97])
    for i,ch in zip(cpos,crib): pt[i]=ch
    P=[int(x) for x in perms[pi]]; ct=[None]*97
    for i in range(97):
        q=T.index(pt[i]); x=(q+k[i]) if mode==0 else (k[i]-q)  # Vig: c=p+k ; Beau: c=k-p
        ct[P[i]]=T[x%26]
    return "".join(ct)
specs=[("fib_KR_KA_Vig",KA,0,[1,1],0,[KA.index('K'),KA.index('R')]),
       ("L3_AZ_Beau",AZ,1,[3,7,11],5,[rng.randrange(26) for _ in range(3)]),
       ("prog_KA_Beau",KA,1,[1],5,[KA.index('S')]),
       ("L2_AZ_Vig_affine",AZ,0,[5,2],9,[rng.randrange(26) for _ in range(2)])]
out=[]
for n,(name,T,mode,c,d,seed) in enumerate(specs):
    pi=rng.randrange(1,NP); out.append(dict(ctl=n,name=name,ct=make(T,mode,c,d,seed,pi),perm=pi,tab="KA" if T==KA else "AZ",mode="Beau" if mode else "Vig",c=c,d=d,L=len(c)))
c6=[rng.randrange(26) for _ in range(6)]
out.append(dict(ctl=4,name="direct_L6_KA_Vig",ct=make(KA,0,c6,4,[rng.randrange(26) for _ in range(6)],0),perm=0,tab="KA",mode="Vig",c=c6,d=4,L=6))
json.dump(out,open("controls80.json","w"),indent=1)
r2=random.Random(8002)
for n in range(5):
    l=list(K4); r2.shuffle(l); open(f"null_{n}.txt","w").write("".join(l))
