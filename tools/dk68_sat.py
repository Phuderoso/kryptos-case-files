# Cycle 68: Doppelkasten (double two-square, the WWII German "Doppelkastenschluessel"): the SAME two arbitrary
# squares applied twice to the same digraph positions. Exact SAT on the 11 crib pairs, intermediate letters free.
# Geometry and pairing conventions are cycle 67's (ts67_sat.py): pair (a,b): a in S1 at (r1,c1), b in S2 at (r2,c2);
# outputs u = X[r1][c2], v = Y[r2][c1]; emitted (u,v) or (v,u) (swap). Intermediates must be letters (6x6 digit cells
# not allowed as intermediates; documented assumption).
import sys, time
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
from ts67_sat import K4, CRIB, SHAPES
LET=[chr(65+i) for i in range(26)]
def solve(ct,shape,off,X,Y,swap,want_model=False):
    R,C=SHAPES[shape]; N=R*C; pool=IDPool(); cl=[]
    x=lambda s,L,k: pool.id(('x',s,L,k))
    rv=lambda s,L,r: pool.id(('r',s,L,r)); cv=lambda s,L,c: pool.id(('c',s,L,c))
    for s in (1,2):
        for L in LET:
            cl+=CardEnc.equals([x(s,L,k) for k in range(N)],1,vpool=pool,encoding=EncType.seqcounter).clauses
            for r in range(R):
                cells=[x(s,L,r*C+c) for c in range(C)]
                cl.append([-rv(s,L,r)]+cells); cl+=[[-e,rv(s,L,r)] for e in cells]
            for c in range(C):
                cells=[x(s,L,r*C+c) for r in range(R)]
                cl.append([-cv(s,L,c)]+cells); cl+=[[-e,cv(s,L,c)] for e in cells]
        for k in range(N):
            cl+=CardEnc.atmost([x(s,L,k) for L in LET],1,vpool=pool,encoding=EncType.seqcounter).clauses
    pairs=[k for k in range(off,96,2) if k in CRIB and k+1 in CRIB]
    # generic "letter variable": either a fixed letter or a one-hot vector t[L]
    def onehot(tag):
        t=[pool.id((tag,L)) for L in LET]
        cl.extend(CardEnc.equals(t,1,vpool=pool,encoding=EncType.seqcounter).clauses); return t
    def rowvar(s,ltr,r):  # ltr is ('fix',L) or ('var',t,tag)
        if ltr[0]=='fix': return rv(s,ltr[1],r)
        t,tag=ltr[1],ltr[2]; v=pool.id(('R',tag,s,r))
        for i,L in enumerate(LET): cl.append([-t[i],-v,rv(s,L,r)]); cl.append([-t[i],v,-rv(s,L,r)])
        return v
    def colvar(s,ltr,c):
        if ltr[0]=='fix': return cv(s,ltr[1],c)
        t,tag=ltr[1],ltr[2]; v=pool.id(('C',tag,s,c))
        for i,L in enumerate(LET): cl.append([-t[i],-v,cv(s,L,c)]); cl.append([-t[i],v,-cv(s,L,c)])
        return v
    def eq(a,b): cl.append([-a,b]); cl.append([a,-b])
    def link(a,b,u,v):  # one two-square step (a,b)->(u,v) with u in X, v in Y
        for r in range(R): eq(rowvar(X,u,r),rowvar(1,a,r)); eq(rowvar(Y,v,r),rowvar(2,b,r))
        for c in range(C): eq(colvar(X,u,c),colvar(2,b,c)); eq(colvar(Y,v,c),colvar(1,a,c))
    for k in pairs:
        a,b=('fix',CRIB[k]),('fix',CRIB[k+1])
        cu,cv_=(ct[k+1],ct[k]) if swap else (ct[k],ct[k+1])
        t1=onehot(('m1',k)); t2=onehot(('m2',k))
        m1=('var',t1,('m1',k)); m2=('var',t2,('m2',k))
        # pass 1: (a,b)->(m1,m2) in emitted order; with swap the emitted pair is (m2,m1) and feeds pass 2 as such
        if swap: link(a,b,m2,m1); link(m1,m2,('fix',cu),('fix',cv_))
        else:    link(a,b,m1,m2); link(m1,m2,('fix',cu),('fix',cv_))
    with Cadical153(bootstrap_with=cl) as S:
        ok=S.solve()
        sq=None
        if ok and want_model:
            m=set(l for l in S.get_model() if l>0); sq={}
            for s in (1,2):
                g=['.']*N
                for L in LET:
                    for k in range(N):
                        if x(s,L,k) in m: g[k]=L
                sq[s]=''.join(g)
        return ok,len(pairs),sq
CONFIGS=[(sh,off,X,Y,sw) for sh in SHAPES for off in (0,1) for X,Y in ((2,1),(1,2),(1,1),(2,2)) for sw in (0,1)]
if __name__=="__main__":
    name,ct=sys.argv[1],sys.argv[2]
    for cfg in CONFIGS:
        t=time.time(); ok,np_,_=solve(ct,*cfg)
        print(name,*cfg,np_,"SAT" if ok else "UNSAT",f"{time.time()-t:.2f}s",flush=True)
