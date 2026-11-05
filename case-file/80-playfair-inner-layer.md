# 80 — Playfair as the inner layer under a 26-letter periodic key (cycle 82)

> *Cycle 21 put Playfair out of the running as the last hand on the copper: it can't write all 26 letters, and S and K would have to encrypt to themselves. Nobody had checked it working behind a second man with a full alphabet.*

## Family (new)
Plaintext → **Playfair** (5×5 keyword square) → **periodic Vigenère / Beaufort / variant** on the KA or A–Z tableau. The outer layer restores all 26 letters, so cycle 21's last-layer exclusion does not apply. No transposition (open).

- **Squares (keywords as meaningful words):** all 367,184 English words of the cycle 64 list (KRYPTOS, PALIMPSEST, ABSCISSA … included) × 2 alphabets (I = J merged, or Q dropped) × 3 fills (rest of the alphabet in A–Z order, rest in KA order, A–Z version written column-wise).
- **Pairing:** pairs start at even or odd positions (both alignments). The cribs contain no doubled pair in either alignment, so no X insertion can fall inside them.
- **Outer key:** periods 1–26, KA/A–Z, Vigenère/Beaufort/variant.

## Exact test
Playfair-encrypting the crib pairs gives the inner letters at 22 (even alignment) or 20 (odd) positions; the outer key must then agree per residue mod p. 6.87 × 10⁸ (square, alignment, tableau, mode, period) configurations per text, 19 s in C (`tools/cycle82/pfv82.c`).

## Results (consistent configurations by period)
| Text | p 1–16 | p 17 | p 23 | p 24 | p 25 | p 26 |
|---|---|---|---|---|---|---|
| **K4** | **0** | 6 | 0 | 46 | 33,944 | all |
| 10 shuffled K4 nulls | 0 | 0–18 (median 2) | 0–2 | 20–85 | 37,288–45,563 | all |

K4's six p = 17 survivors (DROPLING, SODDED, SOOGEE squares; 5 checks each) sit at the null median; p ≥ 17 has too few checks to judge (crib-underdetermined).

## Planted controls (6/6)
Independent Python Playfair (`mkctl82.py`), plaintext from Sanborn-style English with the cribs in place; squares PALIMPSEST, SHADOW, LUCID, ILLUSION, UNDERGRUUND (added to the list for the control), MEMORY across both alignments, all three fills, both alphabets; outer keys ABSCISSA, BERLIN, LANGLEY, COMPASS, CLOCKS, EASTNORTH (p 6–9), all three modes, both tableaux. **Every planted configuration was found at its true period, and in every case the outer key recovered from the cribs alone deciphered all 97 letters back to the planted plaintext** (`analysis/cycle82/cycle82_summary.json`).

## Verdict
**Negative.** Playfair with any English-word keyword square (6 constructions) followed by a periodic KA/A–Z Vigenère/Beaufort/variant key of period ≤ 16 is excluded directly on the copper; p 17–26 cannot be judged by the cribs.

## Still open
Arbitrary (non-word) squares (SAT or annealing); Playfair behind or in front of a transposition; outer running/autokey keys; seriated/two-row Playfair variants; the outer key on mixed alphabets other than KA/A–Z.
