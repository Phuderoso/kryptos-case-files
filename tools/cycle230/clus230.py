import sys; sys.path.insert(0,'../src'); import analyze230 as a
def clusters(lines):
    n=len(lines); par=list(range(n))
    def f(i):
        while par[i]!=i: par[i]=par[par[i]]; i=par[i]
        return i
    ks=[[ord(c)-65 for c in l[7]] for l in lines]
    for i in range(n):
        for j in range(i):
            a_,b_=lines[i],lines[j]
            agree=sum(1 for t in range(24) if ks[i][t]==ks[j][t]); neg=sum(1 for t in range(24) if (ks[i][t]+ks[j][t])%26==0)
            # same X (any Y, any form, any row) and >=16/24 shift agreement (direct or mirrored) -> one cluster
            if a_[2]==b_[2] and max(agree,neg)>=16: par[f(i)]=f(j)
            elif a_[2]==b_[2] and a_[3]==b_[3] and a_[4]==b_[4]: par[f(i)]=f(j)  # same X,Y,form (row twins/neighbours)
    return len({f(i) for i in range(n)})
for crit,fl in (("W9",lambda l:l[5]<=9),("W10",lambda l:l[5]<=10),("D6",lambda l:l[6]<=6)):
    for sc in ("direct","bank","all"):
        k4=clusters([l for l in a.parse(f"R/k4_{sc}.txt")[0] if fl(l)])
        ns=[clusters([l for l in a.parse(f"R/null{i}_{sc}.txt")[0] if fl(l)]) for i in range(10)]
        print(crit,sc,"K4 clusters",k4,"| nulls",ns,"| null-equiv",sum(ns)*2)
