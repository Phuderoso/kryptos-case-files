# Case file 34 — K3's own source book as the running key

*Cycle 35, 2026-11-04. Status: **negative**; 4/4 planted controls recovered; K4 inside the shuffled-null range.*

## 1. Why this
K3 is a lightly edited passage from Howard Carter's account of opening Tutankhamun's tomb (26 November 1922). The K1–K3 style profile ([case file 10](10-style-profile.md)) says each section reuses something from the one before. The most literal "K3 shows how K4 is solved" reading is that the book K3 quotes is the key book for K4. Earlier English running-key tests ([15](15-english-running-key.md), [19](19-running-key-behind-transposition.md)) were source-agnostic but only covered substitution-then-transposition (model A below) and scored by English; transposition-then-substitution (model B), where the key letters under the cribs are scattered, can only be tested with a named text. Cycle 34 did that for text carved on the sculpture; this cycle does it for the source books.

## 2. Sources (text, not photos)
- Carter & Mace, *The Tomb of Tut·ankh·Amen*, vol. I (1923), Internet Archive OCR of the MIT copy [`tomboftutankhame00cart_1`](https://archive.org/details/tomboftutankhame00cart_1): 284,914 letters after cleaning. The K3 passage ("SLOWLY DESPERATELY SLOWLY…") is found at letter 138,840, which checks the text.
- G. Elliot Smith, *Tutankhamen and the Discovery of His Tomb* (1923), [Project Gutenberg #59783](https://www.gutenberg.org/ebooks/59783): 101,923 letters.
- Each forward and reversed. Cleaning in `tools/bookrk_texts.py` (letters only, line-break hyphens rejoined).

## 3. Model
- **Substitutions (29):** every additive tableau Vigenère / Beaufort / variant with plain alphabet, cipher alphabet and key-letter numbering each chosen from {A–Z, KRYPTOS}: 24 tableaux, including the mixed Quagmire I–III types cycle 34 left out; plus the 5 five-bit XOR codes of cycle 33.
- **Layer orders:** A = substitute in plaintext order, then transpose; B = transpose, then substitute in carved order.
- **Transpositions:** the 165,065 of cycle 22 (identity, every column order w ≤ 8, K3-style single and double rotations, inverses).
- **Exact test:** for each (transposition, order, tableau) the 24 crib letters fix 24 required key letters at 24 key positions. Shifted letter bitsets of the book are ANDed constraint by constraint; any surviving offset after all 24 is a full fit. *Depth* = how many constraints one offset satisfied together. 9.6 × 10⁶ configurations × every offset of four texts per run, about 7 min of C (`tools/bookrk.c`).

## 4. Results ([report](../analysis/bookrk_report.txt))
| | Best depth | Full fits (24/24) |
|---|---|---|
| K4 | 8 (19 configurations) | **0** |
| 6 shuffled-K4 nulls | 8–9 | 0 |
| 4 planted controls (English + cribs; Carter forward/reversed and Smith keys; models A and B; mixed and KA tableaux) | 24 | **4/4**, planted offset and tableau found each time |

Two controls also hit 11 other transpositions; all 12 put the same letters on the 24 crib positions (crib-equivalent), so they are the same answer as far as the cribs can tell, not false positives.

## 5. Verdict
Neither Carter's own volume I nor Smith's 1923 book, read forwards or backwards from any letter, works as a running key for K4 under any of the 29 tableaux or XOR codes, directly or with a transposition from the cycle-22 family, in either layer order. K4's best partial is the same as the shuffled copies. **Negative.**

## 6. Limits
OCR text: running heads and page numbers removed only partly, so a key copied from a printed page could be offset by a heading; a few OCR letter errors would break an exact 24/24 match (a 22–23 match would still show; none did for K4: best 8). Volume I only (volumes II–III are not on a clean public text source I could find this cycle). Key advances on every letter. Transposition family as in cycle 22.

## Reproduce
`tools/bookrk_texts.py` (needs the two downloads above), `tools/export_perms.py` (cycle 22, writes `perms97.bin`), `gcc -O3 -march=native -o bookrk tools/bookrk.c`, `tools/bookrk_controls.py`, `tools/bookrk_runall.sh`.
