# Cycle 130 — Periodic Gromark with an unknown keyword

- `pgfree.c` is an exact feasibility test for the ACA Periodic Gromark when the keyword is not known. The cipher alphabet is arbitrary and the L group offsets are free, so the ACA rule is relaxed and a negative is stronger than one for the rule itself. Each crib letter gives one difference equation between a cipher-letter value and a group offset. A weighted union-find detects contradictions, and letters in one component must get distinct values. Primers: every digit string for L 2–9, keyword-rank primers (permutations of 1..L, 10 counted as 0) for L 8–12. Plaintext alphabet A–Z or KRYPTOS; Vigenère (ACA), Beaufort and variant forms (the last two are equivalent under an arbitrary alphabet).
- `plant.py` makes five genuine ACA Periodic Gromark encryptions (cycle 129 generator) as controls, and six shuffled-K4 nulls.
- `run_cycle130.sh` runs everything (~9 min on 8 cores).
