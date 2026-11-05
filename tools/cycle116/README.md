# Cycle 116 — generic stepping disk (minimal step set)
Needs `perms97.bin` (165,065 transpositions) and cycle 115's `pairs.txt` (2,356 keyword alphabet pairs) in /workspace/k4c116/.

    gcc -O3 -march=native -o /workspace/k4c116/stepset stepset116.c
    python3 run116.py      # K4 + 4 nulls + 3 planted controls (|S| = 3, 4, 6)  -> data/cycle116/run116.txt
    python3 check116.py    # m at the controls' true settings, K4's m <= 6 configs, 12 more nulls -> data/cycle116/check116.txt
