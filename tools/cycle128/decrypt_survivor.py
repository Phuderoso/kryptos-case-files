"""Decrypt a seqgro survivor as far as the crib-derived cipher-alphabet fragment allows (unknown letters shown as '?')."""
import sys
AZ="ABCDEFGHIJKLMNOPQRSTUVWXYZ"; KA="KRYPTOSABCDEFGHIJLMNQUVWXZ"
CT,primer,order,model,pa,form=sys.argv[1:7]
PA=KA if pa=="KA" else AZ; beau=form=="beau"; n=len(CT)
d=[int(c) for c in primer]
while len(d)<n: d.append((d[-5]+d[-4])%10)
cols={k:[i for i in range(n) if d[i]==k] for k in range(10)}
sigma={}; pos=0
for c in map(int,order):
    for i in cols[c]: sigma[i]=pos; pos+=1
crib={21+i:ch for i,ch in enumerate("EASTNORTHEAST")}; crib.update({63+i:ch for i,ch in enumerate("BERLINCLOCK")})
L2idx={}
for i,ch in crib.items():
    j=sigma[i]; dig=d[j] if model=="B" else d[i]; a=PA.index(ch)
    L2idx[CT[j]]=(dig-a)%26 if beau else (a+dig)%26
out=[]
for i in range(n):
    j=sigma[i]; dig=d[j] if model=="B" else d[i]; L=CT[j]
    if L not in L2idx: out.append('?'); continue
    idx=L2idx[L]; a=(dig-idx)%26 if beau else (idx-dig)%26
    out.append(PA[a])
s="".join(out); print(s); print("known letters:",n-s.count('?'),"cipher letters pinned:",len(L2idx))
