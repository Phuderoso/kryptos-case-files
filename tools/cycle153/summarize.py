"""Cycle 153: merge hillk1e C lines (direct + bank) per text and (n,k) into one table; list best S/E lines."""
import re, glob, sys, collections
W=sys.argv[1] if len(sys.argv)>1 else "/workspace/k153"
F=["tests","strict","eqdrop_cfg","eq_inv","eq_under","blockdrop_cfg","blockpairs","repair_cons","repair_cons_cfg","repair_inv","repair_inv_cfg","repair_under"]
agg=collections.defaultdict(lambda: collections.Counter()); best=collections.defaultdict(lambda:-99.0); ebest=collections.defaultdict(lambda:-99.0); bl={}; el={}
for f in sorted(glob.glob(W+"/out/*.txt")):
    m=re.match(r".*/(\w+?)_n(\d)_k(\d+)_(D|B)\.txt$",f); 
    if not m: continue
    t,n,k,src=m[1],int(m[2]),int(m[3]),m[4]; key=(t,n,k,src if n==5 else "all")
    for line in open(f):
        if line.startswith("C "):
            for x in F: agg[key][x]+=int(re.search(rf" {x}=(\d+)",line)[1])
            b=float(re.search(r" best=(-?[\d.]+)",line)[1]); e=float(re.search(r" eqbest=(-?[\d.]+)",line)[1])
            best[key]=max(best[key],b); ebest[key]=max(ebest[key],e)
        if line.startswith("B ") and float(re.search(r"meanQ=(-?[\d.]+)",line)[1])>=best[key]: bl[key]=line.strip()[2:]
        if line.startswith("E ") and len(line.split()[-1])==97 and float(re.search(r"meanQ=(-?[\d.]+)",line)[1])>=ebest[key]: el[key]=line.strip()
print("# Cycle 153 results: Hill + key (n 2-4, k 1-14/10/4) and Hill 5 (k 0) under one carving error / one wrong crib letter")
print("# rows = text n k scope; columns:",*F,"best_repair_meanQ best_eqdrop_meanQ")
for key in sorted(agg,key=lambda x:(x[1],x[2],x[3],x[0])):
    print(*key,*[agg[key][x] for x in F],f"{best[key]:.3f}",f"{ebest[key]:.3f}")
print("\n# best repaired decryption per (n,k,scope), K4 only (English ~ -4.1; shuffled ~ -7)")
for key in sorted(bl):
    if key[0]=="K4": print(bl[key][:330])
print("\n# overall best per text")
for t in ("K4","null1","null2"):
    ks=[k for k in agg if k[0]==t]
    if ks: print(t,"best repair %.3f"%max(best[k] for k in ks),"best eqdrop %.3f"%max(ebest[k] for k in ks))
