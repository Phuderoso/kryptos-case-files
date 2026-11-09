"""Cycle 156 independent check (pure Python, no shared code with hill2s.c).
Part A: re-decrypt every planted control from the planted keys (plant.py stderr) and from the keys hill2s printed, count wrong letters.
Part B: recount per-field solution counts for direct texts with a different algorithm: enumerate every f on the crib-touched
key residues and solve (D, e) jointly by Gaussian elimination, counting solutions with D invertible (hill2s uses row-by-row D
enumeration for n=2 in both fields and for every n mod 2).  Compared with the V lines of the direct runs.
usage: python3 check.py controls.txt controls_keys.txt controls_run.txt out_dir"""
import sys, re, itertools, glob
NUMS=["ABCDEFGHIJKLMNOPQRSTUVWXYZ","KRYPTOSABCDEFGHIJLMNQUVWXZ"]
CR={**{21+i:c for i,c in enumerate("EASTNORTHEAST")},**{63+i:c for i,c in enumerate("BERLINCLOCK")}}
PLAIN="THESHADOWFELLACROSSTHEASTNORTHEASTWEWALKEDTOWARDTHEOLDTOWERANDTBERLINCLOCKSTRUCKTHEHOURINSILENCEX"
def dec(C,n,k1,k2,o,nu,D,e,f):
    N=NUMS[nu]; L=[N.index(c) for c in C]; out=[None]*97
    for b in range(o,97-n+1,n):
        for r in range(n): out[b+r]=N[(sum(D[r*n+j]*(L[b+j]-f[(b+j)%k2]) for j in range(n))+e[(b+r)%k1])%26]
    return out
def solve(p,A,b):
    """rank-nullity over Z_p: returns None if inconsistent, else (particular, basis)"""
    A=[row[:]+[bb] for row,bb in zip(A,b)]; u=len(A[0])-1 if A else 0; piv=[]; r=0
    for c in range(u):
        s=next((i for i in range(r,len(A)) if A[i][c]%p),None)
        if s is None: continue
        A[r],A[s]=A[s],A[r]; iv=pow(A[r][c],-1,p); A[r]=[x*iv%p for x in A[r]]
        for i in range(len(A)):
            if i!=r and A[i][c]%p: fct=A[i][c]; A[i]=[(x-fct*y)%p for x,y in zip(A[i],A[r])]
        piv.append(c); r+=1
    if any(A[i][u]%p for i in range(r,len(A))): return None
    part=[0]*u
    for i,c in enumerate(piv): part[c]=A[i][u]
    basis=[]
    for fr in [c for c in range(u) if c not in piv]:
        v=[0]*u; v[fr]=1
        for i,c in enumerate(piv): v[c]=(-A[i][fr])%p
        basis.append(v)
    return part,basis
def det(p,M,n):
    M=[row[:] for row in M]; d=1
    for c in range(n):
        s=next((i for i in range(c,n) if M[i][c]%p),None)
        if s is None: return 0
        M[c],M[s]=M[s],M[c]; iv=pow(M[c][c],-1,p)
        for i in range(c+1,n):
            fct=M[i][c]*iv%p; M[i]=[(x-fct*y)%p for x,y in zip(M[i],M[c])]
    return 1
def count(C,n,k1,k2,o,nu,p):
    N=NUMS[nu]; L=[N.index(c) for c in C]; nb=(97-o)//n
    eqs=[(t,(t-o)%n,o+((t-o)//n)*n,N.index(CR[t])) for t in sorted(CR) if o<=t<o+nb*n]
    Rf=sorted({(bs+j)%k2 for _,_,bs,_ in eqs for j in range(n)}); Re=sorted({t%k1 for t,_,_,_ in eqs})
    tot=0
    for fv in itertools.product(range(p),repeat=len(Rf)):
        f=dict(zip(Rf,fv)); A=[]; b=[]
        for t,r,bs,pv in eqs:
            row=[0]*(n*n+len(Re))
            for j in range(n): row[r*n+j]=(L[bs+j]-f[(bs+j)%k2])%p
            row[n*n+Re.index(t%k1)]=1; A.append(row); b.append(pv%p)
        s=solve(p,A,b)
        if s is None: continue
        part,basis=s
        for co in itertools.product(range(p),repeat=len(basis)):
            x=[(part[i]+sum(c*v[i] for c,v in zip(co,basis)))%p for i in range(len(part))]
            if det(p,[x[r*n:(r+1)*n] for r in range(n)],n): tot+=1
    return tot
if __name__=="__main__":
    ctl={l.split()[0]:l.split() for l in open(sys.argv[1])}
    keys={}
    for l in open(sys.argv[2]):
        w=l.split(); keys[w[1]]={k:list(map(int,v.split(","))) for k,v in (x.split("=") for x in w[2:])}
    print("Part A: planted keys and printed keys -> wrong letters vs control plaintext (decided letters only)")
    for l in open(sys.argv[3]):
        if not l[:1] in "SX": continue
        w=l.split(); nm=w[1]; c=ctl[nm]; n,k1,k2=int(c[1]),int(c[2]),int(c[3]); nu,o=int(w[8][4:]),int(w[9][2:])
        g=dict(x.split("=",1) for x in w[2:] if "=" in x); D=list(map(int,g["D"].split(","))); e=list(map(int,g["e"].split(","))); f=list(map(int,g["f"].split(",")))
        pt=w[-1]; wrong=sum(1 for i,ch in enumerate(pt) if ch!="." and ch!=PLAIN[i]); dcd=sum(ch!="." for ch in pt)
        line=f"  {nm} {w[0]} drop={g['drop']} decided={dcd} wrong_vs_plain={wrong}"
        if c[4]=="-":
            K=keys[nm]; out=dec(c[12],n,k1,k2,o,nu,K["D"],K["e'"],K["f"]); out2=dec(c[12],n,k1,k2,o,nu,D,e,f)
            line+=f" planted-key redecrypt wrong={sum(1 for i,ch in enumerate(out) if ch and ch!=PLAIN[i])} printed-key redecrypt matches={''.join(x or '.' for x in out2)==pt}"
        print(line)
    print("Part B: per-field counts, f-enumeration (Python) vs hill2s V lines")
    same=tot=nz=0
    for fn in sorted(glob.glob(sys.argv[4]+"/*_D_s0.txt")):
        for l in open(fn):
            if not l.startswith("V "): continue
            w=l.split(); lab=w[1][1:]; n,k1,k2,nu,o=(int(x.split("=")[1]) for x in w[2:7]); c2=w[7].split("=")[1]; c13=w[8].split("=")[1]
            C=open("/tmp/kcf/data/k4.txt").read().strip() if lab=="K4" else ctl[lab][12]
            for p,cv in ((2,c2),(13,c13)):
                if "+" in cv or cv=="-": continue
                if p==2 and k2>8: continue
                if p==13 and (n!=2 or k2>3): continue
                py=count(C,n,k1,k2,o,nu,p); tot+=1; same+=py==int(cv); nz+=py>0
                if py!=int(cv): print("  MISMATCH",lab,n,k1,k2,nu,o,p,cv,py)
    print(f"  {same}/{tot} identical ({nz} non-zero)")
