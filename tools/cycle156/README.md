# Cycle 156 tools (IDEAS I-050): key on both sides of the Hill step

- `hill2s.c` — exact solver for Vigenère (period k1) → Hill n×n → Vigenère (period k2). Decoder `out = D·(L − f) + e`.
  Split mod 2 / mod 13; per field either D row by row with prefix pruning (f, e linear) or every f with (D, e) linear.
  Build: `gcc -O2 -march=native -o hill2s hill2s.c`. Usage: `hill2s CT perms.bin|- label lo hi stride n k1 k2`
  (env `DROP=1` one-error block-drop mode, `VERB=1` per-configuration field counts, `MODE13=R|F`, `THR`, `FCAP`, `COMBOCAP`, `QUAD`).
- `plant.py` — ten planted controls (seed 15600) incl. one corrupted carved letter (ctl7) and one wrong crib letter (ctl8), plus
  two shuffled-K4 nulls (seeds 15601–15602). Keys go to stderr (`controls_keys.txt`).
- `check.py` — independent pure-Python check: re-decrypts the controls from planted and printed keys; recounts per-field solution
  counts by enumerating f and solving (D, e) (a different algorithm from the C row-by-row D enumeration).
- `run_cycle156.sh` — the full run (expects `hill2s` in `$W/tools/`, `data/controls.txt`, the 165k bank `perms97.bin`); resumable.
- `summarize.py` — `results_table.txt` from the C lines.
