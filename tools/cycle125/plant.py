"""Cycle 125: independent Digrafid reference encryptor (ACA), planted controls, shuffled-K4 nulls.
Controls are 96-letter plaintexts (cribs at official positions, shifted for the null) encrypted, then a null
letter is inserted at carved position d (model A); one control drops a letter from a 98-letter cipher (model B)."""
import random
K4="OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR"
def alpha(w):
    s=[]
    for c in w+"ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        if c not in s: s.append(c)
    return "".join(s)+"#"
def grids(k1,k2,fill2):
    a1,a2=alpha(k1),alpha(k2)
    g1={a1[t]:(t//9,t%9) for t in range(27)}; G1=[[a1[r*9+c] for c in range(9)] for r in range(3)]
    if fill2==0: g2={a2[t]:(t%9,t//9) for t in range(27)}
    else: g2={a2[t]:(t//3,t%3) for t in range(27)}
    G2=[[None]*3 for _ in range(9)]
    for ch,(r,c) in g2.items(): G2[r][c]=ch
    return g1,G1,g2,G2
def encrypt(pt,k1,k2,p,fill2=0):
    g1,G1,g2,G2=grids(k1,k2,fill2); out=[]
    pairs=[pt[i:i+2] for i in range(0,len(pt),2)]
    for b in range(0,len(pairs),p):
        blk=pairs[b:b+p]; rows=[[],[],[]]
        for a,c in blk:
            ra,ca=g1[a]; rb,cb=g2[c]; rows[0].append(ca); rows[1].append(3*ra+cb); rows[2].append(rb)
        seq=rows[0]+rows[1]+rows[2]
        for i in range(0,len(seq),3):
            x,m,y=seq[i:i+3]; out.append(G1[m//3][x]+G2[y][m%3])
    return "".join(out)
FILL="SLOWLYDESPARATLYSLOWLYTHEREMAINSOFPASSAGEDEBRISTHATENCUMBEREDTHELOWERPARTOFTHEDOORWAYWASREMOVEDWITHTREMBLINGHANDS"
def plain(n,shift_after=None):
    p=["?"]*n; c1,c2=21,63
    if shift_after is not None: c1-= (21>shift_after); c2-= (63>shift_after)
    p[c1:c1+13]="EASTNORTHEAST"; p[c2:c2+11]="BERLINCLOCK"; it=iter(FILL)
    return "".join(ch if ch!="?" else next(it) for ch in p)
if __name__=="__main__":
    r=random.Random(125)
    for name,k1,k2,p,fill2,d in [("ctl1","KRYPTOS","PALIMPSEST",7,0,50),("ctl2","SHADOW","SHADOW",12,0,96),("ctl3","DIGRAFID","BERLINCLOCK",5,1,10)]:
        pt=plain(96,d); ct=encrypt(pt,k1,k2,p,fill2); assert '#' not in pt
        carved=ct[:d]+"Q"+ct[d:]; print(name,carved,k1,k2,p,fill2,"A",d)
    pt=plain(98); ct=encrypt(pt,"LODESTONE","KRYPTOS",9,0); print("ctl4",ct[:97],"LODESTONE","KRYPTOS",9,0,"B",97)
    for s in range(1,4):
        l=list(K4); random.Random(12500+s).shuffle(l); print(f"null{s}","".join(l))
