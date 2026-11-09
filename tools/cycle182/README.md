# Cycle 182 tools (IDEAS I-155 + I-160): Quagmire IV (two keyed alphabets) with a linear-recurrence key behind K3-law decimations / routes

- `PREREG182.md` — pre-registration (pushed before any K4 / registered-null run).
- `lrk182.c` (+ `solve0.inc`, lrk180's GF(p) solve, verbatim) — exact solver. `gcc -O3 -march=native -fopenmp -o lrk182 lrk182.c`;
  audit build `-DSAFE=1`. `lrk182 CT perms.bin alphaA alphaB label qlo qhi method Lmin Lmax tylabel` (A = plaintext side, B = ciphertext
  side; method 0 = CSR union map for a small A list, 1 = syndrome hash join for a large A list, 2 = every pair, audit). Output `H` (per
  L × form: perms, pairs, mod-2 passes, fits), `M` (fits: L, type, form, q, A, B, mod-2 / mod-13 solution lists), `O`, `X`, `END`.
- `run_cycle182.sh` (main run, resumable), `nulls182.txt` (seeds 18211–18229), `summarize182.py` (cells, labels, rank grid, I-160).
- `run_i160_182.sh` — I-160 replication with `../cycle181/lrk181.c` (40 plain shuffles 18241–18280, 20 parity-matched 18281–18300).
- `plant182.py`, `run_controls182.sh`, `checkctl182.py` — planted controls; `decode182.py` — string-level replay + score.
- `mkslice182.py`, `recount182.py`, `cmprecount182.py` — independent numpy brute-force recount on a slice and comparison.
- Support as cycle 181: `all.bin` (md5 946402ca…), `all_s64.bin` (f45bc54b…), `alpha172.txt` (92793b74…), `alpha_themed180.txt`
  (255a21fa…), `alpha_recount180.txt` (../cycle180/), `quadgrams.json`.
