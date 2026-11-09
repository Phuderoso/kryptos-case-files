# Cycle 178 tools (IDEAS I-137 + I-133): linear-recurrence key mod 26 behind K3-law decimations / routes; C2-flag replication

- `PREREG178.md`: the pre-registration (models, null seeds 17811–17829, labels, decodes, 7-cell grid, controls, I-133 rule),
  pushed with `lr178.c`, `plant178.py`, `seeds178.txt`, `nulls178.txt`, `fresh133.txt`, `run_cycle178.sh` before any K4 or
  registered-null run (commits 202c378, dd29766).
- `lr178.c`: the solver. mode 0 = M0 (key on the plaintext index; per-perm linear solve over GF(2) and GF(13), CRT, propagation
  check across the gap); mode 1 = M1 (key on the carved index; mod-2 stream filter as 97-bit masks, then GF(13) elimination per weight
  vector from a precomputed basis table); mode 2 = W0/W1 (weights in {0,1}, vocabulary seeds; hash join / triple-position index).
  Build `gcc -O3 -march=native -fopenmp lr178.c -o lr178`. Run `./lr178 CT perms.bin label qlo qhi mode Lmin Lmax [ix seedfile]`.
- `run_cycle178.sh`: K4 + 19 nulls, resumable. `summarize178.py`: per-cell counts, labels, grid.
- `plant178.py`: independent string-level encryptor (12 positives, 3 negatives, seed 17800). `run_controls178.sh`,
  `checkctl178.py` (planted parameters listed at the planted perm + replayed decode equals the planted plaintext; negatives missed).
- `decode178.py`: string-level replay and decode of any lr178 fit (CRT of the listed mod-2 / mod-13 solutions).
- `recount178.py`: numpy brute force (no algebra) on a perm slice: M0 L 1–3, M1 L 1–2, W L 6.
- I-133: `match133.py` (matched-null selection on the crib-repeat covariate), `run_i133.sh` (gm177 from tools/cycle177, unchanged),
  `summ133.py` (pre-registered decision).
- The blind-kit generator (I-106) is kept off the repo until the review is returned (commitment in `data/cycle178/blindkit178/`).
