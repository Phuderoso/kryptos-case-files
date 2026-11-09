# tools/cycle167 — segment-shifted period-7 key (IDEAS I-082, case file 155)
- `shift3.c` — exact solver. One period-7 Quagmire III key k, three segments with free boundaries (also inside a crib), segment j
  uses k + d_j (d_1 = 0, shifts d_2, d_3 free, in keyed-alphabet index space = another row of the keyed tableau), Vig/Beau per
  segment (8 form triples; same-form triples are the primary model). Union-find with offsets mod 26 over 7 key nodes + 3 shift
  nodes, exhaustive over every boundary pair. Direct or behind the 165k bank (both directions, plaintext/carved index), optional
  leave-one-crib-out (`drop`) and bank stride. Build: `gcc -O3 -march=native -o shift3 shift3.c`.
- `djob.sh` — direct strict + 24 drops for one text. `run_cycle167.sh` — resumable runner (tmp → rename, done marker).
- `plant167.py` — independent textbook encryptor: 18 shifted-key plants (direct / model Q / carved; A–Z, KRYPTOS, random
  dictionary alphabets; same and mixed forms), 4 one-error plants, 4 decoys with three independent keys (must be rejected).
  `controls167.sh` runs them, `checkctl167.py` makes `controls167.txt` (26/26).
- `recount167.py` — independent numpy recount (all 26 × 26 shift pairs × every boundary pair, no union-find, no early exit);
  `compare167.py` checks it against shift3 on 560 cells (plants, K4 + 2 nulls on 12 alphabets, 4 K4 bank configurations).
- `power167.py` — fewest-check / union bound. `summarize167.py` — counts per cell.
- `texts167.txt` — K4 + 24 nulls (same as cycle 166: shuffled seeds 16601–16604, profile-matched `../cycle157/mknulls157.py 20 16600000`).
Inputs not here: `alpha.bin`, `perms97.bin` (support backup), `../cycle127/plant.py` (plant plaintext, via `../cycle166/plant166.py`).
