"""Cycle 79 gap-closing controls: carved texts SHORTER than 97 letters (K1 pt/ct 63, K0 Morse 81) must wrap; bookrk
(cycle 45) cannot test them (non-cyclic offsets). Planted with Sanborn's KA Vigenere behind textbook transpositions."""
import json, random, sys, io, contextlib
with contextlib.redirect_stdout(io.StringIO()): import gen79 as g
texts=dict(l.split() for l in open("carved24.txt"))
PL=[(7,"c34_K1pt","B"),(3,"c34_K0morse","A"),(0,"c34_K1ct_rev","A")]
slice_idx=json.load(open("controls79.json"))["slice"]; meta=[]
for n,(ti,tn,model) in enumerate(PL):
    rr=random.Random(7950+n); T=texts[tn]; pt=g.plain(7950+n); o=rr.randrange(len(T)); f=g.TB[ti][1]
    key=lambda i:T[(o+i)%len(T)]
    if model=="A": car=f("".join(g.E(pt[i],key(i)) for i in range(97)))
    else: t=f(pt); car="".join(g.E(t[j],key(j)) for j in range(97))
    open(f"wctl_{n}.txt","w").write(car)
    meta.append(dict(ctl=n,transposition=g.TB[ti][0],text=tn,model=model,offset=o,pt=pt,
      slice_pos=[slice_idx.index(k) for k in (g.mem[ti]["enc_index"],g.mem[ti]["dec_index"])]))
    print(meta[-1]["ctl"],meta[-1]["transposition"],tn,model,o,meta[-1]["slice_pos"])
json.dump(meta,open("wrap_controls79.json","w"),indent=1)
