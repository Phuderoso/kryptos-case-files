# Cycle 56 planted interrupted-key controls + shuffled-K4 nulls
import random
K4=open('k4.txt').read().strip(); AL=open('alpha.bin','rb').read()
words="IT WAS LATE WHEN WE HEADED EAST NORTHEAST ACROSS THE RIVER UNTIL WE HEARD THE BERLIN CLOCK STRIKE TWELVE IN THE SQUARE".split()
pt=''.join(words); assert len(pt)==97 and pt[21:34]=="EASTNORTHEAST" and pt[63:74]=="BERLINCLOCK"
def enc(a,mode,key,restarts):
    A=AL[26*a:26*a+26]; idx={l:j for j,l in enumerate(A)}; out=[]; j=0
    for i,ch in enumerate(pt):
        if i in restarts: j=0
        k=idx[ord(key[j%len(key)])-65]; p=idx[ord(ch)-65]
        c = (p+k) if mode==0 else (k-p) if mode==1 else (p-k)
        out.append(chr(65+A[c%26])); j+=1
    return ''.join(out)
starts=set(); s=0
for w in words: starts.add(s); s+=len(w)
random.seed(56); rnd=set(random.sample(range(1,97),12))
ctl={'CTL1':enc(1,0,'SHADOW',starts),'CTL2':enc(5000,1,'PALIMPSEST',rnd),'CTL3':enc(1,2,'BURIEDSTONE',starts),
     'CTL4':enc(0,0,'LANGLEY',{0})}  # CTL4: no interruption at all = plain periodic keyword, must also be found
for n in range(5):
    x=list(K4); random.shuffle(x); ctl['NULL%d'%n]=''.join(x)
with open('ctl56.txt','w') as f:
    for k,v in ctl.items(): f.write(k+' '+v+'\n')
print(open('ctl56.txt').read())
