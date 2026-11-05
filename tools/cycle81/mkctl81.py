import random, json, numpy as np
from kryptos_text import K4, KA
AZ="ABCDEFGHIJKLMNOPQRSTUVWXYZ"; rng=random.Random(8101)
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
specs=[("L4_fib4_KA_Vig",KA,0,[1,1,1,1],0,[KA.index(x) for x in "KRYP"]),
       ("L4_AZ_Beau_affine",AZ,1,[2,9,1,17],11,[rng.randrange(26) for _ in range(4)]),
       ("L4_KA_Beau",KA,1,[7,0,3,5],0,[rng.randrange(26) for _ in range(4)]),
       ("L5_direct_AZ_Vig",AZ,0,[4,6,1,22,9],3,[rng.randrange(26) for _ in range(5)])]
out=[]
for n,(name,T,mode,c,d,seed) in enumerate(specs):
    pi=rng.randrange(1,NP) if len(c)==4 else 0
    out.append(dict(ctl=n,name=name,ct=make(T,mode,c,d,seed,pi),perm=pi,tab="KA" if T==KA else "AZ",mode="Beau" if mode else "Vig",c=c,d=d,L=len(c)))
json.dump(out,open("controls81.json","w"),indent=1)
