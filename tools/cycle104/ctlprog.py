import random
exec(open('prog.py').read().split('h=test(K)')[0])
PT="WEDUGTHROUGHTHERUBBLE"+"EASTNORTHEAST"+"ANDFOUNDTHEDOORUNDERTHEOLDBRI"+"BERLINCLOCK"+"TOWERASTHESUNWENTDOWNXX"
r=random.Random(9); ok=0
for t in range(6):
  nm,A=ALS[t%2]; md=['vig','beau','var'][t%3]; per=r.randint(3,21); D=r.randint(1,25); base=[r.randrange(26) for _ in range(per)]
  CT=''
  for i,ch in enumerate(PT):
    k=(base[i%per]+D*(i//per))%26; p=A.index(ch)
    c={'vig':(p+k)%26,'beau':(k-p)%26,'var':(p-k)%26}[md]; CT+=A[c]
  h=test(CT); found=any(x[0]==nm and x[1]==md and x[2]==per and x[3]==D for x in h)
  print(nm,md,per,D,'found' if found else 'MISSED','hits',len(h)); ok+=found
print('controls',ok,'/6')
