# Cycle 85 tools — halfabet

- `halfabet.c` — key-free same-half screen plus periodic key check (L ≤ 26). Build: `gcc -O3 -march=native -o halfabet halfabet.c`.
- `run85.sh BIN SUPPORT_DIR TEXT...` — runs each `TEXT.txt` over 8 alphabet chunks in parallel (needs `perms97.bin`, `alpha.bin` from the support backup).
- `mkctl85.py` — writes the three planted controls (`ctlA/B/C.txt`) and `controls85.json`.
Results: `analysis/cycle85/`. Case file: `case-file/82-halfabet.md`.
