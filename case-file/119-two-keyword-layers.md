# Case file 119 — Two keyword layers stacked (cycle 131)

**Type:** new structural idea. This is the literal "several layers of something simple": K1 and K2 each used one keyword on one tableau, so K4 may be enciphered twice with two keywords, possibly on two different tableaux, with or without a transposition in between.

## Model
- **Layers:** each layer is a periodic keyword substitution on the A–Z or the KRYPTOS tableau, in Vigenère (a + s), Beaufort (s − a) or variant (a − s) form.
- **Keys:** layer 1 uses keyword 1 and layer 2 uses keyword 2, each repeated.
- **Why this is not already covered:**
  - With two different tableaux, the combined substitution changes with every position. It is not a Quagmire of any period, so the SAT results of case file 11 do not cover it.
  - Even on one tableau, the combined period is lcm(L1, L2), usually far above the periods those proofs reach.

Four ways of combining the layers were tested:
- **Direct:** layer 1, then layer 2.
- **M:** layer 1 at the plaintext position, then a transposition, then layer 2 at the carved position.
- **P:** the transposition first, then both layers.
- **Q:** both layers, then the transposition.

## What was tested
- **Direct:** every ordered pair of the 10,056 words (the 97 themed words plus the cycle-56 vocabulary), all 36 layer settings. That is 3.64 × 10⁹ configurations, each checked exactly against all 24 crib letters.
- **With transposition:** every ordered pair of the 97 themed words, with the 16 Vigenère/Beaufort settings. Each was run through all 165,065 bank transpositions in both directions and the three models M, P and Q, for 1.49 × 10¹¹ exact tests.

## Result
| text | direct | with transposition |
|---|---|---|
| **K4** | **0** | **0** |
| shuffled null 1 | 0 | 0 |
| shuffled null 2 | 0 | not run (budget) |
| planted controls | 1/1 (PALIMPSEST on KRYPTOS Vig, then QUARTZ on A–Z variant) | 3/3 (M, P and Q, each at the planted perm; Q also matched 11 other perms that agree with it at the crib positions) |

With no free parameter once the words are fixed, a false survivor has probability around 26⁻²⁴ per test, so the nulls are expected to be zero, and a K4 hit would have been decisive. **Negative.**

## What stays open
- Vocabulary × vocabulary pairs behind transpositions (only themed × themed was run).
- Three or more layers, and layers whose keys come from phrases instead of single words.
- Mixing a keyword layer with a non-periodic layer (autokey, running key) on a second tableau.
