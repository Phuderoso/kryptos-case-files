"""Cycle 118: reflector machines (Enigma, Typex, NEMA, any fixed-point-free involution per position).
A: direct self-encryption proof, incl. crib-block shifts from a dropped/extra carved letter.
B: self-encryption filter behind the 165,065-perm bank, both layer orders, K4 vs shuffled nulls,
   with planted controls (random fixed-point-free involution per position = idealised reflector machine)."""
import numpy as np, random, sys
CT='OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR'
CR=[(21,'EASTNORTHEAST'),(63,'BERLINCLOCK')]
pos=np.array([s+i for s,w in CR for i in range(len(w))]); pl=np.array([ord(c)-65 for s,w in CR for c in w])
A=lambda t: np.array([ord(c)-65 for c in t])
print("== A: direct ==")
c=A(CT); print("self-encryptions at", [int(p) for p in pos[c[pos]==pl]])
for d1 in range(-3,4):
  for d2 in range(-3,4):
    if d2<d1-0 and False: pass
    q=np.concatenate([pos[:13]+d1,pos[13:]+d2]); 
    if q.min()<0 or q.max()>96: continue
    n=int((c[q]==pl).sum()); print(f" shift blk1 {d1:+d} blk2 {d2:+d}: self-enc {n}", "" if n else "  <-- reflector machine NOT excluded")
D='/workspace/k4c116/'; N=165065
P=np.fromfile(D+'perms97.bin',dtype=np.int16).reshape(N,97).astype(np.int64)
Pinv=np.argsort(P,axis=1)
def surv(t):
  t=A(t); a=(t[P[:,pos]]!=pl).all(1); b=(t[Pinv[:,pos]]!=pl).all(1); return int(a.sum()),int(b.sum())
print("== B: behind bank (sub first = A, transposition first = B) ==")
k=surv(CT); print("K4", k, f"({k[0]/N:.3f}, {k[1]/N:.3f}); random expectation (25/26)^24 = {(25/26)**24:.3f}")
R=random.Random(118); nulls=[]
for i in range(20):
  l=list(CT); R.shuffle(l); nulls.append(surv("".join(l)))
na=[x for x,_ in nulls]; nb=[y for _,y in nulls]
print("nulls A min/med/max", min(na), int(np.median(na)), max(na), " B", min(nb), int(np.median(nb)), max(nb))
print("K4 rank among nulls A:", sum(x<k[0] for x in na), "/20 below; B:", sum(y<k[1] for y in nb), "/20 below")
# planted controls: idealised reflector machine (random fixed-point-free involution per position), then a bank perm
def inv_fpf(R):
  l=list(range(26)); R.shuffle(l); m=[0]*26
  for j in range(0,26,2): m[l[j]]=l[j+1]; m[l[j+1]]=l[j]
  return m
pt=("THEPOINTWASNEVERTHEMACHINEBUTTHEMANWHOWROTEEASTNORTHEASTONTHECARDANDLEFT"+"ITBYTHEBERLINCLOCK")
pt=pt[:21]+'EASTNORTHEAST'+pt[34:63]+'BERLINCLOCK'+pt[74:]; pt=(pt+'X'*97)[:97]
for j in range(3):
  p=R.randrange(N); E=[inv_fpf(R)[ord(ch)-65] for ch in pt]
  if j<2:  # sub first: carved[k] such that intermediate k = carved[P[k]]
    car=[0]*97
    for kk in range(97): car[P[p,kk]]=E[kk]
    t="".join(chr(65+x) for x in car); a=(A(t)[P[p,pos]]!=pl).all(); print(f"control {j} (order A, perm {p}): survives at true perm: {bool(a)}; total survivors {surv(t)}")
  else:
    t="".join(chr(65+x) for x in E); print("control direct reflector: self-enc", int((A(t)[pos]==pl).sum()))
