# 17 — The `?` as K4's first symbol: a 98-letter grid (cycle 18)
> *Ninety-seven letters is a prime-ish nuisance. Ninety-eight is fourteen by seven. Somebody left a question mark on the doorstep.*

## 1. Why this
Open lead from cycle 17: the carved `?` between K3 and K4 may belong to K4, not K3. With it, K4 is **98 = 14 × 7 = 2 × 49** symbols, a clean K3-style rectangle (K3 itself is 336 = 24 × 14 and 42 × 8). If Sanborn gridded the 98-symbol block, every earlier test on 97 letters used the wrong rectangle.

## 2. Test (`tools/k4_qgrid98.py`)
No keyword guessing. For every transposition, ask **algebraically** whether the 24 known plaintext letters (EASTNORTHEAST at 21–33, BERLINCLOCK at 63–73 of the 97-letter plaintext) fit **one periodic key**:
- **Transpositions (28,852):** K3-style single and double rotations on 98 symbols, widths 2–49, clockwise or anticlockwise, plus inverses; keyed columnar with 7 columns (all 5,040 orders) and 14 columns (keyword orders from the 90 plain-sight words), plus inverses.
- **Substitutions:** Vigenère, Beaufort, variant Beaufort; KRYPTOS tableau or straight alphabet; periods 1–12.
- **Orders:** Case A, substitute the 97 letters, append `?`, transpose (key follows plaintext position). Case B, transpose plaintext + `?`, then substitute the carved string (key follows carved position, with the `?` either taking a key slot or not).

## 3. Controls ([qgrid98_control.txt](../analysis/qgrid98_control.txt))
4 of 4 planted texts (English with both cribs, random family member, random periods 4–9, both orders) recovered; the only extra hits were multiples of the true period. **PASS.**

## 4. Results ([qgrid98_report.txt](../analysis/qgrid98_report.txt), [qgrid98_nulls.txt](../analysis/qgrid98_nulls.txt))
| Text | Consistent combinations |
|---|---|
| `?` + K4 | **0** |
| K4 + `?` (other orientation) | **0** |
| 3 nulls (`?` + shuffled K4) | 0, 0, 0 |

## 5. Verdict
| Hypothesis | Status |
|---|---|
| K4 + `?` as a 98-symbol rotation or 7/14-column grid, with a periodic (p ≤ 12) Vigenère-family layer before or after | **negative** |
| Same with a non-periodic key (running key, autokey) behind the 98-grid | open |

Honest overlap: cycle 13 ran a similar periodic-key test after transpositions of the 97 letters; what is new here is the 98-symbol geometry, the full 7-column search and the carved-position key order. The `?` most likely just ends K3's question ("Can you see anything?").
