"""Aggregate hill1e chunk outputs (out/*.txt) into a results table."""
import glob,re,collections,sys
d=sys.argv[1] if len(sys.argv)>1 else 'out'
keys=['tests','strict','eqdrop','blockdrop','blockpairs','under','invertible','repair_solutions','repair_configs']
agg=collections.defaultdict(collections.Counter); best={}; bl={}
for f in sorted(glob.glob(d+'/*.txt')):
    for line in open(f):
        if line.startswith('C '):
            lab=line.split()[1]; mode='direct' if lab.startswith('D') else 'bank'; lab=lab[1:] if mode=='direct' else lab
            n=re.search(r' n=(\d)',line).group(1); k=(lab,n,mode)
            for key in keys: agg[k][key]+=int(re.search(' '+key+r'=(\d+)',line).group(1))
            b=float(re.search(r'best=(-?[\d.]+)',line).group(1))
            if b>best.get(k,-99): best[k]=b
        if line.startswith('B '):
            lab=line.split()[2]; mode='direct' if lab.startswith('D') else 'bank'; lab=lab[1:] if mode=='direct' else lab
            n=re.search(r' n=(\d)',line).group(1); k=(lab,n,mode); sc=float(re.search(r'meanQ=(-?[\d.]+)',line).group(1))
            if sc>=best.get(k,-99)-1e-9: bl[k]=line.strip()
print('text n mode '+' '.join(keys)+' best_meanQ')
for k in sorted(agg, key=lambda k:(k[1],k[2],k[0])): print(*k,*[agg[k][x] for x in keys], best.get(k,-99))
print(); [print(v) for v in bl.values()]
