"""Cycle 176 planted controls, written independently of gm176.c / pg176.c (string alphabets, encryption from the definitions).
Ordinary Gromark: d = primer digits, then d[i] = d[i-L] + d[i-L+1] mod 10; c = CA[(PA.index(p) + d) % 26] (vig),
CA[(d - PA.index(p)) % 26] (beau), CA[(PA.index(p) - d) % 26] (variant). ACA Periodic Gromark streams come from
tools/cycle129/mkcfg.py (reproduces the ACA ENIGMA example). Perm convention: plaintext position i -> carved position s[i].
ix 0: substitute on the plaintext index, then transpose; ix 1: transpose, then substitute on the carved index.
usage: plant176.py perms.bin > controls176.txt   (lines: name CT model ix L pa form q primer/cfg)"""
import sys,os,random
import numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,os.path.join(HERE,'..','cycle129')); sys.path.insert(0,os.path.join(HERE,'..','cycle127'))
from mkcfg import aca_ca,stream,dedupe,AZ,KA,ranks
from plant import plain
B=np.fromfile(sys.argv[1],dtype=np.int16).reshape(-1,97)
def gstream(primer,n=97):
    d=[int(c) for c in primer]; L=len(d)
    while len(d)<n: d.append((d[-L]+d[-L+1])%10)
    return d
def gsub(t,primer,PA,CA,form):
    d=gstream(primer)
    f={"vig":lambda x,k:x+k,"beau":lambda x,k:k-x,"var":lambda x,k:x-k}[form]
    return "".join(CA[f(PA.index(c),d[i])%26] for i,c in enumerate(t))
def asub(t,kw,CA,PA,form):
    k=stream(dedupe(kw),CA)
    return "".join(CA[(k[i]-PA.index(c))%26] if form=="beau" else CA[(PA.index(c)+k[i])%26] for i,c in enumerate(t))
def tr(t,s):
    out=[None]*97
    for i,c in enumerate(t): out[s[i]]=c
    return "".join(out)
P=plain(); assert P[21:34]=="EASTNORTHEAST" and P[63:74]=="BERLINCLOCK"
R=random.Random(17601); RCA="".join(R.sample(AZ,26))
def kwprimer(w): return "".join(str(r%10) for r in ranks(dedupe(w)))
rows=[]
def G(name,ix,primer,PA,CA,form,q):
    s=B[q]; ct=tr(gsub(P,primer,PA,CA,form),s) if ix==0 else gsub(tr(P,s),primer,PA,CA,form)
    rows.append((name,ct,"G",ix,len(primer),"az" if PA==AZ else "ka",form,q,primer))
def A(name,ix,kw,cav,PA,form,q):
    CA={"aca":aca_ca(dedupe(kw)),"mix":dedupe(dedupe(kw)+AZ),"ka":KA,"kmix":dedupe(dedupe(kw)+KA)}[cav]; s=B[q]
    ct=tr(asub(P,kw,CA,PA,form),s) if ix==0 else asub(tr(P,s),kw,CA,PA,form)
    rows.append((name,ct,"PG",ix,len(dedupe(kw)),"az" if PA==AZ else "ka",form,q,f"{kw}/{cav}/{'az' if PA==AZ else 'ka'}"))
G("ctl1",0,"74269",AZ,dedupe("PALIMPSEST"+KA),"vig",12345)
G("ctl2",1,"3141",KA,aca_ca("SHADOW"),"beau",98765)
G("ctl3",0,"27182818",KA,RCA,"vig",162000)
G("ctl4",1,kwprimer("KRYPTOS"),AZ,dedupe("BERLIN"+AZ),"vig",163500)
G("ctl5",1,"90210",AZ,dedupe("CLOCK"+AZ),"var",54321)
A("ctl6",1,"PALIMPSEST","aca",AZ,"vig",777)
A("ctl7",0,"SHADOW","kmix",KA,"beau",40000)
G("ctl8",0,"55555",AZ,dedupe("LAYER"+KA),"beau",120000)   # pure digit-5 stream degenerates? kept as an edge plant
# negative: ctl1 with the carved letter under crib slot 0 (plaintext index 21, w = A+7 = H) overwritten by the carved letter under
# crib slot 3 (index 24, plaintext T, a different w) -> two equal ct with different w: the strict test must miss it at q 12345
c=list(rows[0][1]); s0=B[12345]; c[int(s0[21])]=c[int(s0[24])]; rows.append(("neg1","".join(c))+rows[0][2:])
for r in rows: print(*r)
