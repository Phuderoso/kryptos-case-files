# Cycle 67: two-square (Wheatstone/Delastelle two-square), BOTH squares arbitrary, exact SAT on the crib pairs.
# Pair (a,b): a in S1 at (r1,c1), b in S2 at (r2,c2). Outputs u = X[r1][c2], v = Y[r2][c1], X,Y in {S1,S2}
# (horizontal = (S2,S1), vertical = (S1,S2); the other two combos added as a superset), emitted as (u,v) or (v,u).
# Degenerate cases (same row / same column) follow from the geometry (transparent or swapped), as in the textbooks.
import sys, random, itertools, time
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
K4="OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR"
CRIB={21+i:c for i,c in enumerate("EASTNORTHEAST")}; CRIB.update({63+i:c for i,c in enumerate("BERLINCLOCK")})
SHAPES={'2x13':(2,13),'13x2':(13,2),'6x6':(6,6)}
def solve(ct,shape,off,X,Y,swap,want_model=False):
    R,C=SHAPES[shape]; N=R*C; pool=IDPool(); cl=[]
    x=lambda s,L,k: pool.id(('x',s,L,k))
    rv=lambda s,L,r: pool.id(('r',s,L,r)); cv=lambda s,L,c: pool.id(('c',s,L,c))
    pairs=[(k,k+1) for k in range(off,96,2) if k in CRIB and k+1 in CRIB]
    used=set()
    for k,_ in pairs:
        for s,L in ((1,CRIB[k]),(2,CRIB[k+1])): used.add((s,L))
        u,v=(ct[k+1],ct[k]) if swap else (ct[k],ct[k+1])
        used.add((X,u)); used.add((Y,v))
    for s in (1,2):
        letters=[chr(65+i) for i in range(26)]
        for L in letters:
            lits=[x(s,L,k) for k in range(N)]
            cl+=CardEnc.equals(lits,1,vpool=pool,encoding=EncType.seqcounter).clauses
            for r in range(R):
                cells=[x(s,L,r*C+c) for c in range(C)]
                cl.append([-rv(s,L,r)]+cells)
                for e in cells: cl.append([-e,rv(s,L,r)])
            for c in range(C):
                cells=[x(s,L,r*C+c) for r in range(R)]
                cl.append([-cv(s,L,c)]+cells)
                for e in cells: cl.append([-e,cv(s,L,c)])
        for k in range(N):
            cl+=CardEnc.atmost([x(s,L,k) for L in letters],1,vpool=pool,encoding=EncType.seqcounter).clauses
    def eq(a,b):
        cl.append([-a,b]); cl.append([a,-b])
    for k,_ in pairs:
        a,b=CRIB[k],CRIB[k+1]
        u,v=(ct[k+1],ct[k]) if swap else (ct[k],ct[k+1])
        for r in range(R): eq(rv(X,u,r),rv(1,a,r)); eq(rv(Y,v,r),rv(2,b,r))
        for c in range(C): eq(cv(X,u,c),cv(2,b,c)); eq(cv(Y,v,c),cv(1,a,c))
    with Cadical153(bootstrap_with=cl) as S:
        ok=S.solve()
        if ok and want_model:
            m=set(l for l in S.get_model() if l>0)
            sq={s:['.']*N for s in (1,2)}
            for s in (1,2):
                for L in map(chr,range(65,91)):
                    for k in range(N):
                        if x(s,L,k) in m: sq[s][k]=L
            return ok,len(pairs),sq
        return ok,len(pairs),None
if __name__=="__main__":
    name,ct=sys.argv[1],sys.argv[2]
    for shape in SHAPES:
        for off in (0,1):
            for X,Y in ((2,1),(1,2),(1,1),(2,2)):
                for swap in (0,1):
                    t=time.time(); ok,np,_=solve(ct,shape,off,X,Y,swap)
                    print(name,shape,off,f"X{X}Y{Y}",swap,np,"SAT" if ok else "UNSAT",f"{time.time()-t:.2f}s",flush=True)
