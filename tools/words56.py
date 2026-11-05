"""Cycle 56 key vocabulary: themed K1-K3/Kryptos words (cycle 52 list) + K1-K3 plaintext words + the 10,000 most
frequent English words (length 3-14) from five Gutenberg novels in data/."""
import re,collections,sys
sys.path.insert(0,'/workspace/kcl/tools')
src=open('/workspace/kcl/tools/dcol_gen.py').read()
THEMED=re.search(r'THEMED="""(.*?)"""',src,re.S).group(1).split()
from carved_texts import P1,P2f,P3
def S(x): return x if isinstance(x,str) else ''.join(chr(65+v) if isinstance(v,int) else v for v in x)
c=collections.Counter()
for g in ["g84","g1342","g1661","g2701","g98"]:
    t=open(f'/workspace/kcl/data/{g}.txt',errors='ignore').read().upper()
    c.update(w for w in re.findall(r"[A-Z]+",t) if 3<=len(w)<=14)
kw=[]
for p in (P1,P2f,P3): kw+= [w for w in re.findall(r"[A-Z]+",S(p).replace('X',' ')) if 3<=len(w)<=14]
lst=list(dict.fromkeys(THEMED+kw+[w for w,_ in c.most_common(10000)]))
lst=[w for w in lst if 3<=len(w)<=16]
open('words56.txt','w').write('\n'.join(lst)+'\n'); print(len(lst))
