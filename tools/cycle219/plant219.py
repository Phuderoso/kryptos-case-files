"""Cycle 219 planted controls (seed 209233) and shuffled-K4 nulls (seeds 209234-209241) for the I-007 one-error audit.
Independent textbook encryptor (does not import col1e or cycle 124 code):
  grid = 97 letters written row-wise at width w (short last row holds columns 0..97%w-1); pi[c] = read rank of column c.
  COL read: columns in rank order, top to bottom.  ROW read: each row, its cells in column-rank order.
  dir 0: carved = read(layer).  dir 1: carved = read^-1(layer) (read(carved) == layer).
  model A: key on plaintext index, then transposition.  model B: transposition, then key on carved index.
  forms: Vig c=A[p+k], variant c=A[p-k], Beaufort c=A[k-p]; A = A-Z or KRYPTOS-keyed alphabet.
  Odd plant ids: one carved crib letter replaced by a different random letter (one-error control).
usage: plant219.py k123_eng.txt k4.txt > plants219.tsv ; plant219.py --nulls k4.txt > nulls219.tsv"""
import random, sys
KA="KRYPTOSABCDEFGHIJLMNQUVWXZ"; AZ="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
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
def sub(text,key,A,form):
    o=[]
    for i,ch in enumerate(text):
        k=key[i%len(key)]; x=A.index(ch)
        o.append(A[(x+k)%26] if form==0 else A[(x-k)%26] if form==1 else A[(k-x)%26])
    return "".join(o)
def carved_pos_of_layer(w,pi,mode,dir_):
    # position in carved text of layer index i
    order=reading_order(w,pi,mode); pos=[None]*97
    if dir_==0:
        for m,cell in enumerate(order): pos[cell]=m
    else:
        for m,cell in enumerate(order): pos[m]=cell
    return pos
def make(eng,seed=209233,n=20):
    R=random.Random(seed); rows=[]
    for pid in range(n):
        w=9 if pid%4<2 else 10
        pi=list(range(w)); R.shuffle(pi)
        mode=R.randrange(2); dir_=R.randrange(2); al=R.randrange(2); form=R.randrange(3); model=R.randrange(2); p=R.randint(1,18)
        A=AZ if al==0 else KA; key=[R.randrange(26) for _ in range(p)]
        st=R.randrange(len(eng)-97); P=list(eng[st:st+97])
        for t,i in enumerate(CRP): P[i]=CRS[t]
        P="".join(P)
        if model==0: C=transpose(sub(P,key,A,form),w,pi,mode,dir_)
        else: C=sub(transpose(P,w,pi,mode,dir_),key,A,form)
        seat=-1
        if pid%2==1:
            seat=R.randrange(24); pos=carved_pos_of_layer(w,pi,mode,dir_)[CRP[seat]]
            C=list(C); old=C[pos]; C[pos]=R.choice([x for x in AZ if x!=old]); C="".join(C)
        rows.append(dict(pid=pid,w=w,mode=mode,dir=dir_,al=al,form=form,model=model,p=p,key=key,pi=pi,seat=seat,start=st,P=P,C=C))
    return rows
if __name__=="__main__":
    if sys.argv[1]=="--nulls":
        K4=open(sys.argv[2]).read().strip()
        print("seed\tct")
        for s in range(209234,209242):
            l=list(K4); random.Random(s).shuffle(l); print(f"{s}\t{''.join(l)}")
    else:
        eng=open(sys.argv[1]).read().strip()
        print("pid\tw\tmode\tdir\tal\tform\tmodel\tp\tkey\tpi\tseat\tstart\tP\tC")
        for r in make(eng):
            print("\t".join(str(r[k]) if not isinstance(r[k],list) else ",".join(map(str,r[k])) for k in
                  ["pid","w","mode","dir","al","form","model","p","key","pi","seat","start","P","C"]))
