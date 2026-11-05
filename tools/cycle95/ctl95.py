# planted controls with non-Rubin rules; carved produced by encrypting with input wheel = tw alphabet, output wheel random
import random
PT="WEDUGTHROUGHTHERUBBLE"+"EASTNORTHEAST"+"ANDFOUNDTHEDOORUNDERTHEOLDBRI"+"BERLINCLOCK"+"TOWERASTHESUNWENTDOWNXX"
def mv(w,k,r):
    o,p,q=r; s=k+o; t=w[s%26:]+w[:s%26]; x=t.pop(p); t.insert(q,x); return t
def enc(pt,inw,outw,ri,ro):  # input letters looked up in 'inw' (carved side), mapped to outw: here we ENCRYPT so pt sits in outw
    I,O=list(inw),list(outw); c=''
    for ch in pt: i=O.index(ch); c+=I[i]; I=mv(I,i,ri); O=mv(O,i,ro)
    return c
tw=open('tw_alpha.bin','rb').read(); A=lambda i:''.join(chr(65+b) for b in tw[i*26:i*26+26])
# Rubin rule sanity: left=(0,1,13), right=(1,2,13): Rubin vector
assert enc("WELLDONEISBETTERTHANWELLSAID","HXUCZVAMDSLKPEFJRIGTWOBNYQ","PTLNBQDEOYSFAVZKGJRIHWXUMC",(0,1,13),(1,2,13))=="OAHQHCNYNXTSZJRRHJBYHQKSOUJY"
random.seed(95)
for idx,ri,ro in ((150,(2,4,12),(0,3,14)),(5000,(1,5,14),(2,1,12)),(20000,(0,2,13),(1,1,13))):
    O=list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'); random.shuffle(O)
    print(idx,ri,ro,enc(PT,A(idx),''.join(O),ri,ro))
