# 103 — Kryha behind the transposition bank (cycle 115)

**Question.** Cycle 114 tested the Kryha cipher machine directly ([case file 102](102-kryha-machine.md)). K3 used a
transposition, so the K1–K3 recipe suggests a second layer. Does a Kryha layer with K1–K3-style keyword alphabets
survive behind any of the 165,065 transpositions of the bank used since cycle 23 (keyword columnar, K3-style grid
routes, decimations, and inverses)?

**Model.** The machine model, published wheels and 2,356 alphabet pairs are from cycle 114 (`tools/cycle114/kryha114.py`,
`testB114.py`). Cribs are EASTNORTHEAST at 21–33 and BERLINCLOCK at 63–73 (0-based), 24 letters, both senses σ = ±1.
- **A: Kryha first, then the transposition.** The intermediate text X[j] = carved[t[j]] is Kryha text in plaintext
  order. With **any** V1 code wheel of n = 1–48 sectors (steps 5–13 by the +4 rule) the test is exact: the 22
  adjacent crib differences must be legal steps, agree per wheel slot, and the 30-letter gap must be reachable
  (same residue logic as cycle 114's B1).
- **B: transposition first, then Kryha.** The Kryha machine runs over the carved order, so crib j sits at carved
  position t[j], scattered. Exact for the **five published wheels** (15, 17, 18, 19, 23 sectors), any start sector.
  With any wheel the cribs are underdetermined: a gap filter still left about 6,400 (n, setting) hits per
  transposition on K4. That case is not claimed.

**Results** (`tools/cycle115/`, raw output `data/cycle115/run115.txt`).

| text | A: any wheel, keyword pairs | B: published wheels, keyword pairs |
|---|---|---|
| **K4** | **0** of 165,065 × 4,712 × 48 | **0** of 165,065 × 4,712 × 92 |
| 3 shuffled nulls | 0, 0, 0 | 0, 0, 0 |
| planted A controls (n = 5, 17) | 12 hits each, true transposition and pair among them (2/2) | 0 |
| planted B controls (wheel 15) | 0 | 2 and 1 hits, true setting among them (2/2) |

The nulls also give zero, so this is an exclusion with power (planted messages are always found), not a ranking.
Controls in model A hit several wheel sizes because the planted wheel's multiples fit too (n = 5 also fits 10, 15, …).

**Conclusion.** Negative. K1–K3-style keyword Kryha (any V1 wheel) under any bank transposition is excluded. So is a
published-wheel Kryha applied after any bank transposition.

**Still open.** Model B with an arbitrary wheel (needs a language score or SAT per transposition; too wide for the cribs).
Free alphabets behind transpositions. V2 universal disk behind transpositions (cycle 114's C checker is too slow for
7.8 × 10⁸ inputs; a faster prefilter is needed). Transpositions outside the bank.
