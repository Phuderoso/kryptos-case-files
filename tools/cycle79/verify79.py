"""Re-decipher each control from the configuration bookrk reported (perm index into slice.bin, model, offset),
with bookrk's mode-21 convention (KA Vigenere), and compare all 97 letters with the planted plaintext."""
import json, re, numpy as np
from kryptos_text import KA
S=np.fromfile("slice.bin",dtype=np.int16).reshape(-1,97)
texts=dict(l.split() for l in open("texts79.txt")); meta=json.load(open("controls79.json"))["controls"]
for m in meta:
    car=open(f"ctl_{m['ctl']}.txt").read().strip(); res=[]
    for l in sorted(set(x for x in open(f"out/ctl{m['ctl']}.out") if x.startswith("FULL"))):
        p,mod,t,o=int(re.search(r"perm=(\d+)",l)[1]),re.search(r"model=(\w)",l)[1],re.search(r"text=(\S+)",l)[1],int(re.search(r"offset=(\d+)",l)[1])
        P=S[p]; inv=np.argsort(P); T=texts[t]; d=[]
        for i in range(97):
            if mod=="A": c=car[P[i]]; k=T[o+i]
            else: c=car[inv[i]]; k=T[o+inv[i]]
            d.append(KA[(KA.index(c)-KA.index(k))%26])
        res.append((p,mod,t,o,"".join(d)==m["pt"]))
    print(m["ctl"],m["transposition"],m["model"],m["text"],"planted offset",m["offset"],"->",res)
