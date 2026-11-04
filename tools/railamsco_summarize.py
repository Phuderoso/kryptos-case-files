import glob, re, ast
def parse(fn):
    hits=[l for l in open(fn) if l.startswith("HIT")]
    best=max([float(re.search(r"score=(-?[\d.]+)",l).group(1)) for l in hits], default=None)
    part=[l for l in open(fn) if l.startswith("PARTIAL")]
    s0=sum(int(re.search(r"consistent_s0=(\d+)",l).group(1)) for l in open(fn) if "consistent_s0" in l)
    tests=[l for l in open(fn) if l.startswith("SUMMARY")]
    byL={}
    for l in hits:
        L=int(re.search(r" L=(\d+)",l).group(1)); byL[L]=byL.get(L,0)+1
    return len(hits),best,byL,part[0].strip() if part else "",tests[0].strip() if tests else "INCOMPLETE",hits
out=[]
for fam in "AB":
    out.append(f"== family {fam} ==")
    for fn in sorted(glob.glob(f"r{fam}_*.txt")):
        n,b,byL,part,t,hits=parse(fn)
        out.append(f"{fn}: {t} | L<=13 consistent={n} byL={dict(sorted(byL.items()))} best_qg={b} | {part}")
        if "ctl" in fn:
            tag=fn[3:-4]; meta=ast.literal_eval(open(("cb/meta"+tag.replace("ctl","B")+".txt") if fam=="B" else ("meta"+tag.replace("ctl","A")+".txt")).read())
            ok=[h for h in hits if f"perm={meta['perm']} " in h and f"key={meta['key']} " in h]
            ranked=sorted(hits,key=lambda l:-float(re.search(r"score=(-?[\d.]+)",l).group(1)))
            out.append(f"   control truth L={meta['L']} s={meta['s']} perm={meta['perm']}: recovered={bool(ok)} rank1_is_truth={bool(ranked) and ranked[0] in ok}")
print("\n".join(out))
