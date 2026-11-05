# Cycle 82 planted controls: independent Python Playfair + periodic outer key, enciphered with known word squares.
import random, json
from kryptos_text import KA
AZ="ABCDEFGHIJKLMNOPQRSTUVWXYZ"; rng=random.Random(8201)
cpos=list(range(21,34))+list(range(63,74)); crib="EASTNORTHEASTBERLINCLOCK"; src=open("eng.txt").read()
def square(word,om,fill):
    drop='Q' if om else 'J'; used=set(drop); s0=[]
    for ch in word:
        if not om and ch=='J': ch='I'
        if ch not in used: used.add(ch); s0.append(ch)
    for ch in (KA if fill==1 else AZ):
        if ch not in used: used.add(ch); s0.append(ch)
    return [s0[(i%5)*5+i//5] for i in range(25)] if fill==2 else s0
def pf_enc(a,b,sq):
    p1,p2=sq.index(a),sq.index(b); r1,c1,r2,c2=p1//5,p1%5,p2//5,p2%5
    if r1==r2: return sq[r1*5+(c1+1)%5],sq[r2*5+(c2+1)%5]
    if c1==c2: return sq[((r1+1)%5)*5+c1],sq[((r2+1)%5)*5+c2]
    return sq[r1*5+c2],sq[r2*5+c1]
def pf_dec(a,b,sq):
    p1,p2=sq.index(a),sq.index(b); r1,c1,r2,c2=p1//5,p1%5,p2//5,p2%5
    if r1==r2: return sq[r1*5+(c1-1)%5],sq[r2*5+(c2-1)%5]
    if c1==c2: return sq[((r1-1)%5)*5+c1],sq[((r2-1)%5)*5+c2]
    return sq[r1*5+c2],sq[r2*5+c1]
def make(word,om,fill,a,T,mode,key):
    sq=square(word,om,fill); o=rng.randrange(len(src)-100); pt=list(src[o:o+97])
    for i,ch in zip(cpos,crib): pt[i]=ch
    pt=[('I' if (c=='J' and not om) else 'K' if (c=='Q' and om) else c) for c in pt]
    mid=pt[:]
    for i in range(a,96,2):
        if pt[i]==pt[i+1]: pt[i+1]='X' if pt[i]!='X' else 'Z'
        mid[i],mid[i+1]=pf_enc(pt[i],pt[i+1],sq)
    ct=[]
    for i,m in enumerate(mid):
        k=T.index(key[i%len(key)]); q=T.index(m); c=(q+k) if mode==0 else (k-q) if mode==1 else (q-k); ct.append(T[c%26])
    return "".join(ct),"".join(pt)
specs=[("PALIMPSEST",0,0,0,KA,0,"ABSCISSA"),("SHADOW",1,1,1,AZ,1,"BERLIN"),("LUCID",0,2,0,KA,2,"LANGLEY"),
       ("ILLUSION",0,1,1,AZ,0,"COMPASS"),("UNDERGRUUND",1,0,0,KA,1,"CLOCKS"),("MEMORY",0,0,1,KA,0,"EASTNORTH")]
out=[]
for n,(w,om,fill,a,T,mode,key) in enumerate(specs):
    ct,pt=make(w,om,fill,a,T,mode,key)
    out.append(dict(ctl=n,word=w,om=om,fill=fill,a=a,tab="KA" if T==KA else "AZ",mode=mode,key=key,p=len(key),ct=ct,pt=pt))
json.dump(out,open("controls82.json","w"),indent=1)
