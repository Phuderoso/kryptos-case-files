# Fully general periodic substitution: period p, each phase its own ARBITRARY bijection (no tableau structure).
# Crib consistency: within a phase, equal pt <-> equal ct.  Also: same with phase taken mod p of position, p 1..48.
import random
K=open('k4.txt').read().strip()
P={}
for i,c in enumerate('EASTNORTHEAST'): P[21+i]=c
for i,c in enumerate('BERLINCLOCK'): P[63+i]=c
def ok(CT,p):
  f={}; g={}; checks=0
  for i in sorted(P):
    a=(i%p,CT[i]); b=(i%p,P[i])
    if a in f:
      checks+=1
      if f[a]!=P[i]: return False,checks
    if b in g and g[b]!=CT[i]: return False,checks
    f[a]=P[i]; g[b]=CT[i]
  return True,checks
res=[(p,)+ok(K,p) for p in range(1,49)]
print('K4 consistent periods:',[ (p,c) for p,o,c in res if o])
r=random.Random(4); tally={}
for t in range(2000):
  s=list(K); r.shuffle(s); s=''.join(s)
  for p in range(1,49):
    if ok(s,p)[0]: tally[p]=tally.get(p,0)+1
print('null consistency rate by p:',{p:round(v/2000,3) for p,v in sorted(tally.items()) if p<=26})
