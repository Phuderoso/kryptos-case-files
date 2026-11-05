import sys,time
from window110 import count, KINDS, cribs
K4=open('/tmp/kcf/data/k4.txt').read().strip(); CR=cribs()
for k in KINDS:
  t=time.time(); print('K4 w21 p21 dir1',k,count(K4,CR,21,21,k),f'({time.time()-t:.1f}s)',flush=True)
