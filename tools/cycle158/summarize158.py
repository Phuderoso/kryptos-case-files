"""Cycle 158 summary: sums hillw C lines per (text, n, scope) and lists S/X lines."""
import glob, re, collections
agg=collections.defaultdict(lambda: collections.Counter()); exp=collections.defaultdict(float)
for fn in sorted(glob.glob("out/*.txt")):
    if fn.endswith("time.txt"): continue
    name=fn.split("/")[-1][:-4]; lab,n,sc,tag=name.split("_",3)
    scope={"D":"direct-strict" if tag.startswith("c") else ("direct-1err f=themed" if tag=="te" else "direct-1err e=themed"),"B":"bank-strict","E":"bank-power-sample"}[sc]
    for l in open(fn):
        if l.startswith("C "):
            kv=dict(x.split("=") for x in l.split()[2:] if "=" in x)
            k=(lab,n,scope); a=agg[k]
            for f in ("frames","fsets","etests","survivors","drop_survivors"): a[f]+=int(kv[f])
            exp[k]+=float(kv["expected_chance_strict"])
print("%-8s %-3s %-22s %14s %18s %10s %10s %12s"%("text","n","scope","frames","word-pair tests","strict","1-err","E[chance]"))
for k in sorted(agg):
    a=agg[k]; e=exp[k] if k[2]!="bank-strict" else float('nan')
    print("%-8s %-3s %-22s %14d %18d %10d %10s %12.2e"%(k[0],k[1],k[2],a["frames"],a["etests"],a["survivors"],a["drop_survivors"] if "1err" in k[2] else "-",e))
