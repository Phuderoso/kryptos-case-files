import random
K=open('k4.txt').read().strip()
def stat(t):
  d=[i for i in range(len(t)-1) if t[i]==t[i+1]]
  best=0
  for m in range(2,26):
    cnt={}
    for x in d: cnt[x%m]=cnt.get(x%m,0)+1
    if d: best=max(best, max(cnt.values())-len(d)/m)
  return len(d),best
n,b=stat(K); print('K4 doubles',n,'excess',round(b,2))
r=random.Random(3); N=20000; ge=0
for _ in range(N):
  s=list(K); r.shuffle(s); nn,bb=stat(s); ge+= bb>=b-1e-9
print('p(look-elsewhere over moduli 2-25, shuffles)',(ge+1)/(N+1))
