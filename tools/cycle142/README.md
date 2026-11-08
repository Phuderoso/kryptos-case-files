# Cycle 142 tools — Hill 6×6, direct

`hilln.c` generalises cycle 141's row-by-row solver to n ≤ 8. For n = 6 the cribs give each row
of the decryption matrix 3–5 equations in 6 unknowns, solved exactly mod 2 and mod 13 (CRT);
a row is rejected outright when its system is inconsistent. Every row's solution set is
enumerated (26 to 17,576 rows each, about 10¹⁷ joint matrices), and the joint choice is found by
coordinate ascent on mean log10 quadgram (windows outside the cribs) from many random starts,
keeping only invertible endpoints.

`plant.py` builds 3 controls (seed 14200) and 20 shuffled-K4 nulls; `run_cycle142.sh` runs all
6 alignments × 2 numberings for K4 and the nulls at 500 restarts (161 s on 8 cores).
n = 7 is not run: three or more rows keep ≥ 4 free dimensions (≥ 456,976 options), too many to
enumerate per row.
