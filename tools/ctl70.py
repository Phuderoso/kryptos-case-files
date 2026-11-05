"""Cycle 70 controls (X-stripped key texts): planted K4-like texts (English + cribs at official positions) encrypted with a tableau-walk
running key (texts70.txt) behind a transposition from perms97.bin, both models, several substitution modes;
plus 6 shuffled-K4 nulls. Same conventions as carved_rk.c (cycle 34)."""
import random, re, numpy as np
random.seed(70)
N=97; KA="KRYPTOSABCDEFGHIJLMNQUVWXZ"
K4=open("/workspace/kcl/data/k4.txt").read().strip()
perms=np.fromfile("perms97.bin",dtype=np.int16).reshape(-1,N)
texts=dict(l.split() for l in open("texts70.txt"))
ita2=[0x03,0x19,0x0E,0x09,0x01,0x0D,0x1A,0x14,0x06,0x0B,0x0F,0x12,0x1C,0x0C,0x18,0x16,0x17,0x0A,0x05,0x10,0x07,0x1E,0x13,0x1D,0x15,0x11]
def codes(e): return [ita2[l] if e==0 else l if e==1 else l+1 if e==2 else KA.index(chr(65+l))+(e==4) for l in range(26)]
def enc(p,k,md):
    if md<6:
        A=KA if md//3 else "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; ty=md%3; pi,ki=A.index(p),A.index(k)
        return A[(pi+ki)%26 if ty==0 else (ki-pi)%26 if ty==1 else (pi-ki)%26]
    c=codes(md-6); v=c[ord(p)-65]^c[ord(k)-65]
    return chr(65+c.index(v)) if v in c else None
book=re.sub("[^A-Z]","",open("/workspace/kcl/data/g84.txt").read().upper())
plans=[("K2pt_fixed_noX",0,"A",None),("K123pt_noX",4,"B",None),("full_cols_noX",3,"A",None),("K3pt_noX",1,"B",None),("KAtableau_rows_noX",2,"A",None),("K123ct_rev_noX",5,"A",None)]
out=open("controls70.txt","w")
for n,(tn,md,model,pfix) in enumerate(plans,1):
    tn=tn if tn in texts else random.choice(list(texts))
    while True:
        s=random.randrange(len(book)-200); pt=list(book[s:s+N])
        pt[21:34]="EASTNORTHEAST"; pt[63:74]="BERLINCLOCK"
        T=texts[tn]; o=random.randrange(len(T)); pi=pfix if pfix is not None else random.randrange(1,20000); P=perms[pi]
        car=[None]*N
        for i in range(N):
            if model=='A': car[P[i]]=enc(pt[i],T[(o+i)%len(T)],md)
            else: car[i]=enc(pt[P[i]],T[(o+i)%len(T)],md)
        if None not in car: break
    c="".join(car); open(f"ctl_{n}.txt","w").write(c)
    out.write(f"ctl_{n}: text={tn} mode={md} model={model} perm={pi} offset={o} pt={''.join(pt)}\n")
