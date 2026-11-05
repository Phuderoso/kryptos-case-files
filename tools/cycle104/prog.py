# Progressive periodic key: k[i+p] = k[i] + D (mod 26), i.e. a period-p key that shifts by D every period.
# Exact crib test over p 1..48, D 0..25, A-Z and KRYPTOS alphabets, Vigenere/Beaufort/variant. Also shuffled nulls.
import random,sys
K=open('k4.txt').read().strip()
P={}
for i,c in enumerate('EASTNORTHEAST'): P[21+i]=c
for i,c in enumerate('BERLINCLOCK'): P[63+i]=c
ALS=[('AZ','ABCDEFGHIJKLMNOPQRSTUVWXYZ'),('KA','KRYPTOSABCDEFGHIJLMNQUVWXZ')]
def test(CT):
  hits=[]
  for nm,A in ALS:
    for md in ['vig','beau','var']:
      ks={}
      for i in P:
        c,p=A.index(CT[i]),A.index(P[i]); ks[i]={'vig':(c-p)%26,'beau':(c+p)%26,'var':(p-c)%26}[md]
      for per in range(1,49):
        # group crib positions by residue; within a residue class k[i] = k0 + D*(i//per)
        for D in range(26):
          ok=True; base={}; checks=0
          for i in sorted(ks):
            r=i%per; v=(ks[i]-D*(i//per))%26
            if r in base:
              checks+=1
              if base[r]!=v: ok=False;break
            else: base[r]=v
          if ok and checks>=4: hits.append((nm,md,per,D,checks))
  return hits
h=test(K); print('K4 hits',len(h),h[:20])
r=random.Random(5); nn=[]
for t in range(50):
  s=list(K); r.shuffle(s); nn.append(len(test(''.join(s))))
print('null hits (50 shuffles): mean',sum(nn)/50,'max',max(nn),'zero frac',nn.count(0)/50)
