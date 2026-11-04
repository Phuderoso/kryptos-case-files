"""Score every L=21 progressive-key partial fit (K4 and null 3) by English quadgrams, filling key classes the cribs miss greedily."""
import re,glob,numpy as np,sys
from progkw_controls import K4,KA
import random
QG=np.fromfile("qg.bin",dtype=np.float32); perms=np.fromfile("perms_M.bin",dtype=np.int16).reshape(-1,97)
def score(x): return float(np.mean([QG[((x[i]*26+x[i+1])*26+x[i+2])*26+x[i+3]] for i in range(94)]))
cribs=[(21+i,c) for i,c in enumerate("EASTNORTHEAST")]+[(63+i,c) for i,c in enumerate("BERLINCLOCK")]
def run(car,lines):
    out=[]
    for l in lines:
        p,e,m,md,s=re.search(r"perm=(\d+) num=(\w) model=(\w) mode=(\w) s=(\d+)",l).groups(); p=int(p);s=int(s);L=21
        num=(lambda c:ord(c)-65) if e=="A" else (lambda c:KA.index(c)); den=(lambda x:chr(65+x)) if e=="A" else (lambda x:KA[x])
        P=perms[p]; inv=np.argsort(P)
        ct=[num(car[P[k]]) if m=="A" else num(car[k]) for k in range(97)]
        k=[None]*L
        for pos,c in cribs:
            i=pos if m=="A" else inv[pos]; px=num(c); cx=ct[i]
            v=(cx-px)%26 if md=="V" else (cx+px)%26
            k[i%L]=(v-s*(i//L))%26
        miss=[c for c in range(L) if k[c] is None]
        for c in miss: k[c]=0
        def dec():
            pt=[ord(den(((ct[i]-(k[i%L]+s*(i//L)))%26) if md=="V" else ((k[i%L]+s*(i//L)-ct[i])%26)))-65 for i in range(97)]
            return pt if m=="A" else [pt[inv[j]] for j in range(97)]
        for _ in range(2):
            for c in miss:
                best=max(range(26),key=lambda v:(k.__setitem__(c,v),score(dec()))[1]); k[c]=best
        po=dec(); out.append((score(po),len(miss),"".join(chr(65+x) for x in po),l.strip()))
    return sorted(out,reverse=True)
N3=sys.argv[1]
for t,car in [("k4",K4),("n3",N3)]:
    lines=[l for f in sorted(glob.glob(f"l21_{t}_c*.txt")) for l in open(f)]
    r=run(car,lines); print(t,"n=",len(r),"best",round(r[0][0],3),"median",round(r[len(r)//2][0],3))
    for x in r[:3]: print("  %.3f free=%d %s | %s"%x)
