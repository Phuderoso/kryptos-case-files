"""Cycle 154 independent check (pure Python, shares no code with hillcs.c).
Part A (controls): every S/X line of each control is re-decrypted from the carved text with the printed D, f and frame
  (p = D.(L - f)) and compared with the planted English plaintext. Pass = some line decrypts every decided letter
  correctly (for X lines: outside the dropped block). ctl7/ctl8 (one corrupted carved letter / one wrong crib letter)
  must FAIL the strict run and be recovered by DROP=1.
Part B (--counts): for direct texts, counts the per-field solution sets {(D invertible, f on crib-touched residues)} by
  brute force over ALL invertible D in the field and Gaussian elimination for f (a different algorithm from the C code's
  f/D/row-enumeration choice) and compares with hillcs VERB lines.
usage: check.py controls.txt controls_out.txt | check.py --counts verb_out.txt CT label n k fields"""
import sys, os, re, itertools, importlib.util
import numpy as np
NUMS=["ABCDEFGHIJKLMNOPQRSTUVWXYZ","KRYPTOSABCDEFGHIJLMNQUVWXZ"]
CRIB="EASTNORTHEASTBERLINCLOCK"; CPOS=list(range(21,34))+list(range(63,74))
BANK="/home/box/kryptos_support_backup/perms97.bin"
here=os.path.dirname(os.path.abspath(__file__))
def frame(q,d,src):
    if src=="-": return list(range(97))
    B=np.memmap(BANK,dtype=np.int16,mode="r").reshape(-1,97); S=[int(x) for x in B[q]]
    if d: T=[0]*97; [T.__setitem__(S[i],i) for i in range(97)]; S=T
    return S
def decrypt(C,S,ix,nu,o,n,k,D,f):
    N=NUMS[nu]; L=[N.index(C[S[i]]) for i in range(97)] if ix==0 else [N.index(c) for c in C]
    out=[None]*97
    for b in range(o,o+((97-o)//n)*n,n):
        if any(f[(b+j)%k]<0 for j in range(n)): continue
        for r in range(n): out[b+r]=N[sum(D[r*n+j]*(L[b+j]-f[(b+j)%k]) for j in range(n))%26]
    return out if ix==0 else [out[S[p]] for p in range(97)], out
def partA(ctlf,outf):
    spec=importlib.util.spec_from_file_location("p154",os.path.join(here,"plant.py")); pm=importlib.util.module_from_spec(spec); spec.loader.exec_module(pm)
    P=pm.m.m.plain(); outs=open(outf).read().splitlines(); ok=tot=0
    for line in open(ctlf):
        f=line.split()
        if not f[0].startswith("ctl"): continue
        nm,n,k,src,q,d,ix,nu,o,cp,wp,C=f[0],int(f[1]),int(f[2]),f[3],int(f[4]),int(f[5]),int(f[6]),int(f[7]),int(f[8]),int(f[9]),int(f[10]),f[11]
        tot+=1; S=frame(q,d,src); Pw=list(P)
        mine=[l for l in outs if l.split()[1:2]==[nm] and l[0] in "SX"]
        strict=[l for l in mine if l[0]=="S"]; best=None
        for l in mine:
            g=dict(x.split("=",1) for x in l.split()[2:-1] if "=" in x)
            if int(g["perm"])!=q or int(g["dir"])!=d or int(g["ix"])!=ix or int(g["num"])!=nu or int(g["o"])!=o: continue
            D=[int(x) for x in g["D"].split(",")]; fk=[int(x) for x in g["f"].split(",")]; drop=int(g["drop"])
            pt,out=decrypt(C,S,ix,nu,o,n,k,D,fk)
            skip=set()
            if drop>=0:
                blkpos=set(range(drop,drop+n)); skip={p for p in range(97) if (S[p] if ix==1 else p) in blkpos}
            dec=[p for p in range(97) if pt[p] is not None and p not in skip]
            # wrong-crib control: plaintext at wp was altered at planting -> compare against the altered text
            ref=list(P)
            wrong=sum(1 for p in dec if pt[p]!=ref[p] and p!=wp)
            cand=(wrong,-len(dec),l[0],drop)
            if best is None or cand<best: best=cand
        err=(cp>=0 or wp>=0)
        good=bool(best is not None and best[0]==0 and -best[1]>=60 and ((not err and strict) or (err and not strict and best[2]=="X")))
        ok+=good
        print(f"{nm} n={n} k={k} {'error-control' if err else 'clean'} strict_lines={len(strict)} best_wrong={best[0] if best else '-'} decided={-best[1] if best else '-'} via={best[2] if best else '-'} drop={best[3] if best else '-'} -> {'PASS' if good else 'FAIL'}")
    print(f"controls passed {ok}/{tot}")
def gauss(p,A,b):
    """returns number of solutions (p^dim) or 0"""
    A=[r[:]+[v] for r,v in zip(A,b)]; u=len(A[0])-1 if A else 0; r=0
    for c in range(u):
        s=next((i for i in range(r,len(A)) if A[i][c]%p),None)
        if s is None: continue
        A[r],A[s]=A[s],A[r]; iv=pow(A[r][c],-1,p); A[r]=[x*iv%p for x in A[r]]
        for i in range(len(A)):
            if i!=r and A[i][c]%p: t=A[i][c]; A[i]=[(x-t*y)%p for x,y in zip(A[i],A[r])]
        r+=1
    if any(A[i][u]%p for i in range(r,len(A))): return 0
    return p**(u-r)
def det_nz(p,D,n):
    M=[[D[i*n+j]%p for j in range(n)] for i in range(n)]
    for c in range(n):
        s=next((i for i in range(c,n) if M[i][c]),None)
        if s is None: return False
        M[c],M[s]=M[s],M[c]; iv=pow(M[c][c],-1,p)
        for i in range(c+1,n):
            t=M[i][c]*iv%p; M[i]=[(x-t*y)%p for x,y in zip(M[i],M[c])]
    return True
def counts(CT,n,k,p):
    res={}
    for nu in (0,1):
        N=NUMS[nu]; L=[N.index(c) for c in CT]
        for o in range(n):
            nb=(97-o)//n; eqs=[(t,(t-o)%n,o+((t-o)//n)*n,N.index(CRIB[i])) for i,t in enumerate(CPOS) if o<=t<o+nb*n]
            R=sorted({(bs+j)%k for _,_,bs,_ in eqs for j in range(n)}); col={s:i for i,s in enumerate(R)}
            tot=0
            for D in itertools.product(range(p),repeat=n*n):
                if not det_nz(p,D,n): continue
                A=[];b=[]
                for t,r,bs,pv in eqs:
                    row=[0]*len(R)
                    for j in range(n): row[col[(bs+j)%k]]+=D[r*n+j]
                    A.append([x%p for x in row]); b.append((sum(D[r*n+j]*L[bs+j] for j in range(n))-pv)%p)
                tot+=gauss(p,A,b)
            res[(nu,o)]=tot
    return res
def partB(verbf,CT,lab,n,k,fields):
    V={}
    for l in open(verbf):
        if not l.startswith("V "): continue
        g=dict(x.split("=") for x in l.split()[2:])
        if g["n"]==str(n) and g["k"]==str(k) and l.split()[1]==lab: V[(int(g["nu"]),int(g["o"]))]=(g["n2"],g["n13"])
    out=[]; agree=True
    for p in fields:
        c=counts(CT,n,k,p)
        for key,v in sorted(c.items()):
            cv=V.get(key,("?","?"))[0 if p==2 else 1]
            same=(cv==str(v)) or (cv.endswith("+") and v>=int(cv[:-1]))
            agree&=same; out.append(f"{lab} n={n} k={k} p={p} nu={key[0]} o={key[1]} python={v} C={cv} {'same' if same else 'DIFF'}")
    print("\n".join(out)); print(f"{lab} n={n} k={k} fields={fields} {'AGREE' if agree else 'DISAGREE'}")
if __name__=="__main__":
    if sys.argv[1]=="--counts": partB(sys.argv[2],sys.argv[3],sys.argv[4],int(sys.argv[5]),int(sys.argv[6]),[int(x) for x in sys.argv[7].split(",")])
    else: partA(sys.argv[1],sys.argv[2])
