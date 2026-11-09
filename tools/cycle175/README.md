# Cycle 175 tools (IDEAS I-111 + I-113): two slips and Hill 4×4 behind K3-law decimations

- `PREREG175.md`: the pre-registration (models, texts, KMIN 4 information filter, 5-cell grid with the I-115 zero-variance rule and the I-117 two-sided report, labels, controls), pushed before any K4/null run (commit 824e435).
- `slip175.c`: an exact periodic-key test (A–Z/KRYPTOS tableaux, Vig/Beau, key at plaintext or true-ciphertext index, p 1–26) under one dropped (`delx`, n 98) or extra (`insx`, n 96) carved letter **plus** one dropped crib. Drop candidates per p are the intersection of the bad crib pairs. It prints per p: HIST (all), HISTK (checks ≥ KMIN), DPERM, EXPECT and EXPECTK (analytic chance), and HIT lines up to PPRINT.
  Build: `gcc -O3 -march=native -fopenmp slip175.c -o slip175 -lm`. Run: `./slip175 perms.bin n delx|insx CT PMAX PPRINT KMIN lo hi`.
- `hill175.c`: Hill n 2–4, linear/affine, A–Z/KA numbering, block offsets, both orders (models of `tools/cycle174/hill174.c`). The row solver is new: RREF mod 2 and mod 13, kernel basis, CRT. It decodes every invertible key (up to 64 per config). Build: `gcc -O3 -march=native hill175.c -o hill175 -lm`. Run: `./hill175 CT perms.bin label qlo qhi nmin nmax KMIN`.
- `plant175.py`: the independent string-level encryptor for the planted controls (6 two-slip, 1 strict, 1 two-error negative, 4 Hill n 4, 1 Hill negative). `checkctl175.py` checks them and also replays cycle 173's ctl10.
- `run_cycle175.sh`: K4 on the full families, then K4 and 19 nulls on every 8th perm. Resumable.
- `summarize175.py`: per-p table, exact bounds, Hill sub-cells, the pre-registered grid. `decode175.py`: decodes and English scores for slip HITs and Hill K lines.
- `recount175.py`: independent numpy recount of slip175 (full conflict matrix; a drop is consistent iff every conflict touches it). `hillrecount175.py`: brute force over all row vectors mod 2 and mod 13, compared per sub-cell.
