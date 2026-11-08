# Case file 130 — Hill 6×6, direct

**Cycle 142, 2026-11-08. Variant of cycle 141 (case file 129).**

## What was tested

A 6×6 Hill cipher straight on the carved text, every block alignment (o = 0–5), A–Z and KRYPTOS
numbering. As with 5×5, each row of the decryption matrix only meets one residue class, so the
cribs split into six small systems: 3–5 equations for 6 unknowns per row, solved exactly mod 2
and mod 13. There are no spare equations in general, so most configurations cannot be rejected
by the cribs alone. The remaining space (about 10¹⁷ matrices) was searched by coordinate ascent
on quadgrams, 500 random starts per configuration, keeping invertible matrices only.

## Results

- **Exact part.** 6 of K4's 12 configurations are inconsistent outright, from rank deficiencies
  mod 2 or 13 in the ciphertext blocks. The 20 nulls lose 83 of 240 (about 4 of 12 each).
- **Scored part.** K4's best is −5.08 (o = 5, A–Z numbering, nothing readable beyond the cribs).
  The best of each of 20 shuffled K4s ranges from −5.44 to −5.07. K4 ranks 2nd of 21, inside
  the null spread (p ≈ 0.1).
- **Controls.** 3/3 planted 6×6 Hill texts (o = 0, 3, 5, both numberings) came back word-perfect
  at −4.04 to −4.10, with 300 starts.

**Negative.** The freedom left by the cribs lets the search squeeze random text up to about
−5.1, but English sits at −4.1 and K4 behaves like a shuffled text.

## Limits

- Direct only. Behind transpositions the per-configuration search cost (about 3 s) makes the
  bank infeasible in one cycle.
- n ≥ 7 not run: some rows keep 4–5 free dimensions, too many to enumerate per row.
- Numbering limited to A–Z and KRYPTOS; heuristic search, so not exhaustive, but controls show
  it finds a true 6×6 key reliably.
