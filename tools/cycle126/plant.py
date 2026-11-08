"""Cycle 126 planted controls (independent textbook encryptors from cycle 124's plant.py) for Quagmire I/II
behind arbitrary w 9-10 orders and a w 11 control; shuffled-K4 nulls (seeds 12601-12603)."""
import random,sys,os
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','cycle124'))
from plant import columnar,rowread,inv,plain,K4,KA,AZ
def quag(t,key,PA,CA,beau,keyalpha):
    out=[]
    for i,ch in enumerate(t):
        k=keyalpha.index(key[i%len(key)]); p=PA.index(ch)
        out.append(CA[(k-p)%26] if beau else CA[(p+k)%26])
    return "".join(out)
if __name__=="__main__":
    P=plain()
    # ctl1: Quagmire I (pt KA, ct AZ), Vig, key SANBORN (p7) before columnar PALIMPSEST w10   [key letters read on the cipher alphabet]
    print("ctl1",columnar(quag(P,"SANBORN",KA,AZ,0,AZ),"PALIMPSEST"))
    # ctl2: columnar LODESTONE w9 then Quagmire II (pt AZ, ct KA) Beaufort key CLOCKFACE (p9) on carved positions
    print("ctl2",quag(columnar(P,"LODESTONE"),"CLOCKFACE",AZ,KA,1,KA))
    # ctl3: row read SHADOWLESS w10 then Quagmire I Vig key EAST (p4)
    print("ctl3",quag(rowread(P,"SHADOWLESS"),"EAST",KA,AZ,0,AZ))
    # ctl4: w11 columnar UNDERGROUND then Vig AZ key ILLUSION (p8)
    print("ctl4",quag(columnar(P,"UNDERGROUND"),"ILLUSION",AZ,AZ,0,AZ))
    for s in range(1,4):
        l=list(K4); random.Random(12600+s).shuffle(l); print(f"null{s}","".join(l))
