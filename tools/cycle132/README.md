# Cycle 132 tools — two keyword layers, then a transposition, full vocabulary (hashed)

`dblq.c` covers model Q of cycle 131 (both keyword layers applied at the plaintext position, then one of the
165,065 bank transpositions, either direction) for **every ordered pair of the 10,056-word list**, not just the
97 themed words. Trick: under model Q the 24 required carved letters depend only on the keywords, so each bank
permutation σ (and σ⁻¹) is reduced once to its 24-letter crib signature `ct[σ(i_t)]`, stored in a hash table
(330,130 signatures). A configuration survives iff its required letters match a signature: one lookup per
configuration instead of 330,130 permutation checks. Equivalent bank permutations share a signature, so a hit
reports the first one stored.

- `dblq CT list1 list2 perms.bin label lo hi` — rows lo..hi of list1 × all of list2 × 36 settings.
- `plant.py` — 3 independent Python-encrypted controls with vocabulary words and bank perms (incl. an inverse), 2 shuffled nulls (seeds 13201–13202).
- `run_cycle132.sh` — K4 + two nulls, 8-way parallel; 452 s wall.

Lists come from `tools/cycle131/mklists.py`.
