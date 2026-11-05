# Zodiac-340-style diagonal walks: cell k -> (row k mod R, col (a*k + b*(k//R)) mod w)... simplified CRT walk:
# visit k=0..R*w-1 at (r,c)=((k+o) mod R, (a*(k+o)) mod w) with gcd(R,w)=1, gcd(a,w)=1; skip cells with r*w+c>=97.
import struct,math
seen=set(); out=open('z340.bin','wb'); meta=open('z340_meta.txt','w'); n=0
for w in range(2,49):
  R0=-(-97//w)
  for R in range(R0,R0+4):
    if math.gcd(R,w)!=1: continue
    for a in range(1,w):
      if math.gcd(a,w)!=1: continue
      for o in range(R*w):
        s=[]
        for k in range(R*w):
          kk=k+o; r=kk%R; c=(a*kk)%w; x=r*w+c
          if x<97: s.append(x)
        t=tuple(s)
        if t in seen: continue
        seen.add(t); out.write(struct.pack('<97h',*s)); meta.write(f"{n} w={w} R={R} a={a} o={o}\n"); n+=1
print(n)
