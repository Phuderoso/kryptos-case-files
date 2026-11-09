# Cycle 154 tools — Hill first, then a periodic key on the ciphertext side (IDEAS I-012)

- `hillcs.c` — `hillcs CT perms.bin|- label lo hi stride n k`; env `THR` (−4.6), `COMBOCAP` (20000), `FCAP` (4096 solutions per field),
  `RCAP` (200000), `MODE` (0 auto, 1 f-enumeration, 2 D-enumeration, 3 row enumeration, 4 recursive rows), `DROP` (1 = also re-solve with
  each crib-bearing block dropped: one wrong carved or crib letter), `VERB` (1 = per-configuration field counts `V`), `CFG` (file of
  `perm dir ix num o` lines to restrict the run), `QUAD`.
  Decoder `out[t] = Σ_j D[r][j]·(L[bs+j] − f[(bs+j) mod k])`, n = 2–4, frames as cycles 141/144/153 (direct; bank model Q `L[i]=CT[S[i]]`;
  bank carved order `pt[p]=out[S[p]]`; both bank directions; A–Z/KRYPTOS numbering; every alignment).
  Bilinear system split exactly mod 2 and mod 13; in each field the cheaper side is enumerated and the other solved by Gaussian elimination.
  Output: `S` (strict survivor above THR), `X` (one-error survivor above THR), `U` (left unresolved by the caps; re-solve with `MODE=4` and
  larger caps), `V` (counts), `C` (counters).
  The main run used the build before `MODE=4`/`CFG`/`RCAP` were added; the default modes are unchanged.
- `plant.py` — 10 controls (seed 15400) in the encryption direction `L = E·p + f`: 8 clean (n 2–4, k 3–19, direct, model Q, carved,
  inverse entry, KRYPTOS numbering), ctl7 with one corrupted carved letter in a crib block, ctl8 with one wrong crib letter; nulls = K4
  shuffled (seeds 15401–15402).
- `check.py` — independent pure-Python check: part A re-decrypts the controls from the printed D, f; part B (`--counts`) recounts per-field
  solution sets by brute force over all invertible D plus Gauss for f and compares them with the `V` lines.
- `run_cycle154.sh` — K4 + 2 nulls: bank strict n 2 k 1–14, n 3 k 1–9, n 4 k 1–3 (full), n 3 k 10 (stride 20), n 4 k 5–6 (stride 10);
  direct strict + one-error n 2 k 1–24, n 3 k 1–15, n 4 k 1–8. 8 workers, resumable, 519 s. Launch with `setsid timeout`.
- `summarize.py` — merges `C` lines into the results table.

Build: `gcc -O2 -march=native -o hillcs hillcs.c`.
