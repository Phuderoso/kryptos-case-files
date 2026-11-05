# Cycle 88: W-free 92-letter text, no transposition, Quagmire III (one themed keyed alphabet both sides), Vig/Beau, p<=20.
import sys
ct=open(sys.argv[1]).read().strip(); d=open('/home/box/kryptos_support_backup/alpha.bin','rb').read(); A=[''.join(chr(65+b) for b in d[i:i+26]) for i in range(0,len(d),26)]  # alphabet order as letter indices (86,731 themed alphabets from cycle 12/55)
cr=[(20+i,c) for i,c in enumerate("EASTNORTHEAST")]+[(60+i,c) for i,c in enumerate("BERLINCLOCK")]
hits=0; per={}
for al in A:
    if len(al)!=26 or len(set(al))!=26: continue
    ix={c:i for i,c in enumerate(al)}
    for beau in (0,1):
        for p in range(1,21):
            key={}; ok=True
            for i,c in cr:
                k=(ix[ct[i]]+ix[c])%26 if beau else (ix[ct[i]]-ix[c])%26
                if key.setdefault(i%p,k)!=k: ok=False; break
            if ok: hits+=1; per[p]=per.get(p,0)+1; break
print(len(A),hits,dict(sorted(per.items())))
