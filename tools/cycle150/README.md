# Cycle 150 — zig-zag autokey (direction changes every letter)

- `zigauto.c` — exact search. Sub-layer equation c_j = s + a·p_j + b·f_j (mod 26), the form (Vigenère/Beaufort/variant) cycling with period 2 or 3 (36 cycles), feed = ciphertext or plaintext at lag L 1–96, one shift s, A–Z/KRYPTOS numbering; direct or behind the transposition bank, both directions and both layer orders. `gcc -O2 -o zigauto zigauto.c`; usage `zigauto CT perms.bin|- label lo hi minm_ct minm_pt`.
- `plant.py` — planted controls (seed 15000) and two shuffled nulls.
- `run_cycle150.sh` — the full run (8 cores, ~4 min).
