# Planted Doppelkasten controls and shuffled nulls for cycle 68 (parallel, 8 workers).
import random,sys
from multiprocessing import Pool
from dk68_sat import solve,CONFIGS,SHAPES,CRIB,K4
txt=''.join(c for c in open('/workspace/kcl/data/g2701.txt',errors='ignore').read().upper() if 'A'<=c<='Z')
def step(sq,inv,C,X,Y,a,b):
    r1,c1=divmod(sq[1][a],C); r2,c2=divmod(sq[2][b],C)
    return inv[X].get(r1*C+c2), inv[Y].get(r2*C+c1)
def enc(pt,shape,off,X,Y,swap,rng):
    R,C=SHAPES[shape]; N=R*C; sq={}
    for s in (1,2):
        cells=list(range(N)); rng.shuffle(cells); sq[s]={chr(65+i):cells[i] for i in range(26)}
    inv={s:{v:k for k,v in sq[s].items()} for s in (1,2)}
    out=list(pt)
    for k in range(off,96,2):
        u,v=step(sq,inv,C,X,Y,pt[k],pt[k+1])
        if u is not None and v is not None:
            if swap: u,v=v,u
            u,v=step(sq,inv,C,X,Y,u,v)
        if u is None or v is None:
            if k in CRIB and k+1 in CRIB: return None
            u,v=rng.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ'),rng.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        elif swap: u,v=v,u
        out[k],out[k+1]=u,v
    return ''.join(out)
def ctl(i):
    cfg=CONFIGS[i]; rng=random.Random(6800+i)
    while True:
        st=rng.randrange(0,len(txt)-200); pt=list(txt[st:st+97])
        for p,c in CRIB.items(): pt[p]=c
        ct=enc(''.join(pt),*cfg,rng)
        if ct: break
    return cfg,solve(ct,*cfg)[0],ct
def null(i):
    l=list(K4); random.Random(6800+i).shuffle(l); ct=''.join(l)
    res=[solve(ct,*cfg)[0] for cfg in CONFIGS]
    return i,res
if __name__=="__main__":
    with Pool(8) as P:
        if sys.argv[1]=="ctl":
            ok=0
            for cfg,g,ct in P.imap(ctl,range(len(CONFIGS))):
                ok+=g; print("CTL",*cfg,"SAT" if g else "UNSAT",ct,flush=True)
            print(f"controls recovered {ok}/{len(CONFIGS)}")
        else:
            a,b=int(sys.argv[2]),int(sys.argv[3]); per=[0]*len(CONFIGS)
            for i,res in P.imap_unordered(null,range(a,b)):
                for j,r in enumerate(res): per[j]+=r
                print(f"NULL{i} seed {6800+i} SAT configs {sum(res)}/48 "+''.join('1' if r else '0' for r in res),flush=True)
            print("per-config SAT counts over nulls:",per)
