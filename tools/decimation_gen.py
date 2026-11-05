"""Cycle 59: K3's double rotation is exactly a decimation: PT[i] = CT[(192*(i+1)-1) mod 337] (L=336, M=L+1).
Build the K4 analogue family: perm[j] = (a + s*j) mod M, M = 97..112, gcd(s,M)=1, values >= 97 are empty
cells and skipped (ragged), all start offsets a; both directions (perm and its inverse).
Writes dec_perm.bin (int16 x 97) and dec_perm.txt; reports overlap with the cycle-12 set (data/tw_perm.bin)."""
import struct, math, sys
N=97
def build():
    T={}
    for M in range(97,113):
        for s in range(1,M):
            if math.gcd(s,M)!=1: continue
            for a in range(M):
                seq=[(a+s*j)%M for j in range(M)]
                out=[v for v in seq if v<N]          # out[k] = carved index paired with PT position k
                inv=[0]*N
                for k,v in enumerate(out): inv[v]=k
                T.setdefault(tuple(out),f"dec M{M} s{s} a{a}/dec")
                T.setdefault(tuple(inv),f"dec M{M} s{s} a{a}/enc")
    return T
T=build()
c12=set()
raw=open("data/tw_perm.bin","rb").read()
for i in range(len(raw)//194): c12.add(struct.unpack_from("<97h",raw,i*194))
new={p:n for p,n in T.items() if p not in c12}
print("distinct decimation perms",len(T),"already in cycle-12 family",len(T)-len(new),"new",len(new))
with open("dec_perm.bin","wb") as f:
    for p in new: f.write(struct.pack("<97h",*p))
open("dec_perm.txt","w").write("\n".join(new.values())+"\n")
# sanity: K3 law reproduced by the same generator form at L=336, M=337, s=192, a=191
from math import gcd
