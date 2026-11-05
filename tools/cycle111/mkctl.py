import random
from common import *
base=["SLOWLYTHEDESPERATELYSLOWLYTHEREMAINSOFPASSAGEDEBRISTHATENCUMBEREDTHELOWERPARTOFTHEDOORWAYWEREREMOVED",
"ITWASTOTALLYINVISIBLEHOWSTHATPOSSIBLETHEYUSEDTHEEARTHSMAGNETICFIELDTHEINFORMATIONWASGATHEREDANDTRANSMITTED",
"WEWALKEDOUTFROMTHEOLDGATEANDTURNEDTOWARDTHEMARKETSQUAREWHERETHESTREETCLOCKSTOODABOVETHECROWDEDPLATFORMNEARHOME"]
out=[]
for j,b in enumerate(base):
    random.seed(1000+j)
    pt=list(b[:97])
    for i,ch in CRIBS.items(): pt[i]=ch
    pt="".join(pt)
    pins=[[random.randint(0,1) for _ in range(P)] for P in PER]
    n=[0]*21
    for _ in range(27):
        t=random.randrange(22)
        if t<21:n[t]+=1
    for mode in (0,1):
        ct=enc(pt,pins,n,mode)
        out.append(f"ctl{j}m{mode} {ct} {pt}")
open("controls.txt","w").write("\n".join(out)+"\n")
random.seed(111)
nl=[]
for j in range(8):
    l=list(K4);random.shuffle(l);nl.append(f"null{j} {''.join(l)}")
open("nulls.txt","w").write("\n".join(nl)+"\n")
