# tools/cycle166 — three key segments / returning key, period-7 phase (IDEAS I-070, case file 154)
- `split3.c` — exact solver. Models T (three independent period-7 Quagmire III keys) and R (key 1 returns after the middle
  segment); boundaries free, Vig/Beau per segment, shared alphabet out of 86,731 (or A–Z/KRYPTOS only with amax 2); direct or behind
  the 165k bank (both directions, plaintext/carved index); optional leave-one-crib-out (`drop`) and bank stride.
- `djob.sh` — direct strict + 24 drops for one text. `run_cycle166.sh` / `run_cycle166b.sh` — resumable runners (tmp → rename, done markers).
- `plant166.py` — independent textbook encryptor for 20 plants + 4 one-error plants. `controls166.txt` — recovery table.
- `recount166.py` — independent numpy recount over every boundary pair; `compare166.py` runs it against split3 (88 configurations).
- `summarize166.py` — counts per cell; `decode166.py` — decrypts T fits and scores quadgrams; `power166.py` — fewest-check bound.
- `texts166.txt`, `mnulls166.txt` — K4 + 24 nulls (shuffled seeds 16601–16604; profile-matched, `../cycle157/mknulls157.py 20 16600000`).
Inputs not here: `alpha.bin`, `perms97.bin`, `quad.bin` (support backup), `../cycle127/plant.py` (plant plaintext).
