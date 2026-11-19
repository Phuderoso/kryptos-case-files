"""Cycle 220 planted controls (seed 209242) and shuffled-K4 nulls (seeds 209243-209250) for I-312 chunk 1 (w 11, one crib error).
Independent textbook encryptor (no import of col1e4); same grid / read / direction conventions as plant219.py, plus the four
alphabet pairs: al 0 = A-Z/A-Z, 1 = KRYPTOS/KRYPTOS (Quagmire III), 2 = Quagmire I (keyed PT alphabet, straight CT alphabet),
3 = Quagmire II (straight PT alphabet, keyed CT alphabet). Vig c = CA[PA.index(p)+k], variant CA[PA.index(p)-k], Beaufort CA[k-PA.index(p)].
All plants have w = 11; odd ids have one carved crib letter replaced by a different random letter.
usage: plant220.py k123_eng.txt > plants220.tsv ; plant220.py --nulls k4.txt > nulls220.tsv"""
import random, sys
KA="KRYPTOSABCDEFGHIJLMNQUVWXZ"; AZ="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
PAIRS=[(AZ,AZ),(KA,KA),(AZ,KA),(KA,AZ)]  # (CT alphabet, PT alphabet)
CRP=list(range(21,34))+list(range(63,74)); CRS="EASTNORTHEASTBERLINCLOCK"
def reading_order(w,pi,mode):
    n=97; rows=(n+w-1)//w; col_at=sorted(range(w),key=lambda c:pi[c])
    if mode==1: return [r*w+c for c in col_at for r in range(rows) if r*w+c<n]
    return [r*w+c for r in range(rows) for c in col_at if r*w+c<n]
def transpose(text,w,pi,mode,dir_):
    order=reading_order(w,pi,mode)
    if dir_==0: return "".join(text[cell] for cell in order)
    out=[None]*97
    for m,cell in enumerate(order): out[cell]=text[m]
    return "".join(out)
def sub(text,key,al,form):
    CA,PA=PAIRS[al]; o=[]
    for i,ch in enumerate(text):
        k=key[i%len(key)]; x=PA.index(ch)
        o.append(CA[(x+k)%26] if form==0 else CA[(x-k)%26] if form==1 else CA[(k-x)%26])
    return "".join(o)
def carved_pos_of_layer(w,pi,mode,dir_):
    order=reading_order(w,pi,mode); pos=[None]*97
    if dir_==0:
        for m,cell in enumerate(order): pos[cell]=m
    else:
        for m,cell in enumerate(order): pos[m]=cell
    return pos
def make(eng,seed=209242,n=20):
    R=random.Random(seed); rows=[]
    for pid in range(n):
        w=11; pi=list(range(w)); R.shuffle(pi)
        mode=R.randrange(2); dir_=R.randrange(2); al=pid%4; form=R.randrange(3); model=R.randrange(2); p=R.randint(1,18)
        key=[R.randrange(26) for _ in range(p)]
        st=R.randrange(len(eng)-97); P=list(eng[st:st+97])
        for t,i in enumerate(CRP): P[i]=CRS[t]
        P="".join(P)
        C=transpose(sub(P,key,al,form),w,pi,mode,dir_) if model==0 else sub(transpose(P,w,pi,mode,dir_),key,al,form)
        seat=-1
        if pid%2==1:
            seat=R.randrange(24); pos=carved_pos_of_layer(w,pi,mode,dir_)[CRP[seat]]
            C=list(C); old=C[pos]; C[pos]=R.choice([x for x in AZ if x!=old]); C="".join(C)
        rows.append(dict(pid=pid,w=w,mode=mode,dir=dir_,al=al,form=form,model=model,p=p,key=key,pi=pi,seat=seat,start=st,P=P,C=C))
    return rows
if __name__=="__main__":
    if sys.argv[1]=="--nulls":
        K4=open(sys.argv[2]).read().strip(); print("seed\tct")
        for s in range(209243,209251):
            l=list(K4); random.Random(s).shuffle(l); print(f"{s}\t{''.join(l)}")
    else:
        eng=open(sys.argv[1]).read().strip()
        print("pid\tw\tmode\tdir\tal\tform\tmodel\tp\tkey\tpi\tseat\tstart\tP\tC")
        for r in make(eng):
            print("\t".join(str(r[k]) if not isinstance(r[k],list) else ",".join(map(str,r[k])) for k in
                  ["pid","w","mode","dir","al","form","model","p","key","pi","seat","start","P","C"]))
