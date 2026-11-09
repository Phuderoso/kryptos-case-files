"""Cycle 157 (IDEAS I-052): structure-matched shuffled nulls.
A shuffle of K4's 97 letters is accepted only if the 24 cipher letters under the cribs (positions 21-33, 63-73) have
exactly K4's repetition profile: 14 distinct letters with multiplicities {3, 2x8, 1x5}. Feasibility of the free-alphabet
union-find tests depends on the ciphertext only through the partition of the 24 crib positions by cipher letter, so these
nulls differ from K4 only in WHICH positions share a letter, not in how many repeats there are.
usage: mknulls157.py N [seedbase=15700000]   -> lines 'mnullNN SHUFFLE seed profile'; also profiles of the cycle-155 nulls."""
import random,sys
from collections import Counter
K4=open(sys.argv[3] if len(sys.argv)>3 else 'k4.txt').read().strip()
POS=list(range(21,34))+list(range(63,74))
def prof(s): return sorted(Counter(s[i] for i in POS).values(),reverse=True)
N=int(sys.argv[1]); base=int(sys.argv[2]) if len(sys.argv)>2 else 15700000
P=prof(K4); got=0; s=0; tried=0
while got<N:
    l=list(K4); random.Random(base+s).shuffle(l); t=''.join(l); tried+=1
    if prof(t)==P:
        got+=1; print(f"mnull{got:02d} {t} seed={base+s} distinct={len(P)} profile={'-'.join(map(str,P))}")
    s+=1
print(f"# accepted {N} of {tried} shuffles ({N/tried:.4f}); K4 profile {'-'.join(map(str,P))}",file=sys.stderr)
