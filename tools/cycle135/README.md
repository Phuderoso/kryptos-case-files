# Cycle 135 tools — transposition-first periodic Quagmire, vocabulary alphabets

`carveq.c` tests periodic Quagmire I, II and III against every vocabulary-keyed
alphabet (10,056 words, the K1/K2 construction: unique letters then A–Z) on
both sides of the 165,065-entry bank (330,130 permutations counting inverses).

The new index is **transposition first, key at the carved position**: after the
letters are moved, a periodic key of length L is applied at residue
`carved_index % L`. Each permutation is bucketed by the 24 official crib landing
residues; implied key letters must agree inside each bucket, so *any* key of
that length is tested (cycle 13 / 120 did this for 264 themed alphabets; the
open gap was non-themed / vocabulary alphabets). The plaintext-index order
(key at the original position, then transpose) is run on the same alphabets.

- **III** — Quagmire III: both sides keyed by W.
- **I** — Quagmire I: plaintext alphabet keyed by W, cipher alphabet A–Z.
- **II** — Quagmire II: plaintext A–Z, cipher alphabet keyed by W.
- Modes: Vigenère (`K = C−P`; variant Beaufort is the dual and shares
  consistency) and Beaufort (`K = C+P`). Periods 1–16 (the same cutoff as cycles 13 and 120; fewer checks beyond that sit at chance). A hit needs at least 6
  extra crib constraints and is re-checked against all 24 official crib letters.

`carveq CT words.txt perms.bin label lo hi [PMAX]`

`plant.py` — 4 independent Python-encrypted controls and 2 shuffled nulls
(seeds 13501–13502). `run_cycle135.sh` — K4 + two nulls, 8-way parallel.

Lists come from `tools/cycle131/mklists.py` (10,056 words).
