# Cycle 119 — carving-error audit of the generic stepping disk (cycle 116)
    gcc -O3 -o stepset119 stepset119.c
    python3 run119.py   # K4 + 8 nulls + 4 planted controls, full bank; ~6 min on 8 cores
Needs /workspace/k4c116/perms97.bin and pairs.txt (or the support backup).
`stepset119` reports m1 = min over dropped crib letters of the number of distinct remaining adjacent steps.
That is a lower bound on the step-set size a machine needs if exactly one of the 24 crib letters is wrong.
