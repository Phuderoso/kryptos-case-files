"""Cycle 157 summarizer: K4 vs structure-matched nulls (model P, one-error and strict primer counts).
K4 rows not rerun here (L 2-7 digits, L 8-10 ranks) use the cycle-155 counts (all 0, data/cycle155/results.txt).
Empirical upper tail p = (1 + #{nulls with count >= K4}) / (N + 1); lower tail likewise with <=."""
import re,sys,collections,statistics as st
f=sys.argv[1] if len(sys.argv)>1 else 'results_raw.txt'
pat=re.compile(r'C (\S+) P L=(\d+) (\S+) lo=(\d+) tested=(\d+) strict az:vig=(\d+) beau=(\d+) ka:vig=(\d+) beau=(\d+) \| one az:vig=(\d+) beau=(\d+) ka:vig=(\d+) beau=(\d+) \| pairs=(\d+)')
agg=collections.defaultdict(lambda:[0,0,0,0]); seen=set(); exp=collections.Counter()
for l in open(f):
    m=pat.match(l)
    if not m: continue
    T,L,mode,lo=m.group(1,2,3,4)
    if (T,L,mode,lo) in seen: continue
    seen.add((T,L,mode,lo)); v=list(map(int,m.groups()[4:]))
    a=agg[(int(L),mode,T)]; a[0]+=v[0]; a[1]+=sum(v[1:5]); a[2]+=sum(v[5:9]); a[3]+=v[9]
FULL={('all',L):10**L for L in range(2,10)}
import math
for L in range(8,13): FULL[('perm',L)]=math.factorial(L)
K4PRIOR={(L,'all'):(0,0) for L in range(2,8)}; K4PRIOR.update({(L,'perm'):(0,0) for L in (8,9,10)})
nulls=sorted({k[2] for k in agg if k[2]!='K4'})
print(f"# {len(nulls)} structure-matched nulls; columns: strict / one-error-feasible primers (counted over az/ka x vig/beau)")
print("L mode | complete | K4 strict one | matched nulls one-error: min median max #zero | p_upper(one) | null strict min/med/max | per-null one-error counts")
for (L,mode) in sorted({(k[0],k[1]) for k in agg},key=lambda x:(x[1],x[0])):
    rows={T:agg[(L,mode,T)] for T in nulls if (L,mode,T) in agg}
    comp=sum(1 for T in rows if rows[T][0]==FULL[(mode,L)])
    if (L,mode,'K4') in agg and agg[(L,mode,'K4')][0]==FULL[(mode,L)]: ks,ko=agg[(L,mode,'K4')][1:3]; src='rerun'
    else: ks,ko=K4PRIOR.get((L,mode),(None,None)); src='c155'
    one=[rows[T][2] for T in rows if rows[T][0]==FULL[(mode,L)]]; strict=[rows[T][1] for T in rows if rows[T][0]==FULL[(mode,L)]]
    if not one: continue
    pu=(1+sum(x>=ko for x in one))/(len(one)+1)
    print(f"{L} {mode} | {comp}/{len(nulls)} | K4({src}) {ks} {ko} | {min(one)} {st.median(one)} {max(one)} {sum(x==0 for x in one)} | {pu:.3f} | {min(strict)}/{st.median(strict)}/{max(strict)} | {' '.join(map(str,one))}")
