# Case file 69 — The Wheatstone cryptograph (cycle 71)

**Why this test (new family).** Charles Wheatstone's 1867 "cryptograph" is a pocket dial: an outer ring of 27 cells
(A–Z plus a blank) and an inner ring of 26 cells holding a mixed alphabet, with two clock hands geared so that both move
one cell per step. To encipher a letter you turn the long hand clockwise until it points at the plaintext letter and
copy the inner letter under the short hand. Because the rings differ by one cell, the alignment drifts by one every
lap, so the cipher is progressive and depends on the plaintext itself. It is exactly the kind of 19th-century device a
sculptor could have read about in Kahn or in Bazeries-era literature, it has a mixed (keyword) alphabet like K1–K2,
and nobody in our repo had tested it. Cycle 70's journal listed it as a new-family candidate.

## Model

Let T be the total number of steps the hands have moved. The outer cell is T mod 27, the inner cell T mod 26.
For each plaintext letter p, T advances by 1–27 steps to the next cell holding p (a repeated letter costs a full lap).

* **G1 (Wheatstone's own geometry):** outer 27 (the 26 letters in some order with the blank in any of 26 gaps),
  inner 26, arbitrary inner order.
* **G2 (mirror geometry, test only):** outer 26, inner 27 with one cell never used by the ciphertext.
* Direction: clockwise or counter-clockwise (the latter equals the reversed outer order).
* Layering: **direct**, and **model A** = Wheatstone first, then one of the repo's 165,065 transpositions
  (`car[P[i]] = W(pt)[i]`). Model B (transposition first) is blind here: the crib letters would no longer be
  consecutive on the dial, so the step counts inside the cribs would be unknown.

**Exact test.** EASTNORTHEAST and BERLINCLOCK contain no doubled letters and no X/blank, so inside each crib the step
counts are fixed by the outer alphabet alone. That gives the inner index of every crib letter up to one unknown
rotation per crib. A configuration survives only if equal inner indices carry equal ciphertext letters and equal
letters sit on equal indices (the inner ring is a permutation), for crib 1 alone, crib 2 alone, and both cribs at one
of the 26 (or 27) relative rotations. No English scoring is involved, so the test is source-agnostic.

## Runs (`tools/wheat71.c`, `tools/wheat71_sat.py`)

| run | configurations | K4 | shuffled-K4 nulls (6) | planted controls (6) |
|---|---|---|---|---|
| behind 165,065 transpositions × 264 themed outer alphabets × 26 blank gaps (+G2) × 2 directions = 2.35 × 10⁹ | both cribs consistent | **0** | 0 each | 2–60 survivors each, **planted config recovered 6/6** |
| direct × 86,731 outer alphabets × gaps × directions (4.68 M) | both cribs | **0** (crib 1 alone: 0) | 0 (3 nulls tested) | ctl_4 (planted direct): 44 survivors incl. the planted one |
| direct, **any** outer order (SMT, z3, G1, blank fixed at cell 0, inner arbitrary) | both cribs | **UNSAT — proof** | null_1: unknown at 240 s | ctl_4 with its planted outer fixed: SAT (encoding check) |

The nulls also give 0 survivors behind transpositions, so the test's false-positive rate is tiny at this scale: a K4
zero is a real exclusion for the tested layers, not a matter of luck.

## Verdict

**Negative.** The Wheatstone cryptograph cannot have produced K4 directly with any outer order (proof), nor with any
of 264 themed outer alphabets followed by any of the repo's 165,065 transpositions. Only the crib-blind order
(transposition first) and outer alphabets outside the themed list behind transpositions remain.

**Honesty notes.** (1) The unconstrained SMT runs on null_1 and on a planted control timed out, so I only know the
encoding accepts a true instance when the outer alphabet is given; the K4 UNSAT is still a sound proof because z3's
UNSAT is exact. (2) Plaintext blanks/X stops between the cribs do not matter (each crib carries its own free
rotation). (3) A crib that itself contained a doubled letter would need a lap convention; ours do not.

## Still open

* Transposition before the dial (blind to cribs; needs annealing on full decryptions).
* Arbitrary outer alphabet behind transpositions (SMT per transposition is too slow for 165k; a sampled run is possible).
* G2 direct with arbitrary outer order (cheap SMT extension).
* Wheatstone + a second substitution layer.
