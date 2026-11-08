# Cycle 143 tools: affine Hill (Hill plus a period-n additive key)

Model: per block of n letters, `p = D·c + e (mod 26)`, i.e. a Hill cipher whose output is shifted by a period-n
Vigenère-style key on the plaintext side (equivalently `c = M·(p − e)`). Each matrix row plus its shift gives n+1
unknowns; the cribs give exact linear equations per row, solved mod 2 and mod 13 (Gaussian elimination) and CRT-combined,
exactly as in `tools/cycle141/hill5.c`.

- `hillaff.c` — `hillaff CT perms.bin|- label lo hi stride n`; env `THR` (print threshold, −4.6), `ROWCAP`, `COMBOCAP`.
  Tries both bank directions, model Q (ix 0) and carved (ix 1) index orders, A–Z and KRYPTOS numbering, every alignment.
  Output: `S` scored survivors, `C` counters (tests / inconsistent / underdetermined / scored / invertible combos / best), `H` histogram.
- `plant.py` — controls (seed 14300) on the cycle 137 English control plaintext; nulls are K4 shuffled with seeds 14301–14302.
  Imports `../cycle141/plant.py` (which imports cycle 137's).
- `run_cycle143.sh` — controls, then K4 + 2 nulls, n = 2..5, direct + full 165,065-entry bank, 8 processes. 55 s wall.

Build: `gcc -O2 -march=native -o hillaff hillaff.c`.
