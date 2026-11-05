# Cycle 58 inputs: shuffled nulls and planted Portax controls (direct and behind a cycle-12 transposition).
import random, struct
K4=open('/workspace/kcl/data/k4.txt').read().strip()
al=open('/workspace/kcl/data/alpha.bin','rb').read()
A=lambda i:''.join(chr(65+b) for b in al[i*26:i*26+26])
P=open('/workspace/kcl/data/c12_perm.bin','rb').read()
perm=lambda t:list(struct.unpack('97h',P[t*194:(t+1)*194]))
pt=("SLOWLYTHEREMAINSOFPASSAGEDEBRISEASTNORTHEASTWEREREMOVEDWITHTREMBLINGHANDSANDIMADEATINYBERLINCLOCK"
    "BREACHINTHEUPPERLEFTHANDCORNER")
pt=list(pt[:97]); pt[21:34]="EASTNORTHEAST"; pt[63:74]="BERLINCLOCK"; PT="".join(pt)
def ptx(a,b,k):
    if a<13: r1,c1=0,a
    else: r1,c1=1,(a-13-k)%13
    c2,r2=b>>1,b&1
    up=lambda r,c: c if r==0 else 13+(c+k)%13
    return (up(r1,c2),2*c1+r2) if c1!=c2 else (up(1-r1,c1),2*c1+1-r2)
def portax(s,a,key):  # key: list of shifts 0..12, involution
    ix={c:i for i,c in enumerate(a)}; v=[ix[c] for c in s]; o=v[:]; p=len(key)
    for j in range(p):
        t=j
        while t+p<97:
            o[t],o[t+p]=ptx(v[t],v[t+p],key[j]); t+=2*p
    return ''.join(a[x] for x in o)
kw=lambda w:[(ord(c)-65)//2 for c in w]
texts={'K4':K4}
rnd=random.Random(58)
for s in range(5):
    l=list(K4); rnd.shuffle(l); texts[f'NULL{s}']=''.join(l)
texts['CTL1']=portax(PT,A(0),kw('SHADOW'))
texts['CTL2']=portax(PT,A(1),kw('UNDERGRUUND'))
# behind transposition, ord 0: X[pp[i]]=PT[i], CT=portax(X)
pp=perm(5000); assert min(pp)>=0
X=['?']*97
for i in range(97): X[pp[i]]=PT[i]
texts['CTL3']=portax(''.join(X),A(0),kw('LAYER'))
# ord 1: CT[pp[i]] = portax(PT)[i]
pp=perm(20000); assert min(pp)>=0; Y=portax(PT,A(0),kw('PALIMPSEST')); C=['?']*97
for i in range(97): C[pp[i]]=Y[i]
texts['CTL4']=''.join(C)
with open('texts58.txt','w') as f:
    for k,v in texts.items(): assert len(v)==97 and '?' not in v; f.write(f'{k} {v}\n')
print(A(0),A(1)); print(open('texts58.txt').read())
# CTL5: themed alphabet #12 (k:SHADOW? see tw_alpha.txt line 13) behind perm 40000, ord 0, key BERLIN
T=open('/workspace/kcl/data/tw_alpha.bin','rb').read(); TA=lambda i:''.join(chr(65+b) for b in T[i*26:i*26+26])
pp=perm(40000); assert min(pp)>=0; X=['?']*97
for i in range(97): X[pp[i]]=PT[i]
c5=portax(''.join(X),TA(12),kw('BERLIN'))
open('texts58.txt','a').write(f'CTL5 {c5}\n'); print('CTL5',TA(12),c5)
