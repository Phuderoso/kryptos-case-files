# Cycle 89: W as WORD SEPARATOR. K4 split at its Ws into 6 blocks; each block enciphered separately with the
# same periodic key restarting at the block start (W itself dropped). Exact crib consistency, then quadgram scoring.
import sys, json, random
K4=open('/tmp/kcf/data/k4.txt').read().strip()
Q=json.load(open('/home/box/kryptos_support_backup/quadgrams.json')); QF,QQ=Q['floor'],Q['q']
AZ="ABCDEFGHIJKLMNOPQRSTUVWXYZ"; KA="KRYPTOSABCDEFGHIJLMNQUVWXZ"
CRIB={**{21+i:c for i,c in enumerate("EASTNORTHEAST")},**{63+i:c for i,c in enumerate("BERLINCLOCK")}}
def qscore(t): return sum(QQ.get(t[i:i+4],QF) for i in range(len(t)-3))/max(1,len(t)-3)
def offsets(ct):
    off=[];o=0
    for c in ct:
        if c=='W': off.append(None); o=0
        else: off.append(o); o+=1
    return off
def run(ct,alphs,PMAX=20):
    off=offsets(ct); out=[]; per={}
    cr=[(off[i],ct[i],c) for i,c in CRIB.items()]
    assert all(o is not None for o,_,_ in cr)
    for pn,pa,cn,ca in alphs:
        ip={c:i for i,c in enumerate(pa)}; ic={c:i for i,c in enumerate(ca)}
        for beau in (0,1):
            for p in range(1,PMAX+1):
                key={}; ok=True
                for o,x,c in cr:
                    m=len(pa); k=(ic[x]+ip[c])%m if beau else (ic[x]-ip[c])%m
                    if key.setdefault(o%p,k)!=k: ok=False;break
                if not ok: continue
                per[p]=per.get(p,0)+1
                pt="".join(' ' if off[i] is None else ('.' if off[i]%p not in key else pa[((key[off[i]%p]-ic[x]) if beau else (ic[x]-key[off[i]%p]))%len(pa)]) for i,x in enumerate(ct))
                full=len(key)==p
                out.append((qscore(pt.replace(' ','')) if full else None,pn,cn,beau,p,pt)); break
    return per,out
if __name__=="__main__":
    mode=sys.argv[1]; ct=open(sys.argv[2]).read().strip()
    if mode=="basic": alphs=[(a,A,b,B) for a,A in (("AZ",AZ),("KA",KA)) for b,B in (("AZ",AZ),("KA",KA))]
    elif mode=="w25":
        a25=AZ.replace("W",""); k25=KA.replace("W","")
        alphs=[(a,A,b,B) for a,A in (("AZ25",a25),("KA25",k25)) for b,B in (("AZ25",a25),("KA25",k25))]
    else:
        d=open('/home/box/kryptos_support_backup/alpha.bin','rb').read()
        alphs=[(str(i//26),s,str(i//26),s) for i in range(0,len(d),26) for s in ["".join(chr(65+b) for b in d[i:i+26])]]
        if mode=="themed25": alphs=[(a,s.replace("W",""),b,s.replace("W","")) for a,s,b,_ in alphs]
    per,out=run(ct,alphs)
    print(json.dumps(dict(sorted(per.items()))))
    best=sorted([o for o in out if o[0] is not None],key=lambda o:-o[0])[:5]
    for o in best: print(round(o[0],3),*o[1:])
