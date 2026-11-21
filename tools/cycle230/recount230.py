import sys; sys.path.insert(0,'../src'); import analyze230 as a, numpy as np
ct=open('k4.txt').read().strip(); X=a.ALPHA[7623]; xinv={v:i for i,v in enumerate(X)}
xs=np.array([xinv[ord(c)-65] for c in a.CRS])
Y=np.array(a.ALPHA); n=len(Y); yinv=np.zeros((n,26),dtype=int); yinv[np.arange(n)[:,None],Y]=np.arange(26)[None,:]
cc=np.array([ord(ct[i])-65 for i in a.CRP]); ys=yinv[:,cc]
tot=0; keys=set()
for f in range(3):
    k=((ys-xs)%26 if f==0 else (xs-ys)%26 if f==1 else (ys+xs)%26)
    for y in range(n):
        s=set(k[y].tolist()); w,p=a.width_pop(list(s)) if False else a.width_pop(k[y].tolist())
        if w<=14 or p<=12: keys.add((7623,y,f,w,p))
lines,T=a.parse("R/recount_slice_X7623.txt")
c={(l[2],l[3],l[4],l[5],l[6]) for l in lines}
print("python",len(keys),"C",len(c),"equal",keys==c)
d=keys^c
print("diff cells",len(d),"min width among diffs",min(t[3] for t in d),"(loosened WMAX 14 / DMAX 12 test; tool exact only for width <= 13)")
sub=lambda S,W,P:{t for t in S if t[3]<=W or t[4]<=P}
print("restricted to registered thresholds (W<=10, D<=6): equal", sub(keys,10,6)==sub(c,10,6), len(sub(keys,10,6)))
