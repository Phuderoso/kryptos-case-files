"""Cycle 148 controls: constant-digit running keys planted on cycle 137's English control text (via cycle 141's plant.py).
Seed 14800; nulls: K4 shuffled with seeds 14801-14802.  Output: label src perm text"""
import importlib.util, random, os
import numpy as np
here=os.path.dirname(os.path.abspath(__file__))
for cand in (os.path.join(here,"../cycle141/plant.py"),"/workspace/k141/plant.py"):
    if os.path.exists(cand): break
spec=importlib.util.spec_from_file_location("p141",cand); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
NUMS=["ABCDEFGHIJKLMNOPQRSTUVWXYZ","KRYPTOSABCDEFGHIJLMNQUVWXZ"]
ST={l.split()[0]:list(map(int,l.split()[2:])) for l in open("/workspace/k148/streams.txt")}
def enc(text,name,o,c,form,N):
    out=[]
    for i,ch in enumerate(text):
        k=(ST[name][o+i]+c)%26; p=N.index(ch)
        out.append(N[(p+k)%26] if form==0 else N[(k-p)%26] if form==1 else N[(p-k)%26])
    return "".join(out)
def ctl(Pl,name,o,c,form,nu,ix,S):
    N=NUMS[nu]
    if ix==0:
        L=enc(Pl,name,o,c,form,N); C=[None]*97
        for i in range(97): C[S[i]]=L[i]
        return "".join(C)
    t=[None]*97
    for p in range(97): t[S[p]]=Pl[p]
    return enc("".join(t),name,o,c,form,N)
if __name__=="__main__":
    Pl=m.m.plain(); B=np.fromfile("/home/box/kryptos_support_backup/perms97.bin",dtype=np.int16).reshape(-1,97); I=list(range(97))
    print("ctl1 - 0", ctl(Pl,"pi_D1",1234,0,0,0,0,I))
    print("ctl2 - 0", ctl(Pl,"e_P1",777,5,1,1,0,I))
    print("ctl3 P 4242", ctl(Pl,"phi_Q0",300,1,2,0,0,list(B[4242])))
    print("ctl4 P 120000", ctl(Pl,"sqrt2_D1",9001,0,0,1,1,list(B[120000])))
    print("ctl5 I 99999", ctl(Pl,"gamma_P0",4321,13,1,0,1,list(np.argsort(B[99999]))))
    for z in (1,2):
        l=list(m.K4); random.Random(14800+z).shuffle(l); print(f"null{z} - 0","".join(l))
