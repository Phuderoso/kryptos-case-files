# tools/cycle163 — split period-7 key under one error (IDEAS I-069, case file 151)
- `split7e.c` — drop-aware exact solver for the cycle-162 split-key model (two period-7 Quagmire III keys, free boundary b, phase
  kept, 86,731 alphabets, Vig/Beau per segment) with any ONE crib left out, in a single pass. Key fact: if the prefix scan meets its
  first conflict at crib i (against the class reference f), any single removal that repairs it removes i or f, so two rescans give
  the exact one-error bound. Outputs S (same alphabet), Z (A–Z/KRYPTOS cross), X (free alphabet per segment, count) and H lines;
  strict S and X counts are kept as a regression against cycle 162.
- `plant163.py` — planted controls with one corrupted carved letter under a crib behind bank permutations (ctl6–ctl8) and a
  two-error decoy (ctl9), built with the independent cycle-162 encryptor `../cycle162/plant162.py`.
- `run_cycle163.sh` — resumable runner (direct one-error for K4 + 8 nulls; bank for K4, null1, mnull01; `TEXTS="null2 mnull02 …"` adds nulls).
- `recount163.py` — independent numpy recount from the definition: every dropped crib (and none) × every boundary × every alphabet.
- `compare163.py` — compares recount lines with the split7e output.
- `decode163.py` — decrypts every S / Z survivor for every admissible (drop, boundary) and scores quadgrams.
Inputs not in this folder: `alpha.bin` (86,731 alphabets of cycles 54–56, not committed for size), the bank `perms97.bin`,
`quad.bin`, `../cycle162/plant162.py`, `tools/cycle127/plant.py`, nulls from `../cycle162` (`null1`) and `data/cycle163/mnulls.txt`.
