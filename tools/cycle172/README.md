# Cycle 172 tools (IDEAS I-095, Quagmire IV part): periodic Quagmire IV behind K3-law decimations and spiral/diagonal routes

- `mkalpha172.py` — alphabet list: every vocabulary word ([`data/cycle158/vocabulary_all.txt`](../../data/cycle158/vocabulary_all.txt)) keyed on
  A–Z (K1/K2 construction, label `/Z`) and on the KRYPTOS order (word, then the rest of `KRYPTOSABCDEFGHIJLMNQUVWXZ`, label `/K`), plus A–Z and KA;
  18,776 distinct alphabets, every ordered pair PA ≠ CA tested (≈ 3.5 × 10⁸ pairs × 2 modes).
- `q4d172.c` — exact test, derived from [`tools/cycle160/q4v.c`](../cycle160/q4v.c) (same prefilter + hash join): reads the alphabet file,
  one direction (all.bin already holds each perm and its inverse), prints the analytic chance expectation per cell
  (Σ over prefilter-passing configs of 2·nu·(nu−1)·25⁻ᵐ). Build `gcc -O3 -march=native -o q4d172 q4d172.c -lm`.
  Usage `q4d172 CT alpha172.txt perms.bin label qlo qhi PMIN PMAX [drop_crib]`. ix 0 = key at the plaintext index (substitute, then
  transpose); ix 1 = key at the carved index (transpose first). Lines `H` (per cell), `M` (each match), `S` (config with > 40 matches), `END`.
- `run_cycle172.sh` — K4 full family (16 checkpointed chunks) + 8 shuffled nulls (seeds 172000–172007) on every 4th perm; resumable
  (chunks with `END` are skipped). Needs `support/all.bin` (cycle 168), `support/all_s4.bin` (`numpy: P[::4]`), `support/alpha172.txt`, `run/k4.txt`, `run/nulls172.txt`.
- `plant172.py` — nine planted controls with an independent string encryptor (no tables), random alphabets from the list (both
  constructions), random perm, p 5–14, Vig/Beau, both index orders; plant 8 has one altered carved letter under a crib (strict test must miss it).
- `recount172.py` + `recount_run172.sh` — independent numpy brute force over all PA × CA (first-crib-of-class comparison, no prefilter, no hash)
  on 30 configurations; compared with q4d172's per-config counts.
- `decode172.py` — decrypt every match with the crib-fixed key values (`?` where a class holds no crib), mean log10 quadgram off-crib and on all letters.
- `summarize172.py` — per-cell table: configs, prefilter passes, configs with ≥ 1 pair, pairs, chance expectation; K4 also on the nulls' subset.
