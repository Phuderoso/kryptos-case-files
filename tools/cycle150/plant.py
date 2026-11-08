"""Cycle 150 controls: zig-zag autokey (form cycles through Vigenere/Beaufort/variant every letter), planted on the
cycle 137 English control text (via cycle 141's plant.py). Seed 15000; nulls: K4 shuffled with seeds 15001-15002.
Output: label src perm text   (src '-' direct, 'P' bank entry, 'I' inverse of bank entry)"""
import importlib.util, random, os
import numpy as np
here=os.path.dirname(os.path.abspath(__file__))
for cand in (os.path.join(here,"../cycle141/plant.py"),"/workspace/k141/plant.py"):
    if os.path.exists(cand): break
spec=importlib.util.spec_from_file_location("p141",cand); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
R=random.Random(15000); NUMS=["ABCDEFGHIJKLMNOPQRSTUVWXYZ","KRYPTOSABCDEFGHIJLMNQUVWXZ"]; A=[1,-1,1]; B=[1,1,-1]
def enc(text,pat,L,feed,N):
    s=R.randrange(26); pr=[R.randrange(26) for _ in range(L)]; p=[N.index(x) for x in text]; c=[]
    for j in range(len(p)):
        F=pat[j%len(pat)]; f=pr[j] if j<L else (c[j-L] if feed=="CT" else p[j-L])
        c.append((s+A[F]*p[j]+B[F]*f)%26)
    return "".join(N[v] for v in c)
def ctl(Pl,pat,L,feed,nu,ix,S):
    N=NUMS[nu]
    if ix==0:
        Lt=enc(Pl,pat,L,feed,N); C=[None]*97
        for i in range(97): C[S[i]]=Lt[i]
        return "".join(C)
    out=[None]*97
    for p in range(97): out[S[p]]=Pl[p]
    return enc("".join(out),pat,L,feed,N)
if __name__=="__main__":
    Pl=m.m.plain(); Bk=np.fromfile("/home/box/kryptos_support_backup/perms97.bin",dtype=np.int16).reshape(-1,97); I=list(range(97))
    print("ctl1 - 0", ctl(Pl,[0,1],1,"CT",0,0,I))
    print("ctl2 - 0", ctl(Pl,[1,0,2],5,"CT",1,0,I))
    print("ctl3 P 4242", ctl(Pl,[0,1],7,"CT",0,0,list(Bk[4242])))
    print("ctl4 P 120000", ctl(Pl,[2,0,0],3,"CT",1,1,list(Bk[120000])))
    print("ctl5 I 99999", ctl(Pl,[1,2],11,"CT",0,1,list(np.argsort(Bk[99999]))))
    print("ctl6 - 0", ctl(Pl,[0,1],40,"PT",0,0,I))
    for z in (1,2):
        l=list(m.K4); random.Random(15000+z).shuffle(l); print(f"null{z} - 0","".join(l))
