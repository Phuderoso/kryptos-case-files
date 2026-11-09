# Cycle 185 tools (IDEAS I-172): one-error audit of case 172 (Quagmire IV vocabulary × vocabulary with a linear-recurrence key behind K3-law decimations / routes)

- `PREREG185.md` — pre-registration (pushed before any K4 / registered-null run).
- `lrk185.c` — `lrk183.c` verbatim apart from the header line. `gcc -O3 -march=native -fopenmp -o lrk185 lrk185.c`; audit build
  `-DSAFE=1`. Usage as lrk183 (`lrk185 CT perms.bin alphaA alphaB label qlo qhi method Lmin Lmax tylabel`); here method 1 with
  alphaA = alphaB = `alpha172.txt`; method 2 = audit.
- `run_cycle185.sh` (main run, resumable, priority order), `nulls185.txt` (seeds 18511–18529), `summarize185.py` (cells, labels, rank grid).
- `plant185.py`, `run_controls185.sh`, `checkctl185.py` — planted one-error controls (single path); `decode185.py` — replay + score.
- `mkslice185.py`, `recount185.py`, `cmprecount185.py` — independent brute-force one-error recount on a slice and comparison with method 1
  run on the full vocabulary.
- Support as cycle 184 plus `all_s8.bin` (= all.bin[::8], 3dd34d3c…) and `all_s20000.bin` (= all.bin[::20000], 46533f11…).
