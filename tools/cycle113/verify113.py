# Cycle 113: check the C port (win113) against cycle 110's Python counter, case by case.
import sys, os, random, subprocess, time
H=os.path.dirname(os.path.abspath(__file__))
sys.path[:0]=[os.path.join(H,'..',d) for d in ('cycle110','cycle109','cycle105')]
from window110 import count, KINDS, cribs
from subcol_count import encrypt_control
BIN=os.environ.get('WIN113','/workspace/k4c113/win113')
K4=open('/tmp/kcf/data/k4.txt').read().strip(); CR=cribs()
PT="WEDUGTHROUGHTHERUBBLE"+"EASTNORTHEAST"+"ANDFOUNDTHEDOORUNDERTHEOLDBRI"+"BERLINCLOCK"+"TOWERASTHESUNWENTDOWNXX"
def c(ct,w,p,k): return int(subprocess.run([BIN,str(w),str(p),k,ct],capture_output=True,text=True).stdout.split()[0])
R=random.Random(1131); bad=0; n=0
for (w,p) in [(13,13),(14,7),(14,14),(21,7),(21,3),(11,11),(12,6),(10,5),(7,7),(9,3)]:
  for kind in KINDS:
    o=list(range(w)); R.shuffle(o); ct=encrypt_control(PT,w,p,o,kind,1,seed=R.randrange(9999))
    l=list(K4); R.shuffle(l); nul=''.join(l)
    for name,t in (('ctl',ct),('K4',K4),('null',nul)):
      t0=time.time(); a=count(t,CR,w,p,kind); t1=time.time(); b=c(t,w,p,kind); t2=time.time(); n+=1
      if a!=b: bad+=1
      print(f'w{w} p{p} {kind} {name}: py={a} c={b} {"OK" if a==b else "MISMATCH"} (py {t1-t0:.2f}s, c {t2-t1:.2f}s)',flush=True)
print(f'{n} cases, {bad} mismatches')
