# Planted controls and shuffled nulls for cycle 67's two-square SAT.
import random,sys
from ts67_sat import solve,SHAPES,CRIB,K4
txt=''.join(c for c in open('/workspace/kcl/data/g2701.txt',errors='ignore').read().upper() if 'A'<=c<='Z')
def enc(pt,shape,off,X,Y,swap,rng):
    R,C=SHAPES[shape]; N=R*C
    sq={}
    for s in (1,2):
        cells=list(range(N)); rng.shuffle(cells); sq[s]={chr(65+i):cells[i] for i in range(26)}
    inv={s:{v:k for k,v in sq[s].items()} for s in (1,2)}
    out=list(pt)
    for k in range(off,96,2):
        a,b=pt[k],pt[k+1]; r1,c1=divmod(sq[1][a],C); r2,c2=divmod(sq[2][b],C)
        u=inv[X].get(r1*C+c2); v=inv[Y].get(r2*C+c1)
        if u is None or v is None:
            # 6x6: a pair landing on a digit cell. Only crib pairs matter to the exact test, so a non-crib pair
            # that would emit a digit is replaced by random letters (documented); a crib pair forces a retry.
            if k in CRIB and k+1 in CRIB: return None
            u,v=rng.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ'),rng.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        out[k],out[k+1]=(v,u) if swap else (u,v)
    return ''.join(out)
mode=sys.argv[1]
if mode=="ctl":
    rng=random.Random(67); n=0; ok=0
    for shape in SHAPES:
        for off in (0,1):
            for X,Y in ((2,1),(1,2),(1,1),(2,2)):
                for swap in (0,1):
                    while True:
                        st=rng.randrange(0,len(txt)-200); pt=list(txt[st:st+97])
                        for p,c in CRIB.items(): pt[p]=c
                        ct=enc(''.join(pt),shape,off,X,Y,swap,rng)
                        if ct: break
                    good=solve(ct,shape,off,X,Y,swap)[0]
                    # cross-check: same control under the other offset (should usually be UNSAT)
                    n+=1; ok+=good
                    print("CTL",shape,off,f"X{X}Y{Y}",swap,"SAT" if good else "UNSAT",ct,flush=True)
    print(f"controls recovered {ok}/{n}")
else:
    tot=0
    for i in range(int(sys.argv[2]),int(sys.argv[3])):
        l=list(K4); random.Random(6700+i).shuffle(l); ct=''.join(l); sat=0
        for shape in SHAPES:
            for off in (0,1):
                for X,Y in ((2,1),(1,2),(1,1),(2,2)):
                    for swap in (0,1): sat+=solve(ct,shape,off,X,Y,swap)[0]
        tot+=sat>0; print(f"NULL{i} seed {6700+i} SAT configs {sat}/48",flush=True)
    print("nulls with any SAT:",tot)
