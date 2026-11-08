"""Cycle 129 planted controls. The key stream comes from mkcfg.py, whose ACA construction reproduces the ACA's
published ENIGMA example exactly (RHNAAX NRUZBN ... TLUD); the encryption and transposition are applied here
independently of pgcheck.c. Perms are taken from the bank (perms97.bin). Plus shuffled-K4 nulls (seeds 12901-12902)."""
import sys,os,random
import numpy as np
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','cycle127'))
from mkcfg import aca_ca,stream,dedupe,AZ,KA
from plant import plain,K4
B=np.fromfile('/home/box/kryptos_support_backup/perms97.bin',dtype=np.int16).reshape(-1,97)
def sub(t,kw,CA,PA,beau,keyidx):
    k=stream(dedupe(kw),CA)
    return "".join(CA[(k[keyidx(i)]-PA.index(c))%26] if beau else CA[(PA.index(c)+k[keyidx(i)])%26] for i,c in enumerate(t))
def perm(t,s):  # plaintext position i -> carved position s[i]
    out=[None]*97
    for i,c in enumerate(t): out[s[i]]=c
    return "".join(out)
if __name__=="__main__":
    P=plain()
    print("ctl1",sub(P,"PALIMPSEST",aca_ca(dedupe("PALIMPSEST")),AZ,0,lambda i:i))                       # direct ACA
    s=B[40000]; x=sub(P,"SHADOW",KA,KA,0,lambda i:i); print("ctl2",perm(x,s))                  # model A, perm 40000, KA/KA
    s=B[123456]; y=perm(P,s); print("ctl3",sub(y,"BERLIN",dedupe("BERLIN"+AZ),AZ,1,lambda j:j)) # model B, beau, mixed CA
    s=B[777]; inv=np.argsort(s); x=sub(P,"LAYERTWO",aca_ca("LAYERTWO"),KA,0,lambda i:i); print("ctl4",perm(x,inv))  # model A, inverse of perm 777
    for z in (1,2):
        l=list(K4); random.Random(12900+z).shuffle(l); print(f"null{z}","".join(l))
