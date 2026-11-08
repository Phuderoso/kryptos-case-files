# 111 — Cadenus: columns that turn like a dial (cycle 123)

**Question.** Cadenus is the ACA's classic "rotating column" transposition: the text goes into a grid, the columns are put in keyword order, and **each column is rotated** (cyclically shifted) by its own amount before the grid is read by rows. It was never in this file (the README coverage table had no row for it). It fits the K1–K3 profile ([case file 10](10-style-profile.md)): a grid like K3's, a keyword like K1/K2's, and a "dial" motion that suits a clock clue. Pure Cadenus is a transposition, so it cannot be the whole of K4 (E count, see the coverage table); the hypothesis is **Cadenus + a K1-style periodic tableau key**, in either order.

**HYPOTHESIS C123.** K4 = rotated-column transposition (width w, column order π, per-column rotations s_c) composed with a periodic Vigenère/Beaufort key on the A–Z or KRYPTOS tableau.
**Falsification test.** Exact crib consistency over every rotation vector, with planted controls and shuffled nulls.

## Model (generalized so that 97 letters fit)
- 97 is prime, so a true Cadenus rectangle (25 × k) is impossible without padding. The model uses a ragged grid: text written row-wise in w columns, column c holds L_c = ⌈(97 − c)/w⌉ cells and is rotated by **any** s_c ∈ [0, L_c) — this includes Cadenus's keyword-letter shifts and any other rule.
- Columns placed by π; read **by rows** (Cadenus; holes of the short last row skipped) or **by columns** (keyed columnar with rotated columns).
- Both directions: plaintext into the grid (dir 0) or ciphertext into the grid (dir 1 = the inverse permutation).
- Substitution: periodic key p 1–13 (exact, full key fixed by the cribs in model A) and p 14–20 (underdetermined, scored only); A–Z / KRYPTOS tableau; Vigenère / Beaufort (variant Beaufort = Vigenère consistency); key indexed by plaintext position (model A, key before transposition) or carved position (model B).
- Orders: **all** orders w 2–8 (46,232), plus 3,889 keyword orders w 9–13 from the cycle-52 themed list (PALIMPSEST, NORTHEAST, LODESTONE, WELTZEITUHR…), clock/rotation words (CADENUS, ROTATION, CLOCKWISE, WORLDCLOCK…) and the cycle-56 vocabulary.
- Size: ≈ 3.0 × 10¹⁴ (order, rotation vector, read mode, direction) settings × 16 substitution configurations × 13 periods, decided exactly by backtracking (cribs touch every column for w ≤ 13, so every rotation is constrained).

Code: [`tools/cycle123/`](../tools/cycle123/). Data: [`data/cycle123/`](../data/cycle123/).

## Controls and baselines
| Text | Planted | Result |
|---|---|---|
| ctl1 | w 7 CADENUS, rows, dir 0, KRYPTOS-tableau Vigenère PALIMPS, model A | recovered exactly (4 survivors in total; planted one included, score −4.73) |
| ctl2 | w 6 SHADOW, columns, dir 1, A–Z Beaufort ABSCISSA, model B | recovered exactly (256 survivors at p 8, all with key ABSCISSA; rotation of two columns underdetermined) |
| ctl3 | w 10 WELTZEITUH, rows, dir 1, KRYPTOS Beaufort CLOCK, model A | recovered exactly (5 survivors) |
| ctl4 | w 5 BERLI, columns, dir 0, KRYPTOS Vigenère LAYERTWO, model B | recovered exactly (1 survivor) |
| null 1–5 (shuffled K4) | — | p ≤ 13: 1, 0, 0, 0, 0 survivors (null 1: one w 12 survivor at p 13, gibberish, −7.32); w 8 all orders: 0, 0 |

## Result
| Pass | K4 survivors | Nulls |
|---|---|---|
| p 1–13, all orders w 2–7 + keyword w 8–13 | **0** | 1, 0, 0, 0, 0 |
| p 1–13, all 40,320 orders w 8 | **0** | 0, 0 |
| p 14–20 (partial: 300 s cap, first 200,000 printed) | many (underdetermined); best quadgram −6.23 | best −6.17 … −6.36 |

English text scores about −4.7 on this scale (all four controls −4.73). K4's p 14–20 survivors are gibberish at the null level.

**Verdict (fact, for this family).** A rotated-column transposition (Cadenus row read or rotated columnar read, any per-column rotation, both directions, all orders w ≤ 8 and themed keyword orders w 9–13) combined with a periodic tableau key of period ≤ 13 (A–Z or KRYPTOS, Vigenère/Beaufort/variant, key before or after) does **not** produce K4. This also covers plain keyword columnar w 9–13 with themed keywords + periodic key (rotation 0), which the 165k bank does not contain (see audit).

**Still open.** p ≥ 14 (needs a language-model search, not a crib count); arbitrary orders w ≥ 9; Cadenus on a padded 100-letter grid (25 × 4) with 3 nulls; rotated columns + running key or autokey; Cadenus with a 25-letter alphabet merge (V/W) on the substitution side.

## Audit: the bank's frame vs textbook columnar (overdue since cycle 121)
kryptosbot reported "wrong-frame" bugs in other projects' solvers (a transposition built as σ when the encryption used σ⁻¹). Test: build textbook keyword columnar (write rows, read columns in keyword order) with the **independent** cycle-123 encryptor, look σ and σ⁻¹ up in `perms97.bin`, and run planted transposition + key controls through the cycle-41 `progkw` solver.
- KRYPTOS, BERLIN, CLOCK, SHADOW, ABSCISSA, LAYERTWO, COMPASS: **both σ and σ⁻¹ are in the bank** (adjacent indices, e.g. KRYPTOS 2811/2812). The frame is right.
- `progkw` recovers planted KRYPTOS-columnar + PALIMPSEST (KA Vigenère, model A) and KRYPTOS-columnar inverse + ABSCISSA (A–Z Beaufort, model B) exactly at index 2812 (score −4.73).
- **Caveat found.** Keyword columnar with keywords of length ≥ 9 (PALIMPSEST, NORTHEAST, LODESTONE) is **not** in the bank; the bank is "all orders w ≤ 8" plus K3 rotations, as cycles 19–29 state. A few later case files paraphrase it as "keyword columnar", which could be read too broadly. Planted PALIMPSEST-columnar + KRYPTOS key was missed by `progkw` (correctly: not in the bank) and found by the cycle-123 tool. Coverage claims that say "behind 165,065 transpositions" mean w ≤ 8 only; this cycle's rotation-0 subset closes periodic keys behind themed w 9–13 keyword columnar.
