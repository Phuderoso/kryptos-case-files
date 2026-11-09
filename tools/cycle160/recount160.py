"""Cycle 160: compare q4v.c match counts with the independent brute-force recount (indep160.py) on chosen configs."""
import glob,random,collections,subprocess,sys
sys.path.insert(0,'.'); from indep160 import count
ct={l.split()[0]:l.split()[1] for l in open('controls.txt')}; ct['K4']=open('k4.txt').read().strip()
C=collections.Counter()
for f in glob.glob('run/bank_*.txt')+['ctl_out.txt']:
    for l in open(f):
        x=l.split()
        if x[0]=='M': C[(x[1],int(x[2]),int(x[3]),int(x[4]),int(x[5]),x[6])]+=1
        if x[0]=='S': C[(x[1],int(x[2]),int(x[3]),int(x[4]),int(x[5]),'tot')]=int(x[7])
cfg=[]
k4m=sorted({k[:5] for k in C if k[0]=='K4'})
random.seed(16099); cfg+=random.sample([k for k in k4m if k[4]==15],3)+random.sample([k for k in k4m if k[4]==16 and k[3]==0],2)+random.sample([k for k in k4m if k[4]==16 and k[3]==1],2)
nm=sorted({k[:5] for k in C if k[0].startswith('null')}); cfg+=random.sample(nm,3)+[('null1',88885,0,0,16)]
cfg+=[('ctl1',4242,0,1,6),('ctl2',99999,1,0,7),('ctl4',120000,1,1,13)]
cfg+=[('K4',random.randrange(165065),random.randrange(2),random.randrange(2),random.randrange(2,15)) for _ in range(6)]
ok=0
for lab,q,d,ix,p in cfg:
    o,_=count(ct[lab],q,d,ix,p); c=(C[(lab,q,d,ix,p,'vig')],C[(lab,q,d,ix,p,'beau')])
    t=C[(lab,q,d,ix,p,'tot')]
    same=((o['vig'],o['beau'])==c) if not t else (o['vig']+o['beau']==t); ok+=same
    if t: c=(t,'(total, >40 listed as S)')
    print(f"{lab} q {q} dir {d} ix {ix} p {p}: C vig/beau {c[0]}/{c[1]}  python {o['vig']}/{o['beau']}  {'OK' if same else 'MISMATCH'}")
# direct
for lab,p,exp in (('K4',24,13),('K4',8,0),('K4',16,0)):
    o,_=count(ct[lab],-1,0,0,p); print(f"{lab} direct p {p}: C {exp} python {o['vig']+o['beau']} {'OK' if o['vig']+o['beau']==exp else 'MISMATCH'}"); ok+=(o['vig']+o['beau']==exp)
o,_=count(ct['ctl3'],-1,0,0,8); print(f"ctl3 direct p 8: C 1 python {o['vig']}/{o['beau']}"); ok+=(o['vig']+o['beau']==1)
print(f"agreement {ok}/{len(cfg)+4}")
