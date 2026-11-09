"""Cycle 172 independent recount (shares no code with q4d172.c): for a configuration (CT, perms file, q, ix, p)
count ordered alphabet pairs (PA != CA, from support/alpha172.txt) admitting a periodic Quagmire IV key, by brute force
with numpy over all PA x CA: per crib t the key value k_t = CA^-1(c_t) - PA^-1(p_t) (vig) or CA^-1(c_t) + PA^-1(p_t) (beau)
must equal that of the FIRST crib of its residue class. No prefilter, no hashing, no chain, no cache.
usage: recount172.py CT perms.bin q ix p   -> 'vig N beau N'"""
import sys, numpy as np
AZ="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
CRIB={**{21+i:c for i,c in enumerate("EASTNORTHEAST")},**{63+i:c for i,c in enumerate("BERLINCLOCK")}}
A=[l.split()[0] for l in open("support/alpha172.txt")]
INV=np.array([[a.index(ch) for ch in AZ] for a in A],dtype=np.int16); n=len(A)
def count(ct,pf,q,ix,p):
    S=np.fromfile(pf,dtype=np.int16,count=97,offset=q*97*2)
    pos=sorted(CRIB); cl=[AZ.index(ct[S[i]]) for i in pos]; pl=[AZ.index(CRIB[i]) for i in pos]
    res=[(int(S[i]) if ix else i)%p for i in pos]; first={}; pairs=[]
    for t,r in enumerate(res):
        if r in first: pairs.append((first[r],t))
        else: first[r]=t
    Cv=INV[:,cl].astype(np.int32); Pv=INV[:,pl].astype(np.int32); out={}
    for mode,sg in (("vig",1),("beau",-1)):
        tot=0
        # key value for PA a, CA b at crib t: Cv[b,t] - sg*Pv[a,t]; equality with first crib of class
        dC=np.stack([Cv[:,b]-Cv[:,a] for a,b in pairs],1)%26 if pairs else np.zeros((n,0),int)
        dP=np.stack([sg*(Pv[:,b]-Pv[:,a]) for a,b in pairs],1)%26 if pairs else np.zeros((n,0),int)
        for s0 in range(0,n,128):
            eq=(dC[None,:,:]==dP[s0:s0+128,None,:]).all(2)
            for i in range(eq.shape[0]): eq[i,s0+i]=False
            tot+=int(eq.sum())
        out[mode]=tot
    return out
if __name__=="__main__":
    ct,pf=sys.argv[1],sys.argv[2]; q,ix,p=map(int,sys.argv[3:6]); o=count(ct,pf,q,ix,p); print("vig",o["vig"],"beau",o["beau"])
