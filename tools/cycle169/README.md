# tools/cycle169 — one-error running keys behind decimations/routes + masked depths (case file 157)
- `bookrk1e.c` — `bookrk` (cycle 35) with one-error tolerance (bitsets A = no miss, O = ≤ 1 miss; `O ← (O&v)|A`), tail bits
  masked to real offsets (I-090), sparse finish offset by offset. Prints FULL / FIT23 (missed crib index) / CAND1, SUMMARY with
  `hist` (masked strict, all configs), `hist1` (one-error prefix depth), `histS` (masked strict on bookrk's own config set).
  Optional 5th arg `strictcfg` skips XOR configs with an undecodable key symbol, which reproduces bookrk's config set.
- `run_cycle169.sh` — whole pipeline, checkpointed (controls → K4 16 chunks → K4 + 40 nulls on a 1,000-perm slice).
- `ctl169.py` — one-error (e), non-crib-error (n) and two-error (d) controls built from cycle 168's string-level controls.
- `verify169.py` — `verify`: string-level 97-letter decryption of FULL/FIT23 lines + quadgram score; `depth`: numpy recount.
- `summarize169.py` — summary, controls check, null lineup with exact binomial bound, analytic bound.
- `recheck090.py` — I-090: old vs masked depth for single quoted configs cut out of earlier run folders.
