#!/usr/bin/env python3
"""Cycle 213 part B summary: registered labels for the L 17 chance rate per family (boundary-band rule I-281, alpha 0.05)."""
import json, math, sys
R = {}; rows = [json.loads(l) for l in open(sys.argv[1])]
for fam in ("bank", "all"):
    g0 = [d for d in rows if d["family"] == fam and d["i"] == -1][0]["cells"]
    nl = {d["i"]: d["cells"] for d in rows if d["family"] == fam and d["i"] >= 0}
    n = len(nl); k = sum(1 for v in nl.values() if v > 0); p = k / n if n else float("nan")
    se = math.sqrt(p * (1 - p) / n) if n else float("nan"); a = 0.05
    if n < 100: lab = f"INCOMPLETE ({n}/100, resumable; no label)"
    elif g0 != 0: lab = "GATE G0 FAIL"
    elif p <= a - 2 * se and k > 0: lab = "L 17 EXCLUSION DISCRIMINATING (measured rate below 5 %, boundary band clear)"
    elif k == 0: lab = "L 17 EXCLUSION DISCRIMINATING (0/100; rule-of-three upper bound 3 %)"
    elif p >= a + 2 * se: lab = "L 17 NOT DISCRIMINATING"
    else: lab = "UNRESOLVED (boundary band)"
    R[fam] = dict(K4_cells=g0, n=n, with_survivor=k, p=p, se=se, label=lab,
                  survivor_cells=sorted(v for v in nl.values() if v))
json.dump(R, open(sys.argv[2], "w"), indent=1); print(json.dumps(R, indent=1))
