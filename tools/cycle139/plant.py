"""Cycle 139 controls: PT-fed autokey, keyed cipher alphabet y, random plaintext alphabet x,
key read through y, A-Z, KRYPTOS or x; random primer. Independently encrypted here.
Nulls: shuffled K4, seeds 13901-13902."""
import importlib.util, random
import numpy as np
spec=importlib.util.spec_from_file_location("p137","/tmp/kcf/tools/cycle137/plant.py"); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
AZ, keyed, move, K4 = m.AZ, m.keyed, m.move, m.K4
R=random.Random(13900)
def rx():
    l=list(AZ); R.shuffle(l); return "".join(l)
def enc(text, L, yal, xal, zal, form):
    primer="".join(R.choice(AZ) for _ in range(L)); out=[]
    for i,p in enumerate(text):
        k = primer[i] if i<L else text[i-L]
        z = (xal if zal is None else zal).index(k)
        v = xal.index(p)+z if form==0 else xal.index(p)-z
        out.append(yal[v%26])
    return "".join(out)
if __name__=="__main__":
    P=m.plain(); B=np.fromfile("/home/box/kryptos_support_backup/perms97.bin",dtype=np.int16).reshape(-1,97)
    print("ctl1", enc(P,4,keyed("PALIMPSEST"),rx(),keyed("PALIMPSEST"),0))                     # direct z=y vig L4
    print("ctl2", move(enc(P,3,keyed("KRYPTOS"),rx(),AZ,1),B[4242]))                            # model Q z=AZ variant L3
    print("ctl3", enc(move(P,np.argsort(B[99999])),6,keyed("BERLIN"),rx(),None,0))                  # carved z=x sum L6
    print("ctl4", enc(P,3,keyed("CLOCK"),rx(),None,1))                                          # direct z=x diff L3
    print("ctl5", move(enc(P,2,keyed("SHADOW"),rx(),keyed("KRYPTOS"),0),B[160000]))             # model Q z=KRYPTOS vig L2
    print("ctl6", enc(move(P,np.argsort(B[99999])),6,keyed("BERLIN"),rx(),None,1))                  # carved z=x diff L6
    for z in (1,2):
        l=list(K4); random.Random(13900+z).shuffle(l); print(f"null{z}","".join(l))
