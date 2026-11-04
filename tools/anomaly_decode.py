import sys, json, math, numpy as np
from kryptos_text import K4, KA
AZ="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
qg=json.load(open(__import__("os").path.join(__import__("os").path.dirname(__file__), "..", "data", "quadgrams.json")))
floor=qg["floor"]; L=qg["q"]
def score(s):
    s=[c for c in s]; tot=0;n=0
    for i in range(len(s)-3):
        w="".join(s[i:i+4])
        if "?" in w: continue
        tot+=L.get(w,floor); n+=1
    return tot/max(n,1), n
def decode(line, n=98, model="del"):
    f=dict(x.split("=",1) for x in line.split()[1:])
    t=int(f["t"]); d=int(f["d"]); P=np.fromfile(f"perms{n}.bin",dtype=np.int16).reshape(-1,n)[t]
    PA=KA if f["PA"]=="KA" else AZ; CA=KA if f["CA"]=="KA" else AZ; key=f["key"]; p=int(f["p"])
    out=[]
    for j in range(n):
        u=int(P[j]); 
        if model=="del":
            if u==d: out.append("?"); continue
            c=K4[u if u<d else u-1]
        elif model=="ins": c=K4[u if u<d else u+1]
        else: c=K4[u]
        r=(u if f["idx"]=="ct" else j)%p
        if key[r]=="?": out.append("?"); continue
        k=AZ.index(key[r]); cv=CA.index(c)
        pv=(k-cv)%26 if f["mode"]=="beau" else (cv-k)%26
        out.append(PA[pv])
    return "".join(out)
for line in open(sys.argv[1]):
    if not line.startswith("HIT"): continue
    s=decode(line.strip(), int(sys.argv[2]), sys.argv[3]); print(s, "%.2f n=%d"%score(s))
