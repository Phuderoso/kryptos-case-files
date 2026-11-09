"""Cycle 168 key texts for running keys behind K3-law decimations and spiral/diagonal routes.
Sources (prepared in earlier cycles, re-used unchanged): cycle 34 carved texts (K1-K3 pt/ct, K0 Morse, KA tableau rows,
combinations, forward/reversed) made CYCLIC (text + its own wrap so every start 0..T-1 is an offset, as in cycle 79);
Carter & Mace vol. I (K3's source, cycle 35 OCR), G. Elliot Smith 1923 (cycle 35), KJV Gospel of John, KJV New Testament, National Security Act 1947 (as amended) and Reagan's
Berlin speech (cycle 36), forward and reversed. usage: texts168.py c34.txt c35.txt c36.txt out.txt"""
import sys
c34,c35,c36,out=sys.argv[1:5]
T={}
for l in open(c34):
    n,t=l.split(); w=t
    while len(w)<len(t)+96: w+=t
    T["cyc_"+n]=w[:len(t)+96]
for l in open(c35):
    n,t=l.split(); T[n]=t
for l in open(c36):
    n,t=l.split()
    if not n.startswith("c34_"): T[n]=t   # John, NT, Reagan, NSA 1947 (fwd+rev)
with open(out,"w") as f:
    for n,t in T.items(): f.write(f"{n} {t}\n")
for n,t in T.items(): print(n,len(t))
print("total",sum(len(t) for t in T.values()))
