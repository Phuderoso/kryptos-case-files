"""Cycle 107 planted controls: Alberti disk turning by d at every W (model A: in the pre-transposition stream; model B: in the carved stream)."""
import numpy as np, random, subprocess
P=np.fromfile('perms97.bin',dtype=np.int16).reshape(-1,97)
PT=("WEDUGTHROUGHTHERUBBLEX"[:21]+"EASTNORTHEAST"+"ANDFOUNDTHEDOORUNDERTHEOLDBRIDGE"[:29]+"BERLINCLOCK"+"TOWERASTHESUNWENTDOWNXX")
def ka(k):
    s=[];[s.append(c) for c in k+"ABCDEFGHIJKLMNOPQRSTUVWXYZ" if c not in s];return [ord(c)-65 for c in s]
def enc(model,perm,pi,sig,d,inc):
    t=P[perm]; inv=np.argsort(t); pos={pi[k]:k for k in range(26)}; out=[None]*97; nW=0
    order = range(97)
    for n in order:
        j = n if model=='A' else int(inv[n])   # A: stream = pre-transposition; B: stream = carved order
        p=ord(PT[j])-65
        # compute letter with current setting; if inc, a W itself already counts
        c=sig[(pos[p]+nW*d)%26]
        if inc and c==22:  # W turns before itself: re-encipher with next setting is circular; keep excl semantics for W
            pass
        if model=='A': out[int(t[j])]=chr(65+c)
        else: out[n]=chr(65+c)
        if c==22: nW+=1
    return ''.join(out)
r=random.Random(107)
specs=[('A',0),('A',77777),('A',91000),('B',123456),('B',4242),('B',150000)]
for m,perm in specs:
    while True:
        pi=list(range(26)); sig=list(range(26)); r.shuffle(pi); r.shuffle(sig); d=r.randrange(1,26)
        ct=enc(m,perm,pi,sig,d,0)
        if ct.count('W')>=4: break
    P[perm].astype(np.int16).tofile('one.bin')
    one=subprocess.run(['./wturn',ct,'one.bin','1'],capture_output=True,text=True).stdout
    print(m,perm,d,ct.count('W'),'Ws |',' '.join(l for l in one.split('\n') if l.startswith(('HIST','MONO','RESULT'))))
    open(f'ctl_{m}_{perm}.txt','w').write(ct+'\n')
