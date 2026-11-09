"""Cycle 154: merge hillcs C/S/X/U lines into results.txt (per text, n, k, mode)."""
import glob, re, collections, sys, os
W=sys.argv[1] if len(sys.argv)>1 else "/workspace/k154"
agg=collections.OrderedDict(); tops=[]
for f in sorted(glob.glob(f"{W}/out/*.txt")):
    b=os.path.basename(f); m=re.match(r"(\w+?)_n(\d)_k(\d+)_(B|D)_s(\d)\.txt",b); txt,n,k,mode,sl=m.groups()
    for l in open(f):
        if l.startswith("C "):
            g=dict(x.split("=") for x in l.split()[2:])
            key=(txt,int(n),int(k),mode,g["range"].split("/")[1])
            a=agg.setdefault(key,collections.Counter()); a["slices"]+=1
            for x in ("tests","incons","survivors","underdet","scored","combos","drop_survivors"): a[x]+=int(g[x])
            a["best"]=max(a.get("best",-99),float(g["best"]))
        elif l[0] in "SXU": tops.append(l.strip())
print("text n k mode stride slices tests inconsistent strict_survivors underdetermined scored invertible_combos drop1_survivors best_meanQ")
for (t,n,k,mo,st),a in sorted(agg.items(),key=lambda z:(z[0][3],z[0][1],z[0][2],z[0][0])):
    print(t,n,k,mo,st,a["slices"],a["tests"],a["incons"],a["survivors"],a["underdet"],a["scored"],a["combos"],a["drop_survivors"] if mo=="D" else "-",f"{a['best']:.3f}" if a['best']>-90 else "-")
open(f"{W}/top_lines.txt","w").write("\n".join(tops)+"\n")
