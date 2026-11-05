# Cycle 112: finish cycle 110's open case (w21 p21 columns-in) for all 6 tableaux,
# K4 + 3 shuffled nulls (same seed as cycle 110) + 6 planted controls, in parallel.
import sys, time, random, os
sys.path[:0]=[os.path.join(os.path.dirname(__file__),'..',d) for d in ('cycle110','cycle109','cycle105')]
from multiprocessing import Pool
from window110 import count, KINDS, cribs
from subcol_count import encrypt_control
K4=open('/tmp/kcf/data/k4.txt').read().strip(); CR=cribs()
PT="WEDUGTHROUGHTHERUBBLE"+"EASTNORTHEAST"+"ANDFOUNDTHEDOORUNDERTHEOLDBRI"+"BERLINCLOCK"+"TOWERASTHESUNWENTDOWNXX"
def job(a):
  name,ct,kind=a; t=time.time()
  return name,kind,count(ct,CR,21,21,kind),time.time()-t
if __name__=='__main__':
  texts=[('K4',K4)]; R=random.Random(1100)
  for i in range(3):
    l=list(K4); R.shuffle(l); texts.append((f'null{i}',''.join(l)))
  jobs=[(n,c,k) for n,c in texts for k in KINDS]
  R=random.Random(112)
  for k in KINDS:
    o=list(range(21)); R.shuffle(o); jobs.append((f'ctl',encrypt_control(PT,21,21,o,k,1,seed=R.randrange(10**6)),k))
  with Pool(8) as P:
    for n,k,c,dt in P.imap_unordered(job,jobs):
      print(f'{n} w21 p21 dir1 {k}: {c} ({dt:.0f}s)',flush=True)
