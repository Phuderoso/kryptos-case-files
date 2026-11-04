import re,ast,glob
def hits(fns):
    h=[];tests=0
    for fn in fns:
        t=open(fn).read(); h+=[l for l in t.splitlines() if l.startswith("HIT")]; tests+=sum(int(x) for x in re.findall(r"tests=(\d+)",t))
    return h,tests
sc=lambda l: float(re.search(r"score=(\S+)",l).group(1))
print("text | mode | exact tests | consistent configs | best quadgram")
for name,fns,mode in [("k4",["r_k4.txt"],"linear")]+[("null%d"%s,["r_null%d.txt"%s],"linear") for s in range(1,11)]+[("k4",sorted(glob.glob("rq_k4_*.txt")),"second-order"),("null101",sorted(glob.glob("rq_qnull1_*.txt")),"second-order")]:
    h,t=hits(fns); print(name,"|",mode,"|",t,"|",len(h),"|",max(map(sc,h)) if h else "-")
    for l in sorted(h,key=sc,reverse=True)[:5]: print("   ",l)
for s in range(41,49):
    meta=ast.literal_eval(open("meta_ctl%d.txt"%s).read()); h,t=hits(["r_ctl%d.txt"%s])
    top=max(h,key=sc) if h else ""
    print("ctl",s,{k:meta[k] for k in ['perm','num','model','form','a0','r','d','q']},"consistent",len(h),"planted found",any(meta['pt'] in l for l in h),"top is planted",meta['pt'] in top)
