"""Test A: Kryha V1 with the 5 published code wheels, both alphabets FREE (any permutations), any start sector,
both ring senses (exact).  K4, shuffled-ciphertext nulls, planted controls."""
import random, sys, time
from kryha114 import *
NN=int(sys.argv[1]) if len(sys.argv)>1 else 200; NC=int(sys.argv[2]) if len(sys.argv)>2 else 30
t=time.time(); configs=sum(2*w for w in WHEELS)
h=test_v1_published(K4); print(f"K4: {len(h)}/{configs} configs consistent: {h}")
R=random.Random(1141); nz=0; zero=0; tot=0
for k in range(NN):
    l=list(K4); R.shuffle(l); hh=test_v1_published("".join(l)); tot+=len(hh); zero+= (len(hh)==0)
print(f"nulls: {NN} shuffles, {zero} with 0 consistent, mean {tot/NN:.3f} consistent configs/shuffle")
ok=0; extra=0
for k in range(NC):
    F,M=rand_alpha(R),rand_alpha(R); wl=R.choice(list(WHEELS)); st=R.randrange(wl); sg=R.choice((1,-1))
    s0=R.randrange(26); sh=[(x+s0)%26 for x in v1_shifts(wl,st)]
    ct=kryha_enc(PT,F,M,sh,sg); hh=test_v1_published(ct)
    ok+=(wl,st,sg) in hh; extra+=len(hh)-1
    assert kryha_dec(ct,F,M,sh,sg)==PT
print(f"planted controls: {ok}/{NC} true setting recovered; {extra} extra consistent configs in total")
print(f"{time.time()-t:.1f}s")
