"""Cycle 85: planted halfabet controls. Encrypts a 97-letter English text (cribs at the official positions)
with a known alphabet, transposition, split, variant, layer order and periodic key, using the same model as halfabet.c:
plaintext letter j is substituted, then lands at ciphertext position t[j]."""
import numpy as np, json, sys
S='/home/box/kryptos_support_backup'
perms=np.fromfile(f'{S}/perms97.bin',dtype=np.int16).reshape(-1,97)
alph=np.fromfile(f'{S}/alpha.bin',dtype=np.uint8).reshape(-1,26)
pt=("THEROOMWASDARKANDCOLDY"[:21]+"EASTNORTHEAST"+"ANDTHENIGHTWINDCAMEINOVERSTONE"[:29]+"BERLINCLOCK"+"TICKEDSOFTLYUNDERTHEFLO"[:23])
assert len(pt)==97 and pt[21:34]=="EASTNORTHEAST" and pt[63:74]=="BERLINCLOCK"
def enc(a,p,sp,var,mode,key):
    A=alph[a]; t=perms[p]; pos={int(x):i for i,x in enumerate(A)}
    def half(x): q=pos[x]; return (q>=13,q%13) if sp==0 else (q&1,q>>1)
    def letter(h,i): return int(A[13*h+i]) if sp==0 else int(A[2*i+h])
    ct=[None]*97
    for j,ch in enumerate(pt):
        h,i=half(ord(ch)-65); k=key[(j if mode==0 else int(t[j]))%len(key)]
        o=(i+k)%13 if var==0 else (k-i)%13
        ct[int(t[j])]=chr(65+letter(h,o))
    return ''.join(ct)
ctl=[dict(name='ctlA',a=2,p=1234,sp=0,var=0,mode=0,key=[3,7,1,12,5,0,9]),
     dict(name='ctlB',a=40000,p=99001,sp=1,var=1,mode=1,key=[4,4,11,2,8,6,0,10,1,3,7]),
     dict(name='ctlC',a=1,p=0,sp=0,var=1,mode=1,key=[6,2,9,11,5])]
for c in ctl:
    ct=enc(c['a'],c['p'],c['sp'],c['var'],c['mode'],c['key'])
    open(f"{c['name']}.txt",'w').write(ct); c['ct']=ct
json.dump(dict(plaintext=pt,controls=ctl),open('controls85.json','w'),indent=1)
print(json.dumps(ctl))
