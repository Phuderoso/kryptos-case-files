"""Cycle 177 planted controls, written independently of gm177.c / pg177.c (string alphabets, encryption from the definitions).
Ordinary Gromark, base b: d = primer digits, d[i] = d[i-L] + d[i-L+1] mod b; c = CA[(PA.index(p) + d) % 26] (vig),
CA[(d - PA.index(p)) % 26] (beau), CA[(PA.index(p) - d) % 26] (variant). ACA Periodic Gromark streams: tools/cycle129/mkcfg.py.
Perm convention: plaintext position i -> carved position s[i]. ix 0: substitute on the plaintext index, then transpose;
ix 1: transpose, then substitute on the carved index.
One-error plants: (a) wrong carved letter: the carved letter under crib slot t is overwritten by the carved letter under a slot u
with a different w (so the strict test must fail); (b) wrong crib letter: the plaintext letter at crib slot t is changed before
encryption, searching letters until the strict test (checked here in Python) fails at the planted config.
usage: plant177.py perms.bin > controls177.txt  (lines: name CT model ix L pa form base q key errslots)"""
import sys,os,random
import numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,os.path.join(HERE,'..','cycle129')); sys.path.insert(0,os.path.join(HERE,'..','cycle127'))
from mkcfg import aca_ca,stream,dedupe,AZ,KA,ranks
from plant import plain
B=np.fromfile(sys.argv[1],dtype=np.int16).reshape(-1,97)
CI=list(range(21,34))+list(range(63,74)); PT="EASTNORTHEASTBERLINCLOCK"
def gstream(primer,b=10,n=97):
    d=[int(c) for c in primer]; L=len(d)
    while len(d)<n: d.append((d[-L]+d[-L+1])%b)
    return d
F={"vig":lambda x,k:x+k,"beau":lambda x,k:k-x,"var":lambda x,k:x-k}
def gsub(t,primer,PA,CA,form,b=10):
    d=gstream(primer,b); return "".join(CA[F[form](PA.index(c),d[i])%26] for i,c in enumerate(t))
def asub(t,kw,CA,PA,form):
    k=stream(dedupe(kw),CA)
    return "".join(CA[(k[i]-PA.index(c))%26] if form=="beau" else CA[(PA.index(c)+k[i])%26] for i,c in enumerate(t))
def tr(t,s):
    out=[None]*97
    for i,c in enumerate(t): out[s[i]]=c
    return "".join(out)
def wvec(primer,PA,form,ix,s,b=10):
    """w over the 24 crib slots under OUR cribs (variant -> beau with reflected alphabet: same partition)."""
    d=gstream(primer,b); f=F["beau" if form=="var" else form]
    return [f(PA.index(p),d[CI[t] if ix==0 else int(s[CI[t]])])%26 for t,p in enumerate(PT)]
def strict_ok(ct,primer,PA,form,ix,s,b=10):
    w=wvec(primer,PA,form,ix,s,b); c=[ct[int(s[i])] for i in CI]
    return all((w[a]==w[x])==(c[a]==c[x]) for a in range(24) for x in range(a+1,24))
P=plain(); assert P[21:34]=="EASTNORTHEAST" and P[63:74]=="BERLINCLOCK"
R=random.Random(17701); RCA="".join(R.sample(AZ,26))
def kwprimer(w): return "".join(str(r%10) for r in ranks(dedupe(w)))
rows=[]
def wrong_carved(ct,s,w,slots):
    """overwrite the carved letter of each slot t in 'slots' with that of a partner u (different w, partners all distinct)."""
    c=list(ct); usedp=set(slots)
    for t in slots:
        u=next(u for u in range(24) if u not in usedp and w[u]!=w[t] and ct[int(s[CI[u]])]!=ct[int(s[CI[t]])]); usedp.add(u)
        c[int(s[CI[t]])]=ct[int(s[CI[u]])]
    return "".join(c)
def G(name,ix,primer,PA,CA,form,q,err=None,b=10,slots=()):
    s=B[q]; pt=P
    if err=="crib":
        t=slots[0]
        for L in AZ:
            if L==P[CI[t]]: continue
            pt2=P[:CI[t]]+L+P[CI[t]+1:]
            ct=tr(gsub(pt2,primer,PA,CA,form,b),s) if ix==0 else gsub(tr(pt2,s),primer,PA,CA,form,b)
            if not strict_ok(ct,primer,PA,form,ix,s,b): break
    else:
        ct=tr(gsub(pt,primer,PA,CA,form,b),s) if ix==0 else gsub(tr(pt,s),primer,PA,CA,form,b)
        if err=="carved": ct=wrong_carved(ct,s,wvec(primer,PA,form,ix,s,b),slots)
    if err: assert not strict_ok(ct,primer,PA,form,ix,s,b), name
    else: assert strict_ok(ct,primer,PA,form,ix,s,b), name
    rows.append((name,ct,"G",ix,len(primer),"az" if PA==AZ else "ka",form,b,q,primer,",".join(map(str,slots)) or "-"))
def A(name,ix,kw,cav,PA,form,q,err=None,slots=()):
    CA={"aca":aca_ca(dedupe(kw)),"mix":dedupe(dedupe(kw)+AZ),"ka":KA,"kmix":dedupe(dedupe(kw)+KA)}[cav]; s=B[q]; pt=P
    if err=="crib":
        t=slots[0]; L=next(x for x in AZ if x!=P[CI[t]]); pt=P[:CI[t]]+L+P[CI[t]+1:]
    ct=tr(asub(pt,kw,CA,PA,form),s) if ix==0 else asub(tr(pt,s),kw,CA,PA,form)
    if err=="carved":
        c=list(ct)
        for t in slots: j=int(s[CI[t]]); c[j]=AZ[(AZ.index(c[j])+1)%26]
        ct="".join(c)
    rows.append((name,ct,"PG",ix,len(dedupe(kw)),"az" if PA==AZ else "ka",form,10,q,f"{kw}/{cav}/{'az' if PA==AZ else 'ka'}",",".join(map(str,slots)) or "-"))
G("ctl1",0,"7426",AZ,dedupe("PALIMPSEST"+KA),"vig",12345,"carved",slots=(4,))
G("ctl2",1,"3141",KA,aca_ca("SHADOW"),"beau",98765,"crib",slots=(19,))
G("ctl3",0,"27182",KA,RCA,"vig",162000,"carved",slots=(20,))
G("ctl4",1,kwprimer("KRYPTOS"),AZ,dedupe("BERLIN"+AZ),"vig",163500,"carved",slots=(0,))
G("ctl5",1,"90210",AZ,dedupe("CLOCK"+AZ),"var",54321,"crib",slots=(2,))
A("ctl6",1,"PALIMPSEST","aca",AZ,"vig",777,"carved",slots=(0,))
A("ctl7",0,"SHADOW","kmix",KA,"beau",40000,"crib",slots=(5,))
A("ctl8",1,"ILLUSION","mix",AZ,"beau",88888,"carved",slots=(17,))
G("ctl9",0,"314156",AZ,dedupe("LUCID"+KA),"vig",120000,b=7)   # first draft used primer 314159 (digit 9 is not a base-7 digit): control FAILED, plant fixed, rerun
G("ctl10",1,"2413",KA,aca_ca("ABSCISSA"),"beau",777,b=5)
G("ctl11",0,"74269",AZ,dedupe("PALIMPSEST"+KA),"vig",12345)          # strict plant: must show a FULL mask in the err-1 run
G("neg1",0,"7426",AZ,dedupe("PALIMPSEST"+KA),"vig",12345,"carved",slots=(4,16))
A("neg2",1,"PALIMPSEST","aca",AZ,"vig",777,"carved",slots=(0,9))
for r in rows: print(*r)
