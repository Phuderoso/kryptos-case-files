"""Cycle 117: CM-Bifid (conjugated-matrix Bifid: plaintext square S1, ciphertext square S2) on the W-free 92-letter text,
with the OUTPUT square S2 a K1-K3-style keyword square (264 themed keyword alphabets minus W, row- or column-filled = 528),
S1 completely free.  Orientation 0 (cycle 93's notation: ciphertext = Bifid-encrypt(plaintext)).
Key fact: once S2 is known, decryption gives every plaintext position a CELL of S1 (rows = first half of the block's
coordinate stream, columns = second half), so the plaintext is a simple substitution of a known cell sequence.
Cribs (EASTNORTHEAST at 20, BERLINCLOCK at 60 of the W-free text) must map letter->cell consistently and one-to-one;
survivors are completed by quadgram hill-climbing of the 12 unfixed cells.  Periods 1-92 (cycle 93's any-square SAT left
only p 28 and 30 open; the other periods here double as an audit).  Controls: planted CM-Bifid with keyword S2 and random S1.
usage: python3 cmbifid117.py"""
import json, random, sys, numpy as np
A25="ABCDEFGHIJKLMNOPQRSTUVXYZ"
K4=open('/tmp/kcf/data/k4.txt').read().strip(); KW=K4.replace('W','')
assert len(KW)==92
CR=[(20+i,c) for i,c in enumerate("EASTNORTHEAST")]+[(60+i,c) for i,c in enumerate("BERLINCLOCK")]
AL=[l.strip() for l in open('/tmp/kcf/data/cycle114/a264.txt') if l.strip()]
SQ=[];seen=set()
for a in AL:
    s=a.replace('W','')
    for sq in (s, "".join(s[r*5+c] for c in range(5) for r in range(5))):   # row-filled, column-filled
        if sq not in seen: seen.add(sq); SQ.append(sq)
Q=json.load(open('/home/box/kryptos_support_backup/quadgrams.json')); FL=float(Q['floor'])
QA=np.full(26**4,FL,dtype=np.float32)
for k,v in Q['q'].items():
    QA[((ord(k[0])-65)*26+ord(k[1])-65)*26*26+(ord(k[2])-65)*26+ord(k[3])-65]=v
def qscore(t):
    a=np.frombuffer(t.encode(),dtype=np.uint8).astype(np.int64)-65
    return float(QA[((a[:-3]*26+a[1:-2])*26+a[2:-1])*26+a[3:]].mean())
def cells(ct,S2,p):
    pos={c:(i//5,i%5) for i,c in enumerate(S2)}; out=[]
    for b in range(0,len(ct),p):
        blk=ct[b:b+p]; L=len(blk); d=[]
        for c in blk: d+=pos[c]
        out+=[d[i]*5+d[L+i] for i in range(L)]
    return out
def enc(pt,S1,S2,p):
    pos={c:(i//5,i%5) for i,c in enumerate(S1)}; out=""
    for b in range(0,len(pt),p):
        blk=pt[b:b+p]; L=len(blk); d=[pos[c][0] for c in blk]+[pos[c][1] for c in blk]
        out+="".join(S2[d[2*j]*5+d[2*j+1]] for j in range(L))
    return out
def consistent(cl):
    m={}; inv={}
    for i,c in CR:
        x=cl[i]
        if m.setdefault(c,x)!=x or inv.setdefault(x,c)!=c: return None
    return m
def climb(cl,m,R,iters=3000,restarts=6):
    fixedc=set(m.values()); freec=[x for x in range(25) if x not in fixedc]; freel=[c for c in A25 if c not in m]
    best=(-99,None)
    for _ in range(restarts):
        L=freel[:]; R.shuffle(L); key=dict(m); key2={x:L[k] for k,x in enumerate(freec)}
        def txt(): return "".join(key[ {v:k for k,v in key.items()}.get(x,None) ] if False else (inv[x] if x in inv else key2[x]) for x in cl)
        inv={v:k for k,v in m.items()}
        cur=qscore(txt())
        for it in range(iters):
            a,b=R.sample(freec,2); key2[a],key2[b]=key2[b],key2[a]; s=qscore(txt())
            if s>=cur: cur=s
            else: key2[a],key2[b]=key2[b],key2[a]
        if cur>best[0]: best=(cur,txt())
    return best
def scan(ct,R,periods=range(1,93),climb_max=40):
    hits=[]
    for p in periods:
        for si,S2 in enumerate(SQ):
            cl=cells(ct,S2,p); m=consistent(cl)
            if m is not None: hits.append((p,si,cl,m))
    res=[(p,si)+climb(cl,m,R) for p,si,cl,m in hits[:climb_max]]
    return hits,sorted(res,key=lambda x:-x[2])
if __name__=="__main__":
    R=random.Random(1171)
    print(f"{len(SQ)} keyword squares (W-less, row/column fill); W-free K4 = {KW}")
    hits,res=scan(KW,R); print(f"K4: {len(hits)} consistent (p, S2) of {92*len(SQ)}; periods {sorted(set(h[0] for h in hits))}")
    for r in res[:10]: print(f"   p={r[0]} S2={SQ[r[1]]} q={r[2]:.3f} {r[3]}")
    for k in range(6):
        ct="".join(R.sample(KW,92)); h,rs=scan(ct,R,climb_max=10)
        print(f"null{k}: {len(h)} consistent; periods {sorted(set(x[0] for x in h))[:12]}; best q {rs[0][2]:.3f}" if rs else f"null{k}: 0 consistent")
    PT0="WEDUGTHROUGHTHERUBBLEEASTNORTHEASTANDFOUNDTHEDOORUNDERTHEOLDBRIBERLINCLOCKTOWERASTHESUNWENTDOWNXX".replace('W','')
    pt=PT0[:20]+"EASTNORTHEAST"+"ANDFOUNDTHEDOORUNDERTHEOLDBRI"[:27]+"BERLINCLOCK"+"TOERASTHESUNENTDONXXX"; assert len(pt)==92 and pt[20:33]=="EASTNORTHEAST" and pt[60:71]=="BERLINCLOCK"
    for k,p in enumerate((28,30,7)):
        S1="".join(R.sample(A25,25)); si=R.randrange(len(SQ)); ct=enc(pt,S1,SQ[si],p)
        h,rs=scan(ct,R,climb_max=10)
        tr=[x for x in rs if x[0]==p and x[1]==si]
        print(f"ctl{k} p={p} S2#{si}: {len(h)} consistent; true found {any(x[0]==p and x[1]==si for x in h)}; true climbed q={tr[0][2]:.3f} {tr[0][3]}" if tr else f"ctl{k}: true NOT in climbed list ({len(h)} consistent)")
