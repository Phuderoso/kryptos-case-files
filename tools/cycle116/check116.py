"""Cycle 116: (1) m at each planted control's TRUE transposition/pair; (2) K4's m <= 6 configs decrypted with the
minimal-step-set shifts filled greedily is impossible (steps outside cribs unknown), so we list them and show the crib-span
text only; (3) 12 extra shuffled nulls for the distribution of the global minimum."""
import sys, random, subprocess, numpy as np
sys.path.insert(0,'/tmp/kcf/tools/cycle114')
from kryha114 import K4
from testB114 import PAIRS
D='/workspace/k4c116/'; NPERM=165065
P=np.fromfile(D+'perms97.bin',dtype=np.int16).reshape(NPERM,97)
CR=[(21+i,c) for i,c in enumerate("EASTNORTHEAST")]+[(63+i,c) for i,c in enumerate("BERLINCLOCK")]
def m_of(ct,p,pi,sg):
    F,M=PAIRS[pi]; r=[(sg*(M.index(ct[P[p][j]])-F.index(c)))%26 for j,c in CR]
    return len({(r[k+1]-r[k])%26 for k in range(23) if k!=12})
ctls=[l.split()[1:] for l in open(D+'run116.out') if l.strip().startswith('planted:')]
cts=[l.split('ct=')[1].strip() for l in open(D+'run116.out') if l.startswith('== ctl')]
for ct,t in zip(cts,ctls):
    kv=dict(x.split('=') for x in t[:4]); print("control",t,"m at true setting =",m_of(ct,int(kv['perm']),int(kv['pair']),int(kv['sg'])))
out=subprocess.run([D+'stepset',K4,D+'perms97.bin',str(NPERM),D+'pairs.txt','6'],capture_output=True,text=True).stdout
print("K4 configs with m <= 6:"); [print("  ",l) for l in out.split("\n") if l.startswith("BEST")]
R=random.Random(1162); nulls=["".join(R.sample(K4,97)) for _ in range(12)]
ps=[subprocess.Popen([D+'stepset',ct,D+'perms97.bin',str(NPERM),D+'pairs.txt','0'],stdout=subprocess.PIPE,text=True) for ct in nulls]
g=[]
for pr in ps:
    o=pr.communicate()[0]; h=[l for l in o.split("\n") if l.startswith("HIST all")][0]
    g.append((int([l for l in o.split("\n") if l.startswith("GLOBAL")][0].split("=")[1]), h.split(":")[1].split()[0]+":"+h.split(":")[2].split()[0]))
print("12 extra nulls (global min m, count at that m):", g)
