"""Cycle 123: independent reference encryptor (positive controls) and shuffled baselines."""
import random,sys
KA="KRYPTOSABCDEFGHIJLMNQUVWXZ"; AZ="ABCDEFGHIJKLMNOPQRSTUVWXYZ"; N=97
def geom(w,pi,rot,mode):
    """returns place[i] for grid index i (row-wise) -> readout index"""
    L=[(N-c+w-1)//w for c in range(w)]; hs=N//w; inv=[0]*w
    for c in range(w): inv[pi[c]]=c
    cells=[]  # (slot,row') per grid index
    for i in range(N):
        c,r=i%w,i//w; cells.append((pi[c],(r-rot[c])%L[c]))
    if mode=='COL': order=sorted(range(N),key=lambda i:(cells[i][0],cells[i][1]))
    else: order=sorted(range(N),key=lambda i:(cells[i][1],cells[i][0]))
    place=[0]*N
    for k,i in enumerate(order): place[i]=k
    return place
def subst(pt,key,alpha,beau,model,sig):
    A=KA if alpha=='KA' else AZ; ct=[None]*N; p=len(key)
    for i in range(N):
        j=sig[i]; k=A.index(key[(i if model=='A' else j)%p]); x=A.index(pt[i])
        ct[j]=A[(k-x)%26] if beau else A[(x+k)%26]
    return ''.join(ct)
def encrypt(pt,w,pi,rot,mode,dirg,key,alpha,beau,model):
    place=geom(w,pi,rot,mode)
    if dirg==0: sig=place                       # pt i -> ct place[i]
    else:
        sig=[0]*N
        for j in range(N): sig[place[j]]=j        # pt place[j] -> ct j
    return subst(pt,key,alpha,beau,model,sig)
def kworder(word):
    idx=sorted(range(len(word)),key=lambda i:(word[i],i)); r=[0]*len(word)
    for k,i in enumerate(idx): r[i]=k
    return r
PT=("WEMETATTHEBRIDGEXGOTO"+"EASTNORTHEAST"+"ANDWALKTOTHEOLDTOWERXWAITFORT"+"BERLINCLOCK"+"TOSTRIKEMIDNIGHTXTHENGO")
assert len(PT)==97 and PT[21:34]=="EASTNORTHEAST" and PT[63:74]=="BERLINCLOCK"
if __name__=="__main__":
    C=[ # name, w, keyword, rot, mode, dir, key, alpha, beau, model
     ("ctl1",7,"CADENUS",[3,0,11,5,8,1,13],"ROW",0,"PALIMPS","KA",0,"A"),
     ("ctl2",6,"SHADOW",[2,15,7,0,9,4],"COL",1,"ABSCISSA","AZ",1,"B"),
     ("ctl3",10,"WELTZEITUH",[1,2,3,4,5,6,7,8,9,0],"ROW",1,"CLOCK","KA",1,"A"),
     ("ctl4",5,"BERLI",[0,7,3,19,12],"COL",0,"LAYERTWO","KA",0,"B"),
    ]
    for name,w,kw,rot,mode,d,key,al,be,mo in C:
        pi=kworder(kw); ct=encrypt(PT,w,pi,rot,mode,d,key,al,be,mo)
        print(name,ct,w,kw,rot,mode,d,key,al,"Beau" if be else "Vig",mo)
    K4="OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR"
    for s in range(1,6):
        l=list(K4); random.Random(12300+s).shuffle(l); print(f"null{s}",''.join(l))
