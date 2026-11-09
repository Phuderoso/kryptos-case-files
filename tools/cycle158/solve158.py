"""Cycle 158: independent re-solve of hillw survivor lines (pure Python + numpy, no shared code with hillw.c).
For each S/X line: rebuild the frame, brute-force every row of D over Z26^n against the crib equations that row owns
(all, or all but the dropped block), require D invertible mod 26, decrypt the whole stream and score by mean log10 quadgram
over non-crib letters. usage: solve158.py texts_file survivor_lines..."""
import sys, itertools, numpy as np
NUMS=["ABCDEFGHIJKLMNOPQRSTUVWXYZ","KRYPTOSABCDEFGHIJLMNQUVWXZ"]; CRIB="EASTNORTHEASTBERLINCLOCK"
CP=list(range(21,34))+list(range(63,74))
CAP=100000
Q=np.fromfile("/home/box/kryptos_support_backup/quad.bin",dtype=np.float32)
B=None
def det_ok(D):
    n=len(D); M=[r[:] for r in D]
    for p in (2,13):
        A=[[x%p for x in r] for r in M]
        for c in range(n):
            s=next((i for i in range(c,n) if A[i][c]),None)
            if s is None: return False
            A[c],A[s]=A[s],A[c]; iv=pow(A[c][c],-1,p)
            for i in range(c+1,n):
                f=A[i][c]*iv%p; A[i]=[(a-f*b)%p for a,b in zip(A[i],A[c])]
    return True
def solve(text,kv):
    global B
    n=int(kv['n']); perm=int(kv['perm']); d=int(kv['dir']); ix=int(kv['ix']); nu=int(kv['nu']); o=int(kv['o']); drop=int(kv['drop'])
    N=NUMS[nu]; F=[N.index(c) for c in kv['f']]; E=[N.index(c) for c in kv['e']]; sf=int(kv['sf']); se=int(kv['se'])
    if perm<0: S=list(range(97))
    else:
        if B is None: B=np.fromfile("/home/box/kryptos_support_backup/perms97.bin",dtype=np.int16).reshape(-1,97)
        S=[int(x) for x in B[perm]]
        if d: T=[0]*97; [T.__setitem__(S[i],i) for i in range(97)]; S=T
    if ix==0: L=[N.index(text[S[i]]) for i in range(97)]; known={c:N.index(CRIB[k]) for k,c in enumerate(CP)}
    else: L=[N.index(c) for c in text]; known={S[c]:N.index(CRIB[k]) for k,c in enumerate(CP)}
    nb=(97-o)//n; V=[(L[t]+sf*F[t%len(F)])%26 for t in range(97)]
    cand=np.array(list(itertools.product(range(26),repeat=n)),dtype=np.int64)
    D=[]; nsol=1
    for r in range(n):
        ok=np.ones(len(cand),bool)
        for t,pv in known.items():
            if t<o or t>=o+nb*n or (t-o)%n!=r: continue
            bs=o+((t-o)//n)*n
            if bs==drop: continue
            v=np.array([V[bs+j] for j in range(n)]); ok&=((cand@v)%26==(pv+se*E[t%len(E)])%26)
        rows=cand[ok]; nsol*=len(rows)
        if len(rows)==0: return None
        D.append([[int(x) for x in rw] for rw in rows])
    if nsol>CAP: return ("multi",nsol)
    best=None; ninv=0
    for Dc in itertools.product(*D):
        Dc=[list(x) for x in Dc]
        if not det_ok(Dc): continue
        ninv+=1; r=decode(Dc,V,E,se,N,n,o,nb,ix,S)
        if best is None or r[1]>best[1]: best=r
    if best is None: return ("singular",nsol)
    return ("ok",best[0],best[1],best[2],best[3],nsol,ninv)
def decode(D,V,E,se,N,n,o,nb,ix,S):
    out=[None]*97
    for b in range(o,o+nb*n,n):
        for r in range(n):
            out[b+r]=N[(sum(D[r][j]*V[b+j] for j in range(n))-se*E[(b+r)%len(E)])%26]
    pt=out if ix==0 else [out[S[p]] for p in range(97)]
    s=[];
    for i in range(94):
        g=pt[i:i+4]
        if None in g or any(i+z in CP for z in range(4)): continue
        s.append(Q[sum((ord(c)-65)*26**(3-z) for z,c in enumerate(g))])
    pts="".join(c or "." for c in pt)
    wrong=sum(1 for k,c in enumerate(CP) if pt[c] is not None and pt[c]!=CRIB[k])
    return (D,float(np.mean(s)) if s else -99,wrong,pts)
if __name__=="__main__":
    texts={l.split()[0]:l.split()[-1] for l in open(sys.argv[1]) if not l.startswith('#')}
    for fn in sys.argv[2:]:
        for l in open(fn):
            if l[0] not in "SX": continue
            a=l.split(); kv=dict(x.split('=',1) for x in a[2:])
            r=solve(texts[a[1]],kv); print(a[0],a[1]," ".join(a[2:]),"->",r if r is None or r[0]!="ok" else "sols=%d invertible=%d best: D=%s meanQ=%.3f wrong_decided_cribs=%d %s"%(r[5],r[6],r[1],r[2],r[3],r[4]))
