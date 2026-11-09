"""Cycle 172: decrypt every Quagmire IV match (M lines) with the crib-fixed key values; '?' where a residue class holds no crib.
Score English: mean log10 quadgram over the off-crib text (windows without '?'), also on all letters.
usage: decode172.py CT perms.bin quadgrams.json files...   (M lines: M lab q ix p mode PA CA m)"""
import sys, json, numpy as np, math
AZ="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
CRIB={**{21+i:c for i,c in enumerate("EASTNORTHEAST")},**{63+i:c for i,c in enumerate("BERLINCLOCK")}}
ct,pf,qf=sys.argv[1],sys.argv[2],sys.argv[3]
AL={l.split()[1]:l.split()[0] for l in open("support/alpha172.txt")}
J=json.load(open(qf)); Q=J["q"]; floor=J["floor"]  # log10 probabilities as stored
P=np.fromfile(pf,dtype=np.int16).reshape(-1,97)
def score(s,offcrib):
    v=[Q.get(s[i:i+4],floor) for i in range(len(s)-3) if '?' not in s[i:i+4] and (not offcrib or not any(i+k in CRIB for k in range(4)))]
    return sum(v)/len(v) if v else -99
rows=[]
for f in sys.argv[4:]:
    for l in open(f):
        if not l.startswith("M "): continue
        _,lab,q,ix,p,mode,pa,ca,m=l.split(); q,ix,p=int(q),int(ix),int(p); PA,CA=AL[pa],AL[ca]; S=P[q]; sg=1 if mode=="vig" else -1
        key={}
        for j,c in CRIB.items():
            r=(int(S[j]) if ix else j)%p; kv=(CA.index(ct[S[j]])-sg*PA.index(c))%26
            assert key.setdefault(r,kv)==kv, l
        out=[]
        for j in range(97):
            r=(int(S[j]) if ix else j)%p
            out.append('?' if r not in key else PA[(sg*(CA.index(ct[S[j]])-key[r]))%26])
        s="".join(out); assert all(s[j]==c for j,c in CRIB.items())
        rows.append((score(s,True),score(s,False),lab,q,ix,p,mode,pa,ca,s.count('?'),s))
rows.sort(reverse=True)
for r in rows: print("%.3f %.3f %s q=%d ix=%d p=%d %s %s->%s unk=%d %s"%r)
