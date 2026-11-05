# Cycle 88: permutations of the 92-letter W-free K4 (W treated as null/separator).
# P[j] = plaintext position that lands at ciphertext position j. Both P and its inverse are emitted.
import itertools, sys
N=92
def columnar(w,order):
    rows=(N+w-1)//w; P=[]
    for c in order:
        for r in range(rows):
            i=r*w+c
            if i<N: P.append(i)
    return P
def decim(M,s,a,d):
    P=[]; x=a
    for _ in range(M):
        if x<N: P.append(x)
        x=(x+d*s)%M
    return P
perms=set()
for w in range(2,9):
    for o in itertools.permutations(range(w)): perms.add(tuple(columnar(w,o)))
from math import gcd
for M in range(92,108):
    for s in range(2,M-1):
        if gcd(s,M)!=1: continue
        for a in range(M):
            P=decim(M,s,a,1)
            perms.add(tuple(P))
perms.add(tuple(range(N)))
allp=set()
for P in perms:
    assert sorted(P)==list(range(N))
    allp.add(P); inv=[0]*N
    for j,i in enumerate(P): inv[i]=j
    allp.add(tuple(inv))
allp=sorted(allp)
open('perms92.bin','wb').write(bytes(x for P in allp for x in P))
print(len(allp))
