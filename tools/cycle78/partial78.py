import sys, json, re, numpy as np
from kryptos_text import K4, KA
AZ="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
Q=json.load(open("/workspace/k4c25/quadgrams.json")); qf,qq=Q["floor"],Q["q"]
perms=np.fromfile("../k4c77/perms97.bin",dtype=np.int16).reshape(-1,97)
cpos=list(range(21,34))+list(range(63,74)); crib="EASTNORTHEASTBERLINCLOCK"
def partial(ct,pi,T,mode,model,start,p):
    P=[int(x) for x in perms[pi]]; par,val={},{}
    def find(x):
        s=0
        while par.setdefault(x,x)!=x: s+=val[x]; x=par[x]
        return x,s%26
    def nodes(j):
        g=j+start; col,row=g%31,g//31; return ("A",col%p if model=="R" else j%p),("B",row)
    for i,pc in zip(cpos,crib):
        j=P[i]; c,q=T.index(ct[j]),T.index(pc); k=(c-q if mode==0 else c+q if mode==1 else q-c)%26
        (ra,da),(rb,db)=[find(n) for n in nodes(j)]
        if ra==rb: assert (da-db-k)%26==0
        else: par[ra]=rb; val[ra]=(db+k-da)%26
    out=[]
    for i in range(97):
        j=P[i]; (ra,da),(rb,db)=[find(n) for n in nodes(j)]
        if ra!=rb: out.append("."); continue
        k=(da-db)%26; c=T.index(ct[j]); out.append(T[(c-k if mode==0 else k-c if mode==1 else c+k)%26])
    s="".join(out); g=[qq.get(s[i:i+4],qf) for i in range(94) if "." not in s[i:i+4]]
    return s,(sum(g)/len(g) if g else None)
for l in open(sys.argv[1]):
    if not l.startswith("HIT"): continue
    d=dict(x.split("=") for x in l.split()[1:])
    s,sc=partial(K4,int(d["perm"]),KA if d["tab"]=="KA" else AZ,int(d["mode"]),d["model"],int(d["start"]),int(d["p"]))
    print(l.strip(),"|",s,"| qg/4gram",None if sc is None else round(sc,2))
