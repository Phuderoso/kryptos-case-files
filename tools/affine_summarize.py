import re,ast
def summ(fn):
    t=open(fn).read(); hits=[l for l in t.splitlines() if l.startswith("HIT")]
    rows={int(m[0]):(int(m[1]),int(m[2]),float(m[3])) for m in re.findall(r"L=(\d+) consistent=(\d+) determined=(\d+) best_qg=(\S+)",t)}
    return hits,rows
print("text | hits>-5.0 | consistent L1-13 | best qg L1-13 | best qg L14-26")
for name in ["k4"]+["null%d"%s for s in range(1,11)]:
    h,r=summ("r_%s.txt"%name)
    print(name,"|",len(h),"|",sum(r[L][0] for L in range(1,14)),"|",max(r[L][2] for L in range(1,14)),"|",max(r[L][2] for L in range(14,27)))
for s in range(31,40):
    meta=ast.literal_eval(open("meta_ctl%d.txt"%s).read()); h,r=summ("r_ctl%d.txt"%s)
    found=any(("perm=%d "%meta['perm'] in l and "model=%s"%meta['model'] in l and " L=%d "%meta['L'] in l and meta['pt'] in l) for l in h)
    top=max(h,key=lambda l:float(re.search(r"score=(\S+)",l).group(1))) if h else ""
    print("ctl",s,{k:meta[k] for k in ['perm','num','model','L']},"hits",len(h),"planted found",found,"top is planted",meta['pt'] in top)
