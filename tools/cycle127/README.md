# Cycle 127 tools

- `seqtr.c`: ACA Sequence Transposition (5-digit primer extended by chain addition mod 10; each plaintext letter goes to the column of its digit; the ten columns are read in a key order) combined with a periodic tableau key. It runs an exact depth-first search over **all 10! column orders** for each primer, pruning on 24-crib key consistency for every period up to PMAX simultaneously. Model A puts the key before the transposition (indexed by plaintext position) and model B puts it after (indexed by carved position). Alphabets are A–Z or KRYPTOS, Vigenère (the variant cipher has the same consistency) or Beaufort. Build: `gcc -O2 -o seqtr seqtr.c`. Usage: `seqtr CT P0 P1 PMAX label`.
- `plant.py`: an independent textbook encryptor following the ACA rules (keyword → 0-9 or 1-0 labels) for 4 planted controls, plus shuffled-K4 nulls.
- `run_cycle127.sh`: the sweep (about 4 minutes per text on 8 cores at PMAX 14).
