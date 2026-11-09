"""Cycle 159 (I-057) summary: K4's one-error-feasible Periodic Gromark L 8 digit primers vs rank-matched nulls.
Count per text = one-error-feasible (primer, plain alphabet, form) cases summed over az/ka x vig/beau (as cycles 155/157);
also distinct primers and strict counts. Only texts with all 4 chunks (10^8 primers) complete are used.
p_upper = (1 + #{null >= K4}) / (N + 1) (empirical, resolution 1/(N+1)).
usage: [LOS=0,25000000] summarize159.py results_raw.txt nulls.txt K4_count [cycle157 r=6 counts, comma-separated]
LOS restricts to the listed chunk starts (common primer range); a text counts as complete when it has all of them."""
import sys,re,collections,os
LOS=os.environ.get("LOS","0,25000000,50000000,75000000").split(",")
cnt=collections.defaultdict(int); st=collections.defaultdict(int); chunks=collections.defaultdict(set); prim=collections.defaultdict(set)
for l in open(sys.argv[1]):
    m=re.match(r'C (\S+) P L=8 all lo=(\d+) tested=(\d+) strict az:vig=(\d+) beau=(\d+) ka:vig=(\d+) beau=(\d+) \| one az:vig=(\d+) beau=(\d+) ka:vig=(\d+) beau=(\d+)',l)
    if m:
        T,lo=m.group(1),m.group(2)
        if lo in chunks[T] or lo not in LOS: continue
        chunks[T].add(lo); v=list(map(int,m.groups()[3:])); st[T]+=sum(v[:4]); cnt[T]+=sum(v[4:])
    elif l.startswith('S '):
        f=l.split(); pr=f[-1].split('=')[1]
        if str(int(pr)//25000000*25000000) in LOS: prim[f[1]].add(pr)
meta={l.split()[0]:l.split()[2:] for l in open(sys.argv[2]) if not l.startswith('#')}
K4=int(sys.argv[3]); done=[T for T in meta if len(chunks[T])==len(LOS)]
vals=sorted(cnt[T] for T in done); N=len(vals)
print(f"# primer chunks used: {LOS}; complete rank-matched nulls: {N} of {len(meta)}")
for T in meta: print(f"{T} chunks={len(chunks[T])}/{len(LOS)} one={cnt[T] if len(chunks[T])==len(LOS) else 'incomplete'} distinct_primers={len(prim[T])} strict={st[T]} {' '.join(meta[T][2:])}")
ge=sum(v>=K4 for v in vals); p=(1+ge)/(N+1)
med=(vals[N//2] if N%2 else (vals[N//2-1]+vals[N//2])/2) if N else None
print(f"K4 one={K4}; nulls N={N} min={vals[0] if N else None} median={med} max={vals[-1] if N else None} zero={vals.count(0)} >=K4: {ge}  p_upper={p:.4f} (resolution {1/(N+1):.4f})")
print("sorted null counts:",' '.join(map(str,vals)))
if len(sys.argv)>4:
    old=list(map(int,sys.argv[4].split(','))); allv=vals+old; ge2=sum(v>=K4 for v in allv)
    print(f"pooled with cycle-157 r=6 nulls ({','.join(map(str,old))}): N={len(allv)} >=K4: {ge2} p_upper={(1+ge2)/(len(allv)+1):.4f}")
print(f"Bonferroni x4 (L8 row singled out post hoc among the 4 relaxed LOW-POWER rows of case 143): p_adj=min(1,4p)={min(1,4*p):.4f}")
