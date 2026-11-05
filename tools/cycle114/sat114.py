"""Generic Kryha V1 code wheel with FREE alphabets (CP-SAT, exact):
n sectors, step_j = teeth_j + 4 with teeth_j in [TMIN,TMAX]; m(c_i) - f(p_i) = sigma*sum_{k<i} step_{(k) mod n}  (mod 26).
Start sector is absorbed (steps arbitrary), ring start absorbed into m.  Returns status and a model."""
from ortools.sat.python import cp_model
from kryha114 import CRIBS, idx
def solve(ct,n,sigma,tmin=1,tmax=9,plus=4,timeout=60,workers=1,fix=None):
    m=cp_model.CpModel()
    f={p:m.NewIntVar(0,25,'f'+p) for p in sorted({p for _,p in CRIBS})}
    cl=sorted({ct[i] for i,_ in CRIBS}); g={c:m.NewIntVar(0,25,'m'+c) for c in cl}
    m.AddAllDifferent(list(f.values())); m.AddAllDifferent(list(g.values()))
    d=[m.NewIntVar(tmin+plus,tmax+plus,f'd{j}') for j in range(n)]
    m.Add(f['E']==0)  # global rotation symmetry of both alphabets
    if fix:
        for j,v in enumerate(fix): m.Add(d[j]==v)
    for i,p in CRIBS:
        cnt=[0]*n
        for k in range(i): cnt[k%n]+=1
        hi=sum(cnt)*(tmax+plus)+50
        z=m.NewIntVar(-hi//26-2,hi//26+2,f'z{i}')
        m.Add(g[ct[i]]-f[p]-sigma*sum(cnt[j]*d[j] for j in range(n) if cnt[j])==26*z)
    s=cp_model.CpSolver(); s.parameters.max_time_in_seconds=timeout; s.parameters.num_workers=workers
    r=s.Solve(m)
    st={cp_model.OPTIMAL:'SAT',cp_model.FEASIBLE:'SAT',cp_model.INFEASIBLE:'UNSAT'}.get(r,'UNKNOWN')
    return st,([s.Value(x)-plus for x in d] if st=='SAT' else None)
if __name__=="__main__":
    import sys,time
    from kryha114 import K4
    for n in map(int,sys.argv[1:]):
        for sg in (1,-1):
            t=time.time(); print(n,sg,*solve(K4,n,sg),round(time.time()-t,2),flush=True)
