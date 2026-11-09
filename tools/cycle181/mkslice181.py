"""Cycle 181 recount slice: all.bin[::4000] + the planted perms of P4, P7, P8, P11 (appended in that order).
usage: mkslice181.py all.bin plants.json out.bin texts_out.txt K4file nulls181.txt"""
import sys, json
import numpy as np
P = np.fromfile(sys.argv[1], dtype=np.int16).reshape(-1, 97); pl = {p["name"].split("_")[0]: p for p in json.load(open(sys.argv[2]))}
names = ("P4", "P7", "P8", "P11"); S = np.concatenate([P[::4000], P[[pl[n]["q"] for n in names]]]); S.tofile(sys.argv[3])
base = len(P[::4000]); print("slice rows", len(S), "planted rows", {n: base + i for i, n in enumerate(names)})
with open(sys.argv[4], "w") as f:
    f.write("k4 " + open(sys.argv[5]).read().strip() + "\n")
    for l in open(sys.argv[6]).readlines()[:2]: f.write(l)
    for n in names: f.write(f"{n} {pl[n]['ct']}\n")
