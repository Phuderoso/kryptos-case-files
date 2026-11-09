"""Cycle 155 controls: cycle-130 ACA Periodic Gromark plants (genuine ACA generator from cycle 129) with ONE corrupted
carved letter under a crib, one with a wrong crib letter (plaintext differs from the crib at one position), uncorrupted
ones, and ordinary-Gromark plants (arbitrary cipher alphabet, one offset) with and without corruption.
Nulls: the six cycle-130 shuffles (seeds 13001-13006).  Output: name CT L pa form(0 vig,1 beau,2 var) primer note"""
import sys,os,random
H=os.path.dirname(os.path.abspath(__file__)); R=os.environ.get("REPO",os.path.join(H,'..','..'))
sys.path.insert(0,os.path.join(R,'tools','cycle129')); sys.path.insert(0,os.path.join(R,'tools','cycle127'))
from mkcfg import aca_ca,stream,dedupe,ranks,AZ,KA
from plant import plain,K4
P=plain()
def enc(t,k,CA,PA,form): return "".join(CA[[(PA.index(c)+k[i]),(k[i]-PA.index(c)),(PA.index(c)-k[i])][form]%26] for i,c in enumerate(t))
def corrupt(ct,pos,rng):
    l=list(ct); old=l[pos]; l[pos]=rng.choice([c for c in AZ if c!=old]); return "".join(l)
def gstream(primer,n=97):
    d=list(primer); L=len(d)
    while len(d)<n: d.append((d[-L]+d[-L+1])%10)
    return d
rng=random.Random(15501)
out=[]
C=[("ctl1","PALIMST",aca_ca("PALIMST"),AZ,0),("ctl2","SHADOW",KA,KA,0),("ctl3","BERLIN",dedupe("BERLIN"+AZ),AZ,1),
   ("ctl4","BLACKHORSE",aca_ca("BLACKHORSE"),KA,2),("ctl5","CUBANSEDGIW",aca_ca("CUBANSEDGIW"),AZ,0)]
cribpos=list(range(21,34))+list(range(63,74))
for name,kw,CA,PA,f in C:
    k=stream(kw,CA); ct=enc(P,k,CA,PA,f); pr="".join(str(x%10) for x in ranks(kw))
    pos=rng.choice(cribpos); out.append((name+"x",corrupt(ct,pos,rng),len(kw),PA==KA and "ka" or "az",f,pr,f"carved-error@{pos}"))
    if name in("ctl1","ctl4"): out.append((name+"u",ct,len(kw),PA==KA and "ka" or "az",f,pr,"uncorrupted"))
# wrong crib letter: plaintext at one crib position differs from the crib
kw,CA,PA,f="SHADOW",KA,KA,0; k=stream(kw,CA); pos=27; P2=P[:pos]+("Q" if P[pos]!="Q" else "Z")+P[pos+1:]
out.append(("ctl2w",enc(P2,k,CA,PA,f),6,"ka",0,"".join(str(x%10) for x in ranks(kw)),f"wrong-crib-letter@{pos}"))
# ordinary Gromark (one offset), random cipher alphabet
for nm,primer,PA,f,cor in (("gro1",[2,6,7,1,7],AZ,0,True),("gro2",[3,1,4,1,5,9,2],KA,1,True),("gro3",[8,0,4,2,1,6,3,5],AZ,0,False)):
    CA=list(AZ); rng.shuffle(CA); CA="".join(CA); d=gstream(primer); ct=enc(P,d,CA,PA,f)
    note="uncorrupted"
    if cor: pos=rng.choice(cribpos); ct=corrupt(ct,pos,rng); note=f"carved-error@{pos}"
    out.append((nm,ct,len(primer),PA==KA and "ka" or "az",f,"".join(map(str,primer)),note))
for name,ct,L,pa,f,pr,note in out: print(name,ct,L,pa,f,pr,note)
for z in range(1,7):
    l=list(K4); random.Random(13000+z).shuffle(l); print(f"null{z}","".join(l))
