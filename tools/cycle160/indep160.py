"""Cycle 160 independent recount (shares no code with q4v.c): for a configuration (CT, perm q, dir, ix, p)
count ordered alphabet pairs (PA != CA, unique AZ-keyed vocabulary alphabets) for which a periodic
Quagmire IV key exists, by brute force over all PA x CA with numpy: key value k_t = CA^-1(c_t) -/+ PA^-1(p_t)
must equal the value of the FIRST crib of its residue class (no chain, no prefilter, no hashing).
usage: indep160.py CT q dir ix p   (q=-1 -> identity)   prints 'vig N beau N'"""
import sys, numpy as np
AZ="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
CRIB={**{21+i:c for i,c in enumerate("EASTNORTHEAST")},**{63+i:c for i,c in enumerate("BERLINCLOCK")}}
def keyed(w):
    s=[]
    for c in w+AZ:
        if c not in s: s.append(c)
    return "".join(s)
_al=None
def alph():
    global _al
    if _al is None:
        seen={}
        for w in open('vocab.txt').read().split(): seen.setdefault(keyed(w),w)
        A=list(seen)
        _al=(np.array([[a.index(ch) for ch in AZ] for a in A],dtype=np.int16),list(seen.values()))
    return _al
def count(ct,q,d,ix,p,listing=False):
    inv,names=alph(); n=len(inv)
    if q<0: S=np.arange(97)
    else:
        P=np.fromfile('/home/box/kryptos_support_backup/perms97.bin',dtype=np.int16,count=97,offset=q*97*2)
        S=np.argsort(P) if d else P
    pos=sorted(CRIB); cl=[AZ.index(ct[S[i]]) for i in pos]; pl=[AZ.index(CRIB[i]) for i in pos]
    res=[(S[i] if ix else i)%p for i in pos]
    first={}; pairs=[]
    for t,r in enumerate(res):
        if r in first: pairs.append((first[r],t))
        else: first[r]=t
    Cv=inv[:,cl].astype(np.int32); Pv=inv[:,pl].astype(np.int32)
    out={}; lst=[]
    for mode,sg in (('vig',1),('beau',-1)):
        tot=0
        dC=np.stack([Cv[:,b]-Cv[:,a] for a,b in pairs],1)%26 if pairs else np.zeros((n,0),int)
        dP=np.stack([sg*(Pv[:,b]-Pv[:,a]) for a,b in pairs],1)%26 if pairs else np.zeros((n,0),int)
        for s0 in range(0,n,256):
            eq=(dC[None,:,:]==dP[s0:s0+256,None,:]).all(2)   # [PA,CA]
            for i in range(eq.shape[0]): eq[i,s0+i]=False
            tot+=int(eq.sum())
            if listing:
                for a,b in zip(*np.nonzero(eq)): lst.append((mode,names[s0+a],names[b]))
        out[mode]=tot
    return out,lst
if __name__=="__main__":
    ct,q,d,ix,p=sys.argv[1],*map(int,sys.argv[2:6])
    o,_=count(ct,q,d,ix,p); print('vig',o['vig'],'beau',o['beau'])
