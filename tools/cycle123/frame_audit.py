"""Cycle 123 audit: is the textbook keyword columnar (and its inverse) really inside the 165k bank perms97.bin,
in the frame progkw/cycle-41 assumes (model A: carved[P[i]] enciphers pt[i])?  Builds sigma with the
independent cycle-123 reference encryptor (rotations 0) and looks it up."""
import sys,numpy as np
sys.path.insert(0,'/tmp/kcf/tools/cycle123'); from plant import geom,kworder
B=np.fromfile(sys.argv[1],dtype=np.int16).reshape(-1,97); print("bank size",len(B))
idx={bytes(r.astype(np.int16).tobytes()):i for i,r in enumerate(B)}
words="KRYPTOS BERLIN CLOCK SHADOW PALIMPSEST ABSCISSA LAYERTWO COMPASS NORTHEAST LODESTONE".split()
for w_ in words:
    pi=kworder(w_); w=len(w_)
    for mode in ("COL","ROW"):
        place=geom(w,pi,[0]*w,mode)          # pt i -> ct place[i]  (textbook encryption, dir 0)
        inv=[0]*97
        for i,j in enumerate(place): inv[j]=i
        a=idx.get(np.array(place,dtype=np.int16).tobytes()); b=idx.get(np.array(inv,dtype=np.int16).tobytes())
        print(f"{w_:11s} {mode}: sigma(enc frame) idx={a}  sigma^-1 idx={b}")
