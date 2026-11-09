# tools/cycle168 — running keys behind decimations and routes (case file 156)
- `texts168.py` — builds the 48 key texts (carved texts cyclic; Carter, Smith, John, NT, NSA 1947, Reagan; fwd/rev).
- `run_cycle168.sh` — whole pipeline; `run_part_a.sh` — K4 behind all 165,782 perms (16 checkpointed chunks, `../bookrk.c` unchanged);
  `run_nulls_ctl.sh` — 12 planted controls + NNULL (24) shuffled K4s on chunk_15 (checkpointed).
- `rk168_controls.py` — independent string-level encryptor for planted controls (Models A/B, 24 additive modes).
- `rk168_verify.py` — `verify`: string-level decryption of every FULL line; `depth`: numpy recount of bookrk's depth histogram.
- `fragscore168.py` — part B, unnamed English running key (Model A), quadgram score of the 24 forced key letters; K4, nulls, controls.
- `summarize168.py` — summary, controls check, provenance, analytic bound.
