# Cycle 128 tools

- `seqgro.c`: the "one key, two jobs" test. One chain-addition digit stream (5-digit primer) drives both an ACA Sequence Transposition (all 10! column orders, exact DFS) and a Gromark-style digit substitution, before (model A) or after (model B) the transposition. The plaintext alphabet is A–Z or KRYPTOS, the form is Vigenère or Beaufort, and the cipher alphabet is **arbitrary** (enforced as a bijection), so keyword alphabets are covered. Build: `gcc -O2 -o seqgro seqgro.c`. Usage: `seqgro CT P0 P1 label`.
- `plant.py`: planted controls from an independent encryptor (reuses cycle 127's ACA `seqtrans`) and shuffled-K4 nulls.
- `decrypt_survivor.py`: decrypts a survivor as far as the cipher alphabet pinned by the cribs allows.
- `run_cycle128.sh`: the sweep (about 1 minute per text on 8 cores).
