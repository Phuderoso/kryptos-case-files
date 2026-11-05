"""Cycle 74 audit: Sanborn-convention RUNNING-KEY controls. Encipherment = exact inverse of the verified K1/K2
decryptor (KA tableau, key letter added in KA numbering, key advances one letter per plaintext letter).
Key = a running text at a random offset. Model A: substitute in plaintext order then transpose
(carved[P[i]] = E(pt)[i], key index = plaintext position). Model B: transpose then substitute in carved order."""
import random, re, json, numpy as np
from kryptos_text import K1, K2, K3, KA
from solve_k1_k2_k3 import vig_dec
from sanborn_controls import plain
assert vig_dec(K1,"PALIMPSEST").startswith("BETWEENSUBTLESHADING")
def E(p,k): return KA[(KA.index(p)+KA.index(k))%26]
carter=re.sub("[^A-Z]","",open("../k4c35/carter1.txt").read().upper())
k1p=vig_dec(K1,"PALIMPSEST"); k2p=vig_dec(K2.replace("?",""),"ABSCISSA")
texts={"carter1":carter,"carter1_rev":carter[::-1],"k2pt":k2p,"k1pt":k1p}
with open("texts_long.txt","w") as f:
    for n in ("carter1","carter1_rev","k2pt"): f.write(f"{n} {texts[n]}\n")
with open("texts_all.txt","w") as f:
    for n,t in texts.items(): f.write(f"{n} {t}\n")
perms=np.fromfile("p3k.bin",dtype=np.int16).reshape(-1,97)
PLANS=[("carter1","A",None),("carter1","B",None),("carter1_rev","A",None),("k2pt","B",0),("carter1","A","end"),("k1pt","B","wrap"),("k1pt","A","wrap")]
meta=[]
for n,(tn,model,how) in enumerate(PLANS):
    r=random.Random(7400+n); T=texts[tn]; pt=plain(7400+n)
    if how=="end": o=len(T)-97
    elif how=="wrap": o=r.randrange(len(T))
    elif how==0: o=r.randrange(len(T)-97)
    else: o=r.randrange(len(T)-97)
    pi=r.randrange(1,len(perms)); P=perms[pi]
    key=lambda i: T[(o+i)%len(T)]
    car=[None]*97
    if model=="A":
        for i in range(97): car[P[i]]=E(pt[i],key(i))
    else:
        for j in range(97): car[j]=E(pt[P[j]],key(j))
    open(f"ctl_{n}.txt","w").write("".join(car))
    meta.append(dict(ctl=n,text=tn,model=model,perm=int(pi),offset=o,len=len(T),pt=pt))
json.dump(meta,open("controls74.json","w"),indent=1)
for m in meta: print(m["ctl"],m["text"],m["model"],m["perm"],m["offset"],m["len"])
