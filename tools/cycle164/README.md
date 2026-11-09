# Cycle 164 tools (IDEAS I-015): Quagmire I/II/IV autokey with two different keyed alphabets

Lists: `themed.txt` = the 97 themed words (first 97 lines of [`data/cycle158/vocabulary_all.txt`](../../data/cycle158/vocabulary_all.txt)) + `AZ`
(98 distinct alphabets); `vocab.txt` = the 10,056-word vocabulary + `AZ` (9,395 distinct). Keyed alphabet = word letters, then the
rest of A–Z (K1/K2 construction). Identical alphabets are dropped; pairs with X = Y (Quagmire III, case 124) are skipped.
Bank = `perms97.bin` (165,065 permutations, both directions). Cribs EASTNORTHEAST 21–33, BERLINCLOCK 63–73 (0-indexed).

- `q4ak.c` — exact test. Plain alphabet X, cipher alphabet Y, key letter read through Z ∈ {X, Y}; Vigenère `c = Y[x(p)+z(k)]`,
  Beaufort `c = Y[z(k)−x(p)]`, variant `c = Y[x(p)−z(k)]`; PT-fed (`k = p` L places earlier in the layer) and CT-fed
  (`k = c` L places earlier); any primer of length L. Key index = plaintext index (model Q) or carved index (transposition first).
  One 26×26 decryption table per (pair, Z, form). PT-fed: cribs on one residue class mod L are linked by the chain
  `p → D[c][p]` through the carved letters between them (checks = 24 − occupied residues ≥ 8 for L ≤ 16); CT-fed: each crib at
  key index ≥ L must satisfy `D[c_q][c_{q−L}] = p`. Survivors (≥ 6 checks) are re-checked on all 24 crib letters and decrypted.
  Build `gcc -O3 -march=native -o q4ak q4ak.c`. Usage `q4ak CT plain.txt cipher.txt perms.bin|x label plo phi pstep LMAX [recount]`.
  Known limit: the pair loop streams all tables for every permutation (memory-bound) and only writes at the end — block
  permutations and checkpoint before a full-bank run (I-074).
- `plant164.py` — six planted controls encrypted independently (string alphabets), QIV both Z readings, QI (Y = A–Z),
  QII (X = A–Z) CT-fed, both index orders, one direct with a non-vocabulary cipher word (ZEBRAFISH); shuffled nulls 16401–16402.
- `recount164.py` — independent brute-force Python recount (walks each residue class, no tables, no sorting); compared with
  `q4ak ... recount` H lines.
- `run_cycle164.sh` — `direct` (themed × vocabulary both ways, L 1–26, K4 + 22 nulls), `bank` (full pass; stopped unfinished in
  cycle 164), `sample` (every 40th bank entry, K4 + 2 nulls; what was reported).
- Profile-matched nulls: `tools/cycle157/mknulls157.py 20 16410000`.
