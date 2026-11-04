# Cycle 55 planted Ragbaby controls + shuffled nulls
import random
K4=open('/workspace/k4c53/k4.txt').read().strip()
AL=open('alpha.bin','rb').read()
words="IT WAS LATE WHEN WE HEADED EAST NORTHEAST ACROSS THE RIVER UNTIL WE HEARD THE BERLIN CLOCK STRIKE TWELVE IN THE SQUARE".split()
# keep crib positions: build plaintext then check
pt=''.join(words)
assert len(pt)==97 and pt[21:34]=="EASTNORTHEAST" and pt[63:74]=="BERLINCLOCK", (len(pt),pt[21:34],pt[63:74])
def enc(a,dir,d,n0,ws):
    A=AL[26*a:26*a+26]; idx={l:j for j,l in enumerate(A)}; out=[]
    for w,word in enumerate(ws):
        for j,ch in enumerate(word):
            s=n0+d*(w+j); out.append(chr(65+A[(idx[ord(ch)-65]+dir*s)%26]))
    return ''.join(out)
ctl={'CTL1':enc(1,1,1,1,words),'CTL2':enc(5000,-1,1,1,words),'CTL3':enc(20000,1,3,7,words),
     'CTL4':enc(0,1,1,1,"ITWASLATEWHENWEHEADED EASTNORTHEAST ACROSSTHERIVERUNTILWEHEARDTHE BERLINCLOCK STRIKETWELVEINTHESQUARE".split())}
random.seed(55)
for n in range(5):
    s=list(K4); random.shuffle(s); ctl['NULL%d'%n]=''.join(s)
with open('ctl55.txt','w') as f:
    for k,v in ctl.items(): f.write(k+' '+v+'\n')
