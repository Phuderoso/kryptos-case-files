"""Cycle 160 summary: bank H lines per text/ix/p and direct strict + one-error counts."""
import glob,collections,re
T=['K4','null1','null2','null3','null4']
H=collections.defaultdict(lambda:[0]*6)
for f in glob.glob('run/bank_*.txt'):
    for l in open(f):
        if l.startswith('H '):
            x=l.split(); k=(x[1],int(x[2]),int(x[3]))
            for i in range(6): H[k][i]+=int(x[4+i])
print("BANK (165,065 perms x 2 directions = 330,130 per (ix,p)); cells: configs with >=1 QIV pair / QIV pairs")
print("ix p | "+" | ".join(T))
for ix in (0,1):
    for p in range(1,17):
        print(f"{['Q','C'][ix]} {p:2d} | "+" | ".join(f"{H[(t,ix,p)][3]}/{H[(t,ix,p)][4]}" for t in T))
tot={t:sum(H[(t,ix,p)][0] for ix in (0,1) for p in range(1,17)) for t in T}
pf={t:sum(H[(t,ix,p)][1] for ix in (0,1) for p in range(1,17)) for t in T}
cp={t:sum(H[(t,ix,p)][2] for ix in (0,1) for p in range(1,17)) for t in T}
print("configs", tot, "\nprefilter pass", pf, "\njoins computed", cp)
print("\nDIRECT (identity), p with >=1 QIV pair: strict | one-error (sum over 24 dropped cribs, configs with >=1 pair)")
for f in sorted(glob.glob('run/direct_*.txt')):
    lab=f[11:-4]; s={}; d=collections.Counter()
    for l in open(f):
        x=l.split()
        if x[0]=='H': s[int(x[3])]=int(x[8])
        elif x[0].startswith('D') and x[1]=='H' and int(x[9])>0: d[int(x[4])]+=1
    print(f"{lab:8s} strict min p with pairs: {min([p for p in s if s[p]>0],default='-')}  pairs p24={s.get(24,0)}  "
          f"one-error min p: {min(d,default='-')}  drops with pairs at p<=16: {sum(v for p,v in d.items() if p<=16)}  p17-23: {sum(v for p,v in d.items() if 17<=p<=23)}")
