"""Cycle 155 summarizer: sums C lines per text/model/L/mode (resumable runs: one C line per job chunk; S lines of
killed chunks may repeat and are deduplicated)."""
import re,sys,collections
f=sys.argv[1] if len(sys.argv)>1 else 'results_raw.txt'
agg=collections.defaultdict(lambda:[0]*11); seen=set()
pat=re.compile(r'C (\S+) (\S+) L=(\d+) (\S+) lo=(\d+) tested=(\d+) strict az:vig=(\d+) beau=(\d+) ka:vig=(\d+) beau=(\d+) \| one az:vig=(\d+) beau=(\d+) ka:vig=(\d+) beau=(\d+) \| pairs=(\d+)')
for l in open(f):
    m=pat.match(l)
    if not m: continue
    T,M,L,mode,lo=m.group(1,2,3,4,5)
    if (T,M,L,mode,lo) in seen: continue
    seen.add((T,M,L,mode,lo)); v=list(map(int,m.groups()[5:]))
    a=agg[(M,int(L),mode,T)]
    a[0]+=v[0]; a[1]+=sum(v[1:5]); a[2]+=v[9]; a[3]+=v[5]; a[4]+=v[6]; a[5]+=v[7]; a[6]+=v[8]; a[7]+=sum(v[5:9])
texts=['K4']+[f'null{i}' for i in range(1,7)]
print("# model L mode | per text: tested strict one-error-feasible (az:vig/beau ka:vig/beau total); '-' = not run")
for key in sorted({k[:3] for k in agg},key=lambda k:(k[0],k[2],k[1])):
    row=[]
    for T in texts:
        a=agg.get(key+(T,))
        row.append('-' if a is None else f"{T}:{a[0]} s{a[1]} one{a[7]} pairs{a[2]} ({a[3]}/{a[4]} {a[5]}/{a[6]})")
    print(*key,'|',' '.join(row))
