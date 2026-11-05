# Case file 65 — Two-square with both squares arbitrary (cycle 67)

**Why this test.** Cycle 66 opened Delastelle's four-square with *themed* plain squares. Its sibling, Wheatstone's
**two-square** (double Playfair's simpler cousin, in every 1940s–80s cipher manual), had never been tested. It needs only
two scrambled squares and no plain ones, so here **both squares are arbitrary** — any arrangement of the 26 letters —
which removes the "themed alphabet" assumption entirely. As in case file 64, only square shapes that can hold 26 letters
are possible: **2×13, 13×2 and 6×6** (A–Z plus 10 unused/digit cells). New family, so it satisfies the diversity rule.

**Model.** Plaintext pairs (a, b) from a fixed pair offset (pairs start at carved position 1 or 2). a sits at (r1, c1)
in square S1, b at (r2, c2) in S2. The two rectangle corners are emitted: u = X[r1][c2], v = Y[r2][c1], with
(X, Y) = (S2, S1) for the horizontal layout and (S1, S2) for the vertical one; the two mixed combinations (S1, S1),
(S2, S2) are added as a superset, and the output order is (u, v) or (v, u). The textbook degenerate rules (same row:
transparent or swapped; same column: transparent) fall out of the geometry, so no separate convention is needed.
3 shapes × 2 offsets × 4 square pairings × 2 orders = **48 configurations** per text.

**Exact test.** CNF over "letter L of square s is in cell k" with derived row and column indicators; each of the 11 crib
pairs (6 in EASTNORTHEAST, 5 in BERLINCLOCK, at either offset) becomes row/column equalities. Solved with CaDiCaL
(PySAT). Satisfiable ⇔ some pair of squares reproduces all 22 crib letters in those pairs.

**Controls and nulls.** 48 planted controls (one per configuration): Moby-Dick text with the cribs at the official
positions, random squares. For 6×6, a non-crib pair that would emit a digit gets random letters instead (the test only
reads crib pairs; documented, not hidden). 25 shuffled-K4 nulls (seeds 6700–6724), all 48 configurations each.

## Results
| Text | Satisfiable configurations |
|---|---|
| **K4** | **0 / 48** (every shape, offset, pairing and order UNSAT, each in ≤ 0.02 s) |
| 25 shuffled nulls | 24 nulls 0/48; null 14 (seed 6714) 2/48, both 6×6 offset 2 (one solution and its mirror) |
| Planted controls | **48 / 48** satisfiable at their own configuration |

**Verdict.** Two-square on any 26-letter-capable square, with **any** two squares and any of the textbook layouts, is
**excluded as K4's only layer**. The test has power: random letter strings fail 96 % of the time, and every planted
control passes. This is a stronger exclusion than four-square's (cycle 66), because no alphabet was assumed.

**Not tested (open).** Two-square behind or in front of a transposition (11 crib pairs is too thin an alibi behind a
transposition — see case file 64's order-A survivor counts — so it would need a whole-text hill-climb with gated
controls); two-square followed by a periodic key; 98-symbol `?` versions; squares of other sizes holding A–Z with
one merged letter pair (would require a carving anomaly, since K4 uses all 26 letters).

**Reproduce.** `cd tools && python3 ts67_sat.py K4 <ciphertext>`; `python3 ctl67.py ctl`; `python3 ctl67.py null 0 25`
(needs `pip install python-sat` and `data/g2701.txt`). Outputs in `analysis/cycle67/`.
