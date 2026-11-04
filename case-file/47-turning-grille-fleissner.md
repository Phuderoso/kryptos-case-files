# 47 — Turning grille 10×10, classic Fleissner direction, exact SAT (cycle 48)

> *Last night the grille man read through his windows. Tonight he writes through them: twenty-five letters a turn, four turns, three windows left dark at the end, then the whole card read across like a newspaper. Same card, opposite hand. He still never matched the 24 letters we already know.*

## Why
Cycle 47 closed the K3-like reading (convention A) for short keys and listed **convention B** — plaintext written through the holes, grid read row-major — as the first open item. That is the textbook Fleissner direction, so it is the more historically likely of the two. Audit/extension cycle (cycles 46 and 47 were both new families, so the diversity rule is met).

## Method (`tools/fleissner_cnf.py`, `tools/run_cycle48.sh`, controls `tools/ctl48.py`)
- Plaintext letter j goes into the (j mod 25)-th hole, in row-major order, of rotation ⌊j/25⌋ (clockwise turns, same orbit labelling as cycle 47's `grille_sat.py`). The last three hole slots of the fourth turn stay empty; the grid is read row-major with empty cells skipped (97 letters).
- Periodic Vigenère or Beaufort (variant covered by sign), A–Z or KRYPTOS numbering, key applied before the transposition (index = plaintext position) or after it (index = ciphertext position).
- **Exact CNF:** one-hot orientation per orbit (4²⁵ grilles), unary sequential counters give every cell's rank inside its rotation and the number of empty cells before it, so each crib letter becomes plain clauses tying a cell, its ciphertext index and the key. Solved with CaDiCaL via pysat. UNSAT excludes every grille and every key of that length at once. Every SAT answer is re-checked by real encryption through the grille.
- Cycle 47's z3 attempt on one big model was too slow; the CNF version recovers planted keys in 0.1–4 s.

## Results (`analysis/cycle48_grille_B.txt`)
| Text | Key before transposition | Key after transposition |
|---|---|---|
| K4 | **UNSAT for L 1–8** (all 4 tableau/mode settings) | **UNSAT for L 1–6**; L 7–8 timed out at 170–240 s |
| 3 shuffled nulls (L 1–6, KRYPTOS Vigenère, both sides) | 18/18 UNSAT | 18/18 UNSAT |
| planted controls | PALIM (Vig, KRYPTOS, L 5) and K (Vig, A–Z, L 1) recovered, 24/24 | QX (Beaufort, A–Z, L 2) recovered, 24/24 |

Power: 24 cribs carry about (24 − L) × 4.7 bits against about 50 bits of grille freedom, so a random text fits only for L well above 10; the nulls agree.

**Verdict.** No 10×10 turning grille used the classic way (write through the holes, read across), clockwise, with a periodic key of length ≤ 8 before it or ≤ 6 after it, fits K4. **Negative in range.**

## What this does not cover
Counter-clockwise turning (one sign flip in `op()`); other placements of the three empty slots (start of the first turn, or the `?` as a 98th letter with two empties); longer keys (needs longer timeouts or symmetry breaking); grille + running key; grilles of other shapes (e.g. 7×14 rectangles with 180° turns).
