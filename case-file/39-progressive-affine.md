# Case file 39 — Progressive affine substitution (Trithemius-style stepping), with and without a transposition

**Cycle 40, 2026-11-04.** Status: **negative**, exact, with full detection power.

## Why
Cycle 39 gave each position class a fixed affine map and left one door open in its own notes: a cipher whose
multiplier and shift *step* with every letter, the way Trithemius' tableau steps the shift. That is a natural hand
procedure ("multiply by r, add d, move on") and fits the style profile of case file 10 only loosely, but it is a
family no earlier cycle covered, and unlike cycle 39's long periods it has very few free parameters, so the 24 known
letters test it exactly.

## Model (`tools/progaffine.c`)
- Letters numbered A–Z (A=0) or by the KRYPTOS alphabet (K=0); index i = plaintext position (model A: substitute,
  then transpose, `carved[P[i]] = s[i]`) or carved position (model B: transpose, then substitute). Same conventions
  as `tools/affine.c` and `tools/vernam.c`.
- **Form E** (encryption form): carved = a0·rⁱ·plain + b0 + d·i + q·i(i−1)/2 (mod 26).
- **Form D** (decryption form): plain = a0·rⁱ·carved + b0 + d·i + q·i(i−1)/2 (mod 26). Not the same family as E,
  because inverting a stepping map does not keep the shift linear in i.
- a0 and r range over the 12 units mod 26, d and q over 0–25, b0 is fixed by the first crib letter.
  The multiplier can only step *multiplicatively*: an additive step a0 + k·i stays a unit mod 26 for every i only
  when k = 0.
- Special cases contained: plain affine (r = 1, d = q = 0), Caesar, Trithemius progressive shift (a0 = r = 1),
  progressive shift with a fixed multiplier (r = 1), and a second-order ("accelerating") shift (q ≠ 0).
- 165,065 transpositions (cycle 19's family plus identity) × 2 numberings × 2 orders × 2 forms.
  Linear runs (q = 0) on K4, 10 shuffled-K4 nulls and 6 planted controls; second-order runs (q = 0–25) on K4 and
  one shuffled null over every transposition, and on 2 planted second-order controls over a 20,000-transposition
  window around the planted one.
- Every configuration that matches all 24 known letters determines all 97 letters, which are then scored with
  English quadgrams.

## Results (`analysis/cycle40_progaffine.txt`)
| text | mode | exact tests | crib-consistent configs |
|---|---|---|---|
| K4 | linear (q = 0) | 4.94 × 10⁹ | **0** |
| 10 shuffled K4 nulls | linear | 4.94 × 10⁹ each | 0 each |
| K4 | second-order (q 0–25) | 1.29 × 10¹¹ | **0** |
| 1 shuffled null | second-order | 1.29 × 10¹¹ | 0 |
| 8 planted controls (6 linear, 2 second-order; both numberings, models and forms) | — | — | planted plaintext found and ranked **first 8/8** |

## Reading
- **Negative.** No progressive affine key of this shape, on either side of any of the 165,065 transpositions,
  reproduces EASTNORTHEAST and BERLINCLOCK.
- Calibration: with at most 12·12·26·26 ≈ 97,000 keys per configuration against 23 independent letter checks, the
  chance of a false consistent hit is about 97,000 / 26²³ — effectively zero, so nulls are *expected* to show 0; the
  test's power comes from the controls (all 8 recovered exactly; some model-B controls also show near-duplicate
  transpositions that agree on every crib position, all decrypting to the planted text).
- Scope: only the transposition family already used since cycle 19. An unknown, unstructured transposition would
  leave this family untestable, as for every other substitution family in this repo.
