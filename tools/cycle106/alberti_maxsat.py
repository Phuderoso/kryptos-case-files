"""Cycle 106: Alberti disk with BOTH rings arbitrary (any outer order O, any inner order I), directly on the text.
Setting s_j = I(c_j) - O(p_j) mod 26 is constant between disk turns. MaxSAT (RC2) maximises the number E of
adjacent crib pairs with equal setting, i.e. minimises disk turns inside the crib spans (E = 22 - turns).
Beaufort (reversed inner ring) is included because I is arbitrary. usage: alberti_maxsat.py CT [timeout_s]"""
import sys, itertools, time
from pysat.formula import WCNF, IDPool
from pysat.card import CardEnc, EncType
from pysat.examples.rc2 import RC2
ct=sys.argv[1]; C=[ord(x)-65 for x in ct]
cr={21:"EASTNORTHEAST",63:"BERLINCLOCK"}
pos=[];P={}
for st,w in cr.items():
    for k,ch in enumerate(w): P[st+k]=ord(ch)-65
pairs=[(j,j+1) for j in range(21,33)]+[(j,j+1) for j in range(63,73)]
pool=IDPool(); O=lambda l,v: pool.id(('O',l,v)); I=lambda l,v: pool.id(('I',l,v)); e=lambda k: pool.id(('e',k))
w=WCNF()
for R in (O,I):
    for l in range(26):
        for cl in CardEnc.equals([R(l,v) for v in range(26)],1,vpool=pool,encoding=EncType.seqcounter): w.append(cl)
    for v in range(26):
        for cl in CardEnc.equals([R(l,v) for l in range(26)],1,vpool=pool,encoding=EncType.seqcounter): w.append(cl)
w.append([O(P[21],0)]); w.append([I(C[21],0)])   # symmetry: fix one outer and one inner position
for k,(a,b) in enumerate(pairs):
    pa,pb,ca,cb=P[a],P[b],C[a],C[b]
    for x in range(26):
        for y in range(26):
            for z in range(26):
                # O(pa)=x, I(ca)=y, O(pb)=z  ->  I(cb) = z + y - x
                w.append([-e(k),-O(pa,x),-I(ca,y),-O(pb,z),I(cb,(z+y-x)%26)])
    w.append([e(k)],weight=1)
t=time.time()
with RC2(w,solver='g4') as r:
    m=r.compute(); cost=r.cost
S=set(x for x in m if x>0)
Ov=[next(v for v in range(26) if O(l,v) in S) for l in range(26)]
Iv=[next(v for v in range(26) if I(l,v) in S) for l in range(26)]
s=''.join(chr(65+(Iv[C[j]]-Ov[P[j]])%26) for j in sorted(P))
print(f"E_max={22-cost} turns_min={cost} settings={s} time={time.time()-t:.1f}s")
