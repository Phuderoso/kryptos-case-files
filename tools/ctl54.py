# Cycle 54 planted controls and shuffled nulls for splitkey.c
import random
K4=open('/workspace/k4c53/k4.txt').read().strip()
AL=open('alpha.bin','rb').read()
def alpha(a): return [AL[26*a+i] for i in range(26)]
pt="ITWASLATEWHENWEHEADED"+"EASTNORTHEAST"+"ACROSSTHERIVERUNTILWEHEARDTHE"+"BERLINCLOCK"+"STRIKETWELVEINTHESQUARE"
assert len(pt)==97 and pt[21:34]=="EASTNORTHEAST" and pt[63:74]=="BERLINCLOCK"
def enc(pt,a1,v1,k1,a2,v2,k2,b):
    out=[]
    for i,ch in enumerate(pt):
        a,v,k=(a1,v1,k1) if i<b else (a2,v2,k2)
        A=alpha(a); idx={l:j for j,l in enumerate(A)}; kk=idx[ord(k[i%len(k)])-65]
        p=idx[ord(ch)-65]; c=(p+kk)%26 if v==0 else (kk-p)%26
        out.append(chr(65+A[c]))
    return ''.join(out)
ctl={
 'CTL1':enc(pt,1,0,"PALIMPS",1,0,"SHADOW",45),      # KA Vig, p 7/6, split 45
 'CTL2':enc(pt,0,1,"LAYERTWO",1,0,"ABSCI",52),      # AZ Beaufort then KA Vig, cross alphabets
 'CTL3':enc(pt,5000,0,"IQLUSION",5000,1,"DESPARATLY",38), # themed alphabet #5000, Vig then Beaufort p 8/10
}
random.seed(54)
for n in range(5):
    s=list(K4); random.shuffle(s); ctl['NULL%d'%n]=''.join(s)
with open('ctl54.txt','w') as f:
    for k,v in ctl.items(): f.write(k+' '+v+'\n')
print(pt)
