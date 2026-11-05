K4="OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR"
CRIBS={21+i:c for i,c in enumerate("EASTNORTHEAST")}
CRIBS.update({63+i:c for i,c in enumerate("BERLINCLOCK")})
PER=[26,25,23,21,19,17]
from itertools import combinations
TYPES=[(w,) for w in range(6)]+list(combinations(range(6),2))  # 21 lug types
def m209_key(pins,n,i):
    act=[pins[w][i%PER[w]] for w in range(6)]
    return sum(n[t] for t,ty in enumerate(TYPES) if any(act[w] for w in ty))
def enc(pt,pins,n,mode=0,delta=0):
    out=[]
    for i,ch in enumerate(pt):
        p=ord(ch)-65;k=m209_key(pins,n,i)
        c=(25+k-p+delta)%26 if mode==0 else (p+k+delta)%26
        out.append(chr(65+c))
    return "".join(out)
