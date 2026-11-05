# Cycle 110: exact count for "periodic substitution (p | w) first, complete columnar width w last",
# columns-in direction (dir1), by choosing column IDENTITIES only where a column's chunk of the
# substituted text touches a crib; every other slot is a filler of known length (long/short), and
# fillers are counted combinatorially: count = sum over paths of (longs left)! * (shorts left)!.
# Same conventions as tools/cycle109/subcol_count.py (dir1 only).
import sys, time, random
from math import factorial
from functools import lru_cache
from subcol import cribs, keyf, A, KA
from subcol_count import encrypt_control, KINDS, count as count109
def count(CT,CR,w,p,kind):
  N=len(CT); nlong=N%w; Ls=N//w+1; Ss=N//w
  NL=nlong; NS=w-nlong; kf=keyf(kind)
  touches=lambda s,l: any(s+r in CR for r in range(l))
  def cons(c,start,l):
    out={}
    for r in range(l):
      i=start+r
      if i in CR:
        v=kf(CT[r*w+c],CR[i]); ph=i%p
        if out.get(ph,v)!=v: return None
        out[ph]=v
    return out
  @lru_cache(maxsize=None)
  def rec(start,nl,ns,spec,key):
    if start==N:
      sl=sum(1 for c in spec if c<nlong); ss=len(spec)-sl
      return factorial(NL-sl)*factorial(NS-ss)
    tot=0; kd=dict(key)
    for isl,l in ((True,Ls),(False,Ss)):
      if isl and nl>=NL: continue
      if not isl and ns>=NS: continue
      n2=(nl+1,ns) if isl else (nl,ns+1)
      if not touches(start,l):
        tot+=rec(start+l,*n2,spec,key); continue
      for c in (range(nlong) if isl else range(nlong,w)):
        if c in spec: continue
        cs=cons(c,start,l)
        if cs is None: continue
        if any(kd.get(ph,v)!=v for ph,v in cs.items()): continue
        k2=dict(kd); k2.update(cs)
        later={i%p for i in CR if i>=start+l}; k2={ph:v for ph,v in k2.items() if ph in later}
        tot+=rec(start+l,*n2,tuple(sorted(spec+(c,))),tuple(sorted(k2.items())))
    return tot
  # fillers must not reuse specific columns: enforced because filler identities are assigned at the end
  # from the columns not in spec, and the long/short totals are exact.
  return rec(0,0,0,(),())
if __name__=='__main__':
  K4=open('/tmp/kcf/data/k4.txt').read().strip(); CR=cribs(); mode=sys.argv[1]
  PT="WEDUGTHROUGHTHERUBBLE"+"EASTNORTHEAST"+"ANDFOUNDTHEDOORUNDERTHEOLDBRI"+"BERLINCLOCK"+"TOWERASTHESUNWENTDOWNXX"
  if mode=='agree':   # cross-check against cycle 109's counter on configs it could finish
    R=random.Random(1101)
    for (w,p) in [(13,13),(14,7),(14,14),(21,7),(21,3),(11,11),(12,6)]:
      kind=R.choice(KINDS); o=list(range(w)); R.shuffle(o); ct=encrypt_control(PT,w,p,o,kind,1,seed=R.randrange(9999))
      for name,t in (('ctl',ct),('K4',K4)):
        a=count(t,CR,w,p,kind)
        try: b=count109(t,CR,w,p,kind,1,deadline=time.time()+60)
        except TimeoutError: b='T/O'
        print(f'w{w} p{p} {kind} {name}: new={a} cycle109={b} agree={a==b if b!="T/O" else "n/a"}',flush=True)
  elif mode=='ctl':
    R=random.Random(110); w=p=21
    for kind in KINDS:
      o=list(range(w)); R.shuffle(o); ct=encrypt_control(PT,w,p,o,kind,1,seed=R.randrange(10**6))
      t=time.time(); print(f'CTL w21 p21 dir1 {kind}: consistent orders={count(ct,CR,w,p,kind)} ({time.time()-t:.1f}s)',flush=True)
  else:
    n=int(sys.argv[2]); R=random.Random(1100); texts=[('K4',K4)]
    for i in range(n):
      l=list(K4); R.shuffle(l); texts.append((f'null{i}',''.join(l)))
    for name,ct in texts:
      t=time.time(); print(name,'w21 p21 dir1:',' '.join(f'{k}={count(ct,CR,21,21,k)}' for k in KINDS),f'({time.time()-t:.0f}s)',flush=True)
