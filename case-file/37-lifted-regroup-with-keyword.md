# Case file 37 — Hex inside hex with a keyword on top

**Cycle 38, 2026-11-04.** Status: **negative.**

## Why
Cycle 37 closed the mod-26 "hex inside hex" model (letters → digit pairs → digit-level transposition → pairs
folded mod 26) as a single layer, and its journal flagged the obvious gap: K1 and K2 both put a keyword
substitution over the trick, so a K1–K3-style K4 would too. This cycle adds that keyword layer, in both orders.

## Model (`tools/liftkey.py`, reuses `tools/liftregroup.py`)
- **post**: plaintext → lifted regroup (cycle 37) → periodic keyword substitution → carved text.
- **pre**: plaintext → periodic keyword substitution → lifted regroup → carved text.
- Substitution in the scheme's own alphabet (A–Z or KRYPTOS-keyed): Vigenère `c=L+k`, Beaufort `c=k−L`,
  variant `c=L−k`, mod 26, key starting at position 0.
- Keys: cycle 37's 22 themed words (KRYPTOS, PALIMPSEST, ABSCISSA, BERLIN, CLOCK, SHADOW, LUCID, MEMORY, SANBORN,
  SCHEIDT, LANGLEY, EASTNORTHEAST, BERLINCLOCK, HEX, DIGIT, REGROUP, LAYER, IQLUSION, UNDERGRUUND, DESPARATLY,
  EGYPT, CARTER).
- Same 8 digit schemes (A–Z/KRYPTOS numbering, 0/1-based, base 10/16) and same 363 digit transpositions.
- 8 × 363 × 22 × 3 × 2 = **383,328 configurations per text.** Each is first checked with an exact *necessary*
  condition (the 48 plaintext digits forced by the 24 cribs must fit the carved letters at the positions the
  transposition sends them to); survivors are solved exactly with z3 (all 97 plaintext letters must be letters).
  The prefilter can only reject impossible configurations, so a 0 here is exact, not heuristic.

## Results
| text | pass prefilter | SAT |
|---|---|---|
| K4 | 0 | 0 |
| shuffled K4, seeds 1/2/3 | 0/0/0 | 0/0/0 |
| 9 planted controls (seeds 21–29) | 1–4 each | 1–4 each, **planted config recovered 9/9** |

Controls cover both orders (6 pre, 3 post), all three substitution modes, both bases, both alphabets, and
rotations, keyword columnars and inverse columnars. Extra control hits (seeds 24, 27, 28) are rotations by a
multiple of the key period landing on the same plaintext — equivalent configurations, not false positives.

**Negative.** No themed-keyword + mod-26 digit regrouping, in either order, fits the 24 known letters of K4.

## Limits
Key offset fixed at 0 (a nonzero starting offset is untested); keys limited to the 22 words; transposition
family is cycle 37's. An unknown periodic key (z3 unknowns) would be the next widening, but at long periods it
loses power, so it needs the shuffled-null baseline to mean anything.

## Reproduce
`pip install z3-solver`, then `sh tools/run_cycle38.sh` (≈10 s on 8 cores). Output: `analysis/cycle38_liftkey.txt`.
