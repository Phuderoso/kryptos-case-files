"""Cycle 31: disk sets for generalized cylinder test.
THEMED: keyword-mixed alphabets (K1-K3 / KRYPTOS style: keyword letters de-duplicated, then the rest of A-Z in order)
from a list of plain-sight words fixed BEFORE running (preregistered here). M94: the 25 published M-94 disks."""
WORDS = ["KRYPTOS","PALIMPSEST","ABSCISSA","BERLIN","CLOCK","BERLINCLOCK","EASTNORTHEAST","SHADOW","ILLUSION","IQLUSION",
         "LUCID","MEMORY","LANGLEY","SANBORN","SCHEIDT","WEBSTER","CARTER","EGYPT","TUTANKHAMUN","UNDERGRUUND",
         "LAYERTWO","DESPARATLY","DIGETAL","INTERPRETATU","POSITION","MAGNETIC","VIRGINIA","ANTIPODES","MORSE","SLOWLY"]
def kw(w):
    s=[]
    for c in w+"ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        if c not in s: s.append(c)
    return "".join(s)
def themed():
    out=[]
    for w in WORDS:
        a=kw(w)
        if a not in out: out.append(a)
    return out
def m94(): return [l.strip() for l in open("m94.txt") if l.strip()]
if __name__=="__main__":
    t=themed(); assert all(sorted(a)==list("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for a in t+m94())
    open("themed.txt","w").write("\n".join(t)+"\n"); print(len(t),"themed disks;",len(m94()),"M-94 disks")
