"""Cycle 62 planted controls: autokey (both models, both feeds, three modes, themed alphabets) behind random
spiral/diagonal routes from cycle 61's route_perm.bin. Usage: autokey_gen62.py alpha.bin route_perm.bin outdir"""
import struct, random, sys
A=open(sys.argv[1],"rb").read(); al=lambda i:[A[26*i+k] for k in range(26)]
R=open(sys.argv[2],"rb").read(); n=len(R)//194; out=sys.argv[3]
filler="THEROOMWASDARKANDTHEAIRWASSTILLXINTHECORNERSTOODANOLDDESKXWECOULDSEETHEBRASSPLATEANDTHEMAPWHEREVERYTHINGPOINTEDTO"
pt=(filler[:21]+"EASTNORTHEAST"+filler[21:50]+"BERLINCLOCK"+filler[50:73]); assert len(pt)==97
rng=random.Random(62); pidx=[rng.randrange(n) for _ in range(4)]
perms=[struct.unpack_from("<97h",R,i*194) for i in pidx]
def enc(model,feed,mode,L,alpha,perm,seed):
    rnd=random.Random(seed); idx={c:i for i,c in enumerate(alpha)}
    def ak(x):
        o=[]
        for j,p in enumerate(x):
            k=rnd.randrange(26) if j<L else (o[j-L] if feed=="CT" else x[j-L])
            o.append((p+k)%26 if mode=="vig" else (k-p)%26 if mode=="beau" else (p-k)%26)
        return o
    P=[idx[ord(c)-65] for c in pt]; ct=[0]*97
    if model=="A":
        I=ak(P)
        for j in range(97): ct[perm[j]]=I[j]
    else:
        T=[0]*97
        for j in range(97): T[perm[j]]=P[j]
        ct=ak(T)
    return "".join(chr(65+alpha[c]) for c in ct)
specs=[("A","CT","vig",7,5,0),("A","PT","beau",4,1,1),("B","CT","var",11,40,2),("B","PT","vig",2,0,3)]
for i,(m,fd,md,L,ai,pi) in enumerate(specs):
    open(f"{out}/actl{i}.txt","w").write(enc(m,fd,md,L,al(ai),perms[pi],100+i)+"\n")
    print(f"actl{i}: model {m} feed {fd} mode {md} L {L} alpha {ai} route perm index {pidx[pi]}")
