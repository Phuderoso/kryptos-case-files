# 61 — Swagman: the Latin-square transposition (cycle 63)
> *Seven rows, seven numbers, none repeated across or down. A key you could carve on a coaster. The 98-letter block has exactly the shape it wants.*

## 1. Why this
Diversity rule: cycle 62 was an extension, so cycle 63 had to open a family no case file had touched. **Swagman** (ACA, [definition](https://www.cryptogram.org/downloads/aca.info/ciphers/Swagman.pdf)) is a pure transposition keyed by an n × n Latin square. Plaintext is written in n rows; each column is re-stacked according to the matching key-square column (key repeated across), and the result is read off by columns. With n = 7, K4 plus the carved `?` (98 = 7 × 14, case file 17) fills the block exactly, and the key is a small, hand-made object in the K1–K3 spirit. Pure transposition is impossible for K4 (letter counts), so Swagman can only be one layer; here it is paired with a periodic Vigenère-family key.

## 2. Test (`tools/swagman63.c`, exact)
Unknowns: the 7 × 7 Latin key square (only the cells the cribs touch are constrained: rows 1, 2, 4, 5 of every key column, with the Latin row/column rules enforced) and a periodic key. Depth-first search over each key column's choices; every crib letter fixes the CT letter it lands on, and the key slot it uses must take one consistent shift.
- **Block configs (9):** 98 symbols with the carved `?` at the start or end of the carved text × the one unknown plaintext null at the start or end × forward Swagman or its inverse (8); plus the irregular 97-letter block (7 × 14 with the last cell empty, column 13 compacted), forward.
- **Substitution:** Vigenère and Beaufort on themed tableaux (variant Beaufort is equivalent to Vigenère for a consistency test on one tableau). Case A: key before the transposition, indexed by plaintext position. Case B: key after, indexed by carved position.
- **Depth:** 41 themed alphabets (A–Z, KRYPTOS, …) for periods 1–6; A–Z, KRYPTOS and reversed A–Z for periods 1–8. Beyond p ≈ 8 the 24 cribs no longer constrain ~10²⁰ partial squares (expected chance fits > 1), so longer periods are untestable here.

## 3. Controls ([controls.txt](../data/cycle63/controls.txt), [controls output](../analysis/cycle63_controls.txt))
Five planted texts (run on the first 5 themed alphabets, p ≤ 7) (English with both cribs, random Latin square, themed alphabet, Vig/Beau/variant, p 3–7, both cases, forward/inverse/irregular). First draft: 4/5 recovered; the fifth was invalid by construction (a crib letter landed on the cell the `?` replaces, so it could never be checked). The generator now redraws such squares; rerun: **5/5 recovered** at their true config, case, mode and period (plus period multiples, and the equivalent irregular-97 reading for `?`-at-end controls). **PASS.**

## 4. Results ([cycle63_results.txt](../analysis/cycle63_results.txt))
| Text | 41 alphabets, p 1–6 | A–Z/KRYPTOS/Z–A, p 1–8 |
|---|---|---|
| K4 | **0** | **0** |
| 3 shuffled nulls | 0, 0, 0 | 0, 0, 0 |

## 5. Verdict
| Hypothesis | Status |
|---|---|
| 7-row Swagman (98-block, `?` and null at either end; or 97 with empty last cell) + periodic Vig/Beau/variant before or after, p ≤ 6 themed / p ≤ 8 A–Z/KRYPTOS | **negative** |
| Swagman with n = 2 (98 = 2 × 49) | trivial (2 squares); not run separately, open |
| Swagman with nulls padding to 100–104 (n 4, 5, 6, 8) | open (carved length 97 argues against it) |
| Swagman + longer periodic, autokey or running key | open (cribs too weak for p > 8 with this method) |
