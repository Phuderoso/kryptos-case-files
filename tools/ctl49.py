"""Cycle 49 planted controls and shuffled nulls for the Bazeries digit-group reversal test."""
import random, sys
sys.path.insert(0,'/workspace/k4c48'); from kryptos_text import K4, KA
rng=random.Random(49)
fill=("THEQUICKSURVEYORWALKEDSLOWLYALONGTHEOLDWALLCOUNTINGPACESFROMTHEGATEUNTILHEREACHEDTHESTONE"
      "MARKEDWITHACROSSWHEREHEKNELTANDBEGANTODIGCAREFULLYINTOTHEDARKEARTH")
pt=list(fill[:97]); pt[21:34]="EASTNORTHEAST"; pt[63:74]="BERLINCLOCK"; pt=''.join(pt)
def perm(dig,rev):
    r=[0]*97;i=g=0
    while i<97:
        s=min(dig[g%len(dig)],97-i)
        for t in range(s): r[i+t]=i+s-1-t
        i+=s; g+=1
    if rev: r=[96-x for x in r]
    return r
def enc_mono(pt,dig,rev,m):
    r=perm(dig,rev); c=['']*97
    for i,ch in enumerate(pt): c[r[i]]=m[ch]
    return ''.join(c)
def enc_per(pt,dig,rev,key,tab,mode,order):
    A=KA if tab=='KA' else 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'; r=perm(dig,rev); c=['']*97
    for i,ch in enumerate(pt):
        j=r[i]; k=A.index(key[(i if order=='before' else j)%len(key)]); p=A.index(ch)
        c[j]=A[(p+k)%26] if mode=='vig' else A[(k-p)%26]
    return ''.join(c)
L=list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'); rng.shuffle(L); m=dict(zip('ABCDEFGHIJKLMNOPQRSTUVWXYZ',L))
out={'ctl_mono_3752':enc_mono(pt,[3,7,5,2],0,m),
     'ctl_mono_rev_61834':enc_mono(pt,[6,1,8,3,4],1,m),
     'ctl_KAvig_after_SHADOW_2864':enc_per(pt,[2,8,6,4],0,'SHADOW','KA','vig','after'),
     'ctl_AZbeau_before_PALIMPSEST_957':enc_per(pt,[9,5,7],0,'PALIMPSEST','AZ','beau','before'),
     'ctl_KAvig_before_ABSCISSA_rev_4931726':enc_per(pt,[4,9,3,1,7,2,6],1,'ABSCISSA','KA','vig','before')}
for n in range(3):
    s=list(K4); rng.shuffle(s); out[f'null{n}']=''.join(s)
for k,v in out.items(): print(k,v)
