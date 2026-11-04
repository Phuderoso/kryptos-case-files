"""Cycle 46: Myszkowski transposition (keyword with repeated letters; tied columns are read together,
row by row, left to right). Every rank pattern with at least one tie for widths 3-8 (all-distinct patterns
are plain columnar, tested since cycle 13), plus themed keywords with repeated letters at widths 9-18.
Writes P with P[i] = carved position of plaintext letter i (encryption), plus each inverse."""
import numpy as np, sys
N=97
def weak_orders(w):
    # all rank vectors r in 0..k-1 surjective
    res=[]
    def rec(pre,mx):
        if len(pre)==w:
            if mx+1>0 and len(set(pre))==mx+1: res.append(tuple(pre))
            return
        for v in range(mx+2): rec(pre+[v],max(mx,v))
    rec([],-1)
    # rec only produces restricted-growth strings; need all surjections onto 0..k-1
    return res
def all_rank_vectors(w):
    import itertools
    out=set()
    for rgs in weak_orders(w):  # set partition (blocks labelled by first appearance)
        k=max(rgs)+1
        if k==w: continue       # no tie -> plain columnar
        for perm in itertools.permutations(range(k)):
            out.add(tuple(perm[b] for b in rgs))
    return sorted(out)
def mysz(ranks):
    w=len(ranks); out=[]
    rows=(N+w-1)//w
    for v in sorted(set(ranks)):
        cols=[c for c in range(w) if ranks[c]==v]
        for r in range(rows):
            for c in cols:
                i=r*w+c
                if i<N: out.append(i)
    P=[0]*N
    for k,i in enumerate(out): P[i]=k
    return P
THEMED=["PALIMPSEST","EASTNORTHEAST","BERLINCLOCK","UNDERGROUND","UNDERGRUUND","SHADOWFORCES","DESPARATLY",
 "TUTANKHAMEN","HOWARDCARTER","NORTHEAST","INVISIBLE","VIRTUALLYINVISIBLE","MAGNETICFIELD","BERLINWALL",
 "LUCIDMEMORY","IQLUSIONABSCISSA","KRYPTOSABSCISSA","KRYPTOSPALIMPSEST","SANBORNSCHEIDT","LANGLEYVIRGINIA",
 "WHATSTHEPOINT","CANDLEFLAME","SLOWLYDESPARATLY","WORLDCLOCK","DELIVERINGAMESSAGE","EGYPTIANTOMB","WELTZEITUHR",
 "EDWARDSCHEIDT","JAMESSANBORN","ALEXANDERPLATZ","CHECKPOINTCHARLIE","THEPOINT","EASTERLY","MESSAGE"]
seen=set(); res=[]; tags=[]
def add(P,tag):
    for Q,t in ((P,tag+"/enc"),(list(np.argsort(P)),tag+"/dec")):
        key=np.array(Q,dtype=np.int16).tobytes()
        if key in seen: continue
        seen.add(key); res.append(Q); tags.append(t)
add(list(range(N)),"identity")
for w in range(3,9):
    for r in all_rank_vectors(w): add(mysz(r),f"mysz w={w} ranks={''.join(map(str,r))}")
for kw in THEMED:
    if len(set(kw))==len(kw): continue
    r=[sorted(set(kw)).index(c) for c in kw]
    add(mysz(r),f"mysz kw={kw}")
    r2=[sorted(set(kw),key="KRYPTOSABCDEFGHIJLMNQUVWXZ".index).index(c) for c in kw]
    add(mysz(r2),f"mysz kw={kw} KAorder")
np.array(res,dtype=np.int16).tofile("perms_M.bin")
open("perms_M.txt","w").write("\n".join(tags)+"\n")
print(len(res))
