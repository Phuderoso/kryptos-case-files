"""Cycle 31 planted controls (random disk subset/order, phase s, offset per line; K3 plaintext filler + cribs) and shuffled-K4 nulls."""
import random
from kryptos_text import K4
from cylinder_disks import themed, m94
K3PT=("SLOWLYDESPARATLYSLOWLYTHEREMAINSOFPASSAGEDEBRISTHATENCUMBEREDTHELOWERPARTOFTHEDOORWAYWASREMOVEDWITHTREMBLINGHANDSIMADEATINYBREACHINTHEUPPERLEFTHANDCORNER")
N=97
def plant(seed,disks,n):
    r=random.Random(seed); st=r.randrange(0,len(K3PT)-N); pt=list(K3PT[st:st+N])
    for w,o in [("EASTNORTHEAST",21),("BERLINCLOCK",63)]: pt[o:o+len(w)]=list(w)
    order=r.sample(range(len(disks)),n); s=r.randrange(n); g=[r.randrange(1,26) for _ in range(30)]
    y=''.join(disks[order[(i+s)%n]][(disks[order[(i+s)%n]].index(p)+g[(i+s)//n])%26] for i,p in enumerate(pt))
    return y,dict(n=n,s=s)
log=[]
for name,ds in [("themed",themed()),("m94",m94())]:
    for k,n in enumerate([7,13,22]):
        y,info=plant(300+k,ds,n); fn=f"ctl_{name}_{k+1}.txt"; open(fn,"w").write(y); log.append(f"{fn} {info}")
for k in range(20):
    l=list(K4); random.Random(1000+k).shuffle(l); open(f"null_{k+1}.txt","w").write("".join(l))
open("controls_planted.txt","w").write("\n".join(log)+"\n"); print("\n".join(log))

# transposition controls: K4 = T(cyl(P)), X[perm[i]] = y[i]
import numpy as np
perms=np.fromfile('../k4c27/perms97.bin',dtype=np.int16).reshape(-1,N)
log2=[]
for name,ds in [("themed",themed()),("m94",m94())]:
    for k,n in enumerate([9,17]):
        y,info=plant(400+k,ds,n); r=random.Random(500+k); pi=r.randrange(len(perms)); X=['?']*N
        for i in range(N): X[perms[pi][i]]=y[i]
        fn=f"tctl_{name}_{k+1}.txt"; open(fn,"w").write(''.join(X)); info['perm']=pi; log2.append(f"{fn} {info}")
open("controls_planted.txt","a").write("\n".join(log2)+"\n"); print("\n".join(log2))
