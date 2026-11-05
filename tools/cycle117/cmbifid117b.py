"""Cycle 117 part B: CM-Bifid with the INPUT square S1 a keyword square (524) and the output square S2 completely free.
With S1 known, every cribbed plaintext letter puts its row and column into the block's coordinate stream; each ciphertext
letter's (row, col) is a pair of stream digits.  Exact test: per ciphertext letter the known rows (cols) must agree, and
an injective letter->cell completion must exist (bipartite matching).  Periods 1-92, orientation 0, W-free text.
Controls: planted CM-Bifid with keyword S1, random S2."""
import random, sys
sys.argv=[sys.argv[0]]
from cmbifid117 import A25, KW, CR, SQ, enc
CRD=dict(CR)
def feasible(ct,S1,p):
    pos={c:(i//5,i%5) for i,c in enumerate(S1)}; N=len(ct); rowk={}; colk={}
    for b in range(0,N,p):
        L=min(p,N-b); d=[None]*(2*L)
        for i in range(L):
            c=CRD.get(b+i)
            if c: d[i],d[L+i]=pos[c]
        for j in range(L):
            x=ct[b+j]
            for D,v in ((rowk,d[2*j]),(colk,d[2*j+1])):
                if v is not None and D.setdefault(x,v)!=v: return False
    letters=sorted(set(ct)); allow={x:[r*5+c for r in range(5) for c in range(5) if rowk.get(x,r)==r and colk.get(x,c)==c] for x in letters}
    match={}
    def aug(x,seen):
        for y in allow[x]:
            if y in seen: continue
            seen.add(y)
            if y not in match or aug(match[y],seen): match[y]=x; return True
        return False
    return all(aug(x,set()) for x in letters)
def scan(ct): return [(p,si) for p in range(1,93) for si,S1 in enumerate(SQ) if feasible(ct,S1,p)]
if __name__=="__main__":
    R=random.Random(1172)
    h=scan(KW); print(f"K4: {len(h)} feasible (p, S1) of {92*len(SQ)}; periods {sorted(set(x[0] for x in h))}")
    for k in range(6):
        hn=scan("".join(R.sample(KW,92))); print(f"null{k}: {len(hn)} feasible; periods {sorted(set(x[0] for x in hn))}")
    PT0="WEDUGTHROUGHTHERUBBLE".replace('W','')
    pt=PT0[:20]+"EASTNORTHEAST"+"ANDFOUNDTHEDOORUNDERTHEOLDBRI"[:27]+"BERLINCLOCK"+"TOERASTHESUNENTDONXXX"; assert len(pt)==92
    for k,p in enumerate((28,30,7)):
        si=R.randrange(len(SQ)); S2="".join(R.sample(A25,25)); ct=enc(pt,SQ[si],S2,p); hc=scan(ct)
        print(f"ctl{k} p={p} S1#{si}: {len(hc)} feasible; true found {(p,si) in hc}; periods {sorted(set(x[0] for x in hc))}")
