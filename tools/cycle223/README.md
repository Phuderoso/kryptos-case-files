# tools/cycle223 — audit: the case 205 p 21 one-error excess (I-318)

- `PREREG223.md` — pre-registration (committed before any run on K4, plants or nulls).
- `col21.c` — `tools/cycle219/col1e.c` verbatim except: periods from a comma list (20,21), every excess ≤ 1 cell printed, with the carved
  positions j[0..23] of the 24 crib seats after a `|`.
- `plant223.py` — plants (seed 209255; cycle 219 encryptor imported; p 21 ids 0–15, p 20 ids 16–19; odd ids one wrong carved crib letter)
  and 160 shuffled-K4 nulls (seeds 209256–209415). Set `C219=tools/cycle219` if run from elsewhere.
- `run223.sh` — compiles col21 and runs K4, the 8 cycle-219 nulls, the 160 new nulls and the plants (1,879 jobs, `xargs -P 8`, resumable);
  call under `setsid timeout 480`. ~5 min on 8 cores. (Added after the PREREG commit; it only runs what PREREG223 names.)
- `analyze223.py` — gates T / P, R / D2 / D3, rank rule, structural tables, K4 decrypts; writes stamped `results_*.txt` and `summary223.json`.
- `mult223.py` — descriptive multiplicity table (not pre-registered).

Reproduce (from the repo root): `WORK=/some/dir setsid timeout 480 tools/cycle223/run223.sh;
python3 tools/cycle223/analyze223.py $WORK qg.bin $WORK/res .` (qg.bin = float32 log10 quadgrams, support backup).
