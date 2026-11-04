"""Cycle 40: shuffled-K4 nulls and planted progressive-affine controls (both models, numberings, forms)."""
import random, sys, numpy as np
K4="OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR"
KA="KRYPTOSABCDEFGHIJLMNQUVWXZ"; U=[1,3,5,7,9,11,15,17,19,21,23,25]
BASE=("SLOWLYDESPARATLYSLOWLYTHEREMAINSOFPASSAGEDEBRISTHATENCUMBEREDTHELOWERPARTOFTHEDOORWAYWEREREMOVEDWITH"
      "TREMBLINGHANDSIMADEATINYBREACHINTHEUPPERLEFTHANDCORNERANDTHENWIDENINGTHEHOLEALITTLEIINSERTEDTHECANDLE")
def plain(seed):
    r=random.Random(seed); s=r.randrange(0,len(BASE)-97); p=list(BASE[s:s+97])
    p[21:34]="EASTNORTHEAST"; p[63:74]="BERLINCLOCK"; return "".join(p)
def control(seed, perms, quad=False):
    r=random.Random(seed); pt=plain(seed); pi=r.randrange(len(perms)); P=perms[pi]
    e=r.randrange(2); m=r.randrange(2); form=r.randrange(2)
    a0=r.choice(U); rr=r.choice(U); b0=r.randrange(26); d=r.randrange(26); q=r.randrange(1,26) if quad else 0
    num=(lambda c: ord(c)-65) if e==0 else (lambda c: KA.index(c)); den=(lambda x: chr(65+x)) if e==0 else (lambda x: KA[x])
    inva={a:pow(a,-1,26) for a in U}
    def sub(c,i):
        A=a0*pow(rr,i,26)%26; B=(b0+d*i+q*(i*(i-1)//2))%26; x=num(c)
        return den((A*x+B)%26) if form==0 else den(((x-B)*inva[A])%26)   # form D: x_pt = A*y+B  =>  y=(x-B)/A
    car=[None]*97
    if m==0:
        for i in range(97): car[P[i]]=sub(pt[i],i)
    else:
        for k in range(97): car[k]=sub(pt[P[k]],k)
    return "".join(car), dict(perm=pi,num="AK"[e],model="AB"[m],form="ED"[form],a0=a0,r=rr,b0=b0,d=d,q=q,pt=pt)
if __name__=="__main__":
    perms=np.fromfile("perms97.bin",dtype=np.int16).reshape(-1,97)
    kind,seed=sys.argv[1],int(sys.argv[2])
    if kind=="null":
        l=list(K4); random.Random(seed).shuffle(l); print("".join(l))
    else:
        c,meta=control(seed,perms,kind=="qcontrol"); print(c); print(meta,file=sys.stderr)
