# Cycle 131 — two keyword layers stacked

- `dbl.c` checks two stacked keyword-tableau layers (each on the A–Z or KRYPTOS tableau, Vigenère / Beaufort / variant, key = a repeated keyword) against the 24 crib letters. Direct mode: every ordered pair of words from the two lists, all 36 layer settings. Transposition mode: every ordered pair of themed words, Vigenère/Beaufort only (16 settings), all 165,065 bank transpositions in both directions, with the transposition after both layers, between them, or before both. Exact.
- `plant.py` is an independent Python encryptor for four planted controls (one per model), plus two shuffled-K4 nulls. `mklists.py` builds the word lists. `run_cycle131.sh` runs everything (~5 min on 8 cores).
