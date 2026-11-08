# Case file 118 — The periodic Gromark without its name (cycle 130)

**Type:** variant of cycle 129 (case file 117), and the idea logged there: the ACA Periodic Gromark when the keyword is in no list.

## The relaxation
Cycle 129 needed the keyword. Here nothing about it is assumed except its length L:
- **Cipher alphabet:** any of the 26! orderings.
- **Group offsets:** L free values (in the ACA rule they are fixed by the keyword).
- **Primer:** any L digits, or, for the longer keywords, any keyword-rank primer (a permutation of 1..L with 10 as 0, which is what the ACA rule produces).

Every real Periodic Gromark is inside this set, so an empty result rules out every keyword of that length at once.

Each crib letter gives the equation `v(cipher letter) − offset(group) = plain value ± digit`. The test is exact: a weighted union-find finds contradictions, and cipher letters in one connected piece must take distinct values.

## Coverage
- **Every digit primer:** L 2–9 for K4 and nulls 1–2; L 2–8 for nulls 3–6.
- **Keyword-rank primers:** L 8–12 for K4 and nulls 1–2. For nulls 3–6, L 8–11.
- **Settings:** plaintext alphabet A–Z or KRYPTOS; Vigenère, Beaufort or variant form. Beaufort and variant are the same thing once the alphabet is arbitrary.
- **Size:** about 1.6 × 10⁹ primer settings for K4.

## Result
| text | distinct cipher letters under the cribs | feasible primers |
|---|---|---|
| **K4** | 14 | **0 at every L and setting** |
| null 1 | 15 | 0 |
| null 2 | 19 | many (L 5: 9; L 8: 7,129; L 9: 7,136; L 12: 180, …) |
| null 3 | 15 | 38 at L 8 (all digits), else 0 |
| null 4 | 15 | 0 |
| null 5 | 13 | 0 |
| null 6 | 17 | 0 |
| planted controls | — | 5/5 recovered (L 6, 6, 7, 10, 11; each found at its own primer, setting and alphabet; at most one extra hit) |

The test is strict: most shuffles also give 0, and a text whose crib letters repeat little (null 2) leaves enough freedom to pass. K4's crib letters repeat a lot, so 0 is the expected outcome for a wrong family and impossible for the right one. **Negative: K4 is not a direct Periodic Gromark with any keyword of 2–12 letters (any digits up to 9) and either plaintext alphabet.**

## What stays open
- The periodic Gromark behind a transposition (only checked in cycle 129, with listed keywords).
- Keyword-rank primers longer than 12, and other number bases.
