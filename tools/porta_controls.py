import sys,random,numpy as np
sys.path.insert(0,'tools'); from kryptos_text import K4
P=np.fromfile('data/tw_perm.bin',dtype=np.int16).reshape(-1,97)
A=np.fromfile('data/tw_alpha.bin',dtype=np.uint8).reshape(-1,26)
tags=open('data/tw_perm.txt').read().split('\n')
for s in range(1,11):
    l=list(K4); random.Random(s).shuffle(l); open(f'null_{s}.txt','w').write(''.join(l))
pt=("SLOWLYDESPARATLYSLOWL"+"EASTNORTHEAST"+"THEREMAINSOFPASSAGEDEBRISTHATENC"[:29]+"BERLINCLOCK"+"THELOWERPARTOFTHEDOORWAYWAS")[:97]
assert pt[21:34]=="EASTNORTHEAST" and pt[63:74]=="BERLINCLOCK", (pt[21:34],pt[63:74])
def enc(pt,t,alpha,key,var,mode):
    pos={c:i for i,c in enumerate(alpha)}; ct=[None]*97
    for j,ch in enumerate(pt):
        i=pos[ch]; idx=j if mode==0 else int(t[j]); k=key[idx%len(key)]
        if i<13: h=(i+k)%13 if var==0 else (k-i)%13; o=alpha[13+h]
        else:
            h=i-13; lo=(h-k)%13 if var==0 else (k-h)%13; o=alpha[lo]
        ct[t[j]]=o
    return ''.join(ct)
KA="KRYPTOSABCDEFGHIJLMNQUVWXZ"
c1=enc(pt,P[5000],KA,[(ord(c)-65)//2 for c in "PALIMPSEST"],0,0)
c2=enc(pt,P[40000],''.join(chr(65+x) for x in A[300]),[(ord(c)-65)//2 for c in "CLOCK"],1,1)
open('ctl_1.txt','w').write(c1); open('ctl_2.txt','w').write(c2)
print(tags[5000],tags[40000],c1,c2)
