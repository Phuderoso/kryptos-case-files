"""Cycle 132 controls: model Q (two keyword layers at the plaintext position, then a bank transposition), encrypted
independently in Python with vocabulary words, plus shuffled-K4 nulls (seeds 13201-13202)."""
import sys,os,random
import numpy as np
H=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,os.path.join(H,'..','cycle127'))
from plant import plain,K4
A=["ABCDEFGHIJKLMNOPQRSTUVWXYZ","KRYPTOSABCDEFGHIJLMNQUVWXZ"]
def layer(t,T,f,kw):
    X=A[T]; return "".join(X[(X.index(c)+X.index(kw[i%len(kw)]) if f==0 else X.index(kw[i%len(kw)])-X.index(c) if f==1 else X.index(c)-X.index(kw[i%len(kw)]))%26] for i,c in enumerate(t))
def move(t,s):
    o=[None]*97
    for i,c in enumerate(t): o[s[i]]=c
    return "".join(o)
B=np.fromfile('/home/box/kryptos_support_backup/perms97.bin',dtype=np.int16).reshape(-1,97)
P=plain()
print("ctl1",move(layer(layer(P,0,2,"HARBOR"),1,0,"WINDOW"),B[12345]))              # AZ variant, KA vig, perm
print("ctl2",move(layer(layer(P,1,1,"MIRROR"),0,1,"GARDEN"),np.argsort(B[99999]))) # KA beau, AZ beau, inverse perm
print("ctl3",move(layer(layer(P,1,0,"KRYPTOS"),1,2,"QUESTION"),B[160000]))         # KA vig, KA variant
for z in (1,2):
    l=list(K4); random.Random(13200+z).shuffle(l); print(f"null{z}","".join(l))
