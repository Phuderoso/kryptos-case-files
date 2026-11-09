# Cycle 183 tools (IDEAS I-165): one-error audit of case 170 (Quagmire IV with a linear-recurrence key behind K3-law decimations / routes)

- `PREREG183.md` — pre-registration (pushed before any K4 / registered-null run).
- `lrk183.c` — exact one-error solver (self-contained; lrk181's solve0s verbatim). `gcc -O3 -march=native -fopenmp -o lrk183 lrk183.c`;
  audit build `-DSAFE=1`. `lrk183 CT perms.bin alphaA alphaB label qlo qhi method Lmin Lmax tylabel` (A = plaintext side, B = ciphertext
  side; method 0 = dilated union map for a small A list, 1 = dilated syndrome join for a large A list, 2 = every pair, audit). Output `H`
  (per L × form: perms, pairs, one-error mod-2 passes, fits, strict fits, slot fits), `M` (fits: L, form, q, A, B, wild slot t / carved
  index, wildcard value V (−1 strict, −2 block-2 shortcut), mod-2 / mod-13 solution lists), `O`, `X`, `END`.
- `run_cycle183.sh` (main run, resumable), `nulls183.txt` (seeds 18311–18329), `summarize183.py` (cells, labels, rank grid).
- `plant183.py`, `run_controls183.sh`, `checkctl183.py` — planted one-error controls; `decode183.py` — string-level replay + score.
- `mkslice183.py`, `recount183.py`, `cmprecount183.py` — independent brute-force one-error recount on a slice and comparison.
- Support as cycle 182: `all.bin` (md5 946402ca…), `all_s64.bin` (f45bc54b…), `all_s2048.bin` (= all.bin[::2048], 94a1a6c5…),
  `alpha172.txt` (92793b74…), `alpha_themed180.txt` (255a21fa…), `alpha_recount180.txt` (8c579973…), `quadgrams.json`.
