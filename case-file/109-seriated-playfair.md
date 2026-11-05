# 109 — Seriated Playfair (new family, cycle 121)

> *Ordinary Playfair takes its digraphs from the stream. Seriation lays the text in a grid first and takes them down the columns — or keeps them inside each row. Same square, different diffusion. Cycle 82–86 and 91 closed the ordinary and W-free forms. Nobody had put seriation on the board as its own row.*

## Family (new)
Plaintext arranged in a width-`w` grid, then **Playfair on seriated digraphs**, with a 26-letter periodic outer key (Vigenère / Beaufort / variant on the KA or A–Z tableau) on either side of the Playfair layer.

- **S0 — column / classic ACA seriation.** Write row-wise into width `w`; pair DOWN each column with phase `ph` ∈ {0,1} (phase 1 leaves the top cell of each column as a holdover). Unpaired letters stay clear (projected onto the 25-letter alphabet).
- **S1 — row-bounded seriation.** Pair ACROSS each row of width `w` with the same phases; holdovers sit at the odd edge of a row. (Even `w` + `ph = 0` coincides with ordinary Playfair even-alignment on complete rows; `N = 97` leaves a short last row. Odd widths are a genuine interruption of ordinary Playfair.)
- **Squares:** 367,184 English-word keyword squares × 2 alphabets (I = J, or Q dropped) × 3 fills (rest A–Z, rest KA-order, column-wise) — same six constructions as cycle 82.
- **Layer orders.** Order 0: PT → Playfair → mid → outer key → CT. Order 1: PT → outer key → mid → Playfair → CT.
- **Widths / periods.** `w = 2..12` (crib-informative for column seriation mainly at `w ∈ {2..6,8..11}`; phase 1 also lights up `w = 7`). Outer period `p ≤ 16`.

## Exact test
Fully-crib-known digraphs (both letters inside EASTNORTHEAST@21–33 or BERLINCLOCK@63–73) plus crib holdovers give the mid letters at those positions; the outer key must agree per residue mod `p`. Checks = confirming re-uses of a residue. Code: [`tools/cycle121/spf121.c`](../tools/cycle121/spf121.c); planted controls [`mkctl121.py`](../tools/cycle121/mkctl121.py). Outputs in [`data/cycle121/`](../data/cycle121/).

## Planted controls (6/6)
Independent Python encipherment (column and row seriation, both phases, both layer orders, both alphabets/fills, periods 4–8). The C checker recovered every planted configuration at its true `(ser, w, ph, order, om, fill, tab, mode, p)`, with 5–18 checks from the cribs alone.

## Results
| Text | scope | checks ≥ 6 | checks ≥ 4 (max) |
|---|---|---|---|
| **K4** | 367,184 words, full scope, ~9.09×10⁹ exact tests | **0** | 550 (max 5) |
| 5 shuffled K4 nulls | same scope on a 40k-word head sample | **0** | 67–106 (max 4–5) |

K4's weak (checks = 4–5) survivors sit at or below the null baseline once the 40k sample is scaled. No configuration reaches 6 confirming crib checks on the full word list. Periods `p ≤ 3` are empty for both layer orders; the mass of consistent-but-unchecked configs at `p ≥ 12` is the usual crib-underdetermined regime (unique residues, zero checks).

## Verdict
**Negative.** Seriated Playfair (column or row-bounded, either digraph phase, either layer order) with any English-word keyword square under the six cycle-82 constructions, followed or preceded by a periodic KA/A–Z Vigenère/Beaufort/variant key of period ≤ 16, is excluded on the copper for every crib-informative width `w = 2..12`.

## Still open
Arbitrary (non-word) squares under seriation (SAT); seriation behind or in front of a transposition; outer running/autokey keys; widths `w ≥ 13` (column seriation is crib-blind there at phase 0); themed-only 264-alphabet outer tableaux beyond KA/A–Z.
