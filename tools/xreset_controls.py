"""Cycle 26 controls and nulls for xreset.c (interrupted key restarting at X)."""
import random, sys
from kryptos_text import K4
A={'AZ':"ABCDEFGHIJKLMNOPQRSTUVWXYZ",'KA':"KRYPTOSABCDEFGHIJLMNQUVWXZ"}
def enc(pt,key,tab,mode,rule,ph=0):
    a=A[tab]; L=len(key); j=ph; out=[]
    for ch in pt:
        p=a.index(ch); k=a.index(key[j%L])
        c=(p+k)%26 if mode==0 else (k-p)%26 if mode==1 else (p-k)%26
        out.append(a[c])
        if rule==1 and ch=='X': j=0
        elif rule==2 and a[c]=='X': j=0
        elif rule==3 and ch=='X': pass
        else: j+=1
    return ''.join(out)
# planted plaintext: 97 letters, cribs at official positions, X separators (invented example text)
pt=("SLOWLYXTHEDOORXOPENED"+"EASTNORTHEAST"+"OFTHEWALLXWEFOUNDTHEOLDMARKERXNE"[:29]+"BERLINCLOCK")
pt=pt+("XTHEHOURWASLATEXNOONEWASTHERE")[:97-len(pt)]
assert len(pt)==97 and pt[21:34]=="EASTNORTHEAST" and pt[63:74]=="BERLINCLOCK", (len(pt),pt)
if sys.argv[1]=='controls':
    for i,(key,tab,mode,rule) in enumerate([("SHADOW","KA",0,1),("PALIMPSEST","KA",1,2),("ABSCISSA","AZ",2,3)]):
        open(f"ctl_{i+1}.txt","w").write(enc(pt,key,tab,mode,rule,ph=0)+"\n"); print(i+1,key,tab,mode,rule)
else:
    for i in range(1,21):
        r=random.Random(i); s=list(K4); r.shuffle(s); open(f"null_{i}.txt","w").write(''.join(s)+"\n")
