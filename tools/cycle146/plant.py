"""Cycle 146 controls: mixed-direction periodic key (per phase Vigenere or Beaufort), planted on cycle 137's English
control text (via cycle 141's plant.py). Seed 14600; nulls: K4 shuffled with seeds 14601-14602.
Output: label P src perm text   (src '-' direct, 'P' bank entry, 'I' inverse of bank entry)"""
import importlib.util, random, os
import numpy as np
here=os.path.dirname(os.path.abspath(__file__))
for cand in (os.path.join(here,"../cycle141/plant.py"),"/workspace/k141/plant.py"):
    if os.path.exists(cand): break
spec=importlib.util.spec_from_file_location("p141",cand); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
R=random.Random(14600); NUMS=["ABCDEFGHIJKLMNOPQRSTUVWXYZ","KRYPTOSABCDEFGHIJLMNQUVWXZ"]
def enc(text,P,N):
    k=[R.randrange(26) for _ in range(P)]; f=[R.randrange(2) for _ in range(P)]
    if len(set(f))==1: f[0]^=1   # force a genuinely mixed key
    return "".join(N[(N.index(c)+k[i%P])%26] if f[i%P]==0 else N[(k[i%P]-N.index(c))%26] for i,c in enumerate(text))
def ctl(Pl,P,nu,ix,S):
    N=NUMS[nu]
    if ix==0:
        L=enc(Pl,P,N); C=[None]*97
        for i in range(97): C[S[i]]=L[i]
        return "".join(C)
    out=[None]*97
    for p in range(97): out[S[p]]=Pl[p]
    return enc("".join(out),P,N)
if __name__=="__main__":
    Pl=m.m.plain(); B=np.fromfile("/home/box/kryptos_support_backup/perms97.bin",dtype=np.int16).reshape(-1,97); I=list(range(97))
    print("ctl1 7 - 0", ctl(Pl,7,0,0,I))
    print("ctl2 11 - 0", ctl(Pl,11,1,0,I))
    print("ctl3 5 P 4242", ctl(Pl,5,0,0,list(B[4242])))
    print("ctl4 9 P 120000", ctl(Pl,9,1,1,list(B[120000])))
    print("ctl5 13 I 99999", ctl(Pl,13,0,1,list(np.argsort(B[99999]))))
    print("ctl6 19 - 0", ctl(Pl,19,0,0,I))
    for z in (1,2):
        l=list(m.K4); random.Random(14600+z).shuffle(l); print(f"null{z} 0 - 0","".join(l))
