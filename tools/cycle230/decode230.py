import sys; sys.path.insert(0,'../src'); import analyze230 as a
k4=open('k4.txt').read().strip(); nulls=[l.strip() for l in open('nulls230.txt')]
def run(label, ct, fn, fam, tabs, crit_filter):
    lines,T=a.parse(fn); out=[]
    for l in lines:
        if not crit_filter(l): continue
        crit = "W" if l[5]<=9 else "D"
        if fam=="direct": ll=l
        try: bs,sc=a.decode_line(ct, fam, l, tabs, 0, crit)
        except AssertionError as e: print(label,"RECOUNT MISMATCH",l); continue
        print(label, fam, "perm",l[0],"dir",l[1],"X",l[2],"Y",l[3],"form",l[4],"w",l[5],"pop",l[6],"beam NC %.3f"%sc, bs)
filt=lambda l: l[5]<=9 or l[6]<=6
for sc,tabs in (("direct",a.ALPHA),("bank",a.THEMED),("all",a.THEMED)):
    run("K4",k4,f"R/k4_{sc}.txt",sc,tabs,filt)
for i,ct in enumerate(nulls):
    for sc,tabs in (("direct",a.ALPHA),("bank",a.THEMED),("all",a.THEMED)):
        run(f"null{i}",ct,f"R/null{i}_{sc}.txt",sc,tabs,filt)
