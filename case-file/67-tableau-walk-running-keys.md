# Case file 67 — Tableau walk: running keys read off the carved tableau along routes (cycle 69)

**Why this test.** The right-hand panel of Kryptos is a KRYPTOS-keyed Vigenère tableau, sitting in plain sight beside
the ciphertext. Case file 33 used it only as an *idealised* text (26 clean KA rotations read row by row). The real
carving is not clean: a header and footer row `ABCD…ZABCD`, a row label in front of every row, and the famous extra
**L** that makes row N 32 characters long. Reading the carved panel along a K3-style route (columns, diagonals,
spirals) breaks the tableau's cyclic regularity exactly where those irregularities sit, so the result is no longer just a
progressive key. "Several layers of something in plain sight" — this is the most literal version. kryptosbot also
reports newly documented **circled letters on a tableau** in Sanborn's working papers (not public), which makes
tableau-derived keys worth closing in their public form.

**Source.** Tableau rows from Elonka Dunin's text transcript (`data/elonka_panel_rows.txt`, used since cycle 8), not
photos. Header with leading blank, 13 + 13 labelled rows, row N = `NGHIJLMNQUVWXZKRYPTOSABCDEFGHIJL` (32), footer.

**Key texts (108, `data/cycle69/texts69.txt`).** Four versions of the grid (full; without header/footer; without row
labels; body only) × 17 routes (rows L→R, R→L, boustrophedon; columns T→B, B→T, boustrophedon; ↘ and ↙ diagonal
families, each in forward, reversed-within-diagonal and zigzag order; clockwise and counter-clockwise spirals) ×
forward/reversed, duplicates removed. Ragged cells are skipped. Every text is cyclic and used at every offset.

**Test (exact, `tools/carved_rk69.c` = cycle 34's tool with room for 256 texts).** Key letter at index i is
`text[(o+i) mod T]`; 11 substitutions (A–Z/KRYPTOS Vigenère, Beaufort, variant; five 5-bit XOR codes); 165,065
transpositions (identity included) × both layer orders (A: substitute then transpose; B: transpose then substitute).
Every configuration's crib agreement out of 24 is counted.

**Controls.** Six planted K4-like texts (English with the cribs at the official positions) encrypted with a tableau-walk
key behind a transposition, covering both orders, A–Z and KRYPTOS tableaux, Vigenère/Beaufort/variant and one XOR code:
**6/6 recovered at 24/24 with the exact planted configuration** (plus equivalent offsets/routes, as expected from the
tableau's cyclic rows).

**Result.**

| text | best crib agreement | configurations ≥ 12 | 24/24 |
|---|---|---|---|
| K4 | **11** | 0 | 0 |
| shuffled nulls (pooled, 48 chunk runs) | 11–12 | 0–2 per null | 0 |
| planted controls | 24 | — | 6/6 |

K4 sits at or below the shuffled baseline. **Negative**: no route over the carved tableau tested here, used as a
running key behind any of the 165,065 transpositions in either order, yields K4.

**Audit note (honest scope).** A stray generator process from a first, aborted control run rewrote the shuffled-null
files part-way through the run, so the eight perm-chunks of each "null_k" mixed two different shuffles. Each chunk is
still a genuine shuffled-K4 null, so the pooled distribution (best 11–12, at most 2 configurations ≥ 12 per null) is
valid; per-null labels are not. Controls 5–6 were rewritten before their jobs started and match `controls69.txt`.

**Not covered.** Routes that skip letters or step by knight's moves; keys that advance only on non-X letters; the
circled letters in the unpublished working papers; Quagmire IV with the tableau key; transposition families wider
than the standard 165k set.
