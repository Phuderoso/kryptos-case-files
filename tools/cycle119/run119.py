"""Cycle 119: carving-error audit of the generic stepping-disk exclusion (cycle 116).
For each config, drop one crib letter and report m1 = min remaining distinct steps.
K4, 8 shuffled nulls, 4 planted controls:
  ctl_ok4  : |S|=4, no error  (expects m1 ~ 4 at true perm)
  ctl_err4 : |S|=4, one crib letter flipped in CT (expects m1 <= 4 at true perm)
  ctl_ok3  : |S|=3, no error
  ctl_err5 : |S|=5, one crib letter flipped
Also report cycle-116-style m0 (no drop) for the planted texts at their true perm, as a sanity check.
"""
import sys, random, subprocess, numpy as np, time
sys.path.insert(0,'/tmp/kcf/tools/cycle114')
from kryha114 import kryha_enc, PT, K4
from testB114 import PAIRS
D='/workspace/k4c119/'; SRC='/workspace/k4c116/'
NPERM=165065
P=np.fromfile(SRC+'perms97.bin',dtype=np.int16).reshape(NPERM,97)
EXE=D+'stepset119'
R=random.Random(1191)
CRIB_POS=list(range(21,34))+list(range(63,74))
def flip_one_crib(ct, seed):
    L=list(ct); r=random.Random(seed); i=r.choice(CRIB_POS)
    while True:
        c=chr(65+r.randrange(26))
        if c!=L[i]: L[i]=c; return ''.join(L), i
texts={}
texts['K4']=(K4,None)
for k in range(8):
    texts[f'null{k}']=(''.join(R.sample(K4,97)),None)
for name,sz,err in [('ctl_ok3',3,False),('ctl_ok4',4,False),('ctl_err4',4,True),('ctl_err5',5,True)]:
    p=R.randrange(NPERM); pi=R.randrange(len(PAIRS)); sg=R.choice((1,-1)); S=R.sample(range(1,26),sz)
    sh=[R.randrange(26)]
    for i in range(96): sh.append((sh[-1]+R.choice(S))%26)
    X=kryha_enc(PT,*PAIRS[pi],sh,sg); C=['?']*97
    for j in range(97): C[P[p][j]]=X[j]
    ct=''.join(C); note=f"perm={p} pair={pi} sg={sg} |S|={sz} S={sorted(S)}"
    if err:
        ct,fi=flip_one_crib(ct, R.randrange(10**9)); note+=f" flipped_crib_pos={fi}"
    texts[name]=(ct,note)
# write pairs once
open(D+'pairs.txt','w').write(open(SRC+'pairs.txt').read())
t0=time.time()
# run identity-only first for a quick summary, then full bank in parallel batches of texts
ps={}
for nm,(ct,_) in texts.items():
    ps[nm]=subprocess.Popen([EXE,ct,SRC+'perms97.bin',str(NPERM),D+'pairs.txt','3'],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
results={}
for nm,pr in ps.items():
    out,err=pr.communicate(); results[nm]=out
    open(D+nm+'.out','w').write(out)
    print(f"== {nm}  planted={texts[nm][1]}")
    for l in out.splitlines():
        if not l.startswith('BEST'): print('  '+l)
    best=[l for l in out.splitlines() if l.startswith('BEST')]
    truth=texts[nm][1]
    if truth:
        tag='perm='+truth.split()[0].split('=')[1]
        hit=any(tag in l for l in best)
        print(f"  true-perm among BEST (m1<=3): {hit}; nBEST={len(best)}")
        # also show any BEST line for that perm regardless of threshold by grepping m1 at that perm from a dedicated run if needed
print(f"wall {time.time()-t0:.1f}s")
