# Cycle 177 tools (IDEAS I-128 + I-129): one-error Gromark, and Gromark in bases 5–9, behind K3-law decimations / routes

- `PREREG177.md`: the pre-registration (models, texts, null seeds 17711–17729, labels, decode set, 6-cell Poisson grid, controls),
  pushed with `gm177.c` / `pg177.c` before any K4 or registered-null run (commit ee848eb).
- `gm177.c`: model G (ordinary Gromark, arbitrary cipher alphabet, PA A–Z/KRYPTOS, Vig/Beau) in any digit base 5–10, strict
  (err 0, identical to gm176 at base 10) or **one error** (err 1: leave-one-slot-out; reports the drop mask, full = strict).
  ix 0: hash join with 24 masked partition codes per perm; ix 1: brute force with the mask intersected over violated pairs.
  Build `gcc -O3 -march=native -fopenmp gm177.c -o gm177`. Run `./gm177 CT perms.bin label qlo qhi ix Lmin Lmax base err [primerfile]`.
- `pg177.c`: ACA Periodic Gromark (cycle 176's cfg) with ≥ 23/24 exact predictions; ix 0 masked join, ix 1 two-bucket scan
  (crib 0 or crib 1 must match). Run `./pg177 CT perms.bin cfg176.txt label ix`.
- `run_cycle177.sh`: K4 + 19 nulls, resumable. `summarize177.py`: per-cell counts, labels, grid (log-space Poisson tails).
- `plant177.py`: independent string-level encryptor: one-error plants (wrong carved letter / wrong crib letter, checked to break
  the strict test), strict base-5/7 plants, two-error negatives. `run_controls177.sh`, `checkctl177.py`.
- `decode177.py`: replays every fit at string level on its 23/24 slots and decodes it (free alphabet letters by seeded quadgram
  hill-climb, every slot of the drop mask tried). `decode_all177.sh` (K4 + first 5 nulls), `decsum177.py`.
- `recount177.py`: independent numpy recount (pair-violation definition, drop masks; PG1 ≥ 23/24), `cmp_recount177.py`,
  `run_recount177.sh` (49-perm slice, and a targeted L 5 slice of K4's fits).
- `eqpairs177.py`: diagnostic for the C2 flag (mean number of equal-letter pairs among the 24 crib slots over the perm set).
