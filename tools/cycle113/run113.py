# Cycle 113: finish w21 p21 columns-in (dir1) with the C counter. Same 30 jobs as tools/cycle112/par112.py:
# K4 + 3 shuffled nulls (seed 1100) x 6 tableaux, plus 6 planted controls (seed 112).
# Resumable: finished lines are appended to results113.txt and skipped on rerun.
import sys, os, random, subprocess, time
from concurrent.futures import ThreadPoolExecutor
H=os.path.dirname(os.path.abspath(__file__))
sys.path[:0]=[os.path.join(H,'..',d) for d in ('cycle110','cycle109','cycle105')]
from window110 import KINDS
from subcol_count import encrypt_control
BIN=os.environ.get('WIN113','/workspace/k4c113/win113'); OUT=os.environ.get('OUT','/workspace/k4c113/results113.txt')
JOBS=int(os.environ.get('JOBS','4')); PER=int(os.environ.get('PER','240'))
K4=open('/tmp/kcf/data/k4.txt').read().strip()
PT="WEDUGTHROUGHTHERUBBLE"+"EASTNORTHEAST"+"ANDFOUNDTHEDOORUNDERTHEOLDBRI"+"BERLINCLOCK"+"TOWERASTHESUNWENTDOWNXX"
texts=[('K4',K4)]; R=random.Random(1100)
for i in range(3):
  l=list(K4); R.shuffle(l); texts.append((f'null{i}',''.join(l)))
jobs=[(n,c,k) for n,c in texts for k in KINDS]
R=random.Random(112)
for k in KINDS:
  o=list(range(21)); R.shuffle(o); jobs.append(('ctl',encrypt_control(PT,21,21,o,k,1,seed=R.randrange(10**6)),k))
done=set()
if os.path.exists(OUT):
  for line in open(OUT): done.add(tuple(line.split()[:2]))
def run(j):
  n,ct,k=j; t=time.time()
  try: r=subprocess.run([BIN,'21','21',k,ct],capture_output=True,text=True,timeout=PER).stdout.split(); res=f'{r[0]} {r[1]} {r[2]}'
  except subprocess.TimeoutExpired: return f'{n} {k} TIMEOUT ({PER}s)',False
  return f'{n} {k} count={res} ({time.time()-t:.1f}s)',True
todo=[j for j in jobs if (j[0],j[2]) not in done and not (j[0]=='K4' and j[2]=='vigAZ' and 0)]
with ThreadPoolExecutor(JOBS) as ex:
  for line,ok in ex.map(run,todo):
    print(line,flush=True)
    if ok: open(OUT,'a').write(line+'\n')
