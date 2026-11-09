# Cycle 186 tools (IDEAS I-164, prepared, not yet run on K4): Quagmire IV with a linear-recurrence key on the carved index behind K3-law decimations / routes

- `lrk186.c` — exact solver, **written and timed this cycle on the reserved shuffle only** (no K4 run, no registered nulls, no controls
  yet: the cycle's 8-minute heavy budget was used up by the timing probe, see `../../data/cycle186/timing186.txt`).
  `gcc -O3 -march=native -fopenmp -o lrk186 lrk186.c` (needs BMI2 for `_pext_u64`); audit build `-DSAFE=1`.
  `lrk186 CT perms.bin alphaA alphaB label qlo qhi method Lmin Lmax tylabel` (A = plaintext side, B = ciphertext side; L ≤ 4).
  method 1 = per-perm hash join (larger side hashed, probe v ⊕ small-side word for every mod-2 stream word v at L_max);
  method 2 = audit (every (A, B) pair against a per-perm 2^24 bitset). Mod-2 stream projection and the GF(13) loop over c mod 13
  are lrk180 mode 1's code; shortcut (off in SAFE): GF(13) at L_max first, lower L only if L_max fits (exact by nesting).
  Output `H` (per L × form: perms, pairs, mod-2 passes, fits), `M` (fits), `O`, `X` (must never appear), `END`.
- Support as cycles 180–185: `all.bin` (946402ca…), `all_s64.bin` (f45bc54b…), `all_s8.bin` (3dd34d3c…), `all_s2048.bin` (94a1a6c5…),
  `alpha172.txt` (92793b74…), `alpha_themed180.txt` (255a21fa…).
- **Timing (reserved shuffle 9186, all_s64, 6 threads):** L 1–3 ≈ 3.9 s per direction (≈ 4.2 min per direction on the full set);
  L 1–4 ≈ 284 s per direction (≈ 5 h on the full set: the GF(13) stage loops over 13⁴ weight vectors per mod-2 candidate). Still to
  do before a registered run: planted controls (positives in both directions incl. alphabets outside the themed list, a seed-slot
  plant at carved position < L, negatives), SAFE audit on all_s20000, an independent recount, pre-registration.
