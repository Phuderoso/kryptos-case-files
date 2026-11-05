# Cycle 87 audit: numberworld "W-split parity groups have identical letter-frequency histogram shape"
# Preregistered rule (from the blog): split at every occurrence of a letter L, number blocks 1..n,
# group odd blocks vs even blocks; event = equal group lengths AND identical sorted count vectors.
import random, collections, sys, json
K4="OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR"
assert len(K4)==97
def groups(t,L):
    bl=t.split(L); g=["".join(bl[0::2]),"".join(bl[1::2])]; return g
def shape(s): return tuple(sorted(collections.Counter(s).values(),reverse=True))
def event(t,L,need_eq_len=True):
    a,b=groups(t,L)
    if need_eq_len and len(a)!=len(b): return False
    return shape(a)==shape(b)
print("K4 W groups:",[len(x) for x in groups(K4,"W")],shape(groups(K4,"W")[0]),shape(groups(K4,"W")[1]))
hits=[L for L in sorted(set(K4)) if K4.count(L)>=2 and event(K4,L)]
print("letters in real K4 giving event:",hits)
rng=random.Random(87); N=int(sys.argv[1]) if len(sys.argv)>1 else 200000
ev_W=0; eqlen_W=0; shape_given_eq=0; anyL=0
lst=list(K4)
for i in range(N):
    rng.shuffle(lst); t="".join(lst)
    a,b=groups(t,"W")
    if len(a)==len(b):
        eqlen_W+=1
        if shape(a)==shape(b): shape_given_eq+=1
    if any(event(t,L) for L in set(t) if t.count(L)>=2): anyL+=1
# conditional: random 46/46 split of the 92 non-W letters
nw=[c for c in K4 if c!="W"]; cond=0; M=N
for i in range(M):
    rng.shuffle(nw)
    if shape(nw[:46])==shape(nw[46:]): cond+=1
res=dict(N=N,P_eqlen_W=eqlen_W/N,P_event_W=shape_given_eq/N,P_shape_given_eqlen_W=(shape_given_eq/eqlen_W if eqlen_W else None),
         P_event_any_split_letter=anyL/N,P_shape_random_46_46_split=cond/M)
print(json.dumps(res,indent=1)); json.dump(res,open("results87.json","w"),indent=1)
