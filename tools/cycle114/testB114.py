"""Test B: K1-K3-style FIXED alphabet pairs (keyword alphabets, data/cycle114/a264.txt = the a264.bin set of cycles 59-77: 264 themed incl. A-Z, KRYPTOS),
both senses.  Pairs: F in {AZ,KA,ZA,AK} x M in 264;  F in 264 x M in {AZ,KA,ZA,AK};  F = M in 264.
 B1: Kryha V1, ANY code wheel with n sectors (n 1..48), teeth 1..9 (step 5..13, +4 rule), exact residue logic.
 B2: Kryha V2 universal disk, published 52 tooth counts, ANY set of open holes, any start hole (C, exact).
K4 + shuffled-ciphertext nulls + planted controls; survivors decrypted in full."""
import sys, random, subprocess, time
from kryha114 import *
BIN='/workspace/k4c114/v2_114'
AL=[l.strip() for l in open('/tmp/kcf/data/cycle114/a264.txt') if l.strip()]
assert AL[0]==A26 and AL[1].startswith("KRYPTOS")
S4=[A26,AL[1],A26[::-1],AL[1][::-1]]
PAIRS=[]; seen=set()
for F in S4:
    for M in AL:
        for pr in ((F,M),(M,F)):
            if pr not in seen: seen.add(pr); PAIRS.append(pr)
for X in AL:
    if (X,X) not in seen: seen.add((X,X)); PAIRS.append((X,X))
POS=[i for i,_ in CRIBS]
def rvec(ct,F,M,sg):
    fi={c:i for i,c in enumerate(F)}; mi={c:i for i,c in enumerate(M)}
    return [(sg*(mi[ct[i]]-fi[p]))%26 for i,p in CRIBS]
STEPS=range(5,14)
def b1(r,n):
    """exact: exists wheel of n sectors, steps in 5..13, with s_{i+1}-s_i = step_{i mod n}, s matching r at cribs."""
    R=dict(zip(POS,r)); need={}
    for i in list(range(21,33))+list(range(63,73)):
        d=(R[i+1]-R[i])%26
        if d not in STEPS: return False
        j=i%n
        if need.setdefault(j,d)!=d: return False
    tgt=(R[63]-R[33])%26; fixed=0; mult={}
    for k in range(33,63):
        j=k%n
        if j in need: fixed+=need[j]
        else: mult[j]=mult.get(j,0)+1
    reach={fixed%26}
    for j,c in mult.items(): reach={(x+c*d)%26 for x in reach for d in STEPS}
    return tgt in reach
def b1_all(ct):
    hits=[]
    for pi,(F,M) in enumerate(PAIRS):
        for sg in (1,-1):
            r=rvec(ct,F,M,sg)
            for n in range(1,49):
                if b1(r,n): hits.append((pi,sg,n))
    return hits
def b2_all(cts):
    """cts: dict name->ct.  Returns dict name -> list of (pair,sigma,nfeas,first)."""
    lines=[]
    for nm,ct in cts.items():
        for pi,(F,M) in enumerate(PAIRS):
            for sg in (1,-1): lines.append(f"{nm}:{pi}:{sg} "+" ".join(map(str,rvec(ct,F,M,sg))))
    J=4; ch=[lines[k::J] for k in range(J)]
    ps=[subprocess.Popen([BIN],stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True) for _ in range(J)]
    import threading
    outs=[None]*J
    def go(k): outs[k]=ps[k].communicate("\n".join(ch[k])+"\n")[0]
    th=[threading.Thread(target=go,args=(k,)) for k in range(J)]; [x.start() for x in th]; [x.join() for x in th]
    out="".join(outs).split("\n")
    res={nm:[] for nm in cts}
    for l in out:
        if not l.strip(): continue
        t=l.split(); nm,pi,sg=t[0].split(':')
        if int(t[1])>0: res[nm].append((int(pi),int(sg),int(t[1]),list(map(int,t[2:]))))
    return res
PREF=[0]
for x in V2TEETH: PREF.append(PREF[-1]+x)
def v2_shifts(H,a,s0,n=97):
    K=len(H); return [(s0+PREF[H[(a+i)%K]]+PREF[52]*((a+i)//K))%26 for i in range(n)]
if __name__=="__main__":
    NN=int(sys.argv[1]) if len(sys.argv)>1 else 20; NC=int(sys.argv[2]) if len(sys.argv)>2 else 10
    R=random.Random(1142); t=time.time()
    print(f"{len(PAIRS)} alphabet pairs x 2 senses")
    nulls={f"null{k}":"".join(R.sample(K4,97)) for k in range(NN)}
    # controls B1
    c1={}
    for k in range(NC):
        pi=R.randrange(len(PAIRS)); F,M=PAIRS[pi]; sg=R.choice((1,-1)); n=R.randrange(1,30)
        w=[R.choice(STEPS) for _ in range(n)]; sh=[0]
        for i in range(96): sh.append((sh[-1]+w[i%n])%26)
        s0=R.randrange(26); sh=[(x+s0)%26 for x in sh]; c1[f"ctl1_{k}"]=(kryha_enc(PT,F,M,sh,sg),(pi,sg,n))
    # controls B2
    c2={}
    for k in range(NC):
        pi=R.randrange(len(PAIRS)); F,M=PAIRS[pi]; sg=R.choice((1,-1)); K=R.randrange(8,53)
        H=sorted(R.sample(range(52),K)); a=R.randrange(K); s0=R.randrange(26)
        c2[f"ctl2_{k}"]=(kryha_enc(PT,F,M,v2_shifts(H,a,s0),sg),(pi,sg))
    # B1
    h=b1_all(K4); print(f"B1 K4: {len(h)} consistent (pair,sense,n) of {len(PAIRS)*2*48}",flush=True)
    for pi,sg,n in h[:20]: print("   ",pi,PAIRS[pi][0][:8],PAIRS[pi][1][:8],sg,n)
    hn=[len(b1_all(ct)) for ct in nulls.values()]; print(f"B1 nulls: {hn}",flush=True)
    okc=0; ex=[]
    for nm,(ct,tr) in c1.items():
        hh=b1_all(ct); okc+= tr in hh; ex.append(len(hh))
    print(f"B1 controls: {okc}/{NC} true setting recovered; consistent counts {ex}",flush=True)
    # B2
    allct={"K4":K4,**nulls,**{k:v[0] for k,v in c2.items()}}
    res=b2_all(allct)
    print(f"B2 K4: {len(res['K4'])} consistent (pair,sense) of {len(PAIRS)*2}; configs {sum(x[2] for x in res['K4'])}")
    for pi,sg,nf,fst in res['K4'][:30]:
        F,M=PAIRS[pi]; K,a,s0=fst[:3]; H=fst[3:]
        print("   ",pi,F[:8],M[:8],sg,nf,"K",K,"->",kryha_dec(K4,F,M,v2_shifts(H,a,s0),sg))
    print("B2 nulls (pairs consistent):",[len(res[k]) for k in nulls])
    okc=sum(any(x[0]==tr[0] and x[1]==tr[1] for x in res[k]) for k,(ct,tr) in c2.items())
    print(f"B2 controls: {okc}/{NC} true (pair,sense) found; pairs consistent {[len(res[k]) for k in c2]}")
    # verify a control decrypts to PT from the reported config
    for k,(ct,tr) in list(c2.items())[:3]:
        for pi,sg,nf,fst in res[k]:
            if (pi,sg)==tr:
                F,M=PAIRS[pi]; print("   ctl",k,"first-config decrypt:",kryha_dec(ct,F,M,v2_shifts(fst[3:],fst[1],fst[2]),sg))
    print(f"{time.time()-t:.0f}s")
