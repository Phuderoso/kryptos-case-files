import re,ast
def load(fn):
    t=open(fn).read(); h=[l for l in t.splitlines() if l.startswith("HIT")]
    tests=int(re.search(r"tests=(\d+)",t).group(1)); part=dict((int(a),int(b)) for a,b in re.findall(r" (\d+):(\d+)",t.split("PARTIAL_BY_L")[1]))
    return h,tests,part,None
sc=lambda l: float(re.search(r"score=(\S+)",l).group(1))
print("text | exact tests | L<=13 consistent, s=0 (plain periodic) | L<=13 consistent, s>0 | best quadgram (L<=13) | L14-26 consistent, s>0 (overfit, counted only)")
for name in ["k4"]+["null%d"%s for s in range(1,21)]:
    h,t,part,s0=load("r_%s.txt"%name); hs=[l for l in h if " s=0 " not in l]
    print(name,"|",t,"|",len(h)-len(hs),"|",len(hs),"|",max(map(sc,hs)) if hs else "-","|",sum(part.values()),part)
    for l in sorted(hs,key=sc,reverse=True)[:3]: print("   ",l[:200])
for s in range(51,61):
    meta=ast.literal_eval(open("meta_ctl%d.txt"%s).read()); h,t,part,s0=load("r_ctl%d.txt"%s)
    top=max(h,key=sc) if h else ""
    print("ctl",s,{k:meta[k] for k in ['perm','num','model','mode','L','s','key']},"consistent",len(h),"planted found",any(meta['pt'] in l for l in h),"top is planted",meta['pt'] in top, "top score",sc(top) if h else "-")
