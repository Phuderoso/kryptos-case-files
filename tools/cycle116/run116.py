"""Cycle 116 driver: minimal step-set size m for K4, 4 shuffled nulls, 3 planted stepping-disk controls (|S| = 3, 4, 6),
over the identity + 165,065 bank transpositions x 2,356 keyword alphabet pairs x 2 senses (model A)."""
import sys, random, subprocess, numpy as np
sys.path.insert(0,'/tmp/kcf/tools/cycle114')
from kryha114 import kryha_enc, PT, K4
from testB114 import PAIRS
D='/workspace/k4c116/'; NPERM=165065
P=np.fromfile(D+'perms97.bin',dtype=np.int16).reshape(NPERM,97)
R=random.Random(1161); texts={'K4':(K4,None)}
for k in range(4): texts[f'null{k}']=("".join(R.sample(K4,97)),None)
for k,sz in enumerate((3,4,6)):
    p=R.randrange(NPERM); pi=R.randrange(len(PAIRS)); sg=R.choice((1,-1)); S=R.sample(range(1,26),sz)
    sh=[R.randrange(26)]
    for i in range(96): sh.append((sh[-1]+R.choice(S))%26)
    X=kryha_enc(PT,*PAIRS[pi],sh,sg); C=['?']*97
    for j in range(97): C[P[p][j]]=X[j]
    texts[f'ctl{k}']=("".join(C),f"perm={p} pair={pi} sg={sg} |S|={sz} S={sorted(S)}")
ps={nm:subprocess.Popen([D+'stepset',ct,D+'perms97.bin',str(NPERM),D+'pairs.txt'],stdout=subprocess.PIPE,text=True) for nm,(ct,_) in texts.items()}
for nm,pr in ps.items():
    out=pr.communicate()[0].strip().split("\n"); ct,truth=texts[nm]
    print(f"== {nm} ct={ct}"+(f"\n   planted: {truth}" if truth else ""))
    for l in out:
        if not l.startswith("BEST"): print("   "+l)
    best=[l for l in out if l.startswith("BEST")]
    print("   last BEST lines:", best[-3:])
    if truth: print("   true perm reached:", any(truth.split()[0] in l for l in best))
