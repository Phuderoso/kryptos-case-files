"""Cycle 153 independent check (pure Python, shares no code with hillk1e.c).
Part A (controls): every S line of each corrupted-letter control is re-decrypted from the carved text with the printed
  D, key e, frame and repaired letter, and compared with the planted plaintext; the control passes if some S line names
  the corrupted carved position and decrypts with 0 wrong letters. ctl10 (uncorrupted) must be strict; ctl11 (wrong crib
  letter) must have an E line equal to the planted text except at the wrong-crib position.
Part B (counts, with --counts): brute-force REPAIR-AND-RESOLVE (no syndrome trick): for each non-strict configuration,
  each crib block, each carved letter j of it and each delta 1..25, rebuild all 24 crib equations on the repaired text and
  Gauss-eliminate mod 2 and mod 13; also leave-one-crib-out. Prints counts to compare with hillk1e's C lines.
usage: check.py controls.txt controls_out.txt  |  check.py --counts CT label n k perms.bin|- lo hi"""
import sys, importlib.util, os, re
import numpy as np
here=os.path.dirname(os.path.abspath(__file__))
NUMS=["ABCDEFGHIJKLMNOPQRSTUVWXYZ","KRYPTOSABCDEFGHIJLMNQUVWXZ"]
CRIB="EASTNORTHEASTBERLINCLOCK"; CPOS=list(range(21,34))+list(range(63,74))
BANK="/home/box/kryptos_support_backup/perms97.bin"
def frame(q,d,src):
    if src=="-": return list(range(97))
    B=np.memmap(BANK,dtype=np.int16,mode="r").reshape(-1,97); S=[int(x) for x in B[q]]
    if d: T=[0]*97; [T.__setitem__(S[i],i) for i in range(97)]; S=T
    return S
def decrypt(C,S,ix,nu,o,n,k,D,e):
    N=NUMS[nu]; L=[N.index(C[S[i]]) for i in range(97)] if ix==0 else [N.index(c) for c in C]
    out=[None]*97
    for b in range(o,o+((97-o)//n)*n,n):
        for r in range(n):
            t=b+r; ee=0
            if k:
                if e[t%k]<0: continue
                ee=e[t%k]
            out[t]=N[(sum(D[r][j]*L[b+j] for j in range(n))+ee)%26]
    return out if ix==0 else [out[S[p]] for p in range(97)]
def partA(ctlf,outf):
    spec=importlib.util.spec_from_file_location("p153",os.path.join(here,"plant.py")); pm=importlib.util.module_from_spec(spec); spec.loader.exec_module(pm)
    P=pm.m.m.plain(); outs=open(outf).read().splitlines(); ok=0; tot=0
    for line in open(ctlf):
        f=line.split()
        if not f[0].startswith("ctl"): continue
        nm,n,k,src,q,d,ix,nu,o,cpos,wpos,C=f[0],int(f[1]),int(f[2]),f[3],int(f[4]),int(f[5]),int(f[6]),int(f[7]),int(f[8]),int(f[9]),int(f[10]),f[11]
        tot+=1; S=frame(q,d,src); mine=[l for l in outs if l.split()[1:2]==[nm]]
        if cpos>=0:
            good=None; nS=0
            for l in mine:
                if not l.startswith("S "): continue
                nS+=1; mm=re.search(r"perm=(\d+) dir=(\d) ix=(\d) num=(\d) o=(\d) dropblk=\d+ fix@carved(\d+):(\w)->(\w) D=(\S+)\s+e=(\S+)",l)
                qq,dd,ixx,nuu,oo,cp,_,new=int(mm[1]),int(mm[2]),int(mm[3]),int(mm[4]),int(mm[5]),int(mm[6]),mm[7],mm[8]
                Dv=[int(x) for x in mm[9].split(",")]; D=[Dv[r*n:(r+1)*n] for r in range(n)]; e=[int(x) for x in mm[10].split(",")] if k else []
                CC=list(C); CC[cp]=new; out=decrypt("".join(CC),frame(qq,dd,src),ixx,nuu,oo,n,k,D,e)
                wrong=sum(1 for i in range(97) if out[i] is not None and out[i]!=P[i]); dec=sum(1 for x in out if x is not None)
                if cp==cpos and wrong==0: good=(cp,new,dec)
            print(f"{nm} n={n} k={k} corrupted_carved={cpos} S_lines={nS} recovered={'YES' if good else 'NO'}"+(f" fix@{good[0]}->{good[1]} decided={good[2]}/97 wrong=0" if good else ""))
            ok+=bool(good)
        elif wpos>=0:
            El=[l for l in mine if l.startswith("E ") and len(l.split()[-1])==97]; res="NO"
            for l in El:
                pt=l.split()[-1]; diff=[i for i in range(97) if pt[i]!="." and pt[i]!=P[i]]
                if diff==[wpos] or diff==[]: res=f"YES (differs from crib text only at {diff})"
            print(f"{nm} n={n} k={k} wrong_crib_pt={wpos} recovered={res}"); ok+=res.startswith("YES")
        else:
            c=[l for l in mine if l.startswith("C ")][0]; st=int(re.search(r"strict=(\d+)",c)[1])
            print(f"{nm} n={n} k={k} uncorrupted strict={st} recovered={'YES' if st>=1 else 'NO'}"); ok+=st>=1
    print(f"controls recovered {ok}/{tot}")
def consistent(rows,U):
    for p in (2,13):
        M=[[x%p for x in r] for r in rows]; r0=0
        for c in range(U):
            s=next((i for i in range(r0,len(M)) if M[i][c]),None)
            if s is None: continue
            M[r0],M[s]=M[s],M[r0]; iv=pow(M[r0][c],-1,p); M[r0]=[x*iv%p for x in M[r0]]
            for i in range(len(M)):
                if i!=r0 and M[i][c]: f=M[i][c]; M[i]=[(x-f*y)%p for x,y in zip(M[i],M[r0])]
            r0+=1
        if any(M[i][U] for i in range(r0,len(M))): return False
    return True
def partB(CT,lab,n,k,bank,lo,hi):
    tests=strict=eqc=rc=rcc=bd=0
    ents=[(0,0,list(range(97)))] if bank=="-" else [(q,d,frame(q,d,"P")) for q in range(lo,hi) for d in (0,1)]
    for q,d,S in ents:
        for ix in ((0,) if bank=="-" else (0,1)):
            for nu in (0,1):
                N=NUMS[nu]
                if ix==0: L=[N.index(CT[S[i]]) for i in range(97)]; kp={CPOS[z]:N.index(CRIB[z]) for z in range(24)}
                else: L=[N.index(c) for c in CT]; kp={S[CPOS[z]]:N.index(CRIB[z]) for z in range(24)}
                for o in range(n):
                    tests+=1; nb=(97-o)//n; ts=sorted(t for t in kp if o<=t<o+nb*n)
                    res=sorted({t%k for t in ts}) if k else []; col={s:i for i,s in enumerate(res)}; U=n*n+len(res)
                    def eqs(LL,skip=()):
                        R=[]
                        for t in ts:
                            if t in skip: continue
                            bs=o+((t-o)//n)*n; r=(t-o)%n; row=[0]*(U+1)
                            for j in range(n): row[r*n+j]=LL[bs+j]
                            if k: row[n*n+col[t%k]]=1
                            row[U]=kp[t]; R.append(row)
                        return R
                    if consistent(eqs(L),U): strict+=1; continue
                    if any(consistent(eqs(L,(t,)),U) for t in ts): eqc+=1
                    blocks=sorted({(t-o)//n for t in ts}); anyr=False
                    for blk in blocks:
                        bs=o+blk*n
                        if consistent(eqs(L,tuple(t for t in ts if (t-o)//n==blk)),U): bd+=1
                        for j in range(n):
                            for dl in range(1,26):
                                LL=list(L); LL[bs+j]=(L[bs+j]+dl)%26
                                if consistent(eqs(LL),U): rc+=1; anyr=True
                    rcc+=anyr
    print(f"PY {lab} n={n} k={k} tests={tests} strict={strict} eqdrop_cfg={eqc} blockpairs={bd} repair_cons={rc} repair_cons_cfg={rcc}")
if __name__=="__main__":
    if sys.argv[1]=="--counts":
        a=sys.argv; partB(a[2],a[3],int(a[4]),int(a[5]),a[6],int(a[7]),int(a[8]))
    else: partA(sys.argv[1],sys.argv[2])
