"""Cycle 44: transposition families not yet in the repo: rail fence, Redefence (rails read in any order),
AMSCO (alternating 1/2-letter cells, both start sizes, both row conventions, every column order).
Writes P with P[i] = carved position of plaintext letter i (encryption), plus each inverse."""
import itertools, numpy as np, sys
N=97
def rail_rows(r,o):
    cyc=2*r-2; rows=[]
    for i in range(N):
        t=(i+o)%cyc; rows.append(t if t<r else cyc-t)
    return rows
def redefence(r,o,order):
    rows=rail_rows(r,o); out=[]
    for rr in order: out+= [i for i in range(N) if rows[i]==rr]
    P=[0]*N
    for c,i in enumerate(out): P[i]=c
    return P
def amsco(w,start,conv,order):
    # cells: list of (col, [plaintext indices])
    cols=[[] for _ in range(w)]; i=0; size=start; row=0
    while i<N:
        rs = size if conv==0 else (start if row%2==0 else 3-start)
        s=rs
        for c in range(w):
            if i>=N: break
            take=list(range(i,min(N,i+s))); cols[c]+=take; i+=len(take); s=3-s
        if conv==0: size=s
        row+=1
    out=[]
    for c in order: out+=cols[c]
    P=[0]*N
    for k,i in enumerate(out): P[i]=k
    return P
def emit(fam, wmin, wmax):
    seen=set(); res=[]; tags=[]
    def add(P,tag):
        for Q,t in ((P,tag+"/enc"),(list(np.argsort(P)),tag+"/dec")):
            key=bytes(np.array(Q,dtype=np.int16).tobytes())
            if key in seen: continue
            seen.add(key); res.append(Q); tags.append(t)
    add(list(range(N)),"identity")
    if fam=="A":
        for r in range(2,49):
            for o in range(2*r-2): add(redefence(r,o,range(r)),f"rail r={r} o={o}")
        for r in range(3,8):
            for o in range(2*r-2):
                for order in itertools.permutations(range(r)): add(redefence(r,o,order),f"redef r={r} o={o} ord={''.join(map(str,order))}")
    for w in range(wmin,wmax+1):
        for start in (1,2):
            for conv in (0,1):
                if w%2==1 and conv==1: continue
                for order in itertools.permutations(range(w)): add(amsco(w,start,conv,order),f"amsco w={w} start={start} conv={conv} ord={''.join(map(str,order))}")
    return res,tags
fam=sys.argv[1]
res,tags=emit(fam,2 if fam=="A" else 9, 8 if fam=="A" else 9)
np.array(res,dtype=np.int16).tofile(f"perms_{fam}.bin")
open(f"perms_{fam}.txt","w").write("\n".join(tags)+"\n")
print(fam,len(res))
