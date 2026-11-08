# Cycle 144 tools: Hill + additive key of an independent period

Decoder model: Hill n×n on blocks of the (possibly transposed) ciphertext, then an additive key of period k on the
Hill output stream: `out[t] = Σ_j D[r][j]·c[b·n+o+j] + e[t mod k] (mod 26)`. With k = n this is cycle 143's affine Hill.

- `hillvk.c` — `hillvk CT perms.bin|- label lo hi stride n k`; env `THR` (−4.6), `COMBOCAP` (20000).
  All n² + k unknowns are solved jointly and exactly from the 24 crib letters mod 2 and mod 13 (CRT); key residues
  never touched by a crib are dropped and their letters left undecided. Both bank directions, model Q (ix 0) and carved (ix 1),
  A–Z and KRYPTOS numbering, every alignment. Output: `S` survivors above THR, `C` counters.
- `plant.py` — 6 controls (seed 14400) on the cycle 137 English control text; nulls = K4 shuffled, seeds 14401–14402.
- `run_cycle144.sh` — controls, then K4 + 2 nulls for n = 2 (k 1–14), n = 3 (k 1–10), n = 4 (k 1–4), direct + full bank. 170 s on 8 processes.

Build: `gcc -O2 -march=native -o hillvk hillvk.c`.
