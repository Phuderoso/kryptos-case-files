"""Planted M-94 controls (random disk order, random offset per 25-letter line, English-like filler from K3 plaintext) and shuffled-K4 nulls."""
import random, numpy as np
from kryptos_text import K4
from m94_alphabets import M94
K3PT=("SLOWLYDESPARATLYSLOWLYTHEREMAINSOFPASSAGEDEBRISTHATENCUMBEREDTHELOWERPARTOFTHEDOORWAYWASREMOVEDWITHTREMBLINGHANDSIMADEATINYBREACHINTHEUPPERLEFTHANDCORNER")
N=97; perms=np.fromfile('../k4c27/perms97.bin',dtype=np.int16).reshape(-1,N)
def plant(seed, use_perm):
    r=random.Random(seed); s=r.randrange(0,len(K3PT)-N); pt=list(K3PT[s:s+N])
    for k,(w,o) in enumerate([("EASTNORTHEAST",21),("BERLINCLOCK",63)]): pt[o:o+len(w)]=list(w)
    order=list(range(25)); r.shuffle(order); g=[r.randrange(1,26) for _ in range(4)]
    y=[]
    for i,p in enumerate(pt):
        a=M94[order[i%25]]; y.append(a[(a.index(p)+g[i//25])%26])
    if use_perm:
        pi=r.randrange(len(perms)); X=['?']*N
        for i in range(N): X[perms[pi][i]]=y[i]
        return ''.join(X), dict(order=[o+1 for o in order],g=g,perm=pi)
    return ''.join(y), dict(order=[o+1 for o in order],g=g)
for k in range(3):
    t,info=plant(100+k, k>0); open(f'ctl_{k+1}.txt','w').write(t); print(f'ctl_{k+1}',info)
for k in range(20):
    l=list(K4); random.Random(k).shuffle(l); open(f'null_{k+1}.txt','w').write(''.join(l))

# order-2 controls: transpose plaintext first (T(P)[j]=P[p[j]]), then M-94
def plant2(seed):
    r=random.Random(seed); s=r.randrange(0,len(K3PT)-N); pt=list(K3PT[s:s+N])
    for w,o in [("EASTNORTHEAST",21),("BERLINCLOCK",63)]: pt[o:o+len(w)]=list(w)
    pi=r.randrange(len(perms)); tp=[pt[perms[pi][j]] for j in range(N)]
    order=list(range(25)); r.shuffle(order); g=[r.randrange(1,26) for _ in range(4)]
    out=''.join(M94[order[i%25]][(M94[order[i%25]].index(p)+g[i//25])%26] for i,p in enumerate(tp))
    return out, dict(order=[o+1 for o in order], g=g, perm=pi)
for k in range(2):
    t,info=plant2(200+k); open(f'ctl2_{k+1}.txt','w').write(t); print(f'ctl2_{k+1}',info)
