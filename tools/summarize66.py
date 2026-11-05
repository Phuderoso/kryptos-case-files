import re,glob,collections
ctl={l.split()[0]:l.split()[2:] for l in open('ctl66.txt')}
print("== planted controls (must be found at their own perm/alphabet/offset) ==")
for name,meta in ctl.items():
    if not name.startswith('CTL'): continue
    m=dict(x.split('=') for x in meta); s=name.split('_')[1][1]; layer=name.split('_')[2]
    txt=open(f'out/{name}_s{s}.out').read()
    if layer=='direct': pat=f"HIT direct a={m['a']} off={m['off']} "
    else: pat=f"HIT {layer} perm={m['perm']} a={m['a']} off={m['off']} "
    found=pat in txt
    n=re.search(re.escape(pat)+r"n=(\d+)",txt)
    hist=[l for l in txt.splitlines() if l.startswith(f'HIST {layer} off={m["off"]}')]
    print(name,meta,'FOUND' if found else 'not printed', n.group(1) if n else '', hist[0][:150] if hist else '')
print("== K4 vs nulls: consistent configurations (direct; A = four-square then transposition, 11 crib pairs; B = transposition then four-square, n pairs) ==")
for s in range(4):
    for nm in ['K4']+[f'NULL{i}' for i in range(25)]:
        t=open(f'out/{nm}_s{s}.out').read()
        dA=sum(1 for l in t.splitlines() if l.startswith('HIT direct'))
        A=sum(int(x) for l in t.splitlines() if l.startswith('HIST A') for x in re.findall(r'n\d+=(\d+)',l))
        Bh=collections.Counter()
        for l in t.splitlines():
            if l.startswith('HIST B'):
                for k,v in re.findall(r'n(\d+)=(\d+)',l): Bh[int(k)]+=int(v)
        top=max(Bh) if Bh else 0
        print(f"shape{s} {nm:6} direct={dA} A(n=11)={A} B max n={top} count@max={Bh[top]} B n>=8={sum(v for k,v in Bh.items() if k>=8)}")

print("== decoded-pair English check for order-A/direct survivors: non-crib pairs whose two cipher letters are already placed decode fully; best mean bigram log10 over survivors with m>=4 decoded pairs ==")
def best(fn):
    b=(-99,None)
    for l in open(fn):
        mm=re.search(r'm=(\d+) sc=(-?[\d.]+)',l)
        if mm and int(mm.group(1))>=4 and float(mm.group(2))>b[0]: b=(float(mm.group(2)),l.strip())
    return b
for s in range(4):
    row=[]
    for nm in ['K4']+[f'NULL{i}' for i in range(25)]:
        row.append((nm,best(f'out/{nm}_s{s}.out')[0]))
    nul=sorted(v for n,v in row[1:])
    print(f"shape{s} K4 {row[0][1]:.2f}  nulls min {nul[0]:.2f} median {nul[12]:.2f} max {nul[-1]:.2f}; K4 rank {sum(v>=row[0][1] for v in nul)+1}/26")
for name in ctl:
    if name.startswith('CTL'):
        s=name.split('_')[1][1]; m=dict(x.split('=') for x in ctl[name]); layer=name.split('_')[2]
        pat=(f"HIT direct a={m['a']} off={m['off']} " if layer=='direct' else f"HIT {layer} perm={m['perm']} a={m['a']} off={m['off']} ")
        own=[l.strip() for l in open(f'out/{name}_s{s}.out') if l.startswith(pat)]
        print(name,'own config:',own[0] if own else '-','| best survivor:',best(f'out/{name}_s{s}.out')[1])
