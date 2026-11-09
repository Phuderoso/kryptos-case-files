"""Cycle 180 recount slice: all.bin[::4000] + the planted perms of P1, P4, P6, P7 (rows appended in that order).
usage: mkslice180.py all.bin plants.json out.bin texts_out.txt [K4 nulls180.txt (first 2 nulls)]"""
import sys, json
import numpy as np
P = np.fromfile(sys.argv[1], dtype=np.int16).reshape(-1, 97); pl = {p["name"].split("_")[0]: p for p in json.load(open(sys.argv[2]))}
ext = [pl[n]["q"] for n in ("P1", "P4", "P6", "P7")]; S = np.concatenate([P[::4000], P[ext]]); S.tofile(sys.argv[3])
base = len(P[::4000]); print("slice rows", len(S), "planted rows", {n: base + i for i, n in enumerate(("P1", "P4", "P6", "P7"))})
with open(sys.argv[4], "w") as f:
    if len(sys.argv) > 5:
        f.write("k4 " + open(sys.argv[5]).read().strip() + "\n")
        for l in open(sys.argv[6]).readlines()[:2]: f.write(l)
    for n in ("P1", "P4", "P6", "P7"): f.write(f"{n} {pl[n]['ct']}\n")
