import numpy as np, sys
from k4_autokey_trans import family
for n in (96,97,98):
    fam=[(np.arange(n,dtype=np.int16),"identity")]+family(n)
    seen=set(); out=[]; tags=[]
    for p,t in fam:
        k=p.tobytes()
        if k in seen: continue
        seen.add(k); out.append(p); tags.append(t)
    np.stack(out).astype(np.int16).tofile(f"perms{n}.bin")
    open(f"perms{n}_tags.txt","w").write("\n".join(tags)); print(n,len(out))
