import json,glob,re
from kryptos_text import KA
AZ="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
import numpy as np
perms=np.fromfile("perms97.bin",dtype=np.int16).reshape(-1,97)
def cnt(pat):
    h=t=0
    for f in glob.glob(pat):
        s=open(f).read(); h+=s.count("HIT "); m=re.search(r"tests=(\d+)",s); t+=int(m.group(1))
    return h,t
S={"k4_behind_perms_L1_3":cnt("r_k4_*.txt"),"k4_direct_L1_6":(0,1285089624)}
S["nulls_behind_perms_L1_3"]={f"null{n}":cnt(f"r_null{n}_*.txt") for n in range(5)}
S["nulls_direct_L1_6"]={f"null{n}":cnt(f"rd_null{n}.txt") for n in range(5)}
ctl=json.load(open("controls80.json")); res=[]
src=open("eng.txt").read()
for c in ctl:
    s=open(f"r_ctl{c['ctl']}.txt").read()
    planted=f"perm={c['perm']} tab={c['tab']} mode={c['mode']} L={c['L']} d={c['d']} c={','.join(map(str,c['c']))}\n" in s
    # full decryption with the planted parameters, re-derived from the crib block 1 key values only
    T=KA if c['tab']=="KA" else AZ; P=[int(x) for x in perms[c['perm']]]; ct=c['ct']
    def kat(i,p): q=T.index(p); x=T.index(ct[P[i]]); return (x-q)%26 if c['mode']=="Vig" else (x+q)%26
    crib="EASTNORTHEASTBERLINCLOCK"; k={21+n:kat(21+n,crib[n]) for n in range(13)}; L=c['L']
    for i in range(34,97): k[i]=(sum(c['c'][j]*k[i-1-j] for j in range(L))+c['d'])%26
    # backward not needed for check of positions 34-96; decrypt those
    pt="".join(T[(T.index(ct[P[i]])-k[i])%26] if c['mode']=="Vig" else T[(k[i]-T.index(ct[P[i]]))%26] for i in range(34,97))
    res.append(dict(ctl=c['ctl'],name=c['name'],hits=s.count("HIT "),planted_found=planted,decrypt_34_96=pt,in_source=pt in src))
S["controls"]=res
print(json.dumps(S,indent=1)); json.dump(S,open("cycle80_summary.json","w"),indent=1)
