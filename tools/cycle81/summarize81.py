import json,glob,re
import numpy as np
from kryptos_text import KA
AZ="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
perms=np.fromfile("perms97.bin",dtype=np.int16).reshape(-1,97)
def cnt(pat):
    h=t=0
    for f in glob.glob(pat):
        s=open(f).read(); h+=s.count("HIT "); t+=int(re.search(r"tests=(\d+)",s).group(1))
    return h,t
S={"k4_behind_perms_L1_4":cnt("r_k4_[0-7].txt"),"k4_L5_perms_0_19999":cnt("r_k4L5_*.txt"),
   "nulls_behind_perms_L4":{f"null{n}":cnt(f"r_null{n}_*.txt") for n in range(5)},"controls":[]}
crib="EASTNORTHEASTBERLINCLOCK"
for c in json.load(open("controls81.json")):
    s=open(f"r_ctl{c['ctl']}.txt").read()
    key=f"perm={c['perm']} tab={c['tab']} mode={c['mode']} L={c['L']} d={c['d']} c={','.join(map(str,c['c']))}\n"
    T=KA if c['tab']=="KA" else AZ; P=[int(x) for x in perms[c['perm']]]; ct=c['ct']; L=c['L']
    def kat(i,p): q=T.index(p); x=T.index(ct[P[i]]); return (x-q)%26 if c['mode']=="Vig" else (x+q)%26
    k={21+n:kat(21+n,crib[n]) for n in range(13)}
    for i in range(34,97): k[i]=(sum(c['c'][j]*k[i-1-j] for j in range(L))+c['d'])%26
    pt="".join(T[(T.index(ct[P[i]])-k[i])%26] if c['mode']=="Vig" else T[(k[i]-T.index(ct[P[i]]))%26] for i in range(34,97))
    S["controls"].append(dict(ctl=c['ctl'],name=c['name'],hits=s.count("HIT "),planted_found=key in s,decrypt_34_96=pt))
print(json.dumps(S,indent=1)); json.dump(S,open("cycle81_summary.json","w"),indent=1)
