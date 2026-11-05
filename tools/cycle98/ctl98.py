import random,struct,sys
PT="WEDUGTHROUGHTHERUBBLE"+"EASTNORTHEAST"+"ANDFOUNDTHEDOORUNDERTHEOLDBRI"+"BERLINCLOCK"+"TOWERASTHESUNWENTDOWNXX"
assert len(PT)==97
AL=["ABCDEFGHIJKLMNOPQRSTUVWXYZ","KRYPTOSABCDEFGHIJLMNQUVWXZ"]
def perm(fn,n): P=open(fn,'rb').read(); return list(struct.unpack('<97h',P[n*194:(n+1)*194]))
def enc(m,p,k): return (p+k)%26 if m==0 else (k-p)%26 if m==1 else (p-k)%26
def modelP(fn,n,inv,t,m):
    s=perm(fn,n)
    if inv: q=[0]*97; [q.__setitem__(s[i],i) for i in range(97)]; s=q
    ix={ch:k for k,ch in enumerate(AL[t])}; p=[ix[ch] for ch in PT]
    return ''.join(AL[t][enc(m,p[i],p[s[i]])] for i in range(97))
def modelC(fn,n,t,m,seed):
    # C_i = enc(P_i, C_s(i)); walk each cycle from a seed, then fix closure by altering a non-crib plaintext letter
    s=perm(fn,n); ix={ch:k for k,ch in enumerate(AL[t])}; p=[ix[ch] for ch in PT]; c=[None]*97; rnd=random.Random(seed)
    seen=[0]*97
    for st in range(97):
        if seen[st]: continue
        cyc=[]; i=st
        while not seen[i]: seen[i]=1; cyc.append(i); i=s[i]
        # order so that c[s(i)] computed before c[i]: walk backwards along cycle
        last=cyc[-1]  # s(last)=st
        c[st]=rnd.randrange(26)
        for i in reversed(cyc[1:]): c[i]=enc(m,p[i],c[s[i]])
        # closure at st: need c[st]==enc(m,p[st],c[s[st]]); adjust p at a non-crib node? simpler: adjust p[st] if non-crib
        need=c[st]
        cand=[i for i in cyc if not(21<=i<=33 or 63<=i<=73)]
        if enc(m,p[st],c[s[st]])!=need:
            if not(21<=st<=33 or 63<=st<=73):
                for v in range(26):
                    if enc(m,v,c[s[st]])==need: p[st]=v;break
            else: return None
    return ''.join(AL[t][x] for x in c)
out=[]
out.append(('P perms97 n=100000 inv0 KA Beau',modelP('perms97.bin',100000,0,1,1)))
out.append(('P dec n=12345 inv1 AZ Vig',modelP('dec_perm.bin',12345,1,0,0)))
out.append(('P route n=4321 inv0 KA Var',modelP('route_perm.bin',4321,0,1,2)))
out.append(('P affine n=500 inv0 AZ Beau',modelP('affine.bin',500,0,0,1)))
for fn,n,t,m in [('perms97.bin',77777,0,0),('route_perm.bin',999,1,1),('dec_perm.bin',54321,1,2),('affine.bin',3000,0,0)]:
    for seed in range(50):
        r=modelC(fn,n,t,m,seed)
        if r: out.append((f'C {fn} n={n} AZKA={t} m={m}',r)); break
    else: out.append((f'C {fn} n={n} t={t} m={m} UNPLANTABLE (crib start)',None))
for lab,ct in out: print(lab,ct)
