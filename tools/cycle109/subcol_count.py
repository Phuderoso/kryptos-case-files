# Cycle 109: exact COUNT of column orders consistent with the cribs, for "periodic substitution (p | w) first,
# complete columnar width w last" (cycle 105 model and conventions, tools/cycle105/subcol.py).
# Memoized over (columns used, key so far); the start offset is fixed by the set of columns used.
import sys, time, random
sys.setrecursionlimit(10000)
from subcol import cribs, keyf, A, KA
def encrypt_control(PT,w,p,order,kind,direction,seed=1):
  R=random.Random(seed); al=KA if 'KA' in kind else A; k=[R.randrange(26) for _ in range(p)]
  def e(ch,kk):
    x=al.index(ch)
    return al[(x+kk)%26] if kind.startswith('vig') else al[(kk-x)%26] if kind.startswith('beau') else al[(x-kk)%26]
  sub=''.join(e(ch,k[i%p]) for i,ch in enumerate(PT))
  N=len(PT); L=[N//w+(1 if c<N%w else 0) for c in range(w)]
  if direction==0: return ''.join(sub[r*w+c] for c in order for r in range(L[c]))
  out=['']*N; s=0
  for c in order:
    for r in range(L[c]): out[r*w+c]=sub[s+r]
    s+=L[c]
  return ''.join(out)
def count(CT,CR,w,p,kind,direction,only=None,deadline=None):
  N=len(CT); L=[N//w+(1 if c<N%w else 0) for c in range(w)]
  kf=keyf(kind); pre={}
  def cons(c,start):
    k=(c,start)
    if k in pre: return pre[k]
    out={}
    for r in range(L[c]):
      if direction==0: i=r*w+c; j=start+r
      else: i=start+r; j=r*w+c
      if i in CR:
        ph=i%p; v=kf(CT[j],CR[i])
        if out.get(ph,v)!=v: pre[k]=None; return None
        out[ph]=v
    pre[k]=tuple(out.items()); return pre[k]
  memo={}; key=[-1]*p
  def rec(mask,start,depth):
    if mask==(1<<w)-1: return 1
    st=(mask,tuple(key))
    if st in memo: return memo[st]
    if deadline and time.time()>deadline: raise TimeoutError
    tot=0
    for c in (range(w) if only is None else [only[depth]]):
      if mask>>c&1: continue
      cs=cons(c,start)
      if cs is None: continue
      ok=True; set_=[]
      for ph,v in cs:
        if key[ph]==-1: key[ph]=v; set_.append(ph)
        elif key[ph]!=v: ok=False; break
      if ok: tot+=rec(mask|1<<c,start+L[c],depth+1)
      for ph in set_: key[ph]=-1
    if only is None: memo[st]=tot
    return tot
  return rec(0,0,0)
KINDS=['vigAZ','beauAZ','varAZ','vigKA','beauKA','varKA']
if __name__=='__main__':
  K4=open('/tmp/kcf/data/k4.txt').read().strip(); CR=cribs(); mode=sys.argv[1]
  cfgs=[(14,7,1),(14,14,1),(13,13,1),(21,3,0),(21,7,0),(21,21,0),(21,3,1),(21,7,1),(21,21,1)]
  if mode=='ctl':
    PT="WEDUGTHROUGHTHERUBBLE"+"EASTNORTHEAST"+"ANDFOUNDTHEDOORUNDERTHEOLDBRI"+"BERLINCLOCK"+"TOWERASTHESUNWENTDOWNXX"
    R=random.Random(109)
    for (w,p,dr) in cfgs:
      kind=R.choice(KINDS); o=list(range(w)); R.shuffle(o); ct=encrypt_control(PT,w,p,o,kind,dr)
      t=time.time()
      try: n=count(ct,CR,w,p,kind,dr,deadline=time.time()+90)
      except TimeoutError: n='TIMEOUT'
      print(f'CTL w{w} p{p} dir{dr} {kind}: true order accepted={count(ct,CR,w,p,kind,dr,only=o)==1} consistent orders={n} ({time.time()-t:.1f}s)',flush=True)
  else:
    texts=[('K4',K4)]
    R=random.Random(1090)
    for i in range(int(sys.argv[2]) if len(sys.argv)>2 else 0):
      l=list(K4); R.shuffle(l); texts.append((f'null{i}',''.join(l)))
    sel=[c for c in cfgs if f'{c[0]},{c[1]},{c[2]}' in sys.argv[3:]] if len(sys.argv)>3 else cfgs
    for w,p,dr in sel:
      for name,ct in texts:
        row=[]
        for kind in KINDS:
          try: n=count(ct,CR,w,p,kind,dr,deadline=time.time()+20)
          except TimeoutError: n='T/O'
          row.append(f'{kind}={n}')
        print(f'{name} w{w} p{p} dir{dr}: '+' '.join(row),flush=True)
