"""Cycle 69: 'tableau walk' running keys read off the CARVED tableau (data/elonka_panel_rows.txt, text source),
as laid out on the copper: header row, 26 labelled rows (row N carries the extra L, 32 chars), footer row.
Routes: rows (L>R, R>L, boustrophedon), columns (T>B, B>T, boustrophedon), both diagonal families (each direction,
each zigzag), clockwise/counter-clockwise spirals from each corner; each on 4 versions of the grid
(full; without header/footer; without row labels; body only). Ragged rows: cells beyond a row's length are skipped.
Output: texts69.txt in carved_rk format (name text), every text also reversed by the C tool's convention (we write both)."""
import sys
rows=[r.rstrip("\n") for r in open(sys.argv[1])]
tab=rows[14:28]+rows[42:56]
assert len(tab)==28 and tab[0].strip().startswith("ABCD") and tab[14].startswith("NGHIJ") and len(tab[14])==32
def grids():
    full=[list(r) for r in tab]
    yield "full",full
    yield "nohf",full[1:-1]
    yield "nolab",[r[1:] for r in full]
    yield "body",[r[1:] for r in full[1:-1]]
def read(g,cells):
    return "".join(g[r][c] for r,c in cells if r<len(g) and c<len(g[r]) and g[r][c].isalpha())
def routes(g):
    H=len(g);W=max(len(r) for r in g)
    R=lambda:[(r,c) for r in range(H) for c in range(W)]
    out={}
    out["rows"]=R()
    out["rowsRL"]=[(r,c) for r in range(H) for c in range(W-1,-1,-1)]
    out["rowsBou"]=[(r,c if r%2==0 else W-1-c) for r in range(H) for c in range(W)]
    out["cols"]=[(r,c) for c in range(W) for r in range(H)]
    out["colsBT"]=[(r,c) for c in range(W) for r in range(H-1,-1,-1)]
    out["colsBou"]=[(r if c%2==0 else H-1-r,c) for c in range(W) for r in range(H)]
    for name,f in (("diag",lambda d:[(r,d-r) for r in range(H) if 0<=d-r<W]),
                   ("adiag",lambda d:[(r,r-(d-(H-1))) for r in range(H) if 0<=r-(d-(H-1))<W])):
        ds=[f(d) for d in range(H+W-1)]
        out[name]=[x for s in ds for x in s]
        out[name+"Rev"]=[x for s in ds for x in s[::-1]]
        out[name+"Zig"]=[x for i,s in enumerate(ds) for x in (s if i%2==0 else s[::-1])]
    def spiral(cw):
        t,b,l,r=0,H-1,0,W-1;cells=[]
        while t<=b and l<=r:
            if cw:
                cells+=[(t,c) for c in range(l,r+1)];cells+=[(rr,r) for rr in range(t+1,b+1)]
                if t<b:cells+=[(b,c) for c in range(r-1,l-1,-1)]
                if l<r:cells+=[(rr,l) for rr in range(b-1,t,-1)]
            else:
                cells+=[(rr,l) for rr in range(t,b+1)];cells+=[(b,c) for c in range(l+1,r+1)]
                if l<r:cells+=[(rr,r) for rr in range(b-1,t-1,-1)]
                if t<b:cells+=[(t,c) for c in range(r-1,l,-1)]
            t+=1;b-=1;l+=1;r-=1
        return cells
    out["spiralCW"]=spiral(True);out["spiralCCW"]=spiral(False)
    return out
seen=set();n=0
with open("texts69.txt","w") as f:
    for gn,g in grids():
        for rn,cells in routes(g).items():
            s=read(g,cells)
            for nm,t in ((f"{gn}_{rn}",s),(f"{gn}_{rn}_rev",s[::-1])):
                if t in seen: continue
                seen.add(t); f.write(f"{nm} {t}\n"); n+=1
print("texts",n)
