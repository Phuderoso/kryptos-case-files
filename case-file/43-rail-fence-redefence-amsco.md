# 43 — Rail fence, Redefence and AMSCO behind a keyword (cycle 44)

> *Three old route men nobody in this file had questioned yet: the zigzag, its cousin who reads the rails out of order, and the one who hands out letters one and two at a time. I lined them up in front of the same keyword the others had faced. None of them had been in the room.*

## Why
A grep of the case files before this cycle found **no** test of rail fence, Redefence or AMSCO transpositions (165k transposition family = columnar, routes, K3 rotations). All three are textbook ACA transpositions, the kind a 1989 hobbyist manual would hand Sanborn, and the "strips" description of the Smithsonian pages fits a rail read-off. Diversity rule: new transposition families (not in any earlier case file).

## Method (`tools/railamsco_gen.py`, `tools/railamsco.c`, `tools/run_cycle44.sh`)
- **Transpositions.** Family A (422,433 distinct permutations incl. identity, each with its inverse): rail fence, rails 2–48, every zigzag phase; Redefence (rails read out in any order), rails 3–7, every phase, every rail order; AMSCO widths 2–8, every column order, first cell 1 or 2 letters, both row conventions for even widths (alternation continues across rows, or each row starts opposite to the previous one). Family B (1,451,521): AMSCO width 9, every column order. Columns read top to bottom in key order.
- **Substitution.** Cycle 41's exact checker unchanged except for an optional cap: key(i) = k[i mod L] + s·⌊i/L⌋, L 1–26, s 0–25 (s = 0 is the plain periodic key), Vigenère/Beaufort (variant covered by sign), A–Z or KRYPTOS tableau, both layer orders (key indexed by plaintext or carved position). Every crib letter is an exact equation; L ≤ 13 consistent configs are decrypted and quadgram-scored, L ≥ 14 only counted.
- **Nulls:** 10 shuffled K4s on family A, 5 on family B (same seeds as cycle 41). **Controls:** 6 planted progressive-key texts on family A, 3 on family B (on a ±2,000-permutation window around the planted one), and 2 planted plain periodic texts (key ABSCISSA, KRYPTOS tableau) on a rail fence and a Redefence-region permutation.

## Results (`analysis/cycle44_rail_amsco_summary.txt`)
| Text | Family A consistent, L ≤ 13 | lowest L with any consistent config (A / B) |
|---|---|---|
| K4 | **0** (2.28 × 10⁹ tests) | 21 / 21 |
| K4, family B (AMSCO w9) | **0** (7.85 × 10⁹ tests) | — |
| 10 shuffled nulls (A) | 0 each | 20–21 |
| 5 shuffled nulls (B) | 0 each | 19–21 |
| 11 planted controls | 11/11 recovered with key and permutation | — |

Nine of the 11 controls ranked first by quadgrams; in the other two the true plaintext is in the top three, tied with AMSCO column orders that differ only in columns no crib touches (block-swapped English, scores within 0.1). That is a real limit: for AMSCO, the cribs alone cannot pin the uncribbed columns, so a true hit would surface as a small family of near-identical readings, not one line.

**Verdict.** Rail fence, Redefence (≤ 7 rails) and AMSCO (widths 2–9) in front of or behind a periodic or progressive keyword on the A–Z or KRYPTOS tableau: **no consistent configuration at any key length ≤ 20** for K4, the same as shuffled nulls; L ≥ 21 is chance level for every text. **Negative.**

## What this does not cover
Redefence with 8+ rails; AMSCO width ≥ 10 or with a 2-1-1 or keyed cell pattern; mixed (non-tableau) alphabets; running keys behind these transpositions (cheap next: reuse the cycle 35–36 bitset tester with these permutation files).
