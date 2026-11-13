#!/usr/bin/env python3
"""Cycle 211 part C (PREREG211b): 200 shuffled-K4 nulls through unchanged wrbank.c on all.bin at L 16 (counts only).
usage: null211.py WRBANK ALLBIN K4FILE OUT.json"""
import json, random, subprocess, sys, time
BIN, BANK, K4F, OUT = sys.argv[1:5]; k4 = open(K4F).read().strip(); assert len(k4) == 97
r = random.Random(209217); t0 = time.time(); res = []
for i in range(200):
    l = list(k4); r.shuffle(l); ct = "".join(l)
    out = subprocess.run([BIN, ct, BANK, "16", "16", "0"], capture_output=True, text=True, timeout=60).stdout
    tot = [x for x in out.splitlines() if x.startswith("T ")][0]; cells = int(tot.split("=")[-1])
    res.append(dict(i=i, ct=ct, cells=cells))
    if cells: print("null", i, "cells", cells, flush=True)
    if time.time() - t0 > 200: print("wall stop at", i, flush=True); break
n = len(res); k = sum(1 for x in res if x["cells"] > 0)
json.dump(dict(seed=209217, L=16, n=n, with_survivor=k, wall_s=round(time.time() - t0, 1), nulls=res), open(OUT, "w"), indent=1)
print("n", n, "with_survivor", k, "wall", round(time.time() - t0, 1))
