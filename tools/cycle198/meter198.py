"""Cycle 198 meter summary: per text file (cmp198 output), full-power cells (cell U sum <= 0.05) fits vs U; low-power cells: fits among
searched configs (U_config <= 0.05) vs their U sum (a union bound, so fits <= U on average), strict fits reported separately.
usage: meter198.py files..."""
import sys
T = {"full_fits": 0, "full_U": 0.0, "low_sfits": 0, "low_sU": 0.0, "cells_full": 0, "cells": 0}
per = []
for fn in sys.argv[1:]:
    ff = fu = 0
    for l in open(fn):
        w = l.split()
        if w[0] != "H": continue
        cfg, fit, strict, U, sea, fsea, Usea = int(w[8]), int(w[9]), int(w[10]), float(w[11]), int(w[12]), int(w[13]), float(w[14])
        T["cells"] += 1
        if U <= 0.05: T["cells_full"] += 1; T["full_fits"] += fit; T["full_U"] += U; ff += fit; fu += U
        else: T["low_sfits"] += fsea; T["low_sU"] += Usea
    per.append((fn.split("/")[-1], ff, round(fu, 3)))
print(f"texts {len(sys.argv) - 1}: full-power cells {T['cells_full']} of {T['cells']}; fits there {T['full_fits']} vs U {T['full_U']:.3f}; "
      f"low-power cells, searched configs: fits {T['low_sfits']} vs U {T['low_sU']:.1f}")
print("per text (full-power fits, U):", " ".join(f"{a}:{b}/{c}" for a, b, c in per))
