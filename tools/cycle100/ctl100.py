import random,struct
PT="WEDUGTHROUGHTHERUBBLE"+"EASTNORTHEAST"+"ANDFOUNDTHEDOORUNDERTHEOLDBRI"+"BERLINCLOCK"+"TOWERASTHESUNWENTDOWNXX"
assert len(PT)==97
def perm(fn,n,inv):
    P=open(fn,'rb').read(); s=list(struct.unpack('<97h',P[n*194:(n+1)*194]))
    if inv: q=[0]*97; [q.__setitem__(s[i],i) for i in range(97)]; s=q
    return s
def make(fn,n,inv,seed):
    r=random.Random(seed); s=perm(fn,n,inv); letters=sorted(set(PT)); cl=list(range(26)); r.shuffle(cl)
    homs={L:[cl.pop()] for L in letters}
    while cl: homs[r.choice('ETAONRSH')].append(cl.pop()) if r.choice('ETAONRSH') in homs else None
    C=[None]*97
    for i in range(97): C[s[i]]=chr(65+r.choice(homs[PT[i]]))
    return ''.join(C)
for tag,(fn,n,inv,seed) in {'c1':('perms97.bin',1234,0,1),'c2':('dec_perm.bin',50000,1,2),'c3':('route_perm.bin',777,0,3)}.items():
    print(tag,fn,n,inv,make(fn,n,inv,seed))
