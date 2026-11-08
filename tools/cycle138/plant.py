"""Cycle 138 controls: CT-fed autokey, key letter read through the random plaintext
alphabet x, cipher side keyed; independently encrypted in Python. Nulls: seeds 13801-13802."""
import importlib.util, random
import numpy as np
spec=importlib.util.spec_from_file_location("p137","/tmp/kcf/tools/cycle137/plant.py"); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
AZ, keyed, move, K4 = m.AZ, m.keyed, m.move, m.K4
def enc(text, primer, yal, xal, form):
    # form 0 SUM: y(c)=x(p)+x(k); 1 Beaufort: y(c)=x(k)-x(p); 2 variant: y(c)=x(p)-x(k)
    L=len(primer); out=[]
    for i,p in enumerate(text):
        k = primer[i] if i<L else out[i-L]
        xp, xk = xal.index(p), xal.index(k)
        v = xp+xk if form==0 else xk-xp if form==1 else xp-xk
        out.append(yal[v%26])
    return "".join(out)
if __name__=="__main__":
    P=m.plain(); B=np.fromfile("/home/box/kryptos_support_backup/perms97.bin",dtype=np.int16).reshape(-1,97)
    R=random.Random(13800)
    def rx():
        l=list(AZ); R.shuffle(l); return "".join(l)
    print("ctl1", enc(move(P,B[4242]),"SHADOWS",keyed("PALIMPSEST"),rx(),0))          # carved SUM L7
    print("ctl2", enc(move(P,np.argsort(B[99999])),"QWERTYUIOPAS",keyed("KRYPTOS"),rx(),1))  # carved Beaufort L12
    print("ctl3", move(enc(P,"LUCID",keyed("BERLIN"),rx(),2),B[160000]))              # model Q variant L5
    print("ctl4", enc(P,"ABCDEFGHIJKLMNOPQRST",keyed("CLOCK"),rx(),0))                # direct SUM L20
    print("ctl5", enc(P,"NORTH",AZ,rx(),1))                                           # direct Beaufort L5, y=A-Z
    for z in (1,2):
        l=list(K4); random.Random(13800+z).shuffle(l); print(f"null{z}","".join(l))
