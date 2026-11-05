"""Cycle 107: for a given transposition, decrypt the W-turn disk with fixed KRYPTOS/A-Z rings (model B), all d, s0; crib matches + quadgrams."""
import numpy as np,sys,json
K4=sys.argv[2] if len(sys.argv)>2 else open('/tmp/kcf/data/k4.txt').read().strip()
P=np.fromfile('perms97.bin',dtype=np.int16).reshape(-1,97); t=P[int(sys.argv[1])]; inv=np.argsort(t)
Q=json.load(open('/home/box/kryptos_support_backup/quadgrams.json')); q=Q['q']; fl=Q['floor']
sc=lambda s: sum(q.get(s[i:i+4],fl) for i in range(len(s)-3))/(len(s)-3)
def ka(k):
    s=[];[s.append(c) for c in k+"ABCDEFGHIJKLMNOPQRSTUVWXYZ" if c not in s];return [ord(c)-65 for c in s]
rings={'AZ':list(range(26)),'KA':ka('KRYPTOS')}
cr={i:c for i,c in zip(range(21,34),"EASTNORTHEAST")}; cr.update({i:c for i,c in zip(range(63,74),"BERLINCLOCK")})
best=[]
for on,O in rings.items():
  for In,I in rings.items():
    Ip={I[k]:k for k in range(26)}
    for beau in (0,1):
      for d in range(26):
        for s0 in range(26):
          pt=[None]*97; nW=0
          for n in range(97):
            c=ord(K4[n])-65; s=s0+nW*d
            v=(Ip[c]-s)%26 if not beau else (s-Ip[c])%26
            pt[int(inv[n])]=chr(65+O[v])
            if c==22: nW+=1
          pt=''.join(pt); m=sum(pt[i]==c for i,c in cr.items())
          best.append((m,round(sc(pt),3),on,In,beau,d,s0,pt))
best.sort(key=lambda x:(-x[0],-x[1]))
for b in best[:3]: print(b)
