import random,subprocess
PT="WEDUGTHROUGHTHERUBBLE"+"EASTNORTHEAST"+"ANDFOUNDTHEDOORUNDERTHEOLDBRI"+"BERLINCLOCK"+"TOWERASTHESUNWENTDOWNXX"
assert len(PT)==97 and PT[21:34]=="EASTNORTHEAST" and PT[63:74]=="BERLINCLOCK"
def opL(w,i): t=w[i:]+w[:i]; x=t.pop(1); t.insert(13,x); return t
def opR(w,i): t=w[i+1:]+w[:i+1]; x=t.pop(2); t.insert(13,x); return t
def enc(pt,L,R):
    L,R=list(L),list(R); o=''
    for c in pt: i=R.index(c); o+=L[i]; L=opL(L,i); R=opR(R,i)
    return o
def dec(ct,L,R):
    L,R=list(L),list(R); o=''
    for c in ct: i=L.index(c); o+=R[i]; L=opL(L,i); R=opR(R,i)
    return o
# Rubin test vector
assert enc("WELLDONEISBETTERTHANWELLSAID","HXUCZVAMDSLKPEFJRIGTWOBNYQ","PTLNBQDEOYSFAVZKGJRIHWXUMC")=="OAHQHCNYNXTSZJRRHJBYHQKSOUJY"
al=open('words94.bin','rb').read()
def A(i): return ''.join(chr(65+b) for b in al[i*26:i*26+26])
random.seed(94); out=[]
for idx in (12345, 400000, 777777):
    Rr=list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'); random.shuffle(Rr); Rr=''.join(Rr)
    off=random.randrange(26); L=A(idx); L=L[off:]+L[:off]   # rotated input wheel: lemma says rotation is irrelevant
    out.append(('dir0',idx,enc(PT,L,Rr)))           # carved = encrypt(pt): input wheel = left = word alphabet
    # dir1: carved = decrypt(pt) with right wheel = word alphabet
    Lr=list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'); random.shuffle(Lr); out.append(('dir1',idx,dec(PT,''.join(Lr),L)))
for t,i,c in out: print(t,i,c)
