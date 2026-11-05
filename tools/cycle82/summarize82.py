import json,re
from mkctl82 import square,pf_dec,KA,AZ
crib="EASTNORTHEASTBERLINCLOCK"; cpos=list(range(21,34))+list(range(63,74))
from mkctl82 import pf_enc
def cons(f): return [int(x) for x in open(f).read().splitlines()[-1].split("cons_by_p=")[1].split(",")]
S={"K4":cons("r_k4.txt"),"nulls":{n:cons(f"r_null{n}.txt") for n in range(10)},"controls":[]}
for c in json.load(open("controls82.json")):
    s=open(f"r_ctl{c['ctl']}.txt").read()
    found=f"HIT word={c['word']} om={c['om']} fill={c['fill']} a={c['a']} tab={c['tab']} mode={c['mode']} p={c['p']} " in s
    # full decryption: recover key residues from cribs only, then undo outer key and Playfair
    sq=square(c['word'],c['om'],c['fill']); T=KA if c['tab']=="KA" else AZ; ct=c['ct']; p=c['p']; a=c['a']
    key={}
    pt=dict(zip(cpos,crib))
    for i in range(a,96,2):
        if i in pt and i+1 in pt:
            m1,m2=pf_enc(pt[i],pt[i+1],sq)
            for j,m in ((i,m1),(i+1,m2)):
                x,q=T.index(ct[j]),T.index(m); key[j%p]=(x-q)%26 if c['mode']==0 else (x+q)%26 if c['mode']==1 else (q-x)%26
    mid=[]
    for i,ch in enumerate(ct):
        k=key[i%p]; x=T.index(ch); q=(x-k) if c['mode']==0 else (k-x) if c['mode']==1 else (x+k); mid.append(T[q%26])
    out=mid[:]
    for i in range(a,96,2): out[i],out[i+1]=pf_dec(mid[i],mid[i+1],sq)
    dec="".join(out); S["controls"].append(dict(ctl=c['ctl'],word=c['word'],p=p,planted_found=found,key_residues_from_cribs=len(key),
        full_decrypt_matches_planted=dec==c['pt'],decrypt=dec))
json.dump(S,open("cycle82_summary.json","w"),indent=1)
for c in S["controls"]: print(c['word'],c['planted_found'],c['key_residues_from_cribs'],c['full_decrypt_matches_planted'],c['decrypt'][:50])
