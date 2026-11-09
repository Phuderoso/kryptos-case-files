"""Cycle 158: how much of the word-pair space was already covered by free-key exclusions (case 144 direct ranges and bank pairs,
case 132 via lcm(k1, n, k2) inside its tested key periods). Counts ordered (f, e) word pairs; k1 = len(e) (plaintext side), k2 = len(f)."""
from math import lcm
from collections import Counter
def cnt(fn): return Counter(len(w) for w in open(fn).read().split())
A=cnt("all.txt"); C=cnt("core.txt")
ns4=[(9,11),(10,11),(11,12),(12,11)]  # case 144 direct n 2 NO-SIGNAL (not excluded)
def dcov(n,k1,k2):
    if n==2: return 2<=k1<=12 and 2<=k2<=12 and (k1,k2) not in ns4
    if n==3: return 2<=k1<=8 and 2<=k2<=5
    if n==4: return 2<=k1<=3 and 2<=k2<=3
c132={2:14,3:10,4:4}
bank144={(2,9),(3,5),(3,7),(3,8),(3,9),(4,5),(4,7),(5,3),(5,4),(5,6),(5,7),(6,5),(7,3),(7,4),(7,5),(8,3),(9,2),(9,3)}
def bcov(n,k1,k2):
    L=lcm(k1,n,k2)
    if n==2 and (L<=14 or (k1,k2) in bank144): return True
    if n==3 and L in (1,2,3,6,9): return True   # case 132 bank n 3 periods (I-012 reconciliation)
    if n==4 and L in (1,2,4): return True
    return False
for n in (2,3,4):
    tot=sum(A[a]*A[b] for a in A for b in A); cov=sum(A[a]*A[b] for a in A for b in A if dcov(n,b,a))
    tb=sum(C[a]*C[b] for a in C for b in C); cb=sum(C[a]*C[b] for a in C for b in C if bcov(n,b,a))
    print("n=%d direct: %d of %d word pairs (%.1f%%) inside case-144 free-key exclusions -> %.1f%% new; bank core-32: %d of %d (%.1f%%) covered -> %.1f%% new"%(n,cov,tot,100*cov/tot,100-100*cov/tot,cb,tb,100*cb/tb,100-100*cb/tb))
