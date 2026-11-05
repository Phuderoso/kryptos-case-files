# Cycle 65 controls and nulls. Planted Gromark (base 10, primer length 5) with two random alphabets; shuffled K4 nulls.
import random
K4=open('k4.txt').read().strip()
PTS=["THEROADTURNSSHARPLYTO"+"EASTNORTHEAST"+"ANDFOLLOWSTHERIVERUNTILYOUSEE"+"BERLINCLOCK"+"STANDINGBYTHEGATEATDUSK",
     "ITWASHIDDENUNDERSTONE"+"EASTNORTHEAST"+"WHERETHESHADOWFALLSNEARTHEOLD"+"BERLINCLOCK"+"TOWERANDTHEWALLBEHINDIT"]
for p in PTS: assert len(p)==97 and p[21:34]=="EASTNORTHEAST" and p[63:74]=="BERLINCLOCK"
def keygen(pr,n):
    k=list(pr)
    while len(k)<n: L=len(pr); k.append((k[-L]+k[-L+1])%10)
    return k
rng=random.Random(65)
out=[]
for c,(pt) in enumerate(PTS*2):
    pa=list(range(26)); ca=list(range(26)); rng.shuffle(pa); rng.shuffle(ca)  # pa[letter]=index, ca[letter]=index
    cainv={v:i for i,v in enumerate(ca)}
    pr=[rng.randrange(10) for _ in range(5)]; k=keygen(pr,97)
    ct=''.join(chr(65+cainv[(pa[ord(ch)-65]+k[i])%26]) for i,ch in enumerate(pt))
    out.append(f"CTL{c+1} {ct} primer={''.join(map(str,pr))} pt={pt}")
for s in range(6):
    l=list(K4); random.Random(1000+s).shuffle(l); out.append(f"NULL{s} {''.join(l)}")
open('ctl65.txt','w').write('\n'.join(out)+'\n'); print('\n'.join(out))
