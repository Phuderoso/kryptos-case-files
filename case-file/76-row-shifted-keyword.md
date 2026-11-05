# 76 — A keyword on the copper's own rows, shifted row by row (cycle 78)

**Type:** extension of case file 75 (diversity rule: 77 was a new family, so 78 may extend).

## The idea
Case file 75 read K2's ABSCISSA literally: key = column key + row key on a grid. Its one weak spot was exactly the
grid the sculpture gives us: the right panel's carved rows are **31 letters** wide, and widths 24–35 were *blind*
there, because with an arbitrary 31-letter column key the 24 cribs fall into too many separate columns to check each
other. So "the copper's ragged rows as the grid" could not be tested in that general form.

The K1–K3 style profile ([case file 10](10-style-profile.md)) says the keys are *words*, and a word is short. So this
cycle restricts the column key to a repeating keyword of period p (1–31) and keeps the row key arbitrary, one shift
per carved row (K4 sits on 4 carved rows: the tail of the `?OBKR` row and three full rows):

  k = A[a] + B[row]  (mod 26, in the tableau's index space)

- **Model R (restart):** a = column mod p, the keyword starts over at the left edge of every carved row, and each row
  adds its own shift (a K1/K2 keyword tableau re-keyed per line).
- **Model C (continue):** a = position mod p, the keyword runs on through the text, and the row adds a shift (a
  periodic key with a second, row-level key on top).
- K4's first letter sits at column 27 if the `?` is counted, 26 if not; both are run.
- Vigenère, Beaufort, variant Beaufort; KRYPTOS-keyed and plain tableau.

Direct, and behind the 165,065-permutation K3-style transposition set used since cycle 22 (the transposition goes
first; the key is then applied on the carved positions, i.e. on the copper rows). Each configuration is solved
exactly: weighted union-find over the p + 4 unknowns, one difference equation per crib letter, any contradiction
rejects it, every equation beyond a spanning tree is an independent check.

## Results
| Run | Configurations | Consistent | K4 max checks | Shuffled K4 (nulls) |
|---|---|---|---|---|
| Direct | 744 | 60, all at 0 checks (model C, p 26–30 only, where no two cribs share a chain) | 0 | 20 nulls: 60–66 consistent, max 0–1 |
| Behind 165,065 permutations | 122,808,360 | 1,737,693 | **5** | 12 nulls: 1,737,294–1,748,346 consistent, max **3–5** |

- **Direct:** every (tableau, mode, model, start, p) that carries even one check contradicts the cribs. Model R is
  impossible at every p 1–31; the only survivors are model C with p 26–30, where the cribs never meet; they decrypt to fragments like `FXP…RPYZKY` and say nothing.
- **Behind transpositions:** K4's best is 5 checks, inside the shuffled-null range (3–5); no K4 configuration reaches
  6. The single 5-check survivor (permutation 151422, A–Z tableau, model C, p = 25, four equivalent mode/start
  variants) reads `YL.....BEVMBKO.M…EX.....VB…` outside the cribs: noise ([k4_top5.txt](../analysis/cycle78/k4_top5.txt)).

## Controls (planted keys)
- Direct: 8/8 planted keyword-plus-row-shift encryptions of English with the cribs in place were recovered at rank 1
  with 9–17 checks, partial plaintext readable (−4.4 to −4.8 per quadgram).
- Behind transpositions: 6/6 planted (random permutation from the set, random p in 5–13, random model, tableau,
  mode) recovered in a 5,000-permutation window at the top check level (8–17), tied only with equivalent configurations.

So the tool sees this family when it is there, at 8+ checks, and K4 shows no more than random text does.

## What is excluded (a true key is always consistent)
- **Direct:** a keyword column key plus an arbitrary per-row shift on the copper's 31-letter rows, model R at every
  p 1–31 and model C at p 1–25 and 31, both start columns, Vig/Beau/variant, KA/A–Z.
- **Behind the 165,065 permutations:** every configuration that carries ≥ 6 checks (the level where all six planted
  controls sit or above); K4 has none.

## Still open
- Mixed alphabets on both sides (Quagmire-style) with the row shift.
- A row key that is itself a word applied to rows of other widths (case file 75 covers arbitrary row keys for
  w ≠ 24–35).
- Transposition after the row-keyed substitution in the *plaintext* frame (key by plaintext position, rows of the
  plaintext layout) was not run this cycle.

Code: [`tools/cycle78/`](../tools/cycle78/). Totals: [`analysis/cycle78/sweep_totals.txt`](../analysis/cycle78/sweep_totals.txt).
Control English for planting: letters of [`analysis/k1_k3_decryptions.txt`](../analysis/k1_k3_decryptions.txt) saved as `eng.txt`.
