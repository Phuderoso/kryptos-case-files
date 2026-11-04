# 16 — K3's grid over K3 and K4 together (cycle 17)
> *Two safes, one combination? K3's dial turned once more over both doors. Only K3's door stayed shut.*

## 1. Why this
Open lead since cycle 14: maybe Sanborn ran K3's transposition (write in rows, rotate the grid, regrid, rotate again) over the carved K3+K4 block as one text, so K4 is K3's method continued. The numbers invite it: K3's 336 letters + the carved `?` + K4's 97 = **434 = 14 × 31**, a clean rectangle, and the left panel's rows are about 31 letters wide. Cycle 12 already tested K3-style rotations on K4 alone; this is the joint version.

## 2. Test (`tools/k3k4_grid.py`)
- **Texts:** K3+?+K4 (434), K3+K4 (433), K4+?+K3 (434).
- **Permutations:** single and double rotations, clockwise or anticlockwise each, grid widths 2–62 and 217 (ragged last row allowed), plus the inverse of each: **31,000 per text**. K3's own recipe (widths 24 then 8, clockwise) is in the family.
- **Scores:** (1) how many 8-letter pieces of K3's known plaintext come back; (2) the longest piece of EASTNORTHEAST or BERLINCLOCK anywhere; (3) English quadgrams; (4) one more layer, Quagmire III on the KRYPTOS tableau (Vigenère, Beaufort, variant) with 90 keys (the 89 plain-sight words of cycle 7 plus PALIMPSEST, ABSCISSA, LAYERTWO, IDBYROWS, etc.), searched for EASTNORTHEAST, NORTHEAST or BERLINCLOCK **anywhere** (positions shift when K3 is in front).

## 3. Controls ([k3k4_grid_control.txt](../analysis/k3k4_grid_control.txt))
- K3 alone (336): the family reproduces K3's plaintext exactly. **PASS.**
- Planted: a 434-letter English text with both cribs, Vigenère-keyed on the KRYPTOS tableau and transposed by a random family member; recovered in 3 of 3, and the blind scan of all 31,000 permutations × 90 keys × 3 modes returned exactly one EASTNORTHEAST hit, the correct one. **PASS.**

## 4. Results ([k3k4_grid_report.txt](../analysis/k3k4_grid_report.txt), [k3k4_grid_nulls.txt](../analysis/k3k4_grid_nulls.txt))
| Measure | K3+?+K4 | K3+K4 | K4+?+K3 | 8 nulls (K3+?+shuffled K4) |
|---|---|---|---|---|
| K3 plaintext 8-grams recovered (of 329) | ≤ 1 | ≤ 1 | 0 | — |
| Longest crib piece, pure transposition | 6 | 6 | 6 | 6–7 |
| Best quadgram per letter | −6.48 | −6.43 | −6.46 | −6.36 to −6.51 |
| NORTHEAST / BERLINCLOCK / EASTNORTHEAST after the keyword layer | 0 | 0 | 0 | 0 |
| BERLIN alone after the keyword layer | 14 | 6 | 4 | 3–13 |

## 5. Verdict
| Hypothesis | Status |
|---|---|
| One K3-style rotation grid (widths 2–62, 217) over K3 and K4 together | **negative, structurally**: no member keeps K3's solved plaintext together, so it would break the K3 solution everyone verified |
| Same, plus one KRYPTOS-tableau keyword layer | **negative** (0 crib hits; BERLIN-only hits at the null rate) |
| K4 as a continuation of K3's grid with K4 encrypted separately | already covered on K4 alone by cycles 5, 7 and 12 |

The 14 × 31 coincidence is just that: 434 factors that way, but the grid doesn't use it. K3 is sealed on its own; K4's lock is separate.
