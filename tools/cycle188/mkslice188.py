"""Cycle 188 recount slice: all.bin[::4000] + the planted perms of P10, P11 (plants.json).  usage: mkslice188.py all.bin plants.json out.bin"""
import sys, json
import numpy as np
P = np.fromfile(sys.argv[1], dtype=np.int16).reshape(-1, 97); pl = {p["name"].split("_")[0]: p for p in json.load(open(sys.argv[2]))}
rows = list(range(0, P.shape[0], 4000)); base = len(rows); K = ("P10", "P11"); extra = [pl[k]["q"] for k in K]
P[rows + extra].tofile(sys.argv[3]); print("rows", len(rows) + len(extra), "planted rows at", {k: base + i for i, k in enumerate(K)})
