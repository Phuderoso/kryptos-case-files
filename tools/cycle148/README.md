# Cycle 148 — constant-digit running keys

- `streams.py` — builds 40 key streams (8 constants x 5 digit derivations) into `streams.txt` (needs mpmath).
- `constkey.c` — exact search: key[i]=stream[o+i]+c, 3 forms x 2 alphabets, direct or behind the transposition bank, both layer orders. `gcc -O2 -o constkey constkey.c`; usage `constkey CT streams.txt perms.bin|- label lo hi [minm]`.
- `plant.py` — planted-key controls and two shuffled nulls (seed 14800).
- `run_cycle148.sh` — the full run.
