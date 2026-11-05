# Case file 95: Zodiac-340-style diagonal walks, and the width-21 signal

The Zodiac 340 cipher (solved 2020) hid its plaintext along a diagonal walk through the grid, then used homophonic substitution. Its fingerprint was an excess of repeated vertical bigrams at width 19. K4 has the same kind of excess at width 21 (Bean, HistoCrypt 2021). Cycle 103 checks the signal and tests the Zodiac construction on K4.

## 1. The width-21 signal, re-measured
Vertical bigrams (letter i, letter i + w), repeats = pairs − distinct pairs, against 20,000 shuffles of K4's own letters ([`bean.py`](../tools/cycle103/bean.py), [table](../tools/cycle103/bean.txt)):

- w = 21: **11 repeats vs 3.59 expected, p ≈ 0.00035** for that width alone. Over the 48 widths checked, the chance of some width doing this well is about 1–2%. Next best: w 10 (p 0.03), w 1 (0.045). Reproduced.
- Two of the eleven (QZ, ZT) come from three doubled letters spaced exactly 21 apart: QQ at 25, ZZ at 46, TT at 67. Under the cribs QQ is plaintext NO and TT is IN.
- kryptosbot says the five W's "explain" the effect, since deleting them removes it. Audit ([`waudit.py`](../tools/cycle103/waudit.py)): deleting **any** 5 random letters leaves ≤ 6 repeats at width 20/21 in 73% of trials, as deleting the W's does. Any deletion shifts the spacing a width statistic depends on, so this test can't single out the W's. **Not supported as stated.**
- Bean's own reading: English written at width 21 averages 9.7 repeats, so the count fits a one-to-one cipher with no transposition. Both readings stay open.

## 2. Diagonal walks + homophonic substitution
Permutation family ([`gen.py`](../tools/cycle103/gen.py)): grid width w 2–48 with R rows (R from ⌈97/w⌉ to +3, gcd(R, w) = 1). Step k visits row (k + o) mod R, column a·(k + o) mod w, with a coprime to w and every start offset o; cells past 97 are skipped. That is the Z340 walk generalised. **190,605 distinct permutations**, each also used inverted.

| Layer on top | K4 crib-consistent | Shuffled nulls | Planted controls |
|---|---|---|---|
| Homophonic, any many-to-one map (cycle 100 solver) | **0** | 0 and 1 (gibberish, −6.11) | z3 recovered at its true walk (−4.05) |
| + periodic shift key L 1–3, shift before/after the map, A–Z/KRYPTOS (cycle 101 solver) | L2 26, L3 1,001 → **annealed: best −5.09, gibberish** | 988 / 2,517 survivors, best −4.81 / −4.88, gibberish | z1, z2 recovered, readable at −4.13 / −4.04 |

**Reading.** Zodiac-style diagonal walks with homophonic substitution are **excluded** on K4 (exact zero, 3/3 controls). With a short periodic key added they are **excluded for L ≤ 3**: every survivor was read, K4's best is worse than both nulls, and both planted controls came back readable.

## Still open
- Walks with segment breaks, like Z340's separate top and bottom sections; walks starting at the W positions.
- Gromark (Bean's candidate): see earlier case files for what is covered.
