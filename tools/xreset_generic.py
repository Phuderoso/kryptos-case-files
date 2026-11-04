"""Cycle 26: arbitrary key word (any letters) with X-reset (interrupted key).
If the key restarts at plaintext X's (none inside the cribs), the two crib blocks keep
internal period-P structure but their relative key phase d becomes free. For each tableau,
mode and period P, count phases d (0..P-1) for which some key fits all 24 crib letters.
Compare with shuffled-K4 nulls and the plain periodic phase d = 42 mod P."""
import random, sys
from kryptos_text import K4
A={'AZ':"ABCDEFGHIJKLMNOPQRSTUVWXYZ",'KA':"KRYPTOSABCDEFGHIJLMNQUVWXZ"}
CR=[(21+i,c) for i,c in enumerate("EASTNORTHEAST")]+[(63+i,c) for i,c in enumerate("BERLINCLOCK")]
def keyval(a,c,p,mode):
    ci,pi=a.index(c),a.index(p)
    return (ci-pi)%26 if mode==0 else (ci+pi)%26 if mode==1 else (pi-ci)%26
def count(ct):
    res={}
    for tab,a in A.items():
        for mode in range(3):
            for P in range(1,27):
                ok=[]
                for d in range(P):
                    need={}; good=True
                    for pos,p in CR:
                        j=(pos-21)%P if pos<40 else (d+pos-63)%P
                        v=keyval(a,ct[pos],p,mode)
                        if need.setdefault(j,v)!=v: good=False;break
                    if good: ok.append(d)
                res[(tab,mode,P)]=ok
    return res
def summary(r):
    tot=sum(len(v) for v in r.values()); minP=min([k[2] for k,v in r.items() if v],default=None)
    return tot,minP
k=count(K4); print("K4 total (tab,mode,P,d) consistent:",summary(k))
for key,v in sorted(k.items(),key=lambda x:x[0][2]):
    if v and key[2]<=16: print(" ",key,v)
for s in range(1,21):
    r=random.Random(s); x=list(K4); r.shuffle(x); print("null",s,summary(count(''.join(x))))
# control: rule-1 SHADOW KA vig ciphertext
print("ctl_1",summary(count(open('ctl_1.txt').read().strip())))
