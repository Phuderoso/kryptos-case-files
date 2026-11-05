import sys,random; sys.argv=['x']; exec(open('colgen.py').read().split("if __name__")[0])
from collections import Counter
def cnt(CT):
  res=run(CT,8); c=Counter(r[4] for r in res); return [c.get(p,0) for p in range(1,8)]
print('K4  ',cnt(K))
r=random.Random(11)
for t in range(3):
  s=list(K); r.shuffle(s); print('null',cnt(''.join(s)))
