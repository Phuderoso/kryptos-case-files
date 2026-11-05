"""Cycle 71 planted controls: English (book g84) with both cribs at official positions, enciphered with a Wheatstone
cryptograph (random inner alphabet, themed outer alphabet from a264.bin, blank gap, direction), then transposed by a
perm from perms97.bin (model A: car[P[i]] = W(pt)[i]). Same conventions as wheat71.c."""
import random,re,numpy as np
random.seed(71);N=97
perms=np.fromfile("perms97.bin",dtype=np.int16).reshape(-1,N);A=open("a264.bin","rb").read()
book=re.sub("[^A-Z]","",open("/workspace/kcl/data/g84.txt").read().upper())
def wheat(pt,a,g,d,inner):
    seq=list(A[a*26:a*26+26])
    if g>=0: seq.insert(g+1,26)
    if d: seq=seq[::-1]
    Mo=len(seq);Mi=27 if g<0 else 26;pos={s:k for k,s in enumerate(seq)}
    T=random.randrange(1000);cur=seq[T%Mo];out=[]
    for ch in pt:
        s=(pos[ord(ch)-65]-pos[cur])%Mo or Mo;T+=s;cur=ord(ch)-65;out.append(inner[T%Mi])
    return out
plans=[(0,5,0,17),(1,20,0,4242),(7,12,1,120000),(3,25,0,0),(100,8,1,99999),(1,0,1,165001)]
out=open("controls71.txt","w")
for n,(a,g,d,pi) in enumerate(plans,1):
    s=random.randrange(len(book)-200);pt=list(book[s:s+N]);pt[21:34]="EASTNORTHEAST";pt[63:74]="BERLINCLOCK"
    inner=[chr(65+i) for i in range(26)];random.shuffle(inner)
    if g<0: inner=inner+['?']
    w=wheat(pt,a,g,d,inner)
    while '?' in w:  # G2: unused inner cell must not appear; retry start
        w=wheat(pt,a,g,d,inner)
    P=perms[pi];car=[None]*N
    for i in range(N):car[P[i]]=w[i]
    open(f"ctl_{n}.txt","w").write("".join(car))
    out.write(f"ctl_{n}: alpha={a} gap={g} dir={d} perm={pi} pt={''.join(pt)}\n")
