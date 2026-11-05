# 93 — Polyalphabetic homophonic: periodic key + many-to-one map (cycle 101)

Extends [case file 92](92-homophonic-substitution.md). A repeating shift key (period L) is combined with an **arbitrary** map f from the 26 cipher letters to plaintext letters (several cipher letters may share one plaintext letter).

- Model A (shift, then map): `P[i] = f(C[s(i)] − k[q mod L])`
- Model B (map, then shift): `P[i] = f(C[s(i)]) + k[q mod L]`
- q = plaintext position or carved position; A–Z or KRYPTOS index order. Beaufort and variant forms, and one common shift of the key, are absorbed by f, so k[0] = 0 without loss. Exact test: no cipher value may be asked for two different plaintext letters at the 24 crib positions.

## Results
| Layer | Range | K4 consistent | Shuffled nulls | Planted controls |
|---|---|---|---|---|
| Direct | L 1–7, all keys (3.2 × 10⁸ keys × 2 alphabets × 2 forms) | **0 at every L** | 5 nulls: 0 at L ≤ 4; at L 5–7 two nulls 0–609 survivors, three 0 | 3/3 true keys recovered (L 5, 7, 7) |
| Behind 340,256 bank permutations (map + inverse) | L 1–3 | L1 0; L2 44; L3 1,372 | null 1: L2 34, L3 1,608; null 2: L1 16, L2 44, L3 3,742 | 2/2 recovered (L 3, behind a K3-style and a decimation permutation) |

**Reading.** Direct: an exact zero, so the family is **excluded for L ≤ 7** on the carved text (the true key always passes, as the 3 controls show). The zero is not by itself a signal: three of five shuffled texts are also zero, and the test loses power from L 5 up (controls show 1–849 false survivors there).
Behind the bank: K4's survivor counts sit inside the null range, so the crib test cannot judge them. The survivors need a whole-text English check (anneal f with the key fixed); that is **pending**, and is checkpointed for the next cycle (the output cap printed only 200 survivors per file).

Code: [`tools/cycle101/`](../tools/cycle101/).
