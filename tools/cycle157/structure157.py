"""Cycle 157: why survivor counts vary among nulls with the SAME repetition profile.
For model P at period L, crib t is an edge between cipher-letter node c_t and offset node o_{(pos//L)%L}.
Each independent cycle of that graph is one mod-26 equation on the digit stream (about a 1/26 filter), so the number
of chance survivors scales roughly like 26^(-r), r = cycle rank = edges - nodes + components. With K4's profile fixed,
r still varies with WHICH crib positions share letters (how many components the graph splits into).
usage: structure157.py results_raw.txt nulls.txt k4.txt [cycle155 controls.txt]"""
import sys,re,collections,math
POS=list(range(21,34))+list(range(63,74))
def rank(t,L):
    par={}
    def f(x):
        while par.setdefault(x,x)!=x: x=par[x]
        return x
    nodes=set()
    for i in POS:
        a=('c',t[i]); b=('o',(i//L)%L); nodes|={a,b}; ra,rb=f(a),f(b)
        if ra!=rb: par[ra]=rb
    comps=len({f(x) for x in nodes}); return 24-len(nodes)+comps
cnt=collections.defaultdict(int); seen=set()
for l in open(sys.argv[1]):
    m=re.match(r'C (\S+) P L=(\d+) (\S+) lo=(\d+) .*?\| one az:vig=(\d+) beau=(\d+) ka:vig=(\d+) beau=(\d+)',l)
    if m and m.group(1,2,3,4) not in seen: seen.add(m.group(1,2,3,4)); cnt[(m.group(1),int(m.group(2)),m.group(3))]+=sum(map(int,m.group(5,6,7,8)))
texts={'K4':open(sys.argv[3]).read().strip()}
for l in open(sys.argv[2]): n,t=l.split()[:2]; texts[n]=t
old={}
if len(sys.argv)>4:
    for l in open(sys.argv[4]):
        if l.startswith('null'): n,t=l.split()[:2]; old['c155_'+n]=t
for L,mode in ((8,'all'),(11,'perm')):
    print(f"# L={L} {mode}: text cycle-rank r, one-error-feasible primers")
    rows=[(rank(t,L),cnt.get((n,L,mode)),n) for n,t in texts.items()]
    for r,c,n in sorted(rows,key=lambda x:(x[0],x[2])): print(f"  {n} r={r} one={c}")
    by=collections.defaultdict(list)
    for r,c,n in rows:
        if n!='K4' and c is not None: by[r].append(c)
    print("  matched nulls by r: "+'; '.join(f"r={r}: n={len(v)} median={sorted(v)[len(v)//2]} range {min(v)}-{max(v)}" for r,v in sorted(by.items())))
    if old: print("  cycle-155 nulls r: "+' '.join(f"{n[5:]}={rank(t,L)}" for n,t in old.items()))
