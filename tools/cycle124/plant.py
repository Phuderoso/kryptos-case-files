"""Cycle 124 planted controls (independent textbook encryptors) + shuffled-K4 nulls.
Textbook keyword columnar: write row-wise in width len(key), read whole columns in alphabetical key order (ties left to right).
Row variant: write row-wise, read each row with its columns in key order (short last row: present columns only)."""
import random
K4="OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR"
KA="KRYPTOSABCDEFGHIJLMNQUVWXZ"; AZ="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
def kworder(k): return sorted(range(len(k)),key=lambda i:(k[i],i))   # column read first, second, ...
def columnar(t,k):
    w=len(k); return "".join(t[i] for c in kworder(k) for i in range(c,len(t),w))
def rowread(t,k):
    w=len(k); o=kworder(k); return "".join(t[r+c] for r in range(0,len(t),w) for c in o if r+c<len(t))
def inv(f,t,k):
    n=len(t)
    pos=[ord(ch)-200 for ch in f("".join(chr(i+200) for i in range(n)),k)]  # pos[m]=source index of output m
    out=[None]*n
    for m,p in enumerate(pos): out[p]=t[m]
    return "".join(out)
def sub(t,key,alpha,beau,start=0):
    a=alpha; r=[]
    for i,ch in enumerate(t):
        k=a.index(key[(i+start)%len(key)]); p=a.index(ch)
        r.append(a[(k-p)%26] if beau else a[(p+k)%26])
    return "".join(r)
def plain():
    # build exact 97 with cribs at official positions
    p=list("X"*97); p[21:34]="EASTNORTHEAST"; p[63:74]="BERLINCLOCK"
    filler="SLOWLYDESPARATLYSLOWLYTHEREMAINSOFPASSAGEDEBRISTHATENCUMBEREDTHELOWERPARTOFTHEDOORWAYWASREMOVEDWITHTREMBLINGHANDSIMADEATINYBREACH"
    it=iter(filler)
    for i in range(97):
        if p[i]=="X": p[i]=next(it)
    return "".join(p)
if __name__=="__main__":
    P=plain(); assert P[21:34]=="EASTNORTHEAST" and P[63:74]=="BERLINCLOCK"
    # ctl1: Vig KA key KRYPTOS (p7) applied first (model A), then columnar PALIMPSEST (w10)
    print("ctl1",columnar(sub(P,"KRYPTOS",KA,0),"PALIMPSEST"))
    # ctl2: columnar LODESTONE (w9) first, then Beaufort AZ key with period 11 on ciphertext positions (model B)
    print("ctl2",sub(columnar(P,"LODESTONE"),"SHADOWFORCE",AZ,1))
    # ctl3: row read with key UNDERGRUND (w10), then Vig AZ key ABSCISSA (model B)
    print("ctl3",sub(rowread(P,"UNDERGRUND"),"ABSCISSA",AZ,0))
    # ctl4: inverse columnar NORTHEAST (w9, ciphertext written into grid) after Vig KA key with period 16 (model A)
    print("ctl4",inv(columnar,sub(P,"ILLUSIONDIGETALQ",KA,0),"NORTHEAST"))
    for s in range(1,4):
        l=list(K4); random.Random(124+s).shuffle(l); print(f"null{s}","".join(l))
