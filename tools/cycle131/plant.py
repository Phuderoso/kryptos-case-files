"""Cycle 131 planted controls: an independent Python encryptor for two stacked keyword layers, with and without a
bank transposition, on the cycle-127 planted English text; plus shuffled-K4 nulls (seeds 13101-13102)."""
import sys,os,random
import numpy as np
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','cycle127'))
from plant import plain,K4
A=["ABCDEFGHIJKLMNOPQRSTUVWXYZ","KRYPTOSABCDEFGHIJLMNQUVWXZ"]
def layer(text,T,f,kw,pos):
    X=A[T]; out=""
    for i,c in enumerate(text):
        a=X.index(c); s=X.index(kw[pos(i)%len(kw)])
        out+=X[(a+s if f==0 else s-a if f==1 else a-s)%26]
    return out
def move(t,s):
    o=[None]*97
    for i,c in enumerate(t): o[s[i]]=c
    return "".join(o)
B=np.fromfile('/home/box/kryptos_support_backup/perms97.bin',dtype=np.int16).reshape(-1,97)
P=plain(); I=lambda i:i
print("ctl1",layer(layer(P,1,0,"PALIMPSEST",I),0,2,"QUARTZ",I))            # direct, KA vig then AZ variant
s=B[50000]; si=np.argsort(s)
x=move(layer(P,0,1,"ABSCISSA",I),s); print("ctl2",layer(x,1,0,"SHADOW",I))  # model M: AZ beau, perm, KA vig at carved pos
x=move(P,s); print("ctl3",layer(layer(x,1,1,"KRYPTOS",I),1,0,"BERLIN",I))   # model P: perm first, KA beau, KA vig
print("ctl4",move(layer(layer(P,0,0,"COMPASS",I),1,1,"LIGHT",I),si))       # model Q: both layers then inverse perm
for z in (1,2):
    l=list(K4); random.Random(13100+z).shuffle(l); print(f"null{z}","".join(l))
