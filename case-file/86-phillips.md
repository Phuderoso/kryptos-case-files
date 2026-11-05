# Case file 86 — Phillips cipher on the W-free text (cycle 90, new family)

**Why Phillips.** Cycles 88–89 ([84](84-w-as-null.md), [85](85-w-as-word-separator.md)) showed that reading W as a
null or separator points to a **25-letter, W-less cipher alphabet**. The W-free K4 uses exactly the other 25 letters.
The classic 25-letter family not yet in this repo is the **Phillips cipher** (ACA): a 5×5 key square; plaintext in
groups of five; group *g* uses square *g* mod 8, where squares 2–8 are made by moving rows (order 12345, 21345,
23145, 23415, 23451, 32451, 34251, 34521); each letter becomes the letter one down and one right, wrapping. Phillips-C
moves columns instead, Phillips-RC both. It is a K1–K3-era pencil cipher with a keyed square, a period (8 × 5 = 40)
and nothing exotic.

**Test (exact; `tools/cycle90/phillips.py`, Z3).** Treat the 25 positions of the letters in the key square as unknowns
(*any* square, not just keyword squares) and require the 24 crib letters (EASTNORTHEAST at 20–32, BERLINCLOCK at
60–70 of the W-free text) to encrypt correctly. 3 variants (R, C, RC) × 5 group alignments × 2 directions (down-right,
or up-left for a text made by deciphering) = 30 problems per text.

**Results** (`data/cycle90/results.txt`).
| Text | SAT | UNSAT |
|---|---|---|
| K4, W-free | **0** | 30 |
| 3 shuffled W-free nulls | 0 | 30 each |
| 3 planted controls (random squares; R/RC/C; mixed alignment and direction) | 3/3 at the planted config | — |

The cribs alone are enough to exclude every square: the test has teeth (controls are SAT), and K4 fails all 30
configurations. Caveat: a SAT result would not have meant a solution (a planted control also had one spurious SAT
config), but UNSAT is a proof of exclusion.

**Verdict.** Phillips, Phillips-C and Phillips-RC with any 5×5 square are **excluded** for the W-free K4 under W as a
null. **Negative.**

**Still open:** Phillips with a non-standard row-move order; Phillips behind a transposition; other 25-letter families
on the W-free text (Playfair is the obvious one: 92 is even; Bifid 5×5 on the W-free text; Polybius-based nihilist).
