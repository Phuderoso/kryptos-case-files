"""Cycle 72 audit, part 2: K3-law decimation + Sanborn-convention KA Vigenere (real key words), fed to cycle 59's
periodic_exact59. Perm semantics per decimation_gen.py: out[k] = carved index paired with PT position k."""
import numpy as np, json, sys
from sanborn_controls import vig_enc, plain
P=np.fromfile("dec_perm.bin",dtype=np.int16).reshape(-1,97)
cases=[(40780,"ABSCISSA",0),(40781,"PALIMPSEST",1),(40780,"KRYPTOS",1),(40781,"BERLIN",0)]
for n,(pi,key,order) in enumerate(cases):
    out=P[pi]; pt=plain(7300+n); car=[None]*97
    if order==0:   # key indexed by PT position: substitute, then place
        e=vig_enc(pt,key)
        for k in range(97): car[out[k]]=e[k]
    else:          # key indexed by carved position: place, then substitute in carved order
        for k in range(97): car[out[k]]=pt[k]
        car=list(vig_enc("".join(car),key))
    open(f"d{n}.txt","w").write("".join(car)+"\n")
    json.dump(dict(perm=pi,key=key,order=order,pt=pt),open(f"dm{n}.json","w"))
