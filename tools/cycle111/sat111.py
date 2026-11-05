import sys,random,time
from z3 import *
from common import *
def test(ct,mode,fixdelta):
    s=Solver(); s.set("timeout",60000)
    pins=[[Bool(f"p{w}_{j}") for j in range(PER[w])] for w in range(6)]
    n=[Int(f"n{t}") for t in range(21)]
    for x in n: s.add(x>=0,x<=27)
    s.add(Sum(n)<=27)
    d=Int("d"); s.add(d>=0,d<26)
    if fixdelta: s.add(d==0)
    for i,pc in CRIBS.items():
        p=ord(pc)-65;c=ord(ct[i])-65
        act=[pins[w][i%PER[w]] for w in range(6)]
        k=Sum([If(Or([act[w] for w in ty]),n[t],0) for t,ty in enumerate(TYPES)])
        # mode0: c=25+k-p+d ; mode1: c=p+k+d   (mod 26), k in 0..27
        rhs = (c-25+p) if mode==0 else (c-p)
        q=Int(f"q{i}"); s.add(q>=-2,q<=2)
        s.add(k+d==rhs+26*q)
    t=time.time(); r=s.check(); return str(r),round(time.time()-t,1)
if __name__=="__main__":
    which=sys.argv[1]
    random.seed(111)
    texts={"K4":K4}
    for j in range(int(sys.argv[2]) if len(sys.argv)>2 else 0):
        l=list(K4);random.shuffle(l);texts[f"null{j}"]="".join(l)
    for name,ct in texts.items():
        for mode in (0,1):
            for fd in (True,False):
                print(name,"mode",mode,"delta fixed" if fd else "delta free",*test(ct,mode,fd),flush=True)
