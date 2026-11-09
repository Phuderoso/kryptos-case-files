# tools/cycle171 — one-error Porta behind decimations/routes + one-error running keys behind the bank (case file 159)
- `porta171.c` — Porta (case 158 model) with one arbitrary crib pair: key-free half test with ≤ 1 non-crossing pair (forced error d),
  periodic L 1–26 (strict on 23 if d forced, one dissent if d free), running keys ≤ 1 miss (env `RKFREE=1`: only d-free survivors; `NORK=1`: none),
  analytic expectation rows `EXPECT` per cell (I-097).
- `ctl171.py` — 12 planted one-/two-error Porta controls (independent string-level encryptor).
- `ctl171b.py` — 14 planted running-key controls behind bank perms (one crib/carved error, non-crib error, two errors, clean).
- `verify171.py` — `porta` / `bank` control checks, `decode` string-level decryptions of periodic fits.
- `recount171.py` — independent numpy/python recount of the key-free stage and periodic one-error counts.
- `summarize171.py` — all counts, expectations, null lineups with exact binomial (Clopper–Pearson) bounds and the 1/(N+1) floor.
- `run_cycle171.sh` — checkpointed pipeline. Uses `tools/cycle169/bookrk1e.c` unchanged for the bank.
