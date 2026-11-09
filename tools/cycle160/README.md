# Cycle 160 tools (IDEAS I-010): periodic Quagmire IV with two different vocabulary alphabets

Vocabulary = [`data/cycle158/vocabulary_all.txt`](../../data/cycle158/vocabulary_all.txt) (10,056 words, = cycle 135's `all.txt`),
each keyed on A–Z (word letters, then the rest of A–Z; 9,394 distinct alphabets). Bank = `perms97.bin` (165,065 permutations,
cycle 19 family; both directions used). Cribs EASTNORTHEAST 21–33, BERLINCLOCK 63–73 (0-indexed).

- `q4v.c` — exact test. Per configuration (permutation, direction, index order, period p) the cribs fall into residue classes
  (model Q: plaintext index; carved: carved index after the transposition). Inside a class the key value
  `CA⁻¹(c) − PA⁻¹(p)` (Vigenère/variant) or `CA⁻¹(c) + PA⁻¹(p)` (Beaufort) must be equal, i.e. the CA difference vector equals ±
  the PA difference vector. Alphabet-free prefilter (c equal ⇔ p equal), then a hash join over all 9,394 × 9,394 ordered pairs
  (bucket on 3 coordinates, full check after); identical constraint lists cached. Every PA ≠ CA match is printed (`M`), or
  summarised (`S`) when a configuration has > 40. `H` lines: configs / prefilter pass / joins / configs with ≥ 1 match / matches /
  PA = CA matches. Optional `drop_crib` = leave one crib out (one wrong crib letter or one wrong carved letter under a crib).
  Build `gcc -O3 -march=native -o q4v q4v.c`. Usage `q4v CT vocab.txt perms.bin label qlo qhi PMIN PMAX [identity_only [drop]]`.
- `plant160.py` — five planted QIV controls encrypted independently (textbook `c = CA[PA⁻¹(p) + CA⁻¹(k)]` / Beaufort), non-themed
  word pairs, both index orders, one with a corrupted carved letter; four shuffled-K4 nulls (seeds 16001–16004).
  Profile-matched nulls for the direct test: `tools/cycle157/mknulls157.py 20 16010000`.
- `run_cycle160.sh` — full run (resumable: finished slices skipped). `summarize160.py` — `summary.txt`.
- `indep160.py` / `recount160.py` — independent brute-force recount (numpy, all PA × CA pairs, class-first-member comparison, no
  prefilter, no hashing) on 24 chosen configurations.
- `decode160.py` — decrypt every match with the crib-fixed key letters and score English (mean log10 quadgram; also off-crib).
- `overlap160.py` — how much of the vocabulary-pair space earlier cases already covered.
