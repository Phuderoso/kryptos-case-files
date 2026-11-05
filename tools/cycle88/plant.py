import sys
N=92; KA="KRYPTOSABCDEFGHIJLMNQUVWXZ"; AZ="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
q=int(sys.argv[1]); model=int(sys.argv[2]); key=sys.argv[3]; alph=KA if sys.argv[4]=="KA" else AZ
data=open('perms92.bin','rb').read(); P=list(data[q*N:(q+1)*N])
pt=("SLOWLYDESPARATLYSLOWLYTHEREMAINSOFPASSAGEDEBRISTHATEN"*3)
pt=list(pt[:N]); pt[20:33]="EASTNORTHEAST"; pt[60:71]="BERLINCLOCK"; pt="".join(pt)
k=[alph.index(c) for c in key]; p=len(k); ct=[""]*N
for j in range(N):
    i=P[j]; ki = i%p if model==0 else j%p
    ct[j]=alph[(alph.index(pt[i])+k[ki])%26]
print("".join(ct)); print(pt,file=sys.stderr)
