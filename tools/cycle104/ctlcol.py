import sys,random; sys.argv=['x']; exec(open('colgen.py').read().split("if __name__")[0])
PT="WEDUGTHROUGHTHERUBBLE"+"EASTNORTHEAST"+"ANDFOUNDTHEDOORUNDERTHEOLDBRI"+"BERLINCLOCK"+"TOWERASTHESUNWENTDOWNXX"
r=random.Random(21); ok=0
for t,(w,p,mode) in enumerate([(7,3,0),(6,2,1),(8,3,1)]):
  order=list(range(w)); r.shuffle(order); s=colperm(w,order); al=[]
  for _ in range(p): a=list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'); r.shuffle(a); al.append(a)
  CT=['?']*N
  for i in range(N): ph=(i if mode==0 else s[i])%p; CT[s[i]]=al[ph][ord(PT[i])-65]
  CT=''.join(CT); res=run(CT,w,p)
  f=any(x[0]==w and list(x[1])==order and x[2]==0 and x[3]==mode and x[4]==p for x in res); ok+=f; print(w,p,mode,'found' if f else 'MISSED',len(res))
print('controls',ok,'/3')
