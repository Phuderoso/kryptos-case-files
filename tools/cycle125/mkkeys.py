"""Cycle 125 key alphabets for Digrafid: keyword (dedup letters) + rest of A-Z + '#' at the end.
Sources: cycle-52 THEMED list (tools/dcol_gen.py), digrafid/fractionation words, cycle-56 vocabulary.
Writes keys.txt (name alphabet) and pair lists: pairs_same.txt, pairs_themed.txt, pairs_cross.txt."""
import re,os,sys
D=os.path.dirname(os.path.abspath(__file__)); out=sys.argv[1]
src=open(os.path.join(D,'..','dcol_gen.py')).read()
T=re.search(r'THEMED="""(.*?)"""',src,re.S).group(1).split()+"DIGRAFID DELASTELLE FRACTION FRACTIONATE TRIPLE TRIGRAPH GRID MATRIX HASH POUND NULL".split()
V=[l.strip().upper() for l in open(os.path.join(D,'..','..','data','cycle56','words56.txt'))]
def alpha(w):
    s=[]
    for c in re.sub('[^A-Z]','',w)+"ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        if c not in s: s.append(c)
    return "".join(s)+"#"
keys=[];seen={}
for w in T+V:
    w=re.sub('[^A-Z]','',w.upper())
    if not w: continue
    a=alpha(w)
    if a in seen: continue
    seen[a]=len(keys); keys.append((w,a))
nt=len({alpha(re.sub('[^A-Z]','',w.upper())) for w in T})
with open(f'{out}/keys.txt','w') as f:
    for w,a in keys: f.write(f"{w} {a}\n")
themed=sorted({seen[alpha(re.sub('[^A-Z]','',w.upper()))] for w in T})
with open(f'{out}/pairs_same.txt','w') as f:
    for i in range(len(keys)): f.write(f"{i} {i}\n")
with open(f'{out}/pairs_themed.txt','w') as f:
    for i in themed:
        for j in themed:
            if i!=j: f.write(f"{i} {j}\n")
with open(f'{out}/pairs_cross.txt','w') as f:
    ts=set(themed)
    for i in themed:
        for j in range(len(keys)):
            if j not in ts: f.write(f"{i} {j}\n{j} {i}\n")
print(len(keys),"alphabets;",len(themed),"themed",file=sys.stderr)
