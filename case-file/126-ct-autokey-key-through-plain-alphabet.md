# Case file 126 — Ciphertext-fed autokey with the key letter read through the free plaintext alphabet (cycle 138)

**Status:** negative. Exact and complete for the direct cipher; behind the bank it is exact on satisfiability but ranked by a language score, so it is weaker for weakly constrained configurations (see Limits). **Type:** variant of cycle 137 (cycle 137 was the new structure). It closes the "key read through the plain alphabet" item that case file 125 left open.

## Question
In case file 125 the key letter `c_{j−L}` was read through a known alphabet (the cipher alphabet, A–Z or KRYPTOS). In a true Quagmire-style tableau the key letter can instead be looked up on the **plaintext** side, the same free alphabet `x` used for the clear letters:

- SUM: `y(c_j) = x(p_j) + x(c_{j−L})  (mod 26)`
- DIFF: `y(c_j) = x(c_{j−L}) − x(p_j)` (Beaufort; the variant form is the same test after `x → −x`)

Now `x` appears twice in every equation, so it cannot be computed outright.

## Method
Each crib gives one linear equation between two unknown values of `x`. The tool ([`tools/cycle138/ctself.c`](../tools/cycle138/ctself.c), [`ctself2.c`](../tools/cycle138/ctself2.c)) solves the whole system exactly:

1. Build a graph on letters, with one edge per crib equation. Walk each component and write every value as `x_v = s_v·r + o_v`, with one free root `r` per component.
2. Every extra edge closes a cycle and gives `coef·r = rhs (mod 26)` with `coef` 0 or ±2, which fixes the allowed roots (0, 1, 2 or 26 of them).
3. Backtrack over roots so that all assigned values are different (x must be a permutation).

If the system has a solution, the configuration is **satisfiable**: some plaintext alphabet fits all 24 cribs.

## Search
- `y` = K1/K2-style keyed alphabet from a word; both forms; lag L.
- **Direct:** all 10,056 vocabulary words, L 1–26: 2,091,648 exact tests.
- **Behind the bank** (165,065 entries, both directions, key at the carved index and at the plaintext index, model Q), L 1–16, the 239 first words of the list (the 97 themed words, A–Z, and 141 more): 5,070,796,800 tests, 286 s on 8 cores.
- Behind the bank a K4-length text satisfies the cribs by chance about once every 16,000 configurations (most systems have 0–2 cycles), so satisfiability alone does not filter. `ctself2` enumerates up to 300 solutions per satisfiable configuration and keeps the best English quadgram score of the decoded non-crib text (sum of `log10 Q + 5.5` over fully decoded 4-letter windows). Threshold 8.
- **Nulls:** two shuffled K4 texts (seeds 13801–13802) on every tenth bank entry, and in full for the direct pass.

## Results
| text | tests | satisfiable | score ≥ 8 | best score |
|---|---|---|---|---|
| K4, direct, L 1–26 | 2,091,648 | **0** | – | – |
| nulls, direct | 2,091,648 each | 0 | – | – |
| K4, behind the bank | 5,070,796,800 | 315,844 | 84 | 11.3 (gibberish) |
| null 1 (1/10 of the bank) | 507,095,040 | 25,709 | 5 | 8.4 |
| null 2 (1/10 of the bank) | 507,095,040 | 24,985 | 1 | 9.4 |

The best K4 configurations (WITHOUT, CLOCK, VIGENERE, AGAIN, TOMB, YOUR; lags 12–15) decode to fragments such as `.NOTTERSUI?L?NL.EI.` and `F.JD??JVQ??.??.?W`: no English. The cycle-count histograms of K4 and the nulls match (K4 216 configurations with ≥ 4 cycles; null 1 had 25 on one tenth of the bank).

K4 shows somewhat more satisfiable systems per test than the shuffles (6.2×10⁻⁵ against 5.0×10⁻⁵) and more score ≥ 8 hits (84 against about 30 expected from the nulls, which only had 6 hits in total). The null counts are small and every K4 hit reads as noise, so I log this and do not read anything into it.

## Controls
Independently encrypted in Python with a **random** plaintext alphabet ([`plant.py`](../tools/cycle138/plant.py)): 5/5 recovered.

- ctl1 carved, y = PALIMPSEST, SUM, L 7, bank entry 4242: rank 1 in its bank run (score 46.7, next 9.2), reads `…DTHEOLDTOWERANDTBERLINCLOCKSTR?C?THEHOURINSILENC…`.
- ctl2 carved, y = KRYPTOS, Beaufort, L 12, inverse of entry 99999: rank 1 (score 11.0, next 8.4).
- ctl3 model Q, y = BERLIN, variant, L 5, entry 160000: rank 1 (score 12.3).
- ctl4 direct, y = CLOCK, SUM, L 20, and ctl5 direct, y = A–Z, Beaufort, L 5: found exactly, readable partials.

Bank controls ran over the first 7 words against the full bank; the true configuration was the top scorer in each.

## Limits
- ctl2 and ctl3 scored only 11–12 because few cribs constrain `x` when the system has 0 cycles, so only part of the text decodes. A real K4 solution of that weak kind could score about as high as the best K4 noise (11.3). Behind the bank the negative is therefore firm for well-constrained configurations (cycles ≥ 3, long decoded text) and only probable for loosely constrained ones.
- Only 239 of the 10,056 words were run behind the bank (budget); the direct pass covered all of them.
- Lags 17–26 behind the bank are not covered.

## What this closes
CT-fed autokey in which both the clear letter and the key letter are read through the same unknown plaintext alphabet, with a keyed cipher alphabet from the vocabulary: excluded **direct** for every plaintext alphabet and L 1–26 (exact). Behind the 330,130 bank permutations, L 1–16, the 239 leading words, both index orders: no readable candidate, with the scoring limit above.
