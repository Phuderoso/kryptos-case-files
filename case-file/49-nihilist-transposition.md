# Case file 49 — Nihilist transposition (cycle 50)

**Family (new to the repo):** the Nihilist transposition. The plaintext is written row by row into a 10 × 10 square
(97 letters, 3 empty cells), then the rows *and* the columns are reordered by the same permutation σ (in practice the
alphabetical order of one keyword), and the square is read off. It is a square-grid cousin of K3's grid trick and it
needs one keyword, which fits the K1–K3 style profile (case file 10).

**Model.** σ runs over all 10! = 3,628,800 orders (so every keyword of up to 10 letters, and every shorter keyword with
any completion, is covered). Layouts: empty cells at the end or at the start. Reading: row-major or column-major.
Both the map and its inverse. On either side of a periodic or progressive keyword key
(key<sub>i</sub> = k[i mod L] + s·⌊i/L⌋, s 0–25), Vigenère or Beaufort, A–Z or KRYPTOS tableau, L 1–22. Exact test
against the 24 official crib letters (EASTNORTHEAST at 22–34, BERLINCLOCK at 64–74, 1-based), the same checker as
cycles 41, 44 and 46. Tool: [`tools/nihilist.c`](../tools/nihilist.c), run script
[`tools/run_cycle50.sh`](../tools/run_cycle50.sh).

**Coverage this cycle:** σ[0] = 0–7, i.e. 2,903,040 of 3,628,800 orders (80 %), 1.06 × 10¹¹ exact tests.
**Checkpoint:** σ[0] = 8 and 9 are still to run.

## Results
| Text | Sigmas | Consistent, L ≤ 18 | L = 19 | L = 20 | L = 21 | L = 22 |
|---|---|---|---|---|---|---|
| K4 | 2,903,040 (σ[0] 0–7) | **0** | 1 | 826 | 92 | 768 |
| K4 | first 60,001 (σ[0] = 0) | 0 | 0 | 5 | 8 | 33 |
| Shuffled K4, null 0 | first 60,001 | 0 | 0 | 4 | 4 | 39 |
| Shuffled K4, null 1 | first 60,001 | 0 | 0 | 14 | 11 | 48 |
| Shuffled K4, null 2 | first 60,001 | 0 | 0 | 24 | 5 | 38 |

At L ≥ 20 the key has nearly as many unknowns as there are cribs, so consistent configurations are expected noise; K4 sits
inside the null range on the matched slice. The single L = 19 configuration (σ[0] = 7) was only counted, not printed; it
will be printed and scored for English next cycle (`PRINTL=19`). One hit among 2.9 M orders at L = 19 is what noise
should produce, so it is not a lead until it reads as English.

**Planted controls (3/3 recovered, exact σ, layout, reading, direction, key):** CTL1 σ = 0123459876, column-major
reading, Vigenère A–Z, CLOCK; CTL2 σ = 0123465789, empty cells first, KRYPTOS Beaufort, progressive SHADOW s = 3, key
after the transposition; CTL3 σ = 0123546798, inverse map, KRYPTOS Vigenère, PALIMPSEST. Each recovered plaintext
scores −4.09 per quadgram; data in [`data/cycle50/`](../data/cycle50/).

## Verdict
**Negative for L ≤ 18 on 80 % of all orders**; L 19–22 at noise level; σ[0] = 8, 9 pending. Not a solution; no claim.

## Not covered
Rectangular Nihilist variants (different row and column keys), 98-cell or 11 × 9 grids, running keys on top, and
substitution with mixed (non-tableau) alphabets.
