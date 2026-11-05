"""Cycle 115 driver: K4 + shuffled nulls + planted controls (model A any wheel; model B published wheel) over the full bank."""
import sys, random, subprocess, numpy as np
sys.path.insert(0,'/tmp/kcf/tools/cycle114')
from kryha114 import kryha_enc, kryha_dec, PT, K4, WHEELS
from testB114 import PAIRS
D='/workspace/k4c115/'; NPERM=165065
P=np.fromfile(D+'perms97.bin',dtype=np.int16).reshape(NPERM,97)
R=random.Random(1151)
texts={'K4':(K4,None)}
for k in range(3): texts[f'null{k}']=("".join(R.sample(K4,97)),None)
for k in range(2):   # model A: Kryha (any wheel) then transposition
    p=R.randrange(NPERM); pi=R.randrange(len(PAIRS)); sg=R.choice((1,-1)); n=R.randrange(5,40)
    w=[R.randrange(5,14) for _ in range(n)]; sh=[R.randrange(26)]
    for i in range(96): sh.append((sh[-1]+w[i%n])%26)
    X=kryha_enc(PT,*PAIRS[pi],sh,sg); C=['?']*97
    for j in range(97): C[P[p][j]]=X[j]
    texts[f'ctlA{k}']=("".join(C),f"A perm={p} pair={pi} sg={sg} n={n}")
for k in range(2):   # model B: transposition then Kryha (published wheel)
    p=R.randrange(NPERM); pi=R.randrange(len(PAIRS)); sg=R.choice((1,-1)); wl=R.choice(list(WHEELS)); st=R.randrange(wl)
    sh=[0]
    for i in range(96): sh.append((sh[-1]+WHEELS[wl][(st+i)%wl]+4)%26)
    Y=['?']*97
    for j in range(97): Y[P[p][j]]=PT[j]
    texts[f'ctlB{k}']=(kryha_enc("".join(Y),*PAIRS[pi],sh,sg),f"B perm={p} pair={pi} sg={sg} wheel={wl} start={st}")
ps={nm:subprocess.Popen([D+'kbank',ct,D+'perms97.bin',str(NPERM),D+'pairs.txt','40'],stdout=subprocess.PIPE,text=True) for nm,(ct,_) in texts.items()}
for nm,pr in ps.items():
    out=pr.communicate()[0]; ct,truth=texts[nm]
    print(f"== {nm} ct={ct}" + (f"\n   planted: {truth}" if truth else ""))
    lines=out.strip().split("\n")
    hits=[l for l in lines if l[:2] in ("A ","B ")]
    print("   "+"\n   ".join(l for l in lines if not l.startswith(("A ","B ")))) 
    if truth:
        tp=truth.split()[1]; print("   true perm among hits:", any(tp in h and truth.split()[2] in h for h in hits), f"({len(hits)} printed hits)")
    elif hits: print("   first hits:", hits[:10])
