import sys
import os as _os, sys as _sys; _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), ".."))
from kryptos_text import KA
AZ="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
def pf_dec(x,y,sq):
    p1,p2=sq.index(x),sq.index(y); r1,c1,r2,c2=p1//5,p1%5,p2//5,p2%5
    if r1==r2: return sq[r1*5+(c1-1)%5],sq[r2*5+(c2-1)%5]
    if c1==c2: return sq[((r1-1)%5)*5+c1],sq[((r2-1)%5)*5+c2]
    return sq[r1*5+c2],sq[r2*5+c1]
def decrypt(ct,sq,key,tab,mode,a):
    T=KA if tab=="KA" else AZ; inner=[]
    for i,ch in enumerate(ct):
        c=T.index(ch); k=T.index(key[i%len(key)])
        q=(c-k)%26 if mode==0 else (k-c)%26 if mode==1 else (c+k)%26; inner.append(T[q])
    out=inner[:]
    for i in range(a,len(ct)-1,2):
        if inner[i] not in sq or inner[i+1] not in sq or inner[i]==inner[i+1]: return None
        out[i],out[i+1]=pf_dec(inner[i],inner[i+1],sq)
    return "".join(out)
if __name__=="__main__":
    ct,sq,key,tab,mode,a=sys.argv[1:7]; print(decrypt(ct,sq,key,tab,int(mode),int(a)))
