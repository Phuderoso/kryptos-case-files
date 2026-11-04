"""Cycle 53: DISRUPTED (triangular) columnar transposition, exact. Grid width w = keyword length, ceil(97/w) rows,
cells with row-major index >= 97 unused. Disruption areas: the first starts in row 0 at the column ranked 1 by the
key; T1 (ACA 'disrupted columnar'): the area covers columns c..w-1 in its first row, c+1..w-1 in the next, ...
(a triangle shrinking to the right edge), then the next area starts on the following row at the column ranked 2,
and so on cyclically until the rows run out. T2: the mirror-growing triangle (row t of the area covers columns
c..c+t, ending when it reaches the right edge). Plaintext fills the undisrupted cells row by row first, then the
disrupted cells row by row; ciphertext = columns read top-down in key-rank order.
Output: one line per permutation: name P[0..96]  (P[i] = ciphertext index of plaintext letter i)."""
import itertools,sys
N=97
def areas(w,o,variant):
    rows=(N+w-1)//w; dis=set(); r=0; a=0
    while r<rows:
        c=o[a%w]; a+=1
        if variant==1:
            t=0
            while r<rows and c+t<=w-1:
                for cc in range(c+t,w): dis.add((r,cc))
                r+=1; t+=1
        else:
            t=0
            while r<rows and c+t<=w-1:
                for cc in range(c,c+t+1): dis.add((r,cc))
                r+=1; t+=1
    return rows,dis
def perm(w,o,variant):
    rows,dis=areas(w,o,variant)
    cells=[(r,c) for r in range(rows) for c in range(w) if r*w+c<N]
    order=[x for x in cells if x not in dis]+[x for x in cells if x in dis]
    pidx={cell:i for i,cell in enumerate(order)}   # plaintext index per cell
    P=[0]*N; k=0
    for c in o:
        for r in range(rows):
            if r*w+c<N: P[pidx[(r,c)]]=k; k+=1
    assert sorted(P)==list(range(N))
    return P
if __name__=="__main__":
    out=open('dperms.txt','w'); themed=open('dthemed.txt','w'); n=0; seen=set()
    THEMED_N=int(sys.argv[1])
    lines=open('orders.txt').read().split('\n')
    srcs=[]
    for li,l in enumerate(lines):
        if not l.strip(): continue
        f=l.split(); srcs.append((f[0],tuple(map(int,f[2:])),li<THEMED_N))
    for w in range(3,8):
        for o in itertools.permutations(range(w)): srcs.append(("P"+"".join(map(str,o)),o,False))
    for name,o,th in srcs:
        for v in (1,2):
            P=tuple(perm(len(o),o,v))
            if P in seen: continue
            seen.add(P); s=f"{name}_T{v} "+" ".join(map(str,P))+"\n"
            (themed if th else out).write(s); n+=1
    print(n,"distinct disrupted permutations")
