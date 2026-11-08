"""Cycle 148: digit streams of mathematical constants -> key streams (values 0-25), one per line: name len v v v...
D1 single digits; P0/P1 non-overlapping digit pairs mod 26 (phase 0/1); Q0/Q1 non-overlapping pairs kept only if < 26."""
import mpmath as mp
mp.mp.dps=10100
C={'pi':mp.pi,'e':mp.e,'sqrt2':mp.sqrt(2),'sqrt3':mp.sqrt(3),'sqrt5':mp.sqrt(5),'phi':(1+mp.sqrt(5))/2,'ln2':mp.log(2),'gamma':mp.euler}
for n,v in C.items():
    s=mp.nstr(v,10050,strip_zeros=False).replace('.','')[:10000]; d=[int(c) for c in s]
    print(n+'_D1',len(d),*d)
    for ph in (0,1):
        pr=[10*d[i]+d[i+1] for i in range(ph,len(d)-1,2)]
        print(f'{n}_P{ph}',len(pr),*[x%26 for x in pr])
        q=[x for x in pr if x<26]; print(f'{n}_Q{ph}',len(q),*q)
