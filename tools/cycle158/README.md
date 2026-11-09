# Cycle 158 tools (IDEAS I-056): key on both sides of the Hill step, both keys vocabulary words

- `hillw.c` — exact test for "Vigenère/Beaufort word e → Hill n×n → Vigenère/Beaufort word f" with both words from a list
  (phase 0 at the stream start). With the words fixed only D is unknown and its rows are independent; per (frame, f, sign) the
  left null space of each row's crib vectors is computed mod 13 and mod 2 (CRT), and every e word is tested against the resulting
  linear checks with early exit. Exact; no score threshold. Build: `gcc -O3 -march=native -o hillw hillw.c`.
  Usage: `hillw CT perms.bin|- label lo hi stride n fwords ewords` (env `DROP=1` one-error block drop, `VERB=1` per-row/field
  consistency counts, `EXP=0` skip the analytic chance estimate).
- `plant158.py` — ten planted controls (seed 15800) incl. a corrupted carved letter (ctl7) and a wrong crib letter (ctl8), a
  non-themed vocabulary pair (ctl9), bank plants (ctl5, ctl6, ctl10); nulls: two shuffles (seeds 15801–15802) and two
  profile-matched nulls from cycle 157 (mnull01, mnull02).
- `solve158.py` — independent re-solve (pure Python/numpy, brute force over D rows mod 26) of survivor lines: invertibility,
  full decryption, quadgram score.
- `indep158.py` — independent recount of per-row / per-field consistency counts by brute force over all D rows mod p.
- `overlap158.py` — share of the word-pair space already inside the free-key exclusions of cases 132/144.
- `run_cycle158.sh` — full run (expects `tools/hillw`, `texts.txt`, `all.txt` split into `chunk_00..03`, `themed.txt` = first 97
  words, `core.txt` in `/workspace/k4c158`); resumable. `summarize158.py` — `summary.txt` from the C lines.
