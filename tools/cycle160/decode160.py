"""Cycle 160: decrypt every bank / direct QIV match (M lines) with the key letters fixed by the cribs and score
English: mean log10 quadgram over quadgrams whose four letters are all determined (plaintext order, cribs included),
and the same with crib positions excluded ('off-crib').  usage: [DROP=crib_index] decode160.py CT M-lines-file [label]"""
import sys, numpy as np
AZ="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
Q=np.fromfile("/home/box/kryptos_support_backup/quad.bin",dtype=np.float32)
CR={**{21+i:c for i,c in enumerate("EASTNORTHEAST")},**{63+i:c for i,c in enumerate("BERLINCLOCK")}}
B=np.memmap("/home/box/kryptos_support_backup/perms97.bin",dtype=np.int16,mode='r').reshape(-1,97)
def keyed(w):
    s=""
    for c in w+AZ:
        if c not in s: s+=c
    return s
def decode(ct,q,d,ix,p,mode,w1,w2,drop=()):
    S=np.arange(97) if q<0 else (np.argsort(B[q]) if d else np.array(B[q]))
    PA,CA=keyed(w1),keyed(w2); k={}
    for t,(i,pc) in enumerate(sorted(CR.items())):
        if t in drop: continue
        r=(S[i] if ix else i)%p; c=ct[S[i]]
        v=(CA.index(c)-PA.index(pc))%26 if mode=='vig' else (CA.index(c)+PA.index(pc))%26
        assert k.setdefault(r,v)==v, "inconsistent"
    out=[]
    for i in range(97):
        r=(S[i] if ix else i)%p
        if r not in k: out.append('?'); continue
        x=CA.index(ct[S[i]]); y=(x-k[r])%26 if mode=='vig' else (k[r]-x)%26
        out.append(PA[y])
    return "".join(out)
def score(t,skip=()):
    s=[Q[sum((ord(c)-65)*26**(3-z) for z,c in enumerate(t[i:i+4]))] for i in range(94)
       if '?' not in t[i:i+4] and not any(j in skip for j in range(i,i+4))]
    return (float(np.mean(s)) if s else float('nan')),len(s)
if __name__=="__main__":
    ct=sys.argv[1]; rows=[]
    for l in open(sys.argv[2]):
        x=l.split()
        if x[0]!='M': continue
        q,d,ix,p=map(int,x[2:6]); t=decode(ct,q,d,ix,p,x[6],x[7],x[8],tuple(int(v) for v in __import__('os').environ.get('DROP','').split(',') if v))
        a,n=score(t); b,nb=score(t,set(CR))
        rows.append((a,b,nb,t,l.strip()))
    rows.sort(key=lambda r:-r[0] if r[0]==r[0] else 99)
    lab=sys.argv[3] if len(sys.argv)>3 else ''
    print(f"{lab} decoded {len(rows)}; best all-quadgram {rows[0][0]:.3f}; best off-crib "
          f"{max((r[1] for r in rows if r[2]>=5),default=float('nan')):.3f}" if rows else f"{lab} none")
    for r in rows[:5]: print(f"  {r[0]:.3f} offcrib {r[1]:.3f} (n {r[2]}) {r[3]} | {r[4]}")
