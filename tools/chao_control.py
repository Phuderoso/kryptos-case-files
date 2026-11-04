"""Cycle 14 planted controls for tools/c/chao.c (Chaocipher +/- transposition).
Writes ../analysis/chao_control_ct.txt with three planted carved texts."""
import struct
A=open('../data/tw_alpha.bin','rb').read()
alpha=lambda i:list(A[i*26:(i+1)*26])
def perm(fn,t):
    b=open(fn,'rb').read()[t*194:(t+1)*194]; return list(struct.unpack('<97h',b))
def step(L,R,x,enc):
    i=R.index(x) if enc else L.index(x); o=L[i] if enc else R[i]
    L[:]=L[i:]+L[:i]; L[:]=[L[0]]+L[2:14]+[L[1]]+L[14:]
    R[:]=R[i+1:]+R[:i+1]; R[:]=R[:2]+R[3:14]+[R[2]]+R[14:]
    return o
def chao(text,a,b,off,enc=True):
    L=[a[(k+off)%26] for k in range(26)]; R=b[:]
    return ''.join(chr(65+step(L,R,ord(c)-65,enc)) for c in text)
PT=("SLOWLYTHEDOORWAYOPENS"+"EASTNORTHEAST"+"OFTHEWALLLIESTHEOLDSTONEMAPAT"+"BERLINCLOCK"+"WHEREWEMEETATMIDNIGHTXX")
assert len(PT)==97 and PT[21:34]=="EASTNORTHEAST" and PT[63:74]=="BERLINCLOCK"
a,b,off=alpha(4),alpha(5),7       # c:KRYPTOS left, k:PALIMPSEST right, offset 7, standard encrypt (dir 0 to undo)
plain=chao(PT,a,b,off)
p=perm('../data/c12_perm.bin',5000)            # cycle-12 transposition #5000
T=[None]*97
for j in range(97): T[p[j]]=PT[j]
tb=chao(''.join(T),a,b,off)                   # transpose, then Chaocipher
q=perm('../data/c12_perm.bin',20000)           # cycle-12 transposition #20000
I=chao(PT,a,b,off); C=[None]*97
for j in range(97): C[q[j]]=I[j]
ta=''.join(C)                                  # Chaocipher, then transpose
open('../analysis/chao_control_ct.txt','w').write(f"PT {PT}\nplain {plain}\ntb(c12_perm 5000) {tb}\nta(c12_perm 20000) {ta}\nkey: a=4 (c:KRYPTOS) b=5 (k:PALIMPSEST) off=7 dir=0\n")
print(plain); print(tb); print(ta)
