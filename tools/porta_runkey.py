# Running-key Porta on the 14 half-pass survivors: key letter L -> k=(L-'A')//2 (standard Porta pairing),
# best number of the 24 crib constraints matched by any offset of each corpus. Mode 0 key index j, mode 1 key index t[j].
import numpy as np,re,sys
P=np.fromfile('data/tw_perm.bin',dtype=np.int16).reshape(-1,97)
A=np.fromfile('data/tw_alpha.bin',dtype=np.uint8).reshape(-1,26)
K4=open(sys.argv[1]).read().strip(); half=[l.split() for l in open(sys.argv[2]) if l.startswith('HALF')]
cj=list(range(21,34))+list(range(63,74)); cp="EASTNORTHEAST"+"BERLINCLOCK"
corp={}
for f in ['g84','g98','g1342','g1661','g2701','rk_key']:
    s=re.sub('[^A-Z]','',open(f'data/{f}.txt',errors='ignore').read().upper()); corp[f]=(np.frombuffer(s.encode(),np.uint8)-65)//2
best=[]
for h in half:
    a,p=int(h[1][2:]),int(h[2][2:]); al=A[a]; pos=np.argsort(al); t=P[p]
    for var in (0,1):
        ks=[]
        for j,ch in zip(cj,cp):
            x=pos[ord(ch)-65]; y=pos[ord(K4[t[j]])-65]; lo,hi=(x,y-13) if x<13 else (y,x-13)
            ks.append((hi-lo)%13 if var==0 else (hi+lo)%13)
        ks=np.array(ks)
        for mode in (0,1):
            idx=[int(x) for x in (cj if mode==0 else [t[j] for j in cj])]
            for name,c in corp.items():
                n=len(c)-97; m=np.zeros(n,np.int16)
                for i,k in zip(idx,ks): m+= (c[i:i+n]==k)
                best.append((int(m.max()),name,a,p,var,mode,int(m.argmax())))
best.sort(reverse=True); print("top:",best[:5]); print("n_tests",len(best))
