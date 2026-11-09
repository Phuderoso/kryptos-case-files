# Cycle 181 tools (IDEAS I-156): one-error audit of case 168 (keyed-alphabet linear-recurrence keys behind K3-law decimations / routes)

- `PREREG181.md` — pre-registration (pushed before any K4 / registered-null run).
- `lrk181.c` — exact solver. `gcc -O3 -march=native -fopenmp -o lrk181 lrk181.c` (BMI2 for `_pext_u64`); audit build `-DSAFE=1`
  (no block-2 shortcut in mode 0, no first-failing-row shortcut in mode 1). `lrk181 CT perms.bin alphafile label qlo qhi mode Lmin Lmax`;
  mode 0 = key on the plaintext index (L ≤ 8), mode 1 = key on the carved index (L ≤ 4). Output `H` (per L × type × form: perms, pairs,
  one-error mod-2 passes, fits, strict fits, fitting slots), `M` (fits: wild slot t / slot / V or carved position, solution lists;
  `t -1` = strict fit), `O` (overflow, mismatch), `X` (table vs solve disagreement, must never appear), `END`.
- `run_cycle181.sh` (main run, resumable), `nulls181.txt` (seeds 18111–18129), `summarize181.py` (cells, labels, rank grid).
- `plant181.py`, `run_controls181.sh` (`BIN=lrk181safe` for the audit build), `checkctl181.py` — planted controls; `decode181.py` — replay + score.
- `mkslice181.py`, `recount181.py`, `cmprecount181.py` — independent numpy brute-force recount on a slice and comparison (fitting-slot sets).
- Support as cycle 180: `all.bin` (md5 946402ca…), `all_s8.bin` (3dd34d3c…), `all_s64.bin` (f45bc54b…), `alpha172.txt` (92793b74…),
  `alpha_recount180.txt` (../cycle180/), `quadgrams.json`.
