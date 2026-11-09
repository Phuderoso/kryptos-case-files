# Cycle 176 tools (IDEAS I-125): Gromark behind K3-law decimations / routes

- `PREREG176.md`: the pre-registration (models, texts, null seeds, labels, 5-cell Poisson grid, controls), pushed before any K4 or
  registered-null run (commit 5794cbd).
- `gm176.c`: model G, ordinary Gromark (chain addition d[i] = d[i−L] + d[i−L+1] mod 10), plaintext A–Z/KRYPTOS, **cipher alphabet
  arbitrary**, Vig/Beau (variant = Beau under an arbitrary alphabet), behind `all.bin`. ix 0 (key on the plaintext index, then
  transpose) is a hash join of crib-slot partitions (all 10^L primers, L 2–8 in ~12 s); ix 1 (transpose first) is brute force with
  the equal-letter pairs checked first (L 2–5 in ~45 s). A primer file gives named primers.
  Build: `gcc -O3 -march=native -fopenmp gm176.c -o gm176`. Run: `./gm176 CT perms.bin label qlo qhi ix Lmin Lmax [primerfile]`.
- `pg176.c`: model PG, ACA Periodic Gromark with fixed alphabets from `mkcfg176.py cfg` (cycle 129's construction + the new kmix
  alphabet), exact 24-letter predictions; ix 0 hash join, ix 1 per config with perms bucketed by the first crib's carved slot.
  Run: `./pg176 CT perms.bin cfg176.txt label ix`.
- `mkcfg176.py`: `cfg` (137,312 PG configs) and `primers` (22,121 named primers: ACA numerical keys of the vocabulary, raw and
  deduplicated, L 3–16, plus dates/coordinates).
- `plant176.py`: independent string-level encryptor for 8 positive plants and 1 negative; `run_controls176.sh`, `checkctl176.py`.
- `run_cycle176.sh`: K4 (full) and 19 nulls (seeds 17611–17629), resumable. `summarize176.py`: per-L counts and the grid.
- `decode176.py`: replays every fit from the definitions (string level) and decodes it; for model G the cipher-alphabet letters
  not fixed by the cribs are filled by a seeded quadgram hill-climb (3 × 2,500 swaps, same budget for K4, nulls and plants), so
  each score is an upper bound over the free part. `decode_nulls176.sh`, `decsum176.py`.
- `recount176.py`: independent numpy brute force of model G from the pair definition, compared line by line with `gm176` on a
  46-perm slice (L 2–4) and a 5-perm slice (L 5) for K4, 2 nulls and 4 plants.
