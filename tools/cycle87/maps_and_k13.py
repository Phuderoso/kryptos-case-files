# Cycle 87: (a) the W-split event on 97-letter windows of the K1-K2 cipher panel (natural baseline);
# (b) is group 2's histogram a shift/reflection image of group 1's (AZ or KRYPTOS alphabet)? null: random relabelings.
import random, collections, json, re
K4=open('data/k4.txt').read().strip()
def groups(t,L): b=t.split(L); return "".join(b[0::2]),"".join(b[1::2])
def shape(s): return tuple(sorted(collections.Counter(s).values(),reverse=True))
def event(t,L):
    a,b=groups(t,L); return len(a)==len(b) and shape(a)==shape(b)
rows=open('data/elonka_panel_rows.txt').read().split()
panel=re.sub('[^A-Z]','',"".join(rows).split('ABCDEFGHIJKLMNOPQRSTUVWXYZ')[0])[:-1]
win=[panel[s:s+97] for s in range(len(panel)-96)]
wh=sum(any(event(w,L) for L in set(w) if w.count(L)>=2) for w in win)
g1,g2=groups(K4,"W"); c1,c2=collections.Counter(g1),collections.Counter(g2)
AZ="ABCDEFGHIJKLMNOPQRSTUVWXYZ"; KA="KRYPTOSABCDEFGHIJLMNQUVWXZ"
def best(c1,c2):
    return max(sum(1 for c in c1 if c2.get(al[(sg*al.index(c)+s)%26],0)==c1[c]) for al in (AZ,KA) for sg in (1,-1) for s in range(26))
real=best(c1,c2); rng=random.Random(87); vals=[]
for _ in range(3000):
    p=list(AZ); rng.shuffle(p); mp=dict(zip(AZ,p)); vals.append(best(c1,collections.Counter({mp[k]:v for k,v in c2.items()})))
print(json.dumps(dict(panel_letters=len(panel),windows=len(win),window_events=wh,map_real=real,
      map_null_median=sorted(vals)[1500],map_null_max=max(vals),p_ge=sum(v>=real for v in vals)/3000),indent=1))
