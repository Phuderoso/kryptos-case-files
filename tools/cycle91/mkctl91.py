# planted control for the W-free Playfair + mod-25 outer key model
import random, sys
KA="KRYPTOSABCDEFGHIJLMNQUVWXZ"; AZ="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
seed,p,tab,mode,a=int(sys.argv[1]),int(sys.argv[2]),sys.argv[3],int(sys.argv[4]),int(sys.argv[5])
r=random.Random(seed); L=[c for c in AZ if c!='W']; r.shuffle(L); pos={c:(i//5,i%5) for i,c in enumerate(L)}
base="SLOWLYDESPARATLYSLOWLYTHEREMAINSOFPASSAGEDEBRISTHATENCUMBEREDTHELOWERPARTOFTHEDOORWAYWASREMOVED".replace('W','V')*2
pt=list(base[:92])
for i,c in enumerate("EASTNORTHEAST"): pt[20+i]=c
for i,c in enumerate("BERLINCLOCK"): pt[60+i]=c
for i in range(a,91,2):          # break doubled pairs outside cribs
    if pt[i]==pt[i+1]:
        j=i+1 if not (60<=i+1<=70 or 20<=i+1<=32) else i
        pt[j]='Q' if pt[j]!='Q' else 'X'
assert all(pt[i]!=pt[i+1] for i in range(a,91,2))
inner=pt[:]
for i in range(a,91,2):
    (r1,c1),(r2,c2)=pos[pt[i]],pos[pt[i+1]]
    if r1==r2: o=(L[r1*5+(c1+1)%5],L[r2*5+(c2+1)%5])
    elif c1==c2: o=(L[((r1+1)%5)*5+c1],L[((r2+1)%5)*5+c2])
    else: o=(L[r1*5+c2],L[r2*5+c1])
    inner[i],inner[i+1]=o
T=(KA if tab=="KA" else AZ).replace('W',''); key=[r.randrange(25) for _ in range(p)]
ct="".join(T[(T.index(q)+key[i%p])%25] if mode==0 else T[(key[i%p]-T.index(q))%25] if mode==1 else T[(T.index(q)-key[i%p])%25] for i,q in enumerate(inner))
print(ct)
