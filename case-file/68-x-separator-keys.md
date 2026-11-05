# Case file 68 — X as a separator: does the running key skip it? (cycle 70)

**Why this test.** In K1–K3 the letter **X** is punctuation: K2 and K3 use it as a sentence or clause stop
(`…UNDERGRUUNDXWHOKNOWS…`, `…CANYOUSEEANYTHINGQ`). If Sanborn reused the carved texts (or any text) as a running key
for K4, a hand encipherer could easily have treated X as "not a real letter" in one of two places:

1. **Plaintext side** — the key only advances on non-X plaintext letters, so every X stop in K4's plaintext between the
   two cribs shifts the key under BERLINCLOCK relative to EASTNORTHEAST.
2. **Key side** — the X stops in the key text are skipped, i.e. the key is the text with its X's removed.

Both were idea (4) at the end of cycle 69. All earlier running-key cycles (16, 20, 34–36, 45, 69) advanced the key on
every letter.

## 1. Plaintext-side skipping is already ruled out — by the old results (proof, no new run)

Under model A (substitute in plaintext order, then transpose), undoing the transposition puts the cribs back at their
official positions 21–33 and 63–73. Neither crib contains an X, so inside each crib the key advances one letter per
plaintext letter whatever the rule. Skipping X's between the cribs only changes the **gap** between the two key
fragments (13 and 11 letters), never the fragments themselves. A full fit therefore still needs all 13 key letters
under EASTNORTHEAST to appear contiguously in the key text.

The earlier exact runs show that never happens:

| cycle | key texts | K4 best crib agreement | fragment 1 complete (13/13)? |
|---|---|---|---|
| 34 | carved texts (K0–K3, tableau) | 11 of 24 (count, any letters) | impossible (11 < 13) |
| 35 | Carter vol. I, Smith 1923 | ordered depth 8 | no (depth < 13) |
| 36 | KJV John/NT, NSA 1947, Reagan 1987, carved texts | ordered depth 9 | no |
| 45 | carved texts, Carter, John behind rail/Redefence/AMSCO | ordered depth 9 | no |
| 69 | 108 tableau-walk routes | 11 of 24 | impossible |

(`bookrk.c` checks constraints in crib order, so an ordered depth below 13 means no offset ever matched the whole
EASTNORTHEAST fragment; `carved_rk69.c` counts all 24, so a best below 13 also rules out a full fragment.)

So **for every key text and transposition already tested in model A, no rule for skipping plaintext letters between
the cribs — X stops, other nulls, any gap from 0 to 50 letters — can produce a fit.** The same argument makes cycle
16's and 20's fragment-English scoring gap-agnostic. Model B (transpose, then substitute in carved order) is *not*
covered: there the key index follows carved positions and the skipped plaintext X's land at unknown carved places.

## 2. Key-side skipping — new exact run

**Key texts (128, `data/cycle70/texts70.txt`).** Every cycle-34 carved text and every cycle-69 tableau-walk route
that contains an X, with its X's removed, forward and reversed, duplicates dropped (K1–K3 plaintexts and ciphertexts,
K2 as carved and corrected, K1+K2+K3 joined, with and without K0's Morse; the idealised KA tableau; 108 routes over the
carved tableau).

**Test (exact, `tools/carved_rk69.c`, unchanged).** Key letter at index i is `text[(o+i) mod T]`, every offset; 11
substitutions (A–Z/KRYPTOS Vigenère, Beaufort, variant; five 5-bit XOR codes); 165,065 transpositions (identity
included) × both layer orders. Runner `tools/run_cycle70.sh`, summary `tools/summ70.py`; wall time ≈ 6 minutes on 8
cores.

**Controls.** Six planted K4-like texts (English with the cribs at the official positions, `tools/ctl70.py`, seed 70)
encrypted with an X-stripped key behind a transposition, both orders, A–Z and KRYPTOS tableaux, Vigenère/Beaufort/
variant: **6/6 recovered at 24/24 with the planted configuration** (plus equivalent texts/permutations, e.g. K2 carved
vs corrected once the X's are gone). Note: the XOR codes could not be planted with this generator (most XOR outputs fall
outside the alphabet); the XOR modes reuse the cycle-33/34 code paths whose controls passed.

**Shuffled baseline.** Six shuffled-K4 nulls (the cycle-69 files, `data/cycle70/null_*.txt`), same run.

| text | best crib agreement | configurations ≥ 12 | 24/24 |
|---|---|---|---|
| K4 | **11** | 0 | 0 |
| shuffled nulls | 11–12 | 0–11 per null | 0 |
| planted controls | 24 | — | 6/6 |

**Verdict.** K4 sits inside the shuffled baseline. **Negative**: removing the X separators from the carved texts or the
tableau routes does not turn any of them into K4's running key behind any of the 165,065 transpositions, in either
layer order.

## 3. A reduction noted this cycle (no run needed)

Cycle 69's idea (3), "the tableau as a lookup table" (a K4 letter pair gives row and column, the carved cell is the
plaintext), is not a new family. On a KRYPTOS tableau the cell at (row r, column c) is an additive function of r and c,
so the lookup is P = f(C_a + C_b). Disjoint pairs would give a 48-letter plaintext, which contradicts the 97-position
cribs; overlapping pairs at a fixed lag L are exactly ciphertext-fed autokey with lag L (cycles 19 and 60, lags 1–21
and 1–96 behind transpositions). The carved header's irregularities only matter at the ragged row N, one cell.

## Open after this cycle
- Model B with plaintext-side X skipping (needs X positions as unknowns; small k could be enumerated).
- Key-side skipping of other letters (Q, which K3 uses for "?") — cheap to add.
- X-stripped **book** keys are pointless (books have almost no X); not run.
