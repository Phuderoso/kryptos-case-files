import random,struct
PT="WEDUGTHROUGHTHERUBBLE"+"EASTNORTHEAST"+"ANDFOUNDTHEDOORUNDERTHEOLDBRI"+"BERLINCLOCK"+"TOWERASTHESUNWENTDOWNXX"
al=open('alpha.bin','rb').read(); A=lambda i:[al[i*26+k] for k in range(26)]
def enc(pt,alpha,m,d1,d2,W):
    s={alpha[k]:k for k in range(26)}; inv={k:alpha[k] for k in range(26)}; out=''
    for i,ch in enumerate(pt):
        t=i//m; y=W[(s[ord(ch)-65]+d1*t)%26]; out+=chr(65+inv[(y-d2*t)%26])
    return out
random.seed(96); W=list(range(26)); random.shuffle(W)
print('c1 1 1 3 3', enc(PT,A(1),1,3,3,W))          # KA, Hebern, step 3
print('c2 2000 2 5 11', enc(PT,A(2000),2,5,11,W))   # keyed alphabet, rotor every 2 letters
# transposition-first: T = rotor(PT) then carved[perm[j]] = T[j]
Pm=open('c12_perm.bin','rb').read(); perm=struct.unpack('<97h',Pm[777*194:778*194]); T=enc(PT,A(0),1,1,1,W)
c=['?']*97
for j in range(97): c[perm[j]]=T[j]
print('c3 0 1 1 1 perm777', ''.join(c))
# reflector: involution without fixed points
L=list(range(26)); random.shuffle(L); Ref=[0]*26
for k in range(0,26,2): Ref[L[k]]=L[k+1]; Ref[L[k+1]]=L[k]
T=enc(PT,A(1),1,7,7,Ref); c=['?']*97
for j in range(97): c[perm[j]]=T[j]
print('c4 1 1 7 7 perm777 R', ''.join(c))
