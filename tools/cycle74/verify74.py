"""Decrypt each control from the (perm, model, offset) the SOLVER reported, using the solver's own mode-21/mode-3
convention (KA plain, KA cipher, KA key numbering, Vigenere C=P+K), and compare all 97 letters with the planted text."""
import json, re, numpy as np
from kryptos_text import KA
perms=np.fromfile("p3k.bin",dtype=np.int16).reshape(-1,97)
texts=dict(l.split() for l in open("texts_all.txt"))
meta=json.load(open("controls74.json"))
for m in meta:
    car=open(f"out/../ctl_{m['ctl']}.txt").read().strip()
    rep=[l for l in open(f"out/book_ctl{m['ctl']}.out") if l.startswith("FULL")] if m['ctl']<=4 else []
    rep+= [l for l in open(f"out/crk_ctl{m['ctl']}.out") if "matches=24" in l]
    perms_found=sorted({int(re.search(r"perm=(\d+)",l).group(1)) for l in rep})
    T=texts[m['text']]; o=m['offset']; P=perms[m['perm']]; inv=np.argsort(P)
    dec=[]
    for i in range(97):
        if m['model']=="A": c=car[P[i]]; k=T[(o+i)%len(T)]
        else: c=car[inv[i]]; k=T[(o+inv[i])%len(T)]
        dec.append(KA[(KA.index(c)-KA.index(k))%26])
    dec="".join(dec)
    print(m['ctl'],m['text'],m['model'],"planted perm",m['perm'],"reported",perms_found,"full match",dec==m['pt'],dec[:40])
