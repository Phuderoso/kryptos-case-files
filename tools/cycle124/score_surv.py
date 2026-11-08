"""Decrypt cycle-124 survivors (known key residues only; '?' elsewhere) and score with quadgrams.
usage: score_surv.py survivors.out controls.txt k4.txt qg.bin"""
import sys,numpy as np
sys.path.insert(0,__file__.rsplit('/',1)[0])
KA="KRYPTOSABCDEFGHIJLMNQUVWXZ"; AZ="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
CRP=list(range(21,34))+list(range(63,74)); CRS="EASTNORTHEASTBERLINCLOCK"
texts={l.split()[0]:l.split()[1] for l in open(sys.argv[2])}; texts['K4']=open(sys.argv[3]).read().strip()
qg=np.fromfile(sys.argv[4],dtype=np.float32)
def sigma(w,mode,pi,n=97):
    hs,rem=n//w,n%w; col_at=[0]*w
    for c in range(w): col_at[pi[c]]=c
    L=[hs+(c<rem) for c in range(w)]; off=[0]*w; o=0
    for k in range(w): off[k]=o; o+=L[col_at[k]]
    def place(c,r):
        if mode==1: return off[pi[c]]+r
        if r<hs: return r*w+pi[c]
        return w*hs+sum(1 for d in range(rem) if pi[d]<pi[c])
    return [place(i%w,i//w) for i in range(n)]
res=[]
for line in open(sys.argv[1]):
    f=line.split()
    if f[0]!='S': continue
    lab=f[1]; w,mode,dr,al,be,model,p=map(int,f[2:9]); pi=list(map(int,f[9:]))
    C=texts[lab]; A=KA if al else AZ; sg=sigma(w,mode,pi)
    if dr: inv=[0]*97; [inv.__setitem__(sg[i],i) for i in range(97)]; S=inv
    else: S=sg
    key={}
    for t,i in enumerate(CRP):
        j=S[i]; a=A.index(C[j]); b=A.index(CRS[t]); key[(j if model else i)%p]=(a+b)%26 if be else (a-b)%26
    P=[]
    for i in range(97):
        j=S[i]; r=(j if model else i)%p
        if r in key:
            a=A.index(C[j]); P.append(A[(key[r]-a)%26] if be else A[(a-key[r])%26])
        else: P.append('?')
    P="".join(P); q=[]
    for i in range(94):
        s=P[i:i+4]
        if '?' not in s: q.append(qg[((ord(s[0])-65)*26+ord(s[1])-65)*26*26+(ord(s[2])-65)*26+ord(s[3])-65])
    sc=float(np.mean(q)) if q else -9; res.append((sc,lab,P.count('?'),line.strip()[:60],P))
res.sort(reverse=True)
for lab in sorted({r[1] for r in res}):
    rr=[r for r in res if r[1]==lab]; print(lab,"n",len(rr),"distinct plaintexts",len({r[4] for r in rr}),"best",round(rr[0][0],3))
    for r in rr[:3]: print("  ",round(r[0],3),r[2],r[4])
