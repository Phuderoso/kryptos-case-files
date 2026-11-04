# Case file 50 — Double keyed columnar, exact (cycle 52)

**Why this family.** K3 is a double transposition, and the K1–K3 style profile (case file 10) says keys are real words.
The obvious word-keyed version of K3's trick, *two keyed columnar transpositions in a row*, was only ever **annealed**
(cycles 4–5, with weak power: about 68 % detection per configuration and one disruption rule). Cycle 12 covered every
single column order up to width 8 and K3-style rotations, not keyword pairs. This cycle tests the keyword-pair version
exactly. It is a new structural slice, not another single-transposition variant.

**Model.** The plaintext (97 letters) is written row by row under keyword 1 (width = word length, last row short), the
columns are read in alphabetical keyword order (ties left to right); the result is rewritten under keyword 2 and read
the same way. Keyword 2 may be absent (single keyed columnar). Each permutation and its inverse, on either side of a
periodic or progressive keyword key (key<sub>i</sub> = k[i mod L] + s·⌊i/L⌋, s 0–25, L 1–22), Vigenère or Beaufort,
A–Z or KRYPTOS tableau. Exact test against the 24 official crib letters (EASTNORTHEAST 22–34, BERLINCLOCK 64–74,
1-based) with the same checker as cycles 41, 44, 46 and 50.

**Keywords.** 106 themed words (KRYPTOS, PALIMPSEST, ABSCISSA, BERLIN, CLOCK, SHADOW, UNDERGROUND, LODESTONE,
TUTANKHAMEN, CARTER, LANGLEY, SANBORN, SCHEIDT, WEBSTER, compass and Berlin words, …) plus the 3,000 most frequent
English words of length 4–14 in five Gutenberg novels already in `data/`, giving **1,837 distinct column orders**
(widths 4–14) and **3,376,406 ordered pairs** (incl. single columnar). 3.09 × 10¹⁰ exact tests per text.
Tools: [`tools/dcol.c`](../tools/dcol.c), [`tools/dcol_gen.py`](../tools/dcol_gen.py),
[`tools/ctl52.py`](../tools/ctl52.py), [`tools/run_cycle52.sh`](../tools/run_cycle52.sh); orders and raw output in
[`data/cycle52/`](../data/cycle52/).

## Controls
Planted English (cribs at the official positions), run on a 41-order subset containing their keys:
| Control | Transposition | Key | Recovered |
|---|---|---|---|
| CTL1 | KRYPTOS then PALIMPSEST, key after | LAYER, A–Z Vigenère | yes (plus the trivial L = 10 double), −4.09/quadgram |
| CTL2 | SHADOW then BERLIN, inverse, key before | ABSCISSA progressive s = 2, KRYPTOS Beaufort | yes, only hit |
| CTL3 | THOUGHT then PALIMPSEST, key before | CLOCK, KRYPTOS Vigenère | yes (plus L = 10 double) |

## Results (full 3,376,406 pairs)
| Text | Consistent, L ≤ 19 | L = 20 | L = 21 | L = 22 |
|---|---|---|---|---|
| K4 | **0** | 13 | 25 | 893 |
| Shuffled K4, null 0 (seed 5200) | 0 (one at L = 19) | 8 | 64 | 830 |
| Shuffled K4, null 1 (seed 5201) | 0 | 14 | 50 | 866 |

K4 sits inside the null range at every L. The 13 L = 20 fits were decrypted and scored anyway: best **−6.54 per
quadgram** (ALOFT/WHISPER, progressive s = 11), against −4.09 for the planted English; all 13 are crib-in-gibberish.

## Verdict
**Negative.** No pair of these 1,837 keyword column orders, single or double, with a periodic or progressive keyword
key of length ≤ 19 on either side, fits K4's cribs; longer keys are at null level and unreadable.

**Still open:** keywords outside this list (arbitrary double columnar is about 2⁷² keys at width 14, beyond what 24
cribs can judge); double columnar with a running key or a mixed (non-tableau) alphabet; disrupted columnar, exact.
