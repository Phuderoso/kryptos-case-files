# 108 — Quagmire I/II/III with one wrong crib letter (cycle 120)

**Question.** Cycles 13 and 28 ruled out Quagmire I/II/III (themed alphabets, periodic key p ≤ 16, Vigenère/Beaufort, both layer orders) behind the 165,065-permutation bank when all 24 crib letters are trusted. If exactly one crib letter is wrong — a carving slip under a crib, or a wrong assumed plaintext letter — does any configuration survive that the strict test rejected?

**Code.** [`tools/cycle120/q1crib120.c`](../tools/cycle120/q1crib120.c), driver [`run120.py`](../tools/cycle120/run120.py). Same search space as `tools/c/periodic_perm.c` (cycle 13): QI / QII / QIII × Vig / Beau × PT-index / carved-index × period 1..16 × first M themed alphabets (alphabet 0 = A–Z). For each config, `TOTAL_STRICT` counts agreement of all 24 crib key letters within each residue class; `TOTAL_SOFT` allows exactly one crib to be dropped; `TOTAL_SOFT_ONLY` is soft ∧ ¬strict — the configs that would newly survive under one wrong crib. Soft analysis is O(cribs) per config (conflict residues must share a single singleton drop), not 24 full retries. Outputs in [`data/cycle120/`](../data/cycle120/).

**Scope.** (1) identity × M = 264; (2) full bank × M = 2 (A–Z, KRYPTOS); (3) full bank × M = 264 (main). Five shuffled-ciphertext nulls at each scope. About 2.3 minutes wall per full-bank × 264 sweep on 8 cores; ~15 minutes for K4 + 5 nulls at the main scope.

**Controls.** Clean planted Quagmire III (Vigenère p = 5 key `KRYPT` on the KRYPTOS alphabet; Beaufort p = 4 on A–Z), identity and behind bank permutation 1000: recover with `TOTAL_STRICT > 0` and `TOTAL_SOFT_ONLY = 0`. The same QIII plant with crib index 3 flipped in the ciphertext: `TOTAL_STRICT = 0`, `TOTAL_SOFT_ONLY = 1`, drop = 3, recovered key `KRYPT`. So the leave-one-out score finds a real one-error machine when one is there, and does not invent soft survivors for a clean plant.

## Results

| Text | scope | strict | soft | soft_only |
|---|---|---|---|---|
| K4 | identity M=264 | 0 | 0 | 0 |
| K4 | bank M=2 | 0 | 0 | 0 |
| K4 | bank M=264 | **0** | **0** | **0** |
| null 0..4 | bank M=264 | 0,0,0,0,0 | 0,0,0,1,0 | 0,0,0,1,0 (the one at p = 16) |
| null 0..4 | bank M=2 / identity M=264 | all 0 | all 0 | all 0 |
| planted clean / flip | single true perm | as above | as above | as above |

Every period histogram for K4 at the main scope is zero for strict, soft, and soft_only.

## Verdict

- **Quagmire I/II/III behind the bank, themed alphabets, p ≤ 16, remains excluded under one wrong crib letter.** K4 has zero soft_only survivors; cycle 13's exclusion does not soften.
- One of five nulls produced a single soft_only hit at period 16 — chance-level noise that K4 did not match.
- Direct (identity) and the A–Z/KRYPTOS bank slice are likewise zero under leave-one-out.

**Negative. Does not soften cycle 13 / the Quagmire coverage-table row.** Contrast with cycle 119, where the stepping-disk |S| ≤ 5 claim behind the bank *did* soften under the same one-crib audit.
