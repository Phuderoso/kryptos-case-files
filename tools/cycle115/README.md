# Cycle 115 — Kryha behind the transposition bank
Needs `perms97.bin` (165,065 transpositions, from `tools/export_perms.py`) in /workspace/k4c115/.

    python3 pairs115.py                                  # 2,356 keyword alphabet pairs (cycle 114 test B list) -> pairs.txt
    gcc -O3 -march=native -o /workspace/k4c115/kbank kbank115.c
    python3 run115.py                                    # K4 + 3 shuffled nulls + 4 planted controls -> data/cycle115/run115.txt

Model A (Kryha, then transposition): any V1 code wheel n 1–48, exact. Model B (transposition, then Kryha): the five
published V1 wheels, any start, exact. About 40 s wall on 8 cores for all 8 texts.
