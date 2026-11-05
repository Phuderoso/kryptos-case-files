# Cycle 113 extras (cheap once the C counter exists):
#  A) the 6 planted w21 controls: confirm the TRUE column order is crib-consistent (cycle 109 counter, only=order)
#  B) 20 more shuffled nulls at w21 p21 dir1 (seed 1131), 6 tableaux
#  C) new widths 15-20, every p | w with p >= 3, dir1 only: K4 + 1 shuffled null + 1 planted control per (w,p,tableau)
# Resumable: finished lines go to extra113.txt and are skipped on rerun.
import sys, os, random, subprocess, time
from concurrent.futures import ThreadPoolExecutor
H=os.path.dirname(os.path.abspath(__file__))
sys.path[:0]=[os.path.join(H,'..',d) for d in ('cycle110','cycle109','cycle105')]
from window110 import KINDS, cribs
from subcol_count import encrypt_control, count as count109
BIN=os.environ.get('WIN113','/workspace/k4c113/win113'); OUT=os.environ.get('OUT','/workspace/k4c113/extra113.txt')
JOBS=int(os.environ.get('JOBS','4')); PER=int(os.environ.get('PER','60'))
K4=open('/tmp/kcf/data/k4.txt').read().strip(); CR=cribs()
PT="WEDUGTHROUGHTHERUBBLE"+"EASTNORTHEAST"+"ANDFOUNDTHEDOORUNDERTHEOLDBRI"+"BERLINCLOCK"+"TOWERASTHESUNWENTDOWNXX"
if 'A' in sys.argv[1:]:
  R=random.Random(112)
  for k in KINDS:
    o=list(range(21)); R.shuffle(o); ct=encrypt_control(PT,21,21,o,k,1,seed=R.randrange(10**6))
    print(f'A ctl {k}: true order accepted = {count109(ct,CR,21,21,k,1,only=o)==1}',flush=True)
jobs=[]
R=random.Random(1131)
for i in range(20):
  l=list(K4); R.shuffle(l); s=''.join(l)
  for k in KINDS: jobs.append(('B',21,21,f'xnull{i}',k,s))
R=random.Random(1132)
for w in range(15,21):
  for p in [d for d in range(3,w+1) if w%d==0]:
    for k in KINDS:
      l=list(K4); R.shuffle(l); o=list(range(w)); R.shuffle(o)
      jobs+= [('C',w,p,'K4',k,K4),('C',w,p,'null',k,''.join(l)),('C',w,p,'ctl',k,encrypt_control(PT,w,p,o,k,1,seed=R.randrange(10**6)))]
done=set()
if os.path.exists(OUT):
  for line in open(OUT): done.add(tuple(line.split()[:5]))
def run(j):
  g,w,p,n,k,ct=j; t=time.time(); tag=f'{g} w{w} p{p} {n} {k}'
  try: r=subprocess.run([BIN,str(w),str(p),k,ct],capture_output=True,text=True,timeout=PER).stdout.split(); res=r[0]
  except subprocess.TimeoutExpired: return f'{tag} TIMEOUT({PER}s)',False
  except IndexError: return f'{tag} CRASH',False
  return f'{tag} count={res} ({time.time()-t:.1f}s)',True
todo=[j for j in jobs if (j[0],f'w{j[1]}',f'p{j[2]}',j[3],j[4]) not in done]
with ThreadPoolExecutor(JOBS) as ex:
  for line,ok in ex.map(run,todo):
    print(line,flush=True)
    if ok: open(OUT,'a').write(line+'\n')
