#!/usr/bin/env python3
"""Supplement to sat206.py (disclosed in case 193): the registered 300 s cap stopped the null loop after QI-Vig, so the same five
nulls (seed 206207, identical draw) are rerun for QII and QIV, Vigenere form, one process per null. The Beaufort form is
equivalent to the Vigenere form for QI / QII / QIV with a free alphabet (reflect the free alphabet), and K4 gave identical
first-SAT L in both forms. Usage: sat206_nulls.py MODEL INDEX"""
import sys, random, time, json
from sat206 import first_sat, K4
model, idx = sys.argv[1], int(sys.argv[2])
rng = random.Random(206207)
nulls = [rng.sample(K4, 97) for _ in range(5)]
t0 = time.time()
L, log = first_sat("".join(nulls[idx]), model, "vig", 13, {}, t0 + 600)
print(json.dumps({"model": model, "null": idx, "first_SAT_L": L, "seconds": round(time.time() - t0, 1)}), flush=True)
