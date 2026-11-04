"""Cycle 39: make shuffled-K4 nulls and planted periodic-affine controls (both models, both numberings)."""
import random, sys, numpy as np
K4="OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR"
KA="KRYPTOSABCDEFGHIJLMNQUVWXZ"
U=[1,3,5,7,9,11,15,17,19,21,23,25]
BASE=("SLOWLYDESPARATLYSLOWLYTHEREMAINSOFPASSAGEDEBRISTHATENCUMBEREDTHELOWERPARTOFTHEDOORWAYWEREREMOVEDWITH"
      "TREMBLINGHANDSIMADEATINYBREACHINTHEUPPERLEFTHANDCORNERANDTHENWIDENINGTHEHOLEALITTLEIINSERTEDTHECANDLE")
def plain(seed):
    r=random.Random(seed); s=r.randrange(0,len(BASE)-97); p=list(BASE[s:s+97])
    p[21:34]="EASTNORTHEAST"; p[63:74]="BERLINCLOCK"; return "".join(p)
def control(seed, perms, force=None):
    r=random.Random(seed); pt=plain(seed); pi=r.randrange(len(perms)); P=perms[pi]
    e=r.randrange(2); m=r.randrange(2) if force is None else force; L=r.randrange(1,14)
    ka=[r.choice(U) for _ in range(L)]; kb=[r.randrange(26) for _ in range(L)]
    num=(lambda c: ord(c)-65) if e==0 else (lambda c: KA.index(c))
    den=(lambda x: chr(65+x)) if e==0 else (lambda x: KA[x])
    aff=lambda c,k: den((ka[k%L]*num(c)+kb[k%L])%26)
    car=[None]*97
    if m==0:
        for i in range(97): car[P[i]]=aff(pt[i],i)
    else:
        for k in range(97): car[k]=aff(pt[P[k]],k)
    return "".join(car), dict(perm=pi,num="AK"[e],model="AB"[m],L=L,pt=pt)
if __name__=="__main__":
    perms=np.fromfile("perms97.bin",dtype=np.int16).reshape(-1,97)
    kind,seed=sys.argv[1],int(sys.argv[2])
    if kind=="null":
        l=list(K4); random.Random(seed).shuffle(l); print("".join(l))
    else:
        c,meta=control(seed,perms,int(sys.argv[3]) if len(sys.argv)>3 else None); print(c); print(meta,file=sys.stderr)
