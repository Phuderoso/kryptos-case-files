"""Cycle 161 (I-062) summary: K4's Periodic Gromark L 8 one-error count vs the 48 rank-matched cycle-159 nulls, per primer quarter.
Count = one-error-feasible (primer, plain alphabet, form) cases summed over az/ka x vig/beau (as cycles 155/157/159).
Checks: every (text, quarter) chunk exactly once; duplicates or gaps are reported.
K4 per-quarter counts (5,5,5,13) come from the cycle-155/157 survivor lines (data/cycle159/per_quarter.txt).
p_upper = (1 + #{null >= K4}) / (N + 1).
usage: summarize161.py results_raw.txt nulls.txt"""
import sys,re,collections
Q=["0","25000000","50000000","75000000"]; K4=[5,5,5,13]
cnt=collections.defaultdict(dict); dup=[]
for l in open(sys.argv[1]):
    m=re.match(r'C (\S+) P L=8 all lo=(\d+) tested=(\d+) strict az:vig=(\d+) beau=(\d+) ka:vig=(\d+) beau=(\d+) \| one az:vig=(\d+) beau=(\d+) ka:vig=(\d+) beau=(\d+)',l)
    if not m: continue
    T,lo,tested=m.group(1),m.group(2),int(m.group(3)); v=list(map(int,m.groups()[3:]))
    if tested!=25000000: print("WARN short chunk",T,lo,tested)
    if lo in cnt[T]: dup.append((T,lo)); continue
    cnt[T][lo]=(sum(v[:4]),sum(v[4:]))
names=[l.split()[0] for l in open(sys.argv[2]) if not l.startswith('#')]
gaps=[(T,q) for T in names for q in Q if q not in cnt[T]]
print(f"# chunks: {sum(len(cnt[T]) for T in names)} of {4*len(names)}; duplicates {len(dup)} {dup[:5]}; gaps {len(gaps)} {gaps[:5]}")
def stat(label,qs,k4,note=""):
    vals=sorted(sum(cnt[T][q][1] for q in qs) for T in names if all(q in cnt[T] for q in qs)); N=len(vals)
    ge=sum(v>=k4 for v in vals); p=(1+ge)/(N+1); med=(vals[N//2] if N%2 else (vals[N//2-1]+vals[N//2])/2)
    print(f"{label}: K4 {k4}; nulls N={N} min={vals[0]} median={med} max={vals[-1]} zero={vals.count(0)} >=K4 {ge} p_upper={p:.4f} (resolution {1/(N+1):.4f}) {note}")
    print("   sorted:",' '.join(map(str,vals)))
    return p
print("# per text: q0 q1 q2 q3 | full | strict")
for T in names: print(T,' '.join(str(cnt[T][q][1]) if q in cnt[T] else '-' for q in Q),'|',sum(cnt[T][q][1] for q in Q if q in cnt[T]),'|',sum(cnt[T][q][0] for q in Q if q in cnt[T]))
print("K4",' '.join(map(str,K4)),'|',sum(K4))
p=stat("PRIMARY full 10^8 (pre-specified cycle 161; secondary in cycle 159)",Q,28)
print(f"   Bonferroni x4 (L8 row singled out post hoc among 4 relaxed LOW-POWER rows): {min(1,4*p):.4f}")
for i,q in enumerate(Q): stat(f"quarter q{i}",[q],K4[i])
p3=stat("POST-HOC q3 (75-100M; loose end noticed after the fact in cycle 159)",[Q[3]],13)
print(f"   Bonferroni x4 (quarter chosen post hoc) = {min(1,4*p3):.4f}; x16 (quarter and row) = {min(1,16*p3):.4f}")
stat("check: cycle-159 primary 0-50M",Q[:2],10)
