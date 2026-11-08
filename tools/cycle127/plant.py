"""Cycle 127 planted controls: ACA Sequence Transposition (textbook encryptor, written independently of seqtr.c)
with a periodic Vigenere/Beaufort key before (model A) or after (model B); plus shuffled-K4 nulls (seeds 12701-12702)."""
import random,os
HERE=os.path.dirname(os.path.abspath(__file__))
K4=open(os.path.join(HERE,'..','..','data','k4.txt')).read().strip()
AZ="ABCDEFGHIJKLMNOPQRSTUVWXYZ"; KA="KRYPTOSABCDEFGHIJLMNQUVWXZ"
def plain():
    s=("THESHADOWFELLACROSSTHESTONEXTHENORTHGATEWASOPENX"[:21]+"EASTNORTHEAST"+
       "WEWALKEDTOWARDTHEOLDTOWERANDTHENTHE"[:29]+"BERLINCLOCK"+"STRUCKTHEHOURINSILENCEXXSTOPXXX")
    return s[:97]
def seq(primer,n):
    d=[int(c) for c in primer]
    while len(d)<n: d.append((d[-5]+d[-4])%10)
    return d[:n]
def labels(key,conv):  # ACA: alphabetical rank of each key letter, ties left to right; conv 0 -> 0-9, 1 -> 1-0
    idx=sorted(range(10),key=lambda i:(key[i],i)); r=[0]*10
    for n,i in enumerate(idx): r[i]=(n+conv)%10
    return r
def seqtrans(t,primer,key,conv):
    d=seq(primer,len(t)); cols={k:[] for k in range(10)}
    for ch,k in zip(t,d): cols[k].append(ch)
    return "".join("".join(cols[l]) for l in labels(key,conv))
def sub(t,key,alpha,beau):
    return "".join(alpha[(alpha.index(key[i%len(key)])-alpha.index(c))%26] if beau else alpha[(alpha.index(c)+alpha.index(key[i%len(key)]))%26] for i,c in enumerate(t))
if __name__=="__main__":
    P=plain(); assert len(P)==97 and P[21:34]=="EASTNORTHEAST" and P[63:74]=="BERLINCLOCK"
    print("ctl1",seqtrans(sub(P,"SANBORN",AZ,0),"69315","GUMMYBEARS",0))          # model A, A-Z Vig p7
    print("ctl2",sub(seqtrans(P,"42983","CHARTHOUSE",1),"LAYERS",KA,1))           # model B, KA Beau p6
    print("ctl3",sub(seqtrans(P,"75639","BROADCLOTH",0),"PALIMPSEST",KA,0))       # model B, KA Vig p10
    print("ctl4",seqtrans(sub(P,"SHADOWFORC",AZ,1),"00427","KRYPTOSABC",1))       # model A, A-Z Beau p10
    for s in (1,2):
        l=list(K4); random.Random(12700+s).shuffle(l); print(f"null{s}","".join(l))
