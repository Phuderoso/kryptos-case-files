import glob,re,ast
def parse(fns):
    hits=[];tests=0;part={}
    for fn in fns:
        for l in open(fn):
            if l.startswith("HIT"): hits.append(l.strip())
            elif l.startswith("SUMMARY"): tests+=int(re.search(r"tests=(\d+)",l).group(1))
            elif l.startswith("PARTIAL"):
                for k,v in re.findall(r"(\d+):(\d+)",l): part[int(k)]=part.get(int(k),0)+int(v)
    return hits,tests,part
tags=open("perms_M.txt").read().split("\n")
out=[]
for t in ["k4","null1","null2","null3"]:
    fns=sorted(glob.glob(f"rM_{t}_c*.txt")); h,n,p=parse(fns)
    byL={}
    for l in h: L=int(re.search(r" L=(\d+)",l).group(1)); byL[L]=byL.get(L,0)+1
    out.append(f"{t}: chunks={len(fns)} tests={n} consistent(L<=20)={len(h)} byL={dict(sorted(byL.items()))} partial_by_L(21-26 shown)={ {k:v for k,v in sorted(p.items()) if k>=21} }")
    for l in h[:20]:
        pi=int(re.search(r"perm=(\d+)",l).group(1)); out.append("   "+l[:200]+" | "+tags[pi])
for s in [81,82,83,84]:
    h,n,p=parse([f"rM_ctl{s}.txt"]); m=ast.literal_eval(open(f"metaM{s}.txt").read())
    ok=[l for l in h if f"perm={m['perm']} " in l and f"key={m['key']} " in l]
    rk=sorted(h,key=lambda l:-float(re.search(r"score=(-?[\d.]+)",l).group(1)))
    out.append(f"control {s} truth perm={m['perm']} ({tags[m['perm']]}) L={m['L']} s={m['s']} num={m['num']} model={m['model']} mode={m['mode']}: hits={len(h)} recovered={bool(ok)} rank1_truth={bool(rk) and rk[0] in ok}")
print("\n".join(out))
