import random,struct
PT="WEDUGTHROUGHTHERUBBLE"+"EASTNORTHEAST"+"ANDFOUNDTHEDOORUNDERTHEOLDBRI"+"BERLINCLOCK"+"TOWERASTHESUNWENTDOWNXX"
AL=["ABCDEFGHIJKLMNOPQRSTUVWXYZ","KRYPTOSABCDEFGHIJLMNQUVWXZ"]
def perm(fn,n,inv=0):
    P=open(fn,'rb').read(); s=list(struct.unpack('<97h',P[n*194:(n+1)*194]))
    if inv: q=[0]*97; [q.__setitem__(s[i],i) for i in range(97)]; s=q
    return s
def enc(m,p,k): return (p+k)%26 if m==0 else (k-p)%26 if m==1 else (p-k)%26
def cribpos(i): return 21<=i<=33 or 63<=i<=73
def modelP(fn,n,inv,t,m,key):
    s=perm(fn,n,inv); ix={ch:k for k,ch in enumerate(AL[t])}; p=[ix[ch] for ch in PT]; kv=[ix[ch] for ch in key]
    return ''.join(AL[t][(enc(m,p[i],p[s[i]])+kv[i%len(kv)])%26] for i in range(97))
def modelC(fn,n,t,m,key,seed):
    s=perm(fn,n); ix={ch:k for k,ch in enumerate(AL[t])}; p=[ix[ch] for ch in PT]; kv=[ix[ch] for ch in key]; L=len(kv)
    E=lambda i,pv,cs:(enc(m,pv,cs)+kv[i%L])%26
    c=[None]*97; rnd=random.Random(seed); seen=[0]*97
    for st in range(97):
        if seen[st]: continue
        cyc=[]; i=st
        while not seen[i]: seen[i]=1; cyc.append(i); i=s[i]
        c[st]=rnd.randrange(26)
        for i in reversed(cyc[1:]): c[i]=E(i,p[i],c[s[i]])
        if E(st,p[st],c[s[st]])!=c[st]:
            if cribpos(st): return None
            for v in range(26):
                if E(st,v,c[s[st]])==c[st]: p[st]=v;break
            else: return None
    return ''.join(AL[t][x] for x in c)
out=[('P route 4321 inv0 KA Beau key=K',modelP('route_perm.bin',4321,0,1,1,'K')),
     ('P affine 700 inv1 AZ Vig key=X',modelP('affine.bin',700,1,0,0,'X')),
     ('P route 100 inv1 AZ Var key=EW',modelP('route_perm.bin',100,1,0,2,'EW'))]
for lab,fn,n,t,m,key in [('C perms97 60607 AZ Vig key=PALIMPSEST','perms97.bin',60607,0,0,'PALIMPSEST'),('C dec 7777 KA Beau key=ABSCISSA','dec_perm.bin',7777,1,1,'ABSCISSA'),('C route 2000 KA Var key=LAYER','route_perm.bin',2000,1,2,'LAYER')]:
    for seed in range(200):
        r=modelC(fn,n,t,m,key,seed)
        if r: out.append((lab,r)); break
    else: out.append((lab+' UNPLANTABLE',None))
for lab,ct in out: print(lab,ct)
