"""Cycle 123: column orders. All orders for w 2..WMAX_ALL; keyword orders (stable ties) for w up to 13
from the cycle-52 THEMED list + rotation/clock words + words56 vocabulary (if present)."""
import itertools,re,sys,os
WALL=int(sys.argv[1]) if len(sys.argv)>1 else 7
out=open(sys.argv[2] if len(sys.argv)>2 else 'orders.txt','w')
for w in range(2,WALL+1):
    for p in itertools.permutations(range(w)):
        out.write(f"{w} {' '.join(map(str,p))} all\n")
src=open(os.path.join(os.path.dirname(__file__) or '.','..','dcol_gen.py')).read()
T=re.search(r'THEMED="""(.*?)"""',src,re.S).group(1).split()
T+="CADENUS ROTATION ROTATE ROTATED TURNING CLOCKWISE WELTUHR ZEITUHR HOURHAND MINUTEHAND DIALPLATE TIMEZONE WORLDCLOCK".split()
W56='../../data/cycle56/words56.txt'
V=[l.strip() for l in open(os.path.join(os.path.dirname(__file__) or '.',W56))] if os.path.exists(os.path.join(os.path.dirname(__file__) or '.',W56)) else []
seen=set()
def order(word):
    idx=sorted(range(len(word)),key=lambda i:(word[i],i)); r=[0]*len(word)
    for k,i in enumerate(idx): r[i]=k
    return tuple(r)
n=0
for word in T+V:
    word=re.sub('[^A-Z]','',word.upper()); w=len(word)
    if w<=WALL or w>13: continue
    o=order(word)
    if o in seen: continue
    seen.add(o); out.write(f"{w} {' '.join(map(str,o))} {word}\n"); n+=1
print("keyword orders",n,file=sys.stderr)
