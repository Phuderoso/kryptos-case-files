"""Cycle 79 audit of cycle 45 (running keys behind rail fence / Redefence / AMSCO).
Transpositions are re-implemented here from the textbook (ACA) descriptions as STRING operations, independently of
tools/railamsco_gen.py; encipherment is Sanborn's verified K1/K2 rule (KA tableau, C = P + K in KA numbering).
Checks: (1) each textbook transposition is a member of the cycle-44 permutation family (perms_A/B.bin);
(2) planted running-key controls are recovered by the unchanged bookrk on a slice of that family."""
import random, json, re, numpy as np
from kryptos_text import KA, K1, K2
from solve_k1_k2_k3 import vig_dec
from sanborn_controls import plain
assert vig_dec(K1,"PALIMPSEST").startswith("BETWEENSUBTLESHADING")
def E(p,k): return KA[(KA.index(p)+KA.index(k))%26]
def keyorder(word):  # column read order: alphabetical, ties left to right
    return sorted(range(len(word)), key=lambda c:(word[c],c))
def rail(s,r):      # write zigzag starting on the top rail, read rails top to bottom
    rows=[[] for _ in range(r)]; y,d=0,1
    for ch in s:
        rows[y].append(ch)
        if r>1:
            if y==0: d=1
            elif y==r-1: d=-1
            y+=d
    return rows
def railfence(s,r): return "".join("".join(x) for x in rail(s,r))
def redefence(s,word):  # rails read in the order of a key word's letters
    rows=rail(s,len(word)); return "".join("".join(rows[c]) for c in keyorder(word))
def amsco(s,word,first,aca):  # aca=True: each row starts with the opposite cell size of the row above
    w=len(word); cols=[[] for _ in range(w)]; i=0; row=0; size=first
    while i<len(s):
        if aca: size=first if row%2==0 else 3-first
        for c in range(w):
            if i>=len(s): break
            cols[c].append(s[i:i+size]); i+=size; size=3-size
        row+=1
    return "".join("".join(cols[c]) for c in keyorder(word))
def perm_of(f):     # P[i] = carved position of plaintext letter i, derived by tracing distinct symbols
    idx=[chr(0x100+i) for i in range(97)]; out=f("".join(idx)); assert len(out)==97
    P=[0]*97
    for pos,ch in enumerate(out): P[ord(ch)-0x100]=pos
    return P
A=np.fromfile("/workspace/k4c44/perms_A.bin",dtype=np.int16).reshape(-1,97)
B=np.fromfile("/workspace/k4c44/perms_B.bin",dtype=np.int16).reshape(-1,97)
ALL=np.concatenate([A,B]); lookup={ALL[k].tobytes():k for k in range(len(ALL))}
TB=[("rail r=3",lambda s:railfence(s,3)),("rail r=7",lambda s:railfence(s,7)),("rail r=29",lambda s:railfence(s,29)),
    ("redefence CLOCK",lambda s:redefence(s,"CLOCK")),("redefence BERLIN",lambda s:redefence(s,"BERLIN")),("redefence KRYPTOS",lambda s:redefence(s,"KRYPTOS")),
    ("amsco KRYPTOS 1 cont",lambda s:amsco(s,"KRYPTOS",1,False)),("amsco BERLIN 2 aca",lambda s:amsco(s,"BERLIN",2,True)),
    ("amsco BERLIN 1 cont",lambda s:amsco(s,"BERLIN",1,False)),("amsco CLOCK 2 cont",lambda s:amsco(s,"CLOCK",2,False)),
    ("amsco SHADOW 1 aca",lambda s:amsco(s,"SHADOW",1,True)),("amsco NORTHEAST 1 cont",lambda s:amsco(s,"NORTHEAST",1,False)),
    ("amsco NORTHEAST 2 cont",lambda s:amsco(s,"NORTHEAST",2,False)),("amsco LUCID 1 cont",lambda s:amsco(s,"LUCID",1,False))]
mem=[]
for name,f in TB:
    P=np.array(perm_of(f),dtype=np.int16); inv=np.argsort(P).astype(np.int16)
    mem.append(dict(name=name,enc_index=lookup.get(P.tobytes()),dec_index=lookup.get(inv.tobytes())))
    print("member",name,mem[-1])
texts=dict(l.split() for l in open("/workspace/k4c45/texts.txt"))
# controls: (transposition, key text, model, offset rule)
PL=[(0,"carter1","A","rand"),(4,"carter1_rev","B","rand"),(6,"c34_K2pt_carved","A","rand"),(7,"carter1","B","end"),
    (11,"kjv_john","A","rand"),(12,"c34_K3pt_rev","B","rand"),(3,"c34_K123pt","A","rand")]
r=random.Random(7900); slice_idx=sorted(r.sample(range(len(ALL)),3000)); meta=[]
for n,(ti,tn,model,how) in enumerate(PL):
    rr=random.Random(7910+n); T=texts[tn]; pt=plain(7910+n)
    o=len(T)-97 if how=="end" else rr.randrange(len(T)-96)
    f=TB[ti][1]
    if model=="A":   # key letter i enciphers plaintext letter i, then the textbook transposition moves the letters
        sub="".join(E(pt[i],T[o+i]) for i in range(97)); car=f(sub)
    else:            # textbook transposition first, then key letter j enciphers carved position j
        t=f(pt); car="".join(E(t[j],T[o+j]) for j in range(97))
    open(f"ctl_{n}.txt","w").write(car)
    meta.append(dict(ctl=n,transposition=TB[ti][0],text=tn,model=model,offset=o,pt=pt,
        enc_index=mem[ti]["enc_index"],dec_index=mem[ti]["dec_index"]))
    for k in (mem[ti]["enc_index"],mem[ti]["dec_index"]):
        if k is not None and k not in slice_idx: slice_idx.append(k)
slice_idx=sorted(set(slice_idx)); ALL[slice_idx].tofile("slice.bin")
for m in meta: m["slice_pos"]={str(k):slice_idx.index(k) for k in (m["enc_index"],m["dec_index"]) if k is not None}
names=["carter1","carter1_rev","kjv_john","kjv_john_rev","c34_K2pt_carved","c34_K3pt_rev","c34_K123pt"]
open("texts79.txt","w").write("".join(f"{n} {texts[n]}\n" for n in names))
json.dump(dict(membership=mem,controls=meta,slice=slice_idx),open("controls79.json","w"),indent=1)
for m in meta: print(m["ctl"],m["transposition"],m["text"],m["model"],m["offset"],m["slice_pos"])
