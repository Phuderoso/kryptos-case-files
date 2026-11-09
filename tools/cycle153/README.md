# Cycle 153 tools — Hill + key and Hill 5×5 under one carving error (IDEAS I-040)

- `hillk1e.c` — `hillk1e CT perms.bin|- label lo hi stride n k`; env `THR` (−5.0), `COMBOCAP` (4096), `QUAD`.
  Decoder `out[t] = D·L_block + e[t mod k]` (k = 0: plain Hill), n = 2–5, in the cycle 141/144/151 frames (direct; bank model Q
  `L[i]=CT[S[i]]`; bank carved order `pt[p]=out[S[p]]`; both bank directions; A–Z/KRYPTOS numbering; every alignment).
  All n² + k unknowns are solved jointly and exactly mod 2 and mod 13. Per configuration it reduces `[A | b | I]` once per field to
  get the left null space H and syndrome s; dropping a crib block's equations E is consistent iff s ∈ span(H[:,E]). For each
  passing block the system without E is solved (x = x₀ + N·y) and every one-letter repair (carved letter j of the block → +δ,
  δ = 1–25) becomes a small **linear** system in y, checked exactly in both fields. Consistent repairs are enumerated
  (≤ COMBOCAP) for invertible D, decrypted with the repaired letter and quadgram-scored; larger sets are counted (`repair_under`).
  One wrong crib letter: leave-one-equation-out with the same syndrome test (`eqdrop_cfg`, `eq_inv`, `eq_under`).
  Strict-consistent configurations are counted (`strict`) and skipped (they are cycle 141/144 territory).
  Output: `S` (repair, above THR), `E` (one wrong crib letter), `B` (best repair line with D, e and the repaired carved letter), `C` counters.
- `plant.py` — 11 controls (seed 15300): 9 planted Hill + key / Hill 5 encryptions with **one corrupted carved letter** in a crib
  block (n 2–5, k 0–14, direct, model Q, carved, inverse entry, KRYPTOS numbering), 1 uncorrupted, 1 with **one wrong crib letter**;
  nulls = K4 shuffled with seeds 15301–15302.
- `check.py` — independent pure-Python check. Part A re-decrypts each control from its `S` lines (D, e, frame, repaired letter) and
  compares with the planted plaintext. Part B (`--counts`) recounts by brute-force **repair-and-resolve** (rebuild all crib equations on
  every repaired text, plain Gauss mod 2 and mod 13, no syndrome trick) for comparison with the C counters.
- `controls.sh` — plant → hillk1e at each control's configuration → check.py part A.
- `run_cycle153.sh` — K4 + 2 nulls: Hill + key n = 2 (k 1–14), 3 (k 1–10), 4 (k 1–4), direct and full 165,065-entry bank; Hill 5 direct
  (COMBOCAP 2,000,000) and bank stride 20 count-only (COMBOCAP 0). 8 workers, resumable, 494 s wall. Launch with `setsid timeout`.
- `summarize.py` — merges `C`/`B`/`E` lines into `data/cycle153/results.txt`.

Build: `gcc -O2 -march=native -o hillk1e hillk1e.c`.
