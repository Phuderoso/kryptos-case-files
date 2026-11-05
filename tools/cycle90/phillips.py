# Cycle 90 (new family): Phillips cipher on the 92-letter W-free K4 (W as null => 25-letter alphabet without W).
# Phillips: 5x5 key square; plaintext in groups of 5; group g uses square (g mod 8), squares 2-8 made by moving rows
# (ACA order 12345,21345,23145,23415,23451,32451,34251,34521); each letter -> the letter one down and one right (wrapping).
# Variants: R (rows moved), C (columns moved), RC (both). Arbitrary key square solved exactly with Z3 from the 24 cribs.
import sys, json, z3, random
ORD=["12345","21345","23145","23415","23451","32451","34251","34521"]
ORD=[[int(ch)-1 for ch in o] for o in ORD]   # display position d shows base line ORD[g][d]
A25="ABCDEFGHIJKLMNOPQRSTUVXYZ"
CR={**{20+i:c for i,c in enumerate("EASTNORTHEAST")},**{60+i:c for i,c in enumerate("BERLINCLOCK")}}
def disp(g,var):
    # base line -> display position under square g
    inv=[0]*5
    for d,b in enumerate(ORD[g]): inv[b]=d
    return inv
def solve(ct,variant,off,dirn,want_model=False):
    s=z3.Solver(); R={a:z3.Int('r'+a) for a in A25}; C={a:z3.Int('c'+a) for a in A25}
    for a in A25: s.add(R[a]>=0,R[a]<5,C[a]>=0,C[a]<5)
    s.add(z3.Distinct([R[a]*5+C[a] for a in A25]))
    def tab(g):
        inv=disp(g,None); return inv
    for i,p in CR.items():
        c=ct[i]; g=((i+off)//5)%8; inv=disp(g,None)
        def dr(x,use):  # display coordinate of base coordinate x under square g if moved
            return z3.Sum([z3.If(x==b,inv[b],0) for b in range(5)]) if use else x
        rp,rc=dr(R[p],'R' in variant),dr(R[c],'R' in variant)
        cp,cc=dr(C[p],'C' in variant),dr(C[c],'C' in variant)
        s.add((rc-rp-dirn)%5==0 if False else z3.Or([rc==(rp+dirn)%5 if False else rc-rp-dirn==k for k in (-5,0,5)]))
        s.add(z3.Or([cc-cp-dirn==k for k in (-5,0,5)]))
    s.set("timeout",60000); r=s.check()
    if r==z3.sat and want_model:
        m=s.model(); return r,{a:(m[R[a]].as_long(),m[C[a]].as_long()) for a in A25}
    return r,None
def decrypt(ct,sq,variant,off,dirn):
    pos={v:k for k,v in sq.items()}; out=[]
    for i,c in enumerate(ct):
        g=((i+off)//5)%8; inv=disp(g,None); fwd=ORD[g]
        r,cc=sq[c]; dr=inv[r] if 'R' in variant else r; dc=inv[cc] if 'C' in variant else cc
        dr=(dr-dirn)%5; dc=(dc-dirn)%5
        br=fwd[dr] if 'R' in variant else dr; bc=fwd[dc] if 'C' in variant else dc
        out.append(pos[(br,bc)])
    return "".join(out)
def encrypt(pt,sq,variant,off,dirn):
    pos={v:k for k,v in sq.items()}; out=[]
    for i,p in enumerate(pt):
        g=((i+off)//5)%8; inv=disp(g,None); fwd=ORD[g]
        r,cc=sq[p]; dr=inv[r] if 'R' in variant else r; dc=inv[cc] if 'C' in variant else cc
        dr=(dr+dirn)%5; dc=(dc+dirn)%5
        br=fwd[dr] if 'R' in variant else dr; bc=fwd[dc] if 'C' in variant else dc
        out.append(pos[(br,bc)])
    return "".join(out)
if __name__=="__main__":
    ct=open(sys.argv[1]).read().strip(); res={}
    for variant in ("R","C","RC"):
        for off in range(5):
            for dirn in (1,-1):
                r,m=solve(ct,variant,off,dirn,want_model=True)
                res[f"{variant} off{off} dir{dirn}"]=str(r)
                if m: print("SAT",variant,off,dirn,decrypt(ct,m,variant,off,dirn))
    print(json.dumps(res))
