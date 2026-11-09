"""Cycle 182 recount slice: all.bin[::4000] + the planted perms of P1, P5, P7 (plants.json).  usage: mkslice182.py all.bin plants.json out.bin"""
import sys, json
import numpy as np
P = np.fromfile(sys.argv[1], dtype=np.int16).reshape(-1, 97); pl = {p["name"].split("_")[0]: p for p in json.load(open(sys.argv[2]))}
rows = list(range(0, P.shape[0], 4000)); base = len(rows); extra = [pl[k]["q"] for k in ("P1", "P5", "P7")]
P[rows + extra].tofile(sys.argv[3]); print("rows", len(rows) + len(extra), "planted rows at", {k: base + i for i, k in enumerate(("P1", "P5", "P7"))})
