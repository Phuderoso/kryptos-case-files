# Cycle 188 tools (IDEAS I-185): one-error audit of case 174 (carved-index Quagmire IV with a linear-recurrence key behind the K3-law decimations / routes), plus the I-183 add-on

- `lrk188.c` — exact one-error solver (lrk186's carved-index streams + lrk183's Hamming-1 dilation; slot t free = the 23 other rows consistent mod 2 and mod 13).
  `gcc -O3 -march=native -fopenmp -o lrk188 lrk188.c` (BMI2 for `_pext_u64`); audit build `-DSAFE=1` (method 2, no prefilter / shortcut).
  `lrk188 CT perms.bin alphaA alphaB label qlo qhi method Lmin Lmax tylabel` (A = plaintext side, B = ciphertext side; L ≤ 3).
  Output `H` (per L × form: perms, pairs, one-error mod-2 passes, fits, strict fits, slot fits), `M` (fits, with the free slot t and carved position), `O`, `X` (must never appear), `END`.
- `plant188.py` — planted controls (seed 18800, independent string-level encryptor, one injected carving error); `decode188.py` — independent decoder;
  `checkctl188.py`, `run_controls188.sh` — control run and check.
- `run_cycle188.sh` — registered run (C1, grid, audit, recount, C3, gated I-183 add-on with `../cycle186/lrk186.c`'s cycle-187 binary, gated C2 chunks), every job under `setsid timeout`.
- `recount188.py`, `cmprecount188.py`, `mkslice188.py` — independent one-error order-1 recount on a 44-row slice.
- `summarize188.py` — totals, audit, grid ranks, I-183 verdict. `PREREG188.md` — pre-registration (pushed before any K4 / null run).
