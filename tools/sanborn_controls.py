"""Cycle 72 audit: end-to-end controls built with SANBORN'S OWN conventions, not the solver's.
The substitution is the inverse of tools/solve_k1_k2_k3.py's vig_dec, which reproduces the carved K1 and K2
(asserted below), so a control passes only if the solver's KRYPTOS-tableau numbering, key-letter convention and
index frame agree with how K1/K2 were actually enciphered. Keys are Sanborn's real words."""
import random, sys, json, numpy as np
from kryptos_text import K1, K2, KA
from solve_k1_k2_k3 import vig_dec
assert vig_dec(K1,"PALIMPSEST").startswith("BETWEENSUBTLESHADING")
assert "ITWASTOTALLYINVISIBLE" in vig_dec(K2,"ABSCISSA")
def vig_enc(pt,key):  # inverse of vig_dec (key advances on letters only)
    return "".join(KA[(KA.index(c)+KA.index(key[i%len(key)]))%26] for i,c in enumerate(pt))
BASE=("SLOWLYDESPARATLYSLOWLYTHEREMAINSOFPASSAGEDEBRISTHATENCUMBEREDTHELOWERPARTOFTHEDOORWAYWEREREMOVEDWITH"
      "TREMBLINGHANDSIMADEATINYBREACHINTHEUPPERLEFTHANDCORNERANDTHENWIDENINGTHEHOLEALITTLEIINSERTEDTHECANDLE")
def plain(seed):
    r=random.Random(seed); s=r.randrange(0,len(BASE)-97); p=list(BASE[s:s+97])
    p[21:34]="EASTNORTHEAST"; p[63:74]="BERLINCLOCK"; return "".join(p)
CASES=[("PALIMPSEST",0,"A"),("ABSCISSA",None,"A"),("KRYPTOS",None,"B"),("PALIMPSEST",None,"B"),("ABSCISSA",0,"B"),("BERLIN",None,"A")]
if __name__=="__main__":
    perms=np.fromfile("perms97.bin",dtype=np.int16).reshape(-1,97)
    idx=int(sys.argv[1]); key,pi,model=CASES[idx]; r=random.Random(7200+idx)
    if pi is None: pi=r.randrange(len(perms))
    P=perms[pi]; pt=plain(7200+idx)
    if model=="A":   # substitute in plaintext order, then move letters: carved[P[i]] = E(pt)[i]
        e=vig_enc(pt,key); car=[None]*97
        for i in range(97): car[P[i]]=e[i]
    else:            # move letters first, then substitute in carved order: carved = E(pt[P[j]])
        car=list(vig_enc("".join(pt[P[j]] for j in range(97)),key))
    print("".join(car)); print(json.dumps(dict(case=idx,key=key,perm=pi,model=model,pt=pt)),file=sys.stderr)
