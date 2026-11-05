# Cycle 105: cryptodiagnosis by simulation. Which cipher families naturally reproduce K4's three tells?
#  T1 doubles clustered in one residue class (look-elsewhere excess over moduli 2-25 >= K4's 4.14)
#  T2 width-21 vertical-bigram repeats >= 11
#  T3 flat IC <= 0.0400 (K4 0.0361)
import random,re,sys
txt=re.sub('[^A-Z]','',open('/home/box/kryptos_support_backup/rk_plain.txt').read().upper())
A='ABCDEFGHIJKLMNOPQRSTUVWXYZ'; KA='KRYPTOSABCDEFGHIJLMNQUVWXZ'; N=97
K4=open('/workspace/k4c101/k4.txt').read().strip()
def excess(t):
  d=[i for i in range(len(t)-1) if t[i]==t[i+1]]
  if not d: return 0.0
  b=0
  for m in range(2,26):
    c={}
    for x in d: c[x%m]=c.get(x%m,0)+1
    b=max(b,max(c.values())-len(d)/m)
  return b
def rep(t,w):
  pr=[(t[i],t[i+w]) for i in range(len(t)-w)]; return len(pr)-len(set(pr))
def ic(t):
  from collections import Counter
  c=Counter(t); return sum(v*(v-1) for v in c.values())/(len(t)*(len(t)-1))
def colT(s,order):
  w=len(order); return ''.join(s[i] for col in order for i in range(col,len(s),w))
def vig(p,key,al=A):
  return ''.join(al[(al.index(ch)+key[i%len(key)])%26] for i,ch in enumerate(p))
R=random.Random(7)
def pt(): i=R.randrange(len(txt)-200); return txt[i:i+N]
def rkey(L): return [R.randrange(26) for _ in range(L)]
def mono(p):
  a=list(A); R.shuffle(a); return ''.join(a[ord(c)-65] for c in p)
def autokey(p):
  k=rkey(7); out=[]; ks=k[:]
  for i,ch in enumerate(p):
    kk=ks[i]; out.append(A[(ord(ch)-65+kk)%26]); ks.append(ord(ch)-65)
  return ''.join(out)
def gromark(p):
  d=[R.randrange(10) for _ in range(5)]
  while len(d)<N: d.append((d[-5]+d[-4])%10)
  a=list(A); R.shuffle(a); return ''.join(a[(ord(ch)-65+d[i])%26] for i,ch in enumerate(p))
def running(p):
  q=pt(); return ''.join(A[(ord(a)+ord(b)-130)%26] for a,b in zip(p,q))
def prog7(p):
  k=rkey(7); D=R.randrange(1,26); return ''.join(A[(ord(ch)-65+k[i%7]+D*(i//7))%26] for i,ch in enumerate(p))
def qIII(p,L): return vig(p,rkey(L),KA)
def rand_order(w): o=list(range(w)); R.shuffle(o); return o
fam={
 'random letters (null)': lambda p: ''.join(R.choice(A) for _ in range(N)),
 'monoalphabetic': mono,
 'Vigenere p7': lambda p: vig(p,rkey(7)),
 'Vigenere p14': lambda p: vig(p,rkey(14)),
 'Vigenere p21': lambda p: vig(p,rkey(21)),
 'Quagmire III (KA) p7': lambda p: qIII(p,7),
 'progressive p7 (k+D each period)': prog7,
 'PT-autokey primer 7': autokey,
 'Gromark (mixed alphabet)': gromark,
 'running key (English)': running,
 'columnar w7 then Vigenere p7': lambda p: vig(colT(p,rand_order(7)),rkey(7)),
 'Vigenere p7 then columnar w7': lambda p: colT(vig(p,rkey(7)),rand_order(7)),
 'Vigenere p7 then columnar w14': lambda p: colT(vig(p,rkey(7)),rand_order(14)),
 'columnar w21 then mono': lambda p: mono(colT(p,rand_order(21))),
 'Vigenere p21 then columnar w7': lambda p: colT(vig(p,rkey(21)),rand_order(7)),
}
k4=(excess(K4),rep(K4,21),ic(K4)); print('K4 excess %.2f rep21 %d IC %.4f'%k4)
NS=int(sys.argv[1]) if len(sys.argv)>1 else 3000
for name,f in fam.items():
  t1=t2=t3=j=0
  for _ in range(NS):
    c=f(pt()); a=excess(c)>=k4[0]-1e-9; b=rep(c,21)>=11; d=ic(c)<=0.040
    t1+=a; t2+=b; t3+=d; j+=a and d
  print(f'{name:38s} T1 {t1/NS:.4f}  T2 {t2/NS:.4f}  T3 {t3/NS:.3f}  T1&T3 {j/NS:.4f}')

if len(sys.argv)>2:
  print('--- scan: Vigenere p then columnar w (T1, T2, T1&T2&T3) ---')
  for p in (5,7,8,10,14,21):
    row=[]
    for w in (6,7,8,10,13,14,21):
      a1=a2=a3=0
      for _ in range(NS):
        c=colT(vig(pt(),rkey(p)),rand_order(w)); x=excess(c)>=k4[0]-1e-9; y=rep(c,21)>=11; z=ic(c)<=0.040
        a1+=x; a2+=y; a3+=x and y and z
      row.append(f'w{w}:{a1/NS:.4f}/{a2/NS:.4f}/{a3/NS:.5f}')
    print('p',p,' '.join(row))
