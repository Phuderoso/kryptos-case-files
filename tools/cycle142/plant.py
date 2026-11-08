"""Cycle 142 controls: Hill 6x6 planted directly on cycle 137's English control plaintext.
Seed 14200; nulls: 20 shuffled K4 (seeds 14201-14220)."""
import importlib.util, random, sys
spec=importlib.util.spec_from_file_location("p141","/workspace/k141/plant.py"); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
R=random.Random(14200); m.R=R
def rmat(n):
    while True:
        D=[[R.randrange(26) for _ in range(n)] for _ in range(n)]; E=m.inv26(D)
        if E: return D,E
def hill(text,M,o,N,n):
    t=list(text)
    for b in range(o,97-n+1,n):
        v=[N.index(c) for c in text[b:b+n]]
        for r in range(n): t[b+r]=N[sum(M[r][j]*v[j] for j in range(n))%26]
    return "".join(t)
P=m.m.plain()
for name,o,nu in (("ctl1",0,0),("ctl2",3,1),("ctl3",5,0)):
    D,E=rmat(6); print(name,o,nu,hill(P,E,o,m.NUMS[nu],6))
for z in range(1,21):
    l=list(m.K4); random.Random(14200+z).shuffle(l); print(f"null{z}",-1,-1,"".join(l))
