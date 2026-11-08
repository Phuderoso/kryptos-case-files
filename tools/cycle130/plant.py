"""Cycle 130 controls: genuine ACA Periodic Gromark encryptions (generator from cycle 129, which reproduces the ACA
ENIGMA example) of the cycle-127 planted English text, plus shuffled-K4 nulls (seeds 13001-13006)."""
import sys,os,random
H=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,os.path.join(H,'..','cycle129')); sys.path.insert(0,os.path.join(H,'..','cycle127'))
from mkcfg import aca_ca,stream,dedupe,AZ,KA
from plant import plain,K4
def enc(t,kw,CA,PA,form):
    k=stream(kw,CA); o=[]
    for i,c in enumerate(t):
        a=PA.index(c); o.append(CA[[(a+k[i]),(k[i]-a),(a-k[i])][form]%26])
    return "".join(o)
P=plain()
C=[("ctl1","PALIMST",aca_ca("PALIMST"),AZ,0),("ctl2","SHADOW",KA,KA,0),("ctl3","BERLIN",dedupe("BERLIN"+AZ),AZ,1),
   ("ctl4","BLACKHORSE",aca_ca("BLACKHORSE"),KA,2),("ctl5","UNDERGROUND"[:0]+"CUBANSEDGIW",aca_ca("CUBANSEDGIW"),AZ,0)]
for name,kw,CA,PA,f in C: print(name,enc(P,kw,CA,PA,f),len(kw),PA==KA and "ka" or "az",f)
for z in range(1,7):
    l=list(K4); random.Random(13000+z).shuffle(l); print(f"null{z}","".join(l))
