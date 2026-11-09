# Cycle 184 tools (IDEAS I-163): Quagmire IV with both alphabets from the 18,776 vocabulary and a linear-recurrence key behind K3-law decimations / routes

- `PREREG184.md` — pre-registration (pushed before any K4 / registered-null run).
- `lrk184.c` (+ `solve0.inc`) — `lrk182.c` verbatim apart from the header line. `gcc -O3 -march=native -fopenmp -o lrk184 lrk184.c`;
  audit build `-DSAFE=1`. Here both list arguments are `alpha172.txt` (method 1 main, method 0 and method 2 audits).
- `run_cycle184.sh` (main run, resumable), `nulls184.txt` (seeds 18411–18429), `summarize184.py` (cells, labels, rank grid).
- `plant184.py`, `run_controls184.sh`, `checkctl184.py` — planted controls; `decode184.py` — string-level replay + score (decode182 logic).
- `mkslice184.py`, `recount184.py`, `cmprecount184.py` — independent numpy brute-force recount on a slice and comparison.
- Support as cycle 183: `all.bin` (md5 946402ca…), `all_s64.bin` (f45bc54b…), `all_s512.bin` (2a8c7ba2…), `all_s2048.bin` (94a1a6c5…),
  `alpha172.txt` (92793b74…), `alpha_recount180.txt`, `alpha_themed180.txt` (255a21fa…, plants only), `quadgrams.json`.
