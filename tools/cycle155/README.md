# Cycle 155 — Gromark / Periodic Gromark under one error (IDEAS I-008)

- `gromark1e.c` — exact one-error feasibility for the cycle-130 model (arbitrary cipher alphabet, plain A–Z/KRYPTOS, chain-addition digits)
  in two forms: **P** = periodic Gromark with L free group offsets (relaxed ACA Periodic Gromark, as cycle 130) and **G** = ordinary
  Gromark (one offset, absorbed in the alphabet). The digit stream does not depend on the ciphertext, so one wrong carved letter under a
  crib or one wrong crib letter breaks exactly one equation (a wrong carved letter elsewhere breaks none). If all 24 equations are
  infeasible, the dropped one must lie in every infeasibility certificate; the program takes one certificate (the cycle closing the first
  weighted union-find contradiction, or the tree path joining two letters forced to the same value) and re-tests without each of its edges.
  Optional base argument (digits mod b) for the cycle-10 bases 5–9. Prints `C` count lines and, with `SHOW=1`, every survivor (`S`).
- `acakw1e.c` — stage 2: for a stage-1 rank primer (L 8–12), enumerates every keyword with that primer (each set of L distinct letters gives
  exactly one), builds the ACA keyword-columnar / keyword-mixed / KRYPTOS cipher alphabet and keyword offsets (cycle 129 generator rules),
  and counts crib mismatches (≤ 1 reported). Stage 1 is an exact superset, so stage 1 + stage 2 test the ACA rule with **any** keyword.
- `plant155.py` — controls: cycle-130 ACA plants with one corrupted carved letter under a crib, two uncorrupted, one wrong crib letter,
  three ordinary-Gromark plants (random cipher alphabet); the six cycle-130 shuffled-K4 nulls (seeds 13001–13006).
- `indep_check.py` — independent recount (no shared code): all 24 single drops, BFS propagation, injectivity per component.
- `summarize155.py` — aggregates the `C` lines. `run_cycle155.sh` — resumable stage-1 runner (finished chunks are skipped).

## Reproduce (W = scratch dir, REPO = repo root)
```
python3 tools/cycle155/plant155.py > $W/controls.txt                      # controls + nulls
bash tools/cycle155/run_cycle155.sh                                         # stage 1, model P (resumable)
# model G: for T in K4 null1..null6: L 2-8 base 10, and L 2-7 for bases 5..9
SHOW=1 ./gromark1e $(cat ct_K4.txt) 8 all 0 100000000 K4 G 10
./acakw1e $(cat ct_K4.txt) 12 908632145217 K4                              # stage 2 for each perm survivor
python3 tools/cycle155/indep_check.py $(cat ct_K4.txt) 5 K4 P              # independent recount
```
