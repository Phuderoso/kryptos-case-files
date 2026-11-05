# Cycle 105: periodic substitution (period p | w) FIRST, columnar transposition width w LAST.
# Exact crib-feasibility by backtracking over column orders. Both read directions.
# Tableaux: Vigenere/Beaufort/variant over AZ and KA, plus 'general' (free alphabet per phase).
import sys, random, time
A='ABCDEFGHIJKLMNOPQRSTUVWXYZ'; KA='KRYPTOSABCDEFGHIJLMNQUVWXZ'
def cribs():
  d={}
  for s,w in ((21,'EASTNORTHEAST'),(63,'BERLINCLOCK')):
    for j,ch in enumerate(w): d[s+j]=ch
  return d
def keyf(kind):
  al=KA if 'KA' in kind else A
  if kind.startswith('vig'):  return lambda c,p:(al.index(c)-al.index(p))%26
  if kind.startswith('beau'): return lambda c,p:(al.index(c)+al.index(p))%26
  if kind.startswith('var'):  return lambda c,p:(al.index(p)-al.index(c))%26
KINDS=['vigAZ','beauAZ','varAZ','vigKA','beauKA','varKA','general']
def solve(CT,CR,w,p,kind,direction,limit=5,only=None):
  N=len(CT); L=[N//w+(1 if c<N%w else 0) for c in range(w)]
  kf=None if kind=='general' else keyf(kind)
  sols=[]; used=[False]*w; order=[]
  # state: key per phase (tableau) or maps per phase (general)
  key={}; fmap=[dict() for _ in range(p)]; rmap=[dict() for _ in range(p)]
  def pairs_for(c,start):
    # list of (plaintext index i, ct index j) for crib positions when column c sits at slot with this start
    out=[]
    if direction==0:   # write rows, read columns: P[r*w+c] -> CT[start+r]
      for r in range(L[c]):
        i=r*w+c
        if i in CR: out.append((i,start+r))
    else:              # write columns in order, read rows: P[start+r] -> CT[r*w+c]
      for r in range(L[c]):
        i=start+r
        if i in CR: out.append((i,r*w+c))
    return out
  def rec(start):
    if len(sols)>=limit: return
    if len(order)==w: sols.append(order[:]); return
    for c in (range(w) if only is None else [only[len(order)]]):
      if used[c]: continue
      pr=pairs_for(c,start); undo=[]; ok=True
      for i,j in pr:
        ph=i%p; P=CR[i]; C=CT[j]
        if kf:
          k=kf(C,P)
          if ph in key:
            if key[ph]!=k: ok=False;break
          else: key[ph]=k; undo.append(('k',ph))
        else:
          a=fmap[ph].get(P); b=rmap[ph].get(C)
          if a is None and b is None: fmap[ph][P]=C; rmap[ph][C]=P; undo.append(('m',ph,P,C))
          elif a!=C or b!=P: ok=False;break
      if ok:
        used[c]=True; order.append(c); rec(start+L[c]); order.pop(); used[c]=False
      for u in undo:
        if u[0]=='k': del key[u[1]]
        else: del fmap[u[1]][u[2]]; del rmap[u[1]][u[3]]
      if len(sols)>=limit: return
  rec(0); return sols
def encrypt_control(PT,w,p,order,kind,direction,seed=1):
  R=random.Random(seed); al=KA if 'KA' in kind else A; k=[R.randrange(26) for _ in range(p)]
  sub=''.join(al[(al.index(ch)+k[i%p])%26] for i,ch in enumerate(PT))
  N=len(PT); L=[N//w+(1 if c<N%w else 0) for c in range(w)]
  if direction==0: return ''.join(sub[r*w+c] for c in order for r in range(L[c]))
  out=['']*N; s=0
  for c in order:
    for r in range(L[c]): out[r*w+c]=sub[s+r]
    s+=L[c]
  return ''.join(out)
if __name__=='__main__':
  K4=open('/workspace/k4c101/k4.txt').read().strip(); CR=cribs()
  mode=sys.argv[1]
  if mode=='ctl':
    PT="WEDUGTHROUGHTHERUBBLE"+"EASTNORTHEAST"+"ANDFOUNDTHEDOORUNDERTHEOLDBRI"+"BERLINCLOCK"+"TOWERASTHESUNWENTDOWNXX"
    R=random.Random(105)
    for (w,p,kind,dr) in [(14,7,'vigAZ',0),(14,7,'vigKA',1),(7,7,'vigAZ',0),(10,5,'vigKA',0),(12,6,'vigAZ',1)]:
      o=list(range(w)); R.shuffle(o); ct=encrypt_control(PT,w,p,o,kind,dr)
      t=time.time(); s=solve(ct,CR,w,p,kind,dr,limit=5000)
      a=bool(solve(ct,CR,w,p,kind,dr,only=o)); g=bool(solve(ct,CR,w,p,'general',dr,only=o))
      print(f'CTL w{w} p{p} {kind} dir{dr}: true order accepted={a} general_accepts={g} found_in_search={o in s} nsol(<=5000)={len(s)} ({time.time()-t:.1f}s)')
  else:
    tl=float(sys.argv[2]) if len(sys.argv)>2 else 400; T0=time.time()
    for w in range(5,22):
      for p in [d for d in range(3,w+1) if w%d==0]:
        for dr in (0,1):
          for kind in KINDS:
            if time.time()-T0>tl: print('TIME LIMIT at',w,p,dr,kind); sys.exit()
            t=time.time(); s=solve(K4,CR,w,p,kind,dr,limit=5)
            print(f'K4 w{w} p{p} dir{dr} {kind:8s} sols={len(s)}{" "+str(s[0]) if s else ""} ({time.time()-t:.1f}s)',flush=True)
