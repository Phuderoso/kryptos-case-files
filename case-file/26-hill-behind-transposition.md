# 26 — Hill matrices on either side of a transposition (cycle 27)

> *A matrix cipher mixes letters in blocks, so no single letter keeps its own key. Cycle 2 shut the door on a Hill cipher sitting right on the copper. Nobody had checked a Hill cipher hiding behind a grid. Cheap to check, so I checked.*

## Why this hypothesis (inference, labelled)
- **Fact:** Sanborn called the found text "scrambled plain text" (Nov 2025, [case file 03](03-k4-evidence.md)), which points to a transposition layer; cycle 2 tested Hill 2×2 and 3×3 only directly on the carved text.
- **Inference:** a Hill layer is a simple, period-free substitution that every periodic, autokey and running-key test in cycles 13–26 would miss. It is not K1–K3 style (no tableau), so this is a coverage check, not a favourite.

## Method (`tools/hill_trans.c`)
Decryption form: the plaintext block equals D × the ciphertext block (mod 26). The ciphertext is fully known, so **every one of the 24 crib letters gives one linear equation on one row of D**, including crib letters in partly known blocks. Each row's system is solved exactly mod 2 and mod 13 (Gaussian elimination; Chinese remainder theorem gives mod 26).

- Block sizes n = 2, 3, 4, 5; every block alignment.
- Letter numbering: straight A–Z and KRYPTOS-keyed (KA).
- 165,065 transpositions (cycle 19 family plus identity: all column orders w ≤ 8, K3-style single/double rotations, inverses).
- Both layer orders: Hill then transposition, and transposition then Hill.
- A configuration counts as **testable** only when every row of D gets at least n + 1 equations.

**Self-audit inside the cycle:** my first version used only blocks whose plaintext letters were all known. It returned 24 "consistent" configs for K4, all at the bare minimum of equations, and their decryptions did not even reproduce the other crib letters. That version was too weak; the decryption form above replaced it and is the one published.

## Results
| n | testable configs | consistent for K4 | consistent for 5 shuffled-K4 nulls |
|---|---|---|---|
| 2 | 1,291,262 | **0** | 0 |
| 3 | 1,851,796 | **0** | 0 |
| 4 | 1,603,448 | **0** | 0 |
| 5 | 0 (too few equations per row) | untestable | untestable |

Planted controls (invented example English plaintext carrying the two cribs at the official positions, labelled in `tools/hill_controls.py`): 6 of 7 recovered their exact transposition, layer order, numbering, n and alignment. Control 6 landed in a configuration the checker itself marks untestable (one row of D had 3 equations for 4 unknowns), so it was correctly not claimed; control 7 repeats its settings in a testable configuration and is recovered.

**Audit of cycle 2:** the identity transposition is in the family, so direct Hill is re-confirmed impossible for n = 2, 3, 4 with both numberings (cycle 2 had n = 2, 3 with A–Z only).

## Verdict
**Negative.** No Hill matrix of size 2–4 (A–Z or KRYPTOS numbering) on either side of any of 165,065 transpositions fits the 24 crib letters, where the test has power. Limits: n ≥ 5, Hill with an arbitrary mixed numbering, transpositions outside the family, and Hill combined with a periodic or carved-anomaly layer remain untested.
