"""I-377(b) bar-reading check (cycle 241). Recomputes R_t of case 218 calibration texts from data/cycle232/R with summary232 betas,
splits R_t into per-unit residuals, and compares with the case 221 null R_t (single unit nq 64)."""
import sys,json,re,math,os,numpy as np
from scipy.stats import mannwhitneyu
REPO=sys.argv[1]; W=sys.argv[2]
B=json.load(open(W+'/summary232.json')); beta=B['fit']['beta']; KT=B['bar']['k_text']
fit=lambda N,q: beta[0]+beta[1]*math.log(max(N,10))+beta[2]*math.log(max(N,10))**2+beta[3]*q
YRE=re.compile(r"^Y model=(\w) p=(\d+) nq=(\d+) n=(\d+) pass=(\d+) max=(-?[\d.]+)")
FILES=["direct_a","direct_b","bank_Q_r10","all_Q_r10","bank_V_a","bank_V_b","all_V_a","all_V_b"]
def units(s):
    U={}
    for f in FILES:
        for l in open(f"{REPO}/data/cycle232/R/null{s}_{f}.txt"):
            m=YRE.match(l)
            if m and int(m[3])>=10:
                u=U.setdefault(int(m[3]),[0,-99.]); u[0]+=int(m[4]); u[1]=max(u[1],float(m[6]))
    return U
cal={s:units(s) for s in range(209609,209629)}
R={};nu={};res=[];hi={}
for s,U in cal.items():
    r={q:mx-fit(n,q) for q,(n,mx) in U.items() if n>=10}
    R[s]=max(r.values()); nu[s]=len(r); res+=list(r.values()); hi[s]=r
print("recomputed k_text %.6f vs summary232 %.6f  diff %.2e"%(max(R.values()),KT,max(R.values())-KT))
sm=B['bar']['Rcal']; print("max |R_t - summary232 Rcal| %.2e"%max(abs(R[s]-sm[str(s)]) for s in R))
print("units per cal text: min %d median %d max %d  total %d"%(min(nu.values()),np.median(list(nu.values())),max(nu.values()),len(res)))
res=np.array(res);print("per-unit residual: mean %+.3f median %+.3f sd %.3f p95 %.3f max %.3f"%(res.mean(),np.median(res),res.std(),np.percentile(res,95),res.max()))
Rs=np.array(sorted(R.values()));print("R_t(max over units) cal: median %+.3f max %.3f min %.3f"%(np.median(Rs),Rs.max(),Rs.min()))
# calibration texts restricted to one unit
nq64={s:hi[s].get(64) for s in hi}
print("cal texts with an nq 64 unit:",sum(v is not None for v in nq64.values()))
big={s:max(((q,v) for q,v in hi[s].items() if q>=45),key=lambda t:t[0],default=None) for s in hi}
v64=[v for v in nq64.values() if v is not None]
# case 221 nulls (single unit)
S5=json.load(open(W+'/summary235.json'))['nulls']; R221=np.array([r['R'] for r in S5])
S0=json.load(open(W+'/summary240.json'))['nulls']; R240=np.array([r['R'] for r in S0])
print("case221 null R_t (24): median %+.3f max %.3f ; case240 (12): median %+.3f max %.3f"%(np.median(R221),R221.max(),np.median(R240),R240.max()))
rng=np.random.default_rng(209731)
# resample: single random unit per cal text (what a one-unit family sees) vs. R_t; and max over m random units
for m in (1,2,3,5,8):
    sims=[]
    for _ in range(20000):
        s=rng.choice(list(hi)); r=list(hi[s].values()); sims.append(max(rng.choice(r,size=min(m,len(r)),replace=False)))
    sims=np.array(sims); print("max of %d random units of one cal text: median %+.3f  p95 %+.3f  P(>=0.879)=%.4f"%(m,np.median(sims),np.percentile(sims,95),(sims>=KT).mean()))
if v64:
    print("nq64 unit cal residuals n=%d median %+.3f max %+.3f"%(len(v64),np.median(v64),max(v64)))
for name,x in(("per-unit residuals (cal)",res),):
    u=mannwhitneyu(R221,x,alternative='two-sided',method='asymptotic'); print("MW221 vs",name,"p %.3g median diff %.3f"%(u.pvalue,np.median(R221)-np.median(x)))
u=mannwhitneyu(R221,Rs,alternative='two-sided',method='exact');print("exact MW case221 vs cal R_t: p %.3g (U %.1f)"%(u.pvalue,u.statistic))
# PREREG232 l.38 reading: bar = fit + k_text; verify K4 case 221 unit headroom
print("bar218(64,343) %.5f ; shifted %.5f"%(fit(343,64)+KT,fit(343,64)+KT-0.23881117221901338))
print("one-unit expectation: per-text one-unit bar at 1/21 level = 95th pct of per-unit residuals = %.3f vs k_text %.3f (diff %.3f)"%(np.percentile(res,95),KT,KT-np.percentile(res,95)))
print("R_t cal sorted:"," ".join("%+.3f"%v for v in Rs))
v64=np.array(v64); u=mannwhitneyu(R221,v64,alternative='two-sided',method='exact'); print("exact MW case221 nulls (24) vs cal nq64 single-unit residuals (20): p %.3g U %.1f; HL shift %.3f"%(u.pvalue,u.statistic,np.median([a-b for a in R221 for b in v64])))
Rall=np.concatenate([R221,R240]); u=mannwhitneyu(Rall,v64,alternative='two-sided',method='exact'); print("same with 36 nulls (221+240): p %.3g HL %.3f"%(u.pvalue,np.median([a-b for a in Rall for b in v64])))
print("sorted nq64 cal residuals:"," ".join("%+.3f"%v for v in sorted(v64)))
print("sorted R221:"," ".join("%+.3f"%v for v in sorted(R221)))
