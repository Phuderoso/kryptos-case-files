"""Cycle 114: the Kryha cipher machine (new family).

Source (precise text): J.-F. Bouchaudy, "How the Kryha works", http://www.jfbouch.fr/crypto/kryha/working.html
(accessed 2026-11-05), which follows P. Marks, "Operational Use and Cryptanalysis of the Kryha Cipher Machine",
Cryptologia 35(2):114-155 (2011), and Deavours & Kruh, Machine Cryptography and Modern Cryptanalysis (1985);
mechanism also in US patent 1,744,347 (Kryha, "Coding machine").

Model.  A fixed alphabet F (plain side) faces a movable alphabet M (cipher side).  With the movable ring turned
s positions:  c = M[F^-1(p) + sigma*s]  (sigma = +-1 covers ring direction, which alphabet carries the plaintext,
and encrypt/decrypt mode once F and M are free or range over a list that is closed enough).  Per letter the ring
advances by a step and the shifts are cumulative mod 26.
  V1 (removable code wheel): the wheel advances one sector per letter; step = teeth(sector) + 4.
      Published wheels (Marks via Bouchaudy): 15, 17 (standard), 18, 19, 23 sectors.
  V2 (universal disk): 52 sectors with fixed tooth counts; screws open a set H of holes; one step = all teeth
      from the current open hole to the next one (no +4: Bouchaudy's worked example 6,10,7,10,3).
'Shift before/after encryption' only moves the start sector/hole by one, so it is absorbed by the start setting;
the initial ring position is absorbed by s0.
"""
import random
A26="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
WHEELS={15:[2,1,2,7,5,4,2,4,6,9,5,8,4,3,2], 17:[3,2,3,1,2,3,2,4,2,6,1,2,1,3,2,1,5],
        18:[3,3,5,6,5,4,5,1,3,4,4,2,5,4,5,6,2,2], 19:[1,2,3,4,1,2,4,1,3,2,1,2,5,3,1,2,1,3,5],
        23:[2,5,4,6,2,5,3,4,6,3,5,4,6,2,3,5,6,1,3,2,1,3,6]}
V2TEETH=[4,3,4,3,3,3,4,3,4,4,3,3, 3,3,4,4,3,3,4,3,3,4,3,3, 4,3,3,4,4,4,3,3,4,3,3,3, 4,3,4,3,3,4,5,3,3,3,3,4, 3,3,4,5]
assert len(V2TEETH)==52
K4=open('/tmp/kcf/data/k4.txt').read().strip(); assert len(K4)==97
PT="WEDUGTHROUGHTHERUBBLE"+"EASTNORTHEAST"+"ANDFOUNDTHEDOORUNDERTHEOLDBRI"+"BERLINCLOCK"+"TOWERASTHESUNWENTDOWNXX"
CRIBS=[(21+i,c) for i,c in enumerate("EASTNORTHEAST")]+[(63+i,c) for i,c in enumerate("BERLINCLOCK")]
assert len(PT)==97 and all(PT[i]==c for i,c in CRIBS)
def idx(s): return [A26.index(c) for c in s]

def v1_shifts(wheel,start,n=97):
    """s_i (before sigma) for letter i; advance after each letter, sector start+i used between i and i+1."""
    w=WHEELS[wheel] if isinstance(wheel,int) else wheel; L=len(w); s=[0]
    for i in range(n-1): s.append((s[-1]+w[(start+i)%L]+(4 if isinstance(wheel,int) else 0))%26)
    return s
def kryha_enc(pt,F,M,shifts,sigma):
    fi={c:i for i,c in enumerate(F)}
    return "".join(M[(fi[p]+sigma*shifts[i])%26] for i,p in enumerate(pt))
def kryha_dec(ct,F,M,shifts,sigma):
    mi={c:i for i,c in enumerate(M)}
    return "".join(F[(mi[c]-sigma*shifts[i])%26] for i,c in enumerate(ct))

# ---------- exact feasibility with FREE alphabets: m(c) - f(p) = sigma*s_i  (weighted union-find + injectivity)
def free_feasible(ct,eqs):
    """eqs: list of (pletter, cletter, value): m(c)-f(p) = value mod 26.  True iff some pair of permutations
    (f = F^-1, m = M^-1) satisfies every equation (exact: potentials + injective component placement)."""
    par={}; pot={}  # pot[x] = value(x) - value(parent)
    # simpler: recursive find with potentials
    def fnd(x):
        if x not in par: par[x]=x; pot[x]=0
        if par[x]==x: return x,0
        r,pr=fnd(par[x]); pot[x]=(pot[x]+pr)%26; par[x]=r; return r,pot[x]
    def union(a,b,v):  # value(a)-value(b)=v
        ra,pa=fnd(a); rb,pb=fnd(b)
        if ra==rb: return (pa-pb-v)%26==0
        # value(a)=pa+R(ra), value(b)=pb+R(rb): R(ra)-R(rb)=v-pa+pb
        par[ra]=rb; pot[ra]=(v-pa+pb)%26; return True
    for e in eqs:
        p,c,v=e[0],e[1],e[2]
        if not union(('C',c),('P',p),v): return False
    # injectivity: group nodes by component
    comps={}
    for x in list(par):
        r,px=fnd(x); comps.setdefault(r,[]).append((x,px))
    groups=[]
    for r,mem in comps.items():
        P=[px for (x,px) in mem if x[0]=='P']; C=[px for (x,px) in mem if x[0]=='C']
        if len(set(P))<len(P) or len(set(C))<len(C): return False
        groups.append((P,C))
    # assign offsets to components so that all P values distinct and all C values distinct (exact backtracking)
    groups.sort(key=lambda g:-(len(g[0])+len(g[1])))
    usedP=set(); usedC=set()
    def bt(k):
        if k==len(groups): return True
        P,C=groups[k]
        for o in range(26 if k else 1):
            sp={(x+o)%26 for x in P}; sc={(x+o)%26 for x in C}
            if sp&usedP or sc&usedC: continue
            usedP.update(sp); usedC.update(sc)
            if bt(k+1): return True
            usedP.difference_update(sp); usedC.difference_update(sc)
        return False
    return bt(0)

def eqs_from_shifts(ct,shifts,sigma):
    return [(p,ct[i],(sigma*shifts[i])%26) for i,p in CRIBS]

def test_v1_published(ct):
    hits=[]
    for wl in WHEELS:
        for st in range(wl):
            s=v1_shifts(wl,st)
            for sg in (1,-1):
                if free_feasible(ct,eqs_from_shifts(ct,s,sg)): hits.append((wl,st,sg))
    return hits

def rand_alpha(R):
    a=list(A26); R.shuffle(a); return "".join(a)
