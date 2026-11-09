# tools/cycle162 — split period-7 key (IDEAS I-013, case file 150)
- `split7.c` — exact solver: two period-7 Quagmire III keys switching at a free boundary b (phase from position 0), 86,731
  alphabets, Vig/Beau per segment, direct or behind the 165k bank (both directions, key at plaintext or carved index); models S
  (same alphabet), Z (A–Z/KRYPTOS cross), X (free alphabet per segment, count only). Optional leave-one-crib-out.
- `plant162.py` — independent textbook encryptor for the 5 planted controls + shuffled nulls (seeds 16201–16204).
- `run_cycle162.sh` — resumable runner (direct strict + one-error for 9 texts; bank for K4 + 4 nulls, 8 slices each).
- `recount162.py` — independent numpy recount from the definition (every alphabet, every boundary).
- `decode162.py` — decrypts every model-X configuration with all consistent alphabet choices and scores quadgrams.
Inputs not in this folder: `alpha.bin` (86,731 alphabets of cycles 54–56, 26 bytes each, not committed for size), the bank `perms97.bin`, quadgram table `quad.bin`, `tools/cycle127/plant.py`
(plaintext for plants), `tools/cycle157/mknulls157.py` (profile-matched nulls).
