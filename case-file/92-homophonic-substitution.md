# 92 — Homophonic (many-to-one) substitution, alone and behind transpositions (cycle 100)

**Family (new to this repo):** each of the 26 cipher letters stands for one plaintext letter, but several cipher letters may stand for the same one (a homophonic cipher with 26 symbols, i.e. *any* function f from cipher letters to plaintext letters, not only a permutation). A letter-wise substitution commutes with a transposition, so one model covers both layer orders: `P[i] = f(C[s(i)])`.

**Why it matters:** K4's flat letter counts (no E excess) fit a homophonic cipher well — spreading E, T, A over several symbols is the textbook way to flatten frequencies. Plain monoalphabetic and pure transposition were already out; the many-to-one middle ground had not been tested.

## Test (exact)
The 24 crib letters must never ask one cipher letter for two different plaintext letters. That check is exact and needs no key guess. Where it passes, the free values of f are hill-climbed (cribs fixed) for English quadgram score and compared with shuffled-ciphertext nulls and planted controls.

| Layer | Configurations | K4 consistent | Shuffled nulls (5) | Best K4 English score |
|---|---|---|---|---|
| Direct (no transposition) | 1 | **0** | — | — |
| Cycle 98 permutation bank (165,065 K3-style/columnar + 159,712 decimation + 9,409 affine + 6,070 routes), map and inverse | 680,513 | **0** | 0, 2, 2, 0, 0 | — |
| Every irregular columnar order, widths 2–9 | 818,224 | **0** | 0 (w 9) | — |
| Width 10 (all 10! orders, map + inverse) | 7,257,600 | 4 | 0, 5, 0, 10, 0 | −5.45 |
| Width 11 | 79,833,600 | 2 | 50, 0, 0, 0, 1,516 | −5.72 |
| Width 12 | 958,003,200 | 4 | 0, 58, 286, 112, 0 | −4.86 (w 12/13 pooled) |
| Width 13 | 12,454,041,600 | 239 | not run (cost) | (pooled above) |

Planted controls (English with the cribs, random homophonic key with 1–4 symbols per letter, behind a random permutation from the bank): **3/3** found, each true permutation among only 2 consistent configs, recovered text −4.02 to −4.05 per quadgram and readable ("…THE DOOR UNDER THE OLD BRI…"). K4's best survivor (−4.86) is gibberish (`RASSEANESIAISIRCRBSORE…`) and sits at the null level (null 3's 286 survivors reach −4.95; null 5's 1,516 reach −5.25; the maximum grows with survivor count).

## Verdict
**Excluded:** homophonic/many-to-one substitution directly and behind every columnar order w ≤ 9 and the 340k-permutation bank (exact, zero consistent). **Null-level, negative:** columnar w 10–13 survivors (counts within the shuffled range, English score at null level, controls at −4.0).
**Still open:** homophonic with *more than 26 symbols* is impossible here (K4 uses only 26 letters, so this is the general case for one alphabet); open is homophonic combined with a periodic key (polyalphabetic homophonic), and behind transposition families outside the bank (e.g. double columnar with long keys).

Code: [`tools/cycle100/`](../tools/cycle100/) (`homo.c` bank + annealing, `homocol.c` exhaustive columnar, `ctl100.py` controls).
