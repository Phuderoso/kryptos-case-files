import glob,re,collections
res=collections.defaultdict(lambda:{"best":0,"full":0,"hist":collections.Counter(),"cands":[]})
for f in sorted(glob.glob("out/*.out")):
    name=f.split("/")[-1].rsplit("_",1)[0]
    for l in open(f):
        if l.startswith("SUMMARY"):
            m=re.search(r"best=(\d+) full=(\d+) hist:(.*)",l); r=res[name]
            r["best"]=max(r["best"],int(m[1])); r["full"]+=int(m[2])
            for kv in m[3].split(): k,v=kv.split(":"); r["hist"][int(k)]+=int(v)
        elif l.startswith("CAND"): res[name]["cands"].append(l.strip())
for n,r in res.items():
    ge12=sum(v for k,v in r["hist"].items() if k>=12)
    print(f"{n}: best={r['best']} full24={r['full']} configs>=12:{ge12} top:", sorted(r['hist'].items())[-3:])
    for c in [c for c in r["cands"] if "matches=24" in c][:3]: print("   ",c)
