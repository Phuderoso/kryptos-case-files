"""Case 221 addendum (I-377 item a): exact two-sided Mann-Whitney p beside the normal approximation for H2 (R_t of the 24 case-235
nulls vs the 20 case-218 calibration R_t). Reads only published files: data/cycle235/R, data/cycle235/nulls235.tsv,
data/cycle232/summary232.json; same fit/unit code as tools/cycle235/analyze235.py. usage: python3 mw221.py REPO"""
import sys, re, json, math
from scipy.stats import mannwhitneyu
REPO = sys.argv[1]; W = REPO + '/data/cycle235'
B = json.load(open(REPO + '/data/cycle232/summary232.json')); beta = B['fit']['beta']; RCAL = sorted(B['bar']['Rcal'].values())
def fit(N, q): x = math.log(max(N, 10)); return beta[0] + beta[1] * x + beta[2] * x * x + beta[3] * q
YRE = re.compile(r'^Y nq=64 n=(\d+) max=(-?[\d.]+)')
def unit(tag):
    N, mx = 0, -99.0
    for f in ('direct', 'bank_r10', 'all_r10'):
        for l in open(f'{W}/R/{tag}_{f}.txt'):
            m = YRE.match(l)
            if m: n, v = int(m[1]), float(m[2]); N += n; mx = max(mx, v) if n else mx
    return N, mx
Rn = []
for l in open(W + '/nulls235.tsv'):
    seed = l.split('\t')[0]; N, mx = unit(f'null{seed}'); Rn.append(mx - fit(N, 64))
print('n_null', len(Rn), 'n_cal', len(RCAL), 'ties', len(set(Rn) & set(RCAL)))
for meth in ('asymptotic', 'exact'):
    u = mannwhitneyu(Rn, RCAL, alternative='two-sided', method=meth)
    print(f'{meth:10s} U {u.statistic:.1f} p {u.pvalue:.3g}')
u0 = mannwhitneyu(Rn, RCAL, alternative='two-sided', method='asymptotic', use_continuity=False)
print(f'normal, no continuity correction U {u0.statistic:.1f} p {u0.pvalue:.3g}')
