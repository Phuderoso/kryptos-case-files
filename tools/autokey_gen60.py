"""Cycle 60 inputs: (1) N=98 decimations ('?' as symbol 0, K3's law over 98 symbols, M = 98..112, both directions);
(2) planted autokey controls behind random decimations (both models, both feeds, three modes, themed alphabets);
(3) shuffled-K4 nulls are reused from cycle 59 (data/cycle59/null*.txt). Run from the working copy root's sibling dir."""
import struct, math, random, sys
K4=open(sys.argv[1]).read().split()[0]
def decs(N,Ms):
    T={}
    for M in Ms:
        for s in range(1,M):
            if math.gcd(s,M)!=1: continue
            for a in range(M):
                out=[v for v in ((a+s*j)%M for j in range(M)) if v<N]
                inv=[0]*N
                for k,v in enumerate(out): inv[v]=k
                T.setdefault(tuple(out),f"dec98 M{M} s{s} a{a}/dec"); T.setdefault(tuple(inv),f"dec98 M{M} s{s} a{a}/enc")
    return T
T=decs(98,range(98,113))
with open("dec98.bin","wb") as f:
    for p in T: f.write(struct.pack("<98h",*p))
open("dec98.txt","w").write("\n".join(T.values())+"\n"); print("N=98 decimations",len(T))
open("k4q.txt","w").write("?"+K4+"\n")
# controls
A=open(sys.argv[2],"rb").read(); al=lambda i:[A[26*i+k] for k in range(26)]
filler="THEROOMWASDARKANDTHEAIRWASSTILLXINTHECORNERSTOODANOLDDESKXWECOULDSEETHEBRASSPLATEANDTHEMAPWHEREVERYTHINGPOINTEDTO"
pt=(filler[:21]+"EASTNORTHEAST"+filler[21:50]+"BERLINCLOCK"+filler[50:73])
assert len(pt)==97
perms=[struct.unpack_from("<97h",open(sys.argv[3],"rb").read(),i*194) for i in (777,40404,123456,9001)]
def enc(model,feed,mode,L,alpha,perm,seed):
    rnd=random.Random(seed); idx={c:i for i,c in enumerate(alpha)}
    def ak(x):  # x list of indices -> autokey ciphertext indices, random primer
        out=[]
        for j,p in enumerate(x):
            if j<L: k=rnd.randrange(26)
            else: k=out[j-L] if feed=="CT" else x[j-L]
            out.append((p+k)%26 if mode=="vig" else (k-p)%26 if mode=="beau" else (p-k)%26)
        return out
    P=[idx[ord(c)-65] for c in pt]
    ct=[0]*97
    if model=="A":
        I=ak(P)
        for j in range(97): ct[perm[j]]=I[j]
    else:
        Tt=[0]*97
        for j in range(97): Tt[perm[j]]=P[j]
        ct=ak(Tt)
    return "".join(chr(65+alpha[c]) for c in ct)
specs=[("A","CT","vig",7,5,0),("A","PT","beau",4,1,1),("B","CT","var",11,40,2),("B","PT","vig",2,0,3)]
for i,(m,fd,md,L,ai,pi) in enumerate(specs):
    open(f"actl{i}.txt","w").write(enc(m,fd,md,L,al(ai),perms[pi],i)+"\n")
    print(f"actl{i}: model {m} feed {fd} mode {md} L {L} alpha {ai} perm index {(777,40404,123456,9001)[pi]}")
