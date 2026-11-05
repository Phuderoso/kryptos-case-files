"""Cycle 61: geometric route transpositions not in the cycle-12 family (which had 8 row/column/boustrophedon
routes). New: spiral routes (4 corners x CW/CCW, inward; outward = reversed) and diagonal routes
(4 corners x 2 first-step directions, straight and zigzag diagonals) on w x h grids, w = 2..48, h = ceil(97/w),
with the empty cells either at the end or at the start of the row-major fill, plus the column-major fill.
Each route gives a reading sequence of text positions; both the permutation and its inverse are kept.
Convention (as periodic_exact59.c): perm[j] = carved position that holds plaintext letter j.
Writes route_perm.bin (int16 x 97); reports overlap with data/c12_perm.bin. Also writes nulls and planted controls."""
import struct, random, numpy as np
N=97
def spiral(w,h,corner,cw):
    # generate cell coords for inward spiral starting at given corner, CW or CCW
    top,bot,left,right=0,h-1,0,w-1; out=[]
    # start at top-left going right (CW) canonical, then transform
    while top<=bot and left<=right:
        for c in range(left,right+1): out.append((top,c))
        for r in range(top+1,bot+1): out.append((r,right))
        if top<bot:
            for c in range(right-1,left-1,-1): out.append((bot,c))
        if left<right:
            for r in range(bot-1,top,-1): out.append((r,left))
        top+=1;bot-=1;left+=1;right-=1
    if not cw: out=[(r,c) for (r,c) in out]  # CCW from top-left = transpose of CW on transposed grid
    return out
def spiral_any(w,h,corner,cw):
    if cw: base=spiral(w,h,0,True)
    else: base=[(r,c) for (c,r) in spiral(h,w,0,True)]
    fr,fc=corner&1,corner>>1
    return [((h-1-r) if fr else r,(w-1-c) if fc else c) for r,c in base]
def diag(w,h,corner,first,zig):
    out=[]
    for s in range(w+h-1):
        cells=[(r,s-r) for r in range(h) if 0<=s-r<w]
        if first: cells=cells[::-1]
        if zig and s%2: cells=cells[::-1]
        out+=cells
    fr,fc=corner&1,corner>>1
    return [((h-1-r) if fr else r,(w-1-c) if fc else c) for r,c in out]
perms=set()
for w in range(2,49):
    h=-(-N//w); E=w*h-N
    fills=[]
    for mode in range(3):
        grid={}
        if mode==0: cells=[(r,c) for r in range(h) for c in range(w)][:N]
        elif mode==1: cells=[(r,c) for r in range(h) for c in range(w)][E:]
        else: cells=[(r,c) for c in range(w) for r in range(h)][:N]
        for i,cell in enumerate(cells): grid[cell]=i
        fills.append(grid)
    routes=[]
    for corner in range(4):
        for cw in (0,1): routes.append(spiral_any(w,h,corner,cw))
        for first in (0,1):
            for zig in (0,1): routes.append(diag(w,h,corner,first,zig))
    for grid in fills:
        for rt in routes:
            for rr in (rt,rt[::-1]):
                seq=tuple(grid[c] for c in rr if c in grid)
                assert len(seq)==N and len(set(seq))==N
                inv=[0]*N
                for k,v in enumerate(seq): inv[v]=k
                perms.add(seq); perms.add(tuple(inv))
old=np.fromfile('data/c12_perm.bin',dtype=np.int16).reshape(-1,N)
oldset=set(map(tuple,old.tolist()))
new=sorted(p for p in perms if p not in oldset and p!=tuple(range(N)))
print("route perms",len(perms),"already in cycle-12 family",len(perms)-len(new)-(tuple(range(N)) in perms),"new",len(new))
with open('route_perm.bin','wb') as f:
    for p in new: f.write(struct.pack('<97h',*p))
# nulls and planted controls
k4=open('data/k4.txt').read().split()[0]
rnd=random.Random(61)
for i in range(3):
    l=list(k4); rnd.shuffle(l); open(f'data/cycle61/null{i}.txt','w').write(''.join(l)+'\n')
def ka(word):
    s=[]
    for ch in word+'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        if ch not in s: s.append(ch)
    return ''.join(s)
pt=("SLOWLYDESPARATLYSLOWEASTNORTHEASTTHEREMAINSOFPASSAGEDEBRISTHATENCUMBEREDTHELOWERPARTBERLINCLOCKOFTHEDOORWAYWASREMOVED")
pt=(pt[:21]+"EASTNORTHEAST"+pt[34:63]+"BERLINCLOCK"+pt[74:])[:N]
pt=pt[:21]+"EASTNORTHEAST"+pt[34:]; pt=pt[:63]+"BERLINCLOCK"+pt[74:]; pt=(pt+"X"*N)[:N]
assert pt[21:34]=="EASTNORTHEAST" and pt[63:74]=="BERLINCLOCK"
ctls=[(1234,'KRYPTOS','PALIMPSEST',0,0),(len(new)-7,'KRYPTOS','SHADOW',1,1),(len(new)//2,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','ABSCISSA',0,1)]
info=[]
for n,(pi,aw,key,mode,order) in enumerate(ctls):
    perm=new[pi]; al=ka(aw); idx={c:i for i,c in enumerate(al)}
    inter=[None]*N  # inter[j] = substituted letter for plaintext position j
    for j in range(N):
        kpos=j if order==0 else perm[j]
        k=idx[key[kpos%len(key)]]; p=idx[pt[j]]
        c=(p+k)%26 if mode==0 else (k-p)%26
        inter[j]=al[c]
    ct=['?']*N
    for j in range(N): ct[perm[j]]=inter[j]
    open(f'data/cycle61/ctl{n+1}.txt','w').write(''.join(ct)+'\n')
    info.append(f"ctl{n+1}: perm {pi} alphabet {aw} key {key} mode {'vig' if mode==0 else 'beau'} order {order}")
open('data/cycle61/controls.txt','w').write('\n'.join(info)+'\n'); print('\n'.join(info))
