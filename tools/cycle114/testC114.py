"""Test C: generic Kryha V1 code wheel (n sectors, teeth 1..9, +4) with BOTH alphabets free: CP-SAT, exact.
Small n is the only informative range (n >= 5 is SAT for K4: crib-underdetermined).  K4, nulls, planted controls."""
import sys, random
from sat114 import solve
from kryha114 import *
R=random.Random(1143); NS=range(1,8)
nulls=["".join(R.sample(K4,97)) for _ in range(10)]
ctls=[]
for k in range(6):
    n=R.choice([1,2,3,4]); w=[R.randrange(1,10) for _ in range(n)]; sg=R.choice((1,-1))
    sh=v1_shifts(w,0); sh=[0]
    for i in range(96): sh.append((sh[-1]+w[i%n]+4)%26)
    ctls.append((kryha_enc(PT,rand_alpha(R),rand_alpha(R),sh,sg),n,sg,w))
for n in NS:
    for sg in (1,-1):
        k4=solve(K4,n,sg,timeout=60)[0]
        nl=[solve(c,n,sg,timeout=30)[0] for c in nulls]
        print(f"n={n} sigma={sg:+d}  K4 {k4}  nulls SAT {nl.count('SAT')}/10 UNSAT {nl.count('UNSAT')} UNKNOWN {nl.count('UNKNOWN')}",flush=True)
for ct,n,sg,w in ctls:
    st,d=solve(ct,n,sg,timeout=60); st2,_=solve(ct,n,sg,timeout=60,fix=[x+4 for x in w])
    print(f"control n={n} sigma={sg:+d} teeth={w}: {st}; with the true wheel fixed: {st2}",flush=True)
