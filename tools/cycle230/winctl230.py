"""Descriptive calibration (post hoc, not a registered decision): beam NC of each K4 W9 cluster representative versus the same (row, X, Y, form)
with 40 random width-9 windows (random offset) in place of the crib-consistent window. Seed 209587 (random.Random(209587))."""
import sys, random; sys.path.insert(0,'../src'); import analyze230 as a
from multiprocessing import Pool
ct=open('k4.txt').read().strip()
reps=[("direct",-1,0,7623,60126,2,a.ALPHA),("all",102426,0,126,44,0,a.THEMED),("all",139826,1,53,101,2,a.THEMED)]
def job(args):
    sc,q,d,xi,yi,form,off=args
    tabs=a.ALPHA if sc=="direct" else a.THEMED
    ks,S,X,Y=a.kvals(ct,sc,q,d,xi,yi,form,tabs)
    kset=[(off+t)%26 for t in range(9)]
    return a.beam(ct,S,X,Y,form,kset)[1]
if __name__=="__main__":
    r=random.Random(209587); jobs=[]
    for rep in reps:
        for _ in range(40): jobs.append(rep[:6]+(r.randrange(26),))
    with Pool(8) as p: sc=p.map(job,jobs)
    for i,rep in enumerate(reps):
        v=sorted(sc[i*40:(i+1)*40]); print(rep[:6],"random-window beam NC min %.3f median %.3f max %.3f"%(v[0],v[20],v[-1]), "n>= -3.456:",sum(1 for x in v if x>=-3.456))
