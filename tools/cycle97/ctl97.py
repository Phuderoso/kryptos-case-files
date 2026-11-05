import random,struct
PT="WEDUGTHROUGHTHERUBBLE"+"EASTNORTHEAST"+"ANDFOUNDTHEDOORUNDERTHEOLDBRI"+"BERLINCLOCK"+"TOWERASTHESUNWENTDOWNXX"
tw=open('tw264.bin','rb').read(); A=lambda i:[tw[i*26+k] for k in range(26)]
def enc(pt,alpha,m,d1,d2,W):
    s={alpha[k]:k for k in range(26)}; inv={k:alpha[k] for k in range(26)}; out=''
    for i,ch in enumerate(pt):
        t=i//m; y=W[(s[ord(ch)-65]+d1*t)%26]; out+=chr(65+inv[(y-d2*t)%26])
    return out
def place(T,fn,t):
    P=open(fn,'rb').read(); perm=struct.unpack('<97h',P[t*194:(t+1)*194]); c=['?']*97
    for j in range(97): c[perm[j]]=T[j]
    return ''.join(c)
random.seed(97); W=list(range(26)); random.shuffle(W)
print('dec', place(enc(PT,A(100),1,5,5,W),'dec_perm.bin',12345))      # rotor behind K3-law decimation
print('route', place(enc(PT,A(7),3,2,9,W),'route_perm.bin',4321))     # m=3 behind a route
print('p97', place(enc(PT,A(1),2,4,4,W),'perms97.bin',100000))        # KA, m=2 behind 165k family
