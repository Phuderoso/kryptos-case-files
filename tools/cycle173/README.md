# Cycle 173 tools (IDEAS I-105 + I-107 + I-104): the one-letter anomaly behind K3-law decimations

- `PREREG173.md` — pre-registration (family, models, 104-cell grid, max-over-cells rule, labels), committed before the K4/null runs.
- `decgen173.py` — cycle 59's decimation generator rebuilt for a true ciphertext of n = 96 / 97 / 98 letters (`dec96.bin` 168,858, `dec97.bin` 160,204 = case 57, `dec98.bin` 170,258 perms; int16 × n).
- `anom173.c` — exact periodic-key test (A–Z/KRYPTOS tableaux, Vig/Beau, key at plaintext or true-ciphertext index, p 1–26) under one anomaly: del / ins / chg / swp / none (case 23 conventions, from `tools/c/anomaly_periodic.c`). Pairwise bad-period masks; prints per p the count, distinct perms (I-101) and the analytic chance expectation (I-097). `-DSAME` restricts to PA = CA (case 57's alphabets).
  Build: `gcc -O3 -march=native -fopenmp anom173.c -o anom173 -lm`. Run: `./anom173 perms.bin n model CT PMAX PPRINT lo hi`.
- `plant173.py` — independent planted controls (string alphabets; 10 plants over the 4 models + 1 two-anomaly plant that must be missed), `checkctl173.py` — runs and checks them.
- `run_cycle173.sh` — K4 full families + K4 and 19 shuffled nulls on every 4th perm; resumable.
- `summarize173.py` — per-cell table, chance expectations, I-107 max-over-cells rank; `decode173.py` — decrypts p ≤ 21 survivors, English score; `recount173.py` — independent brute-force recount on sampled configs; `wordkey173.py` — I-104 word-key check on cycle 172's survivors.
