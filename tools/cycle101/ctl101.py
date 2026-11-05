import random,struct
PT="WEDUGTHROUGHTHERUBBLE"+"EASTNORTHEAST"+"ANDFOUNDTHEDOORUNDERTHEOLDBRI"+"BERLINCLOCK"+"TOWERASTHESUNWENTDOWNXX"
AL=["ABCDEFGHIJKLMNOPQRSTUVWXYZ","KRYPTOSABCDEFGHIJLMNQUVWXZ"]
def perm(fn,n,inv):
    if fn is None: return list(range(97))
    P=open(fn,'rb').read(); s=list(struct.unpack('<97h',P[n*194:(n+1)*194]))
    if inv: q=[0]*97; [q.__setitem__(s[i],i) for i in range(97)]; s=q
    return s
def make(fn,n,inv,t,kp,m,key,seed):
    r=random.Random(seed); s=perm(fn,n,inv); ix={ch:i for i,ch in enumerate(AL[t])}; k=[ix[ch] if t else ord(ch)-65 for ch in key]; L=len(k)
    # homophone sets over index space: plain index -> list of x indices
    syms=list(range(26)); r.shuffle(syms)
    plain=sorted(set(ix[PT[i]] if m==0 else (ix[PT[i]]-k[(s[i] if kp else i)%L])%26 for i in range(97)))
    homs={p:[syms.pop()] for p in plain}
    while syms: homs[r.choice(plain)].append(syms.pop())
    C=[None]*97
    for i in range(97):
        kk=k[(s[i] if kp else i)%L]; p=ix[PT[i]]
        if m==0: C[s[i]]=AL[t][(r.choice(homs[p])+kk)%26]
        else:  C[s[i]]=AL[t][r.choice(homs[(p-kk)%26])]
    return ''.join(C)
cfg=[('d1',None,0,0,0,0,0,'ACORN',1),('d2',None,0,0,1,0,1,'LAYERED',2),('d3',None,0,0,0,0,1,'SHADOWS',3),
     ('b1','perms97.bin',4321,0,1,1,0,'XQR',4),('b2','dec_perm.bin',99,1,0,0,1,'ZEB',5)]
for c in cfg: print(c[0],c[1],c[2],c[3],c[4],c[5],c[6],c[7],make(*c[1:]))
