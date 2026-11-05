"""Cycle 106 planted Alberti-disk controls and shuffled nulls. Same model as alberti.c:
plaintext letter j enciphered with the disk setting of its segment, then placed at ciphertext position t[j]."""
import numpy as np, random, json
K4="OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR"
perms=np.fromfile('perms97.bin',dtype=np.int16).reshape(-1,97)
tw=np.fromfile('tw264.bin',dtype=np.uint8).reshape(-1,26)
AZ=list(range(26))
PT=("WEDUGTHROUGHTHERUBBLEX"[:21]+"EASTNORTHEAST"+"ANDFOUNDTHEDOORUNDERTHEOLDBRIDGE"[:29]+"BERLINCLOCK"+"TOWERASTHESUNWENTDOWNXX")
assert len(PT)==97 and PT[21:34]=="EASTNORTHEAST" and PT[63:74]=="BERLINCLOCK"
def enc(pt,O,I,beau,segs,t):
    Opos={O[k]:k for k in range(26)}; ct=[None]*97; j=0
    for L,s in segs:
        for _ in range(L):
            if j>=97: break
            p=ord(pt[j])-65; v=(s-Opos[p])%26 if beau else (Opos[p]+s)%26
            ct[int(t[j])]=chr(65+I[v]); j+=1
    return ''.join(ct)
def segs(rng,lo,hi):
    out=[];n=0
    while n<97: L=rng.randint(lo,hi); out.append((L,rng.randrange(26))); n+=L
    return out
rng=random.Random(106); out={}
cases=[('ctl_direct_QIII_KA',list(tw[1]),list(tw[1]),0,0,(4,9)),
       ('ctl_perm77777_QIII_tw100_beau',list(tw[100]),list(tw[100]),1,77777,(3,8)),
       ('ctl_perm123456_QI_tw7',AZ,list(tw[7]),0,123456,(5,12)),
       ('ctl_perm4242_QII_tw55_beau',list(tw[55]),AZ,1,4242,(2,6))]
for name,O,I,b,p,(lo,hi) in cases:
    sg=segs(rng,lo,hi); ct=enc(PT,O,I,b,sg,perms[p]); out[name]=dict(ct=ct,perm=p,segs=sg)
    # true E
    s=[];j=0
    for L,v in sg: s+= [v]*L
    E=sum(s[k]==s[k+1] for k in list(range(21,33))+list(range(63,73)))
    out[name]['trueE']=E; print(name,p,E,ct)
for n in range(5):
    l=list(K4); random.Random(1000+n).shuffle(l); out[f'null{n}']=dict(ct=''.join(l)); print(f'null{n}',''.join(l))
json.dump(out,open('controls106.json','w'),indent=1)
