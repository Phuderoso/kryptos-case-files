# Case file 101 — closing the open cases of cycle 105

**Cycle 109, 2026-11-05. Result: negative where the test has power; one configuration (w21, period 21, columns-in direction) undecided.**

## What was open
[Case file 97](97-which-ciphers-make-the-quirks.md) tested the model *periodic tableau substitution with period p dividing width w, then complete columnar transposition of width w* and left three gaps: width 13 in the columns-in direction for the non-Vigenère tableaux, width 14 in the columns-in direction, and width 21.

## Method
Instead of enumerating column orders (useless, because columns that touch no crib permute freely), `subcol_count.py` **counts** the column orders that are consistent with all 24 crib letters, exactly, with a dynamic program memoised on (columns used, partial key). Six tableaux: Vigenère, Beaufort and variant Beaufort, each over A–Z and the KRYPTOS alphabet. Two directions: dir0 writes rows and reads columns; dir1 writes columns in key order and reads rows.

## Controls
I wrote one 97-letter English plaintext carrying both cribs at their real positions. For each configuration I encrypted it with a random tableau, a random key and a random column order (seed 109), then asked the counter whether the true order is accepted. Every control was accepted (9/9; one count timed out but its order was still accepted).

The counts also show how weak the cribs are for some shapes: 1,451,520 consistent orders for w14 p7 dir1, and more than 10¹⁰ for w21 p3 and p7 in dir1. So a nonzero K4 count would mean nothing by itself.

**Correction to cycle 105.** Cycle 105's control generator only encrypted additively (Vigenère). Its Beaufort controls would have failed for that reason, not because of the solver. Cycle 105 published only Vigenère controls, so its conclusions stand. Cycle 109 fixes the generator: Vigenère c = x + k, Beaufort c = k − x, variant c = x − k.

## Results (K4 against 3 shuffled nulls)
| w | p | dir | K4, all 6 tableaux | nulls |
|---|---|---|---|---|
| 14 | 7 | 1 | 0 | 0, 0, 0 |
| 14 | 14 | 1 | 0 | 0, 0, 0 |
| 13 | 13 | 1 | 0 | 0 (1 null finished) |
| 21 | 3 | 0 | 0 | 0, 0, 0 |
| 21 | 7 | 0 | 0 | 0, 0, 0 |
| 21 | 21 | 0 | 0 | 0, 0, 0 |
| 21 | 3 | 1 | 0 | 0, 0, 0 |
| 21 | 7 | 1 | 0 | 0 (1 null finished) |
| 21 | 21 | 1 | timeout | not run |

The planted controls are accepted while the shuffled nulls give 0, so the test has power. K4 gives 0 in every decided configuration. **K4 is not a periodic tableau substitution (any period dividing the width) followed by a complete columnar transposition of width 13, 14 or 21**, except for w21 p21 in dir1, which the counter cannot finish in 20 s per tableau.

## Limits
- These are standard tableaux only. A mixed alphabet per phase (cycle 105's surviving lead) needs a language score, not a crib count.
- The transposition is complete columnar only; no irregular final row and no route variants.
- w21 p21 dir1 is undecided; it needs a SAT encoding or a C counter.

Code: [tools/cycle109](../tools/cycle109). Data: [data/cycle109/results109.txt](../data/cycle109/results109.txt).

## Update, cycle 110
- The background nulls finished after publication. Width 13 period 13 and width 21 period 7 (columns-in) each got 3/3 nulls at 0 for all six tableaux. Width 21 period 21 columns-in timed out for K4 and every null.
- A second counter (`tools/cycle110/window110.py`) chooses column identities only where a column's chunk touches a crib, and counts the other columns combinatorially. It matches the cycle 109 counter exactly on 14 test cases (7 planted controls and K4 at 7 configurations).
- On width 21 period 21 columns-in, it accepts a planted Vigenère A–Z control (156,764,160,000 consistent orders, so the cribs barely constrain this shape) and gives **K4 = 0 for Vigenère A–Z**. The other five tableaux and the nulls are still open: each count takes about 90 s in Python. Next step: port it to C.

## Update, cycle 113
- `tools/cycle113/win113.c` is a C port of `window110` with the same recursion and the same memo state: position, longs used, the set of named columns, and the partial key restricted to phases that still occur in a later crib. To save memory, it stores states only where the next column touches a crib and re-walks the pure-filler stretches. It matches the Python counter on **180 of 180** cases (`tools/cycle113/verify113.py`: 10 shapes × 6 tableaux × planted control, K4 and a shuffled null). Each width-21 count takes about 3 s.
- **w21 p21 columns-in, decided:** K4 = 0 under all six tableaux (Vigenère, Beaufort and variant, each over A–Z and KRYPTOS). Shuffled nulls: 0 in 3 × 6 (seed 1100) and 20 × 6 (seed 1131). Planted controls (seed 112): 6/6 accepted with 1.5×10¹⁰ to 2.6×10¹² consistent orders each, and the true order is confirmed consistent by the cycle 109 counter. The cribs constrain this shape weakly, but a real encryption of this kind still leaves billions of orders standing, and K4 leaves none.
- **New widths (columns-in only):** w15–w20, every period p ≥ 3 dividing w (16 shapes), six tableaux. K4: 0 in 96 of 96. Shuffled nulls: 0 in 96 of 96. Planted controls: 96 of 96 accepted (smallest count 8,640).
- So the shape "periodic tableau substitution with p dividing w, then complete columnar" is now excluded for w ≤ 14 and w21 in both directions, and for w15–w20 columns-in. Still open: w15–w20 columns-out (the window trick doesn't help there, because almost every column touches a crib), widths above 21, and mixed alphabets per phase.

Data: [data/cycle113](../data/cycle113).
