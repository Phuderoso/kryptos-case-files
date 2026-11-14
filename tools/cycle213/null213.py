#!/usr/bin/env python3
"""Cycle 213 part B (PREREG213, IDEAS I-277): the L 17 R1 frontier with a measured chance rate.
100 fresh shuffled-K4 nulls (random.Random(209221), shuffle i = i-th shuffle of K4) through the UNCHANGED wrbank.c
(sha256 1001272d...) at L 17 only, behind BOTH families: bank.bin (165,065 rows) and all.bin (165,782 K3-law decimations/routes).
Gate G0: K4 itself gives 0 cells at L 17 in both families (reproduces cases 193/195).
Resumable: results are appended to OUT.jsonl; already-done (i, family) pairs are skipped. 6 worker processes, wall cap WALL s.
usage: null213.py WRBANK BANK ALLBIN K4FILE OUT.jsonl"""
import json, os, random, subprocess, sys, time
from concurrent.futures import ProcessPoolExecutor, as_completed
BIN, BANK, ALLB, K4F, OUT = sys.argv[1:6]; k4 = open(K4F).read().strip(); assert len(k4) == 97
WALL = float(os.environ.get("WALL", "420")); NNULL = 100; L = 17
FAM = {"bank": BANK, "all": ALLB}
def cells(ct, fam):
    out = subprocess.run([BIN, ct, FAM[fam], str(L), str(L), "20"], capture_output=True, text=True, timeout=120).stdout
    tot = [x for x in out.splitlines() if x.startswith("T ")][0]
    return int(tot.split("=")[-1]), [x for x in out.splitlines() if x.startswith("S ")]
r = random.Random(209221); cts = []
for i in range(NNULL):
    l = list(k4); r.shuffle(l); cts.append("".join(l))
done = set()
if os.path.exists(OUT):
    for ln in open(OUT): d = json.loads(ln); done.add((d["i"], d["family"]))
t0 = time.time()
if not any(d[0] == -1 for d in done):
    for fam in FAM:
        c, s = cells(k4, fam)
        with open(OUT, "a") as f: f.write(json.dumps(dict(i=-1, family=fam, ct="K4", cells=c, S=s)) + "\n")
        print("G0", fam, c, flush=True)
jobs = [(i, fam) for i in range(NNULL) for fam in FAM if (i, fam) not in done]
with ProcessPoolExecutor(6) as ex:
    futs = {}
    it = iter(jobs)
    def submit():
        try: i, fam = next(it)
        except StopIteration: return
        futs[ex.submit(cells, cts[i], fam)] = (i, fam)
    for _ in range(6): submit()
    while futs:
        for fu in as_completed(list(futs)):
            i, fam = futs.pop(fu); c, s = fu.result()
            with open(OUT, "a") as f: f.write(json.dumps(dict(i=i, family=fam, ct=cts[i], cells=c, S=s)) + "\n")
            if c: print("null", i, fam, "cells", c, flush=True)
            if time.time() - t0 < WALL: submit()
            break
print("wall", round(time.time() - t0, 1), flush=True)
