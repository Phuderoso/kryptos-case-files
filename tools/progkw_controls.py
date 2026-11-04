"""Cycle 41: shuffled-K4 nulls and planted progressive-keyword controls (both models, numberings, modes)."""
import random, sys, numpy as np
K4="OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR"
KA="KRYPTOSABCDEFGHIJLMNQUVWXZ"
BASE=("SLOWLYDESPARATLYSLOWLYTHEREMAINSOFPASSAGEDEBRISTHATENCUMBEREDTHELOWERPARTOFTHEDOORWAYWEREREMOVEDWITH"
      "TREMBLINGHANDSIMADEATINYBREACHINTHEUPPERLEFTHANDCORNERANDTHENWIDENINGTHEHOLEALITTLEIINSERTEDTHECANDLE")
def plain(seed):
    r=random.Random(seed); s=r.randrange(0,len(BASE)-97); p=list(BASE[s:s+97])
    p[21:34]="EASTNORTHEAST"; p[63:74]="BERLINCLOCK"; return "".join(p)
def control(seed, perms):
    r=random.Random(seed); pt=plain(seed); pi=r.randrange(len(perms)); P=perms[pi]
    e=r.randrange(2); m=r.randrange(2); md=r.randrange(2); L=r.randrange(1,14); s=r.randrange(1,26)
    k=[r.randrange(26) for _ in range(L)]
    num=(lambda c: ord(c)-65) if e==0 else (lambda c: KA.index(c)); den=(lambda x: chr(65+x)) if e==0 else (lambda x: KA[x])
    def sub(c,i):
        key=(k[i%L]+s*(i//L))%26; x=num(c)
        return den((x+key)%26) if md==0 else den((key-x)%26)
    car=[None]*97
    if m==0:
        for i in range(97): car[P[i]]=sub(pt[i],i)
    else:
        for j in range(97): car[j]=sub(pt[P[j]],j)
    kw="".join(den(x) for x in k)
    return "".join(car), dict(perm=pi,num="AK"[e],model="AB"[m],mode="VB"[md],L=L,s=s,key=kw,pt=pt)
if __name__=="__main__":
    perms=np.fromfile("perms97.bin",dtype=np.int16).reshape(-1,97)
    kind,seed=sys.argv[1],int(sys.argv[2])
    if kind=="null":
        l=list(K4); random.Random(seed).shuffle(l); print("".join(l))
    else:
        c,meta=control(seed,perms); print(c); print(meta,file=sys.stderr)
