# Cycle 151 tools: Hill n = 2–4 under one carving error

- `hill1e.c` — `hill1e CT perms.bin|- label lo hi stride n`; env `THR` (−5.0), `COMBOCAP` (4096), `QUAD`.
  Plain Hill decryption `out[t] = D·L_block` in the cycle 27/141–144 frames (direct; bank model Q `L[i]=CT[S[i]]`;
  bank carved order `pt[p]=out[S[p]]`; both bank directions; A–Z/KRYPTOS numbering; every alignment).
  For every Hill block carrying crib letters, its equations are dropped, each matrix row is solved exactly mod 2 and mod 13,
  invertible D are enumerated, and the dropped block must admit an exact **one-letter repair** reproducing all its crib letters.
  Counters `strict`, `eqdrop` (one wrong crib letter), `blockdrop`, `invertible`, `repair_*`, `under` (blind spot).
- `plant.py` — 8 controls (seed 15100): six Hill encryptions (n 2/3/4; direct, model Q, carved inverse entry) with one
  **corrupted carved letter** in a crib-bearing block, and two uncorrupted; nulls = K4 shuffled with seeds 15101–15102.
- `run_cycle151.sh` — K4 + 2 nulls, n = 2, 3, 4, direct + full bank in 8 chunks (resumable). 38 s wall on 8 processes.
- `summarize.py` — aggregates chunk outputs into `data/cycle151/results.txt`.

Build: `gcc -O2 -march=native -o hill1e hill1e.c`.
