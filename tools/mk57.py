# Cycle 57 inputs: quadgram table, shuffled nulls, planted Nicodemus and Slidefair controls.
import json, random, struct
K4=open('data/k4.txt').read().strip()
Q=json.load(open('data/quadgrams.json')); fl=Q['floor']
arr=[fl]*(26**4)
for k,v in Q['q'].items(): arr[((ord(k[0])-65)*26+ord(k[1])-65)*676+(ord(k[2])-65)*26+ord(k[3])-65]=v
open('data/cycle57/qg.bin','wb').write(struct.pack(f'{len(arr)}d',*arr))
al=open('data/alpha.bin','rb').read()
A=lambda i:''.join(chr(65+b) for b in al[i*26:i*26+26])
pt=("SLOWLYTHEREMAINSOFPASSAGEDEBRISEASTNORTHEASTWEREREMOVEDWITHTREMBLINGHANDSANDIMADEATINYBERLINCLOCK"
    "BREACHINTHEUPPERLEFTHANDCORNER")
pt=list(pt[:97]); pt[21:34]="EASTNORTHEAST"; pt[63:74]="BERLINCLOCK"; PT="".join(pt)
def nico(pt,a,key,sig,h,mode):
    w=len(key); idx={c:i for i,c in enumerate(a)}; rows=-(-97//w); out=[]
    enc=[a[(idx[p]+idx[key[i%w]])%26] if mode==0 else a[(idx[key[i%w]]-idx[p])%26] for i,p in enumerate(pt)]
    for r0 in range(0,rows,h):
        for c in sig:
            for r in range(r0,min(r0+h,rows)):
                i=r*w+c
                if i<97: out.append(enc[i])
    return ''.join(out)
def order(word): return [i for _,i in sorted((ch,i) for i,ch in enumerate(word))]
texts={'K4':K4}
rnd=random.Random(57)
for s in range(5):
    l=list(K4); rnd.shuffle(l); texts[f'NULL{s}']=''.join(l)
# classic ACA Nicodemus: keyword gives both column shifts and order, blocks of 5
texts['NCTL1']=nico(PT,A(0),'CLOCK'[:0]+'SHADOW',order('SHADOW'),5,0)
texts['NCTL2']=nico(PT,A(1),'LUCIDMEMORY'[:9],[3,0,8,5,1,7,2,6,4],4,1)   # KA, Beaufort, w9 arbitrary order, h4
texts['NCTL3']=nico(PT,A(1500),'BERLINS',order('BERLINS'),3,0)          # themed alphabet #1500, w7, h3
# Slidefair controls
def slide(pt,a,key,mode,off):
    idx={c:i for i,c in enumerate(a)}; out=list(pt)
    for j,i in enumerate(range(off,96,2)):
        k=idx[key[j%len(key)]]
        bot=lambda x:a[(x+k)%26] if mode==0 else (a[(k-x)%26] if mode==1 else a[(x-k)%26])
        binv={bot(x):x for x in range(26)}
        x1=idx[pt[i]]; y2=binv[pt[i+1]]
        if x1!=y2: out[i]=bot(x1); out[i+1]=a[y2]
        else: out[i]=bot((x1+1)%26); out[i+1]=a[(x1+1)%26]
    return ''.join(out)
texts['SCTL1']=slide(PT,A(0),'PALIMPSEST',0,0)
texts['SCTL2']=slide(PT,A(1),'ABSCISSA',1,1)
texts['SCTL3']=slide(PT,A(4000),'IQLUSION',2,0)
with open('data/cycle57/texts57.txt','w') as f:
    for k,v in texts.items(): assert len(v)==97; f.write(f'{k} {v}\n')
print(A(1500),A(4000)); print(open('data/cycle57/texts57.txt').read())
