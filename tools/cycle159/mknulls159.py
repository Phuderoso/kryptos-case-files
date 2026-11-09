"""Cycle 159 (IDEAS I-057): shuffled nulls matched to K4 on BOTH
  (a) the repetition profile of the 24 cipher letters under the cribs (positions 21-33, 63-73; K4 3-2x8-1x5, 14 distinct), and
  (b) the cycle rank r of the model-P crib graph at period L (cipher-letter nodes <-> group-offset nodes, group = (pos//L) % L).
Rejection sampling of plain shuffles of K4's 97 letters (seeds base, base+1, ...). Also prints r at L 9, 11, 12 for reference.
usage: mknulls159.py N [seedbase=15900000] [k4.txt] [L=8]  -> lines 'rnullNN SHUFFLE seed=.. r8=.. r9=.. r11=.. r12=..'"""
import random,sys
from collections import Counter
POS=list(range(21,34))+list(range(63,74))
def prof(s): return sorted(Counter(s[i] for i in POS).values(),reverse=True)
def rank(t,L):
    par={}
    def f(x):
        while par.setdefault(x,x)!=x: x=par[x]
        return x
    nodes=set()
    for i in POS:
        a=('c',t[i]); b=('o',(i//L)%L); nodes|={a,b}; ra,rb=f(a),f(b)
        if ra!=rb: par[ra]=rb
    comps=len({f(x) for x in nodes}); return len(POS)-len(nodes)+comps
if __name__=='__main__':
    N=int(sys.argv[1]); base=int(sys.argv[2]) if len(sys.argv)>2 else 15900000
    K4=open(sys.argv[3] if len(sys.argv)>3 else 'k4.txt').read().strip(); L=int(sys.argv[4]) if len(sys.argv)>4 else 8
    P=prof(K4); R=rank(K4,L); got=0; s=0; tried=0; pm=0
    while got<N:
        l=list(K4); random.Random(base+s).shuffle(l); t=''.join(l); tried+=1; s+=1
        if prof(t)!=P: continue
        pm+=1
        if rank(t,L)!=R: continue
        got+=1; print(f"rnull{got:02d} {t} seed={base+s-1} profile={'-'.join(map(str,P))} "+' '.join(f"r{x}={rank(t,x)}" for x in (8,9,11,12)))
    print(f"# K4 profile {'-'.join(map(str,P))} r{L}={R}; shuffles {tried}, profile-matched {pm} ({pm/tried:.4f}), also r-matched {N} ({N/pm:.3f} of profile-matched)",file=sys.stderr)
