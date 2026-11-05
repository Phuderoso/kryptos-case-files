# Cycle 66 controls and nulls. Controls: English text with the cribs at the official positions, encrypted by a
# four-square with random cipher squares and a themed plain square, optionally with a cycle-12 transposition.
import random,struct,sys
K4="OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR"
A=open('a264.bin','rb').read(); NA=len(A)//26
P=open('c12_perm.bin','rb').read(); NP=len(P)//194
def perm(i): return struct.unpack('<97H',P[i*194:(i+1)*194])
txt=''.join(c for c in open('/workspace/kcl/data/g2701.txt',errors='ignore').read().upper() if c.isalpha())
SYM="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
def coords(a,shape):
    al=list(A[a*26:(a+1)*26]); seq=[]
    for L in al:
        seq.append(L)
        if shape==3 and L<10: seq.append(26+(L+1)%10)
    if shape==2: seq+=list(range(26,36))
    Cc=13 if shape==0 else 2 if shape==1 else 6
    return {s:(i//Cc,i%Cc) for i,s in enumerate(seq)},Cc,len(seq)
def fsq(pt,a,shape,off,rng):
    co,Cc,S=coords(a,shape); C1=list(range(S)); C2=list(range(S)); rng.shuffle(C1); rng.shuffle(C2)
    out=[SYM.index(c) for c in pt]
    for k in range(off,96,2):
        if k+1>=97: break
        p,q=SYM.index(pt[k]),SYM.index(pt[k+1]); (ra,ca),(rb,cb)=co[p],co[q]
        out[k]=C1[ra*Cc+cb]; out[k+1]=C2[rb*Cc+ca]
    return ''.join(SYM[x] for x in out)
rng=random.Random(66)
print("K4",K4)
for i in range(5):
    l=list(K4); random.Random(6600+i).shuffle(l); print(f"NULL{i}",''.join(l))
for shape in range(4):
    for j,layer in enumerate(["direct","A","B"]):
        s=rng.randrange(len(txt)-200); pt=list(txt[s:s+97]); pt[21:34]="EASTNORTHEAST"; pt[63:74]="BERLINCLOCK"; pt=''.join(pt)
        a=rng.randrange(NA); off=rng.randrange(2); pi=rng.randrange(min(NP,96630))
        if layer=="direct": ct=fsq(pt,a,shape,off,rng)
        elif layer=="A":
            I=fsq(pt,a,shape,off,rng); p=perm(pi); ct=['?']*97
            for jj in range(97): ct[p[jj]]=I[jj]
            ct=''.join(ct)
        else:
            p=perm(pi); I=''.join(pt[p[jj]] for jj in range(97)); ct=fsq(I,a,shape,off,rng)
        print(f"CTL_s{shape}_{layer}",ct,f"a={a} off={off} perm={pi if layer!='direct' else -1}",file=sys.stdout)
