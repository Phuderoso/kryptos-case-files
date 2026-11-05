"""Cycle 108 planted feedback-key controls (model A: key stream on the plaintext order, then transposition) + shuffled nulls."""
import numpy as np, random, subprocess
P=np.fromfile('perms97.bin',dtype=np.int16).reshape(-1,97)
KA="KRYPTOSABCDEFGHIJLMNQUVWXZ"; AZ="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
PT=("WEDUGTHROUGHTHERUBBLEX"[:21]+"EASTNORTHEAST"+"ANDFOUNDTHEDOORUNDERTHEOLDBRIDGE"[:29]+"BERLINCLOCK"+"TOWERASTHESUNWENTDOWNXX")
def enc(perm,mode,L,a,b,e,d,r):
    al=KA if mode>>1 else AZ; beau=mode&1; t=P[perm]
    p=[al.index(ch) for ch in PT]; k=[0]*97; x=[0]*97
    for j in range(97):
        k[j]= r.randrange(26) if j<L else (a*k[j-1]+b*p[j-L]+e*x[j-L]+d)%26
        x[j]= (k[j]-p[j])%26 if beau else (p[j]+k[j])%26
    out=[None]*97
    for j in range(97): out[int(t[j])]=al[x[j]]
    return ''.join(out)
r=random.Random(108)
cases=[(0,0,1,1,1,0,3),(0,3,1,1,0,1,0),(77777,2,2,5,3,7,11),(123456,1,3,0,1,0,4),(4242,2,1,1,1,0,0),(150000,3,2,3,0,2,9)]
res=[]
for perm,mode,L,a,b,e,d in cases:
    ct=enc(perm,mode,L,a,b,e,d,r); P[perm].astype(np.int16).tofile('one.bin')
    one=subprocess.run(['./fbkey',ct,'one.bin','1'],capture_output=True,text=True).stdout.strip().split('\n')
    full=subprocess.run(['./fbkey',ct,'perms97.bin',str(len(P))],capture_output=True,text=True).stdout.strip().split('\n')
    hit=[l for l in full if l.startswith('FULL') and f'perm={perm} ' in l]
    print(f'ctl perm={perm} mode={mode} L={L} (a,b,e,d)=({a},{b},{e},{d}) | true-perm: {one[-1]} | full search: {full[-1]} | true found: {bool(hit)}')
    open(f'ctl_{perm}_{mode}_{L}.txt','w').write(ct+'\n')
