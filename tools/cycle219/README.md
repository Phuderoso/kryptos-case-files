# tools/cycle219 — audit: case 112 under one crib error (I-007), plus the results-file convention

- `PREREG219.md` — pre-registration (filed and committed before any run on K4, plants or nulls).
- `col1e.c` — every column order of width 9 and 10 (9! + 10!), ROW / COL read, both directions, × periodic key p 1–22 on the A–Z or
  KRYPTOS tableau, Vigenère (= variant for consistency) or Beaufort, key on plaintext (model A) or carved (model B) index. Per
  configuration: excess = Σ over key classes (class size − largest equal group); 0 = strict, 1 = one crib seat dissents. Written
  fresh: the transposition is built by ranking grid cells, not with cycle 124's `place()`.
- `plant219.py` — independent textbook encryptor; 20 plants (seed 209233; odd ids one carved crib letter wrong) and eight shuffled-K4
  nulls (seeds 209234–209241).
- `run219.sh` — compiles and runs everything (130 jobs, `xargs -P 8`); call it under `setsid timeout 480`. ~3.5 min on 8 cores.
- `analyze219.py` — gate R (strict counts reproduce case 112), gate P, per-p labels, crib-distinct collapse, crib-key decrypts + quadgram
  scores of K4's hits (needs `qg.bin`, float32 log10 quadgrams, from the support backup).
- `stamp219.py` — **results-file convention (from cycle 219):** every results file starts with `#` lines: `scope=…`, `text=…
  input_sha256=…` (sha256 of the exact 97-letter string, no newline), `tool=… tool_sha256=…`, `seed=… args=…`. Summaries repeat the
  per-file input sha (`summary219.json` → `inputs`). Two zero-hit outputs of different texts can no longer be byte-identical.

Reproduce: `WORK=/some/dir; cp data/cycle219/plants219.tsv data/cycle219/nulls219.tsv $WORK/; setsid timeout 480 tools/cycle219/run219.sh;
python3 tools/cycle219/analyze219.py $WORK qg.bin $WORK/res`.
