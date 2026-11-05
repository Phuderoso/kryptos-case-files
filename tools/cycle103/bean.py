import random
K=open('/workspace/k4c101/k4.txt').read().strip()
def rep(t,w):
    pr=[(t[i],t[i+w]) for i in range(len(t)-w)]; return len(pr)-len(set(pr))
r=random.Random(1); NS=20000
res=[]
for w in range(1,49):
    k=rep(K,w); ge=0; tot=0
    for _ in range(NS):
        s=list(K); r.shuffle(s); v=rep(s,w); tot+=v; ge+=v>=k
    res.append((w,k,tot/NS,(ge+1)/(NS+1)))
for w,k,m,p in res: print(w,k,round(m,2),f"{p:.5f}")
