"""Cycle 129: ACA Periodic Gromark key streams.
ACA rule (cryptogram.org PeriodicGromark.pdf): keyword (repeats removed) -> keyword-mixed alphabet written under the
keyword and read off by columns in keyword order = cipher alphabet CA; numerical key = rank order of the keyword letters
(1-based, 10 -> 0) used as primer and chain-added with lag L (d[i] = d[i-L] + d[i-L+1] mod 10); the text is cut in
groups of L; group g starts the cipher alphabet at the position (in CA) of keyword letter g mod L. ct = CA[(pt + off + d) mod 26].
Variants also emitted: CA = plain keyword-mixed alphabet, CA = KRYPTOS alphabet; plaintext alphabet A-Z or KRYPTOS.
Output lines: label CA PA k0..k96 (key numbers as letters A=0)."""
import re,sys
AZ="ABCDEFGHIJKLMNOPQRSTUVWXYZ"; KA="KRYPTOSABCDEFGHIJLMNQUVWXZ"; N=97
def dedupe(w): return "".join(dict.fromkeys(w))
def ranks(w):
    idx=sorted(range(len(w)),key=lambda i:(w[i],i)); r=[0]*len(w)
    for n,i in enumerate(idx): r[i]=n+1
    return r
def aca_ca(kw):
    mixed=dedupe(kw+AZ); L=len(kw); r=ranks(kw)
    cols=[mixed[c::L] for c in range(L)]
    return "".join(cols[c] for c in sorted(range(L),key=lambda c:r[c]))
def stream(kw,CA):
    L=len(kw); d=[x%10 for x in ranks(kw)]
    while len(d)<N: d.append((d[-L]+d[-L+1])%10)
    return [(CA.index(kw[(i//L)%L])+d[i])%26 for i in range(N)]
def cfgs(words):
    seen=set()
    for w in words:
        kw=dedupe(w)
        if not (3<=len(kw)<=12) or kw in seen: continue
        seen.add(kw)
        for caname,CA in (("aca",aca_ca(kw)),("mix",dedupe(kw+AZ)),("ka",KA)):
            k="".join(AZ[x] for x in stream(kw,CA))
            for paname,PA in (("az",AZ),("ka",KA)):
                yield f"{w}/{caname}/{paname}",CA,PA,k
if __name__=="__main__":
    src=open('/tmp/kcf/tools/dcol_gen.py').read()
    th=re.search(r'THEMED="""(.*?)"""',src,re.S).group(1).split()
    voc=[l.split()[0].upper() for l in open('/tmp/kcf/data/cycle56/words56.txt') if l.strip()]
    words=list(dict.fromkeys([w for w in th+voc if w.isalpha()]+[a+b for a in th for b in th if a!=b]))
    if len(sys.argv)>1 and sys.argv[1]=="ctl":
        words=sys.argv[2:]
    n=0
    for c in cfgs(words): print(*c); n+=1
    print(n,file=sys.stderr)
