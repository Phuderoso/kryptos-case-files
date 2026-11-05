import random, json, numpy as np
from kryptos_text import K4, KA
AZ="ABCDEFGHIJKLMNOPQRSTUVWXYZ"; rng=random.Random(7801)
perms=np.fromfile("../k4c77/perms97.bin",dtype=np.int16).reshape(-1,97); NP=len(perms)
cpos=list(range(21,34))+list(range(63,74)); crib="EASTNORTHEASTBERLINCLOCK"; src=open("eng.txt").read()
out=[]
for n in range(6):
    T=rng.choice([KA,AZ]); mode=rng.randrange(3); model=rng.randrange(2); start=rng.choice([26,27]); p=rng.choice([5,7,8,10,11,13]); pi=rng.randrange(NP)
    o=rng.randrange(len(src)-100); pt=list(src[o:o+97])
    for i,c in zip(cpos,crib): pt[i]=c
    A=[rng.randrange(26) for _ in range(p)]; B=[rng.randrange(26) for _ in range(5)]; P=[int(x) for x in perms[pi]]
    ct=[None]*97
    for i in range(97):
        j=P[i]; g=j+start; col,row=g%31,g//31; a=col%p if model==0 else j%p; k=(A[a]+B[row])%26; q=T.index(pt[i])
        c=(q+k) if mode==0 else (k-q) if mode==1 else (q-k); ct[j]=T[c%26]
    out.append(dict(ctl=n,ct="".join(ct),perm=pi,tab="KA" if T==KA else "AZ",mode=mode,model="RC"[model],start=start,p=p))
json.dump(out,open("controls78.json","w"),indent=1)
rng2=random.Random(7802)
for n in range(12):
    l=list(K4); rng2.shuffle(l); open(f"null_{n}.txt","w").write("".join(l))
