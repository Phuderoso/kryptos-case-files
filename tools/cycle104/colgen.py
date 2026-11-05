# Width-w columnar transposition (any column order, both directions) + fully general periodic substitution
# (period p, arbitrary independent alphabet per phase), phase on plaintext position (sub first) or carved position (sub last).
import itertools,random,sys
K=open('k4.txt').read().strip(); N=97
P={}
for i,c in enumerate('EASTNORTHEAST'): P[21+i]=c
for i,c in enumerate('BERLINCLOCK'): P[63+i]=c
CR=sorted(P)
def colperm(w,order):
  # s[i] = carved position of plaintext position i
  s=[0]*N; pos=0
  for col in order:
    for i in range(col,N,w): s[i]=pos; pos+=1
  return s
def consistent(CT,s,p,mode):
  f={}; g={}
  for i in CR:
    ph=(i if mode==0 else s[i])%p; c=CT[s[i]]; a=(ph,c); b=(ph,P[i])
    if f.get(a,P[i])!=P[i] or g.get(b,c)!=c: return False
    f[a]=P[i]; g[b]=c
  return True
def run(CT,wmax,pmax=26):
  out=[]
  for w in range(2,wmax+1):
    for order in itertools.permutations(range(w)):
      s=colperm(w,order); inv=[0]*N
      for i in range(N): inv[s[i]]=i
      for d,ss in ((0,s),(1,inv)):
        for mode in (0,1):
          for p in range(1,min(pmax,14)+1):
            if consistent(CT,ss,p,mode): out.append((w,order,d,mode,p))
  return out
if __name__=='__main__':
  CT=sys.argv[1] if len(sys.argv)>1 else K; wmax=int(sys.argv[2]) if len(sys.argv)>2 else 8
  res=run(CT,wmax)
  from collections import Counter
  print('total',len(res)); print(sorted(Counter(r[4] for r in res).items()))
  for r in res:
    if r[4]<=7: print(r)
