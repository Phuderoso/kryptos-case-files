# Cycle 120 — Quagmire I/II/III one-crib-error audit

Leave-one-out crib consistency for Quagmire I/II/III behind the 165,065-permutation bank
(adaptation of `tools/c/periodic_perm.c` from cycle 13).

## Build

```bash
gcc -O3 -fopenmp -o q1crib120 q1crib120.c
```

## Run

```bash
# identity, 264 themed alphabets, periods 1..16
./q1crib120 /path/to/alpha.bin ident97.bin "$K4" 264 16

# full bank, A–Z + KRYPTOS only
./q1crib120 /path/to/alpha.bin perms97.bin "$K4" 2 16

# full bank, 264 alphabets (main sweep; ~2.3 min on 8 cores)
./q1crib120 /path/to/alpha.bin perms97.bin "$K4" 264 16 [PRINT_CAP]
```

`PRINT_CAP` (optional, default 0) prints up to that many `SOFT_ONLY` hit lines.

Driver with planted controls + 5 shuffled nulls:

```bash
python3 run120.py
```

Needs `alpha.bin` and `perms97.bin` from the support backup (or `/workspace/k4c116/`).

## Output lines

- `TOTAL_STRICT` — configs where all 24 crib letters agree on the periodic key
- `TOTAL_SOFT` — configs where some leave-one-out of 23 agrees
- `TOTAL_SOFT_ONLY` — soft but not strict (would-be survivors under one wrong crib)
- `HIST_*` — counts by period

## Scope covered this cycle

1. Identity × 264 alphabets × QI/QII/QIII × Vig/Beau × both index orders × p ≤ 16
2. Full bank × M=2 (A–Z, KRYPTOS) × same
3. Full bank × M=264 × same (main)
4. Five shuffled-ciphertext nulls at each of those three scopes
5. Planted QIII (+ transposition) clean and one-crib-flip controls
