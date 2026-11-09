"""Cycle 161 quick planted controls for the unchanged cycle-155 solver (model P, digit primers, L 8), reusing the
plant() generator of tools/cycle159/plant159.py, but with primers forced into the resumed range (50-100M, quarters q2/q3).
Output: name CT pa form primer note"""
import random,os
src=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','cycle159','plant159.py')).read()
src=src[:src.index('rng=random.Random(15901)')]; g={}; exec(src,g)
rng=random.Random(16101)
for name,PA,form,err,lo in (("p1",g['KA'],1,'carved',50),("p2",g['AZ'],0,'crib',75),("p3",g['KA'],0,None,75)):
    while True:
        ct,pr,note=g['plant'](rng,8,PA,form,err)
        if lo<=int(pr)//1000000<lo+25: break
    print(name,ct,'az' if PA==g['AZ'] else 'ka','vig' if form==0 else 'beau',pr,note)
