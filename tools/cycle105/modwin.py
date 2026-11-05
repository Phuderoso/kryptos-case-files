# Which modulus wins when T1 fires, per family (needs sim.py functions)
import sys; sys.argv=['x','1']
exec(open('sim.py').read().split("k4=(excess")[0])
from collections import Counter
k4e=excess(K4)
def best_m(t):
  d=[i for i in range(len(t)-1) if t[i]==t[i+1]]; bm=None;b=0
  for m in range(2,26):
    c=Counter(x%m for x in d); v=max(c.values())-len(d)/m
    if v>b: b,bm=v,m
  return bm
for name in ['random letters (null)','Vigenere p7','Vigenere p7 then columnar w7','Vigenere p7 then columnar w14','columnar w21 then mono']:
  f=fam[name]; C=Counter(); n=0
  for _ in range(40000):
    c=f(pt())
    if excess(c)>=k4e-1e-9: C[best_m(c)]+=1; n+=1
  print(f'{name:32s} hits {n:4d}  winning moduli {C.most_common(6)}')
print('K4 winning modulus', best_m(K4))
