# Cycle 55b planted control: Ragbaby (c:KRYPTOS alphabet #33191, dir +1, d=1) then cycle-12 transposition #5000 / #77777
import random,struct
exec(open('ctl55.py').read().split('ctl={')[0])
P=open('/workspace/kcl/data/c12_perm.bin','rb').read()
def perm(n): return struct.unpack('<97H',P[194*n:194*n+194])
def tr(I,n):
    p=perm(n); C=[None]*97
    for j in range(97): C[p[j]]=I[j]
    return ''.join(C)
out={'PCTL1':tr(enc(33191,1,1,1,words),5000),'PCTL2':tr(enc(0,-1,1,3,words),77777)}
random.seed(555)
for n in range(3):
    s=list(K4); random.shuffle(s); out['PNULL%d'%n]=''.join(s)
open('ctl55b.txt','w').write(''.join(k+' '+v+'\n' for k,v in out.items()))
