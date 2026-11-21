import sys; sys.path.insert(0,'../src'); import analyze230 as a
exec(open('../src/clus230.py').read().split("for crit,fl")[0].replace("import sys; sys.path.insert(0,'../src'); import analyze230 as a",""))
D230="/workspace/k4c230/repo/data/cycle230/R"
for sc,(nf,sf,n0,s0) in {"direct":(8,5,10,20),"bank":(20,20,10,20),"all":(20,20,10,20)}.items():
  for crit,fl in (("W9",lambda l:l[5]<=9),("W10",lambda l:l[5]<=10)):
    f=[[l for l in a.parse(f"R/null{i}_{sc}.txt")[0] if fl(l)] for i in range(nf)]
    o=[[l for l in a.parse(f"{D230}/null{i}_{sc}.txt")[0] if fl(l)] for i in range(n0)]
    # pooled full-scale equivalent: mean of per-null (count*scale); fresh and c230 nulls at their own scales
    eq=[len(x)*sf for x in f]+[len(x)*s0 for x in o]; eqc=[(clusters(x) if x else 0)*sf for x in f]+[(clusters(x) if x else 0)*s0 for x in o[:0]]
    eqc+= [(clusters(x) if x else 0)*s0 for x in o]
    k4=[l for l in a.parse(f"{D230}/k4_{sc}.txt")[0] if fl(l)]
    print(sc,crit,"K4 raw",len(k4),"cl",clusters(k4),"| pooled nulls n=%d texts with>=1: %d | pooled null-equiv raw %.1f cl %.1f"%(len(eq),sum(1 for x in f+o if x),sum(eq)/len(eq),sum(eqc)/len(eqc)))
