# Case file 32 — Vernam: the teleprinter XOR, with and without a transposition

*Cycle 33, 2026-11-04. Status: **negative** for periodic keys of length 1–26; **no signal** for English running keys; controls recovered.*

## 1. Why this
Nothing in this file had tested a bit-level layer. Berlin in the Cold War was teleprinter country (the 1955 Berlin tunnel tapped teleprinter lines), and the classic teleprinter cipher is Vernam's: write each letter as a 5-bit code and XOR it with a key tape. It is "code inside code", the layered-simple-thing hunch in its purest form, and it is reciprocal like Porta. A hand-made version only needs a code table and a key word.

## 2. Model
- Letter codes (5 encodings): ITA2/Baudot-Murray letter shift; A=0…25 and A=1…26 in binary; position in the KRYPTOS alphabet 0…25 and 1…26. (Bit order does not matter: reversing bits commutes with XOR.)
- Layer orders: (A) XOR in plaintext order, then a transposition; (B) a transposition, then XOR in carved order.
- Transpositions: the 165,065 of cycle 22 (identity, all column orders w ≤ 8, K3-style rotations, inverses).
- Keys: periodic, any 5-bit value per residue, L = 1–26; a configuration counts only if the 24 crib letters agree *and* every decryptable position gives a letter code (K4 has no control characters). English running key: when all 24 derived key codes are letters (model A), the two fragments under the cribs are scored by quadgrams.
- Exact, key-free algebra: each crib letter fixes its key code, so consistency is a direct check.

## 3. Results ([report](../analysis/vernam_report.txt))
| Test | K4 | Shuffled-K4 nulls (10) | Planted controls |
|---|---|---|---|
| Periodic L ≤ 20, consistent | 0 | 0 | 3/3 recovered, full English plaintext |
| Periodic L 21–26, consistent and all-letter | 0 | 2 nulls with one L = 26 hit each (chance) | — |
| Running key, best fragment score | −5.87 | −5.63 to −6.37 | −3.68 and −3.81, ranked first |

1.65 × 10⁶ configurations per text (165,065 × 5 × 2) × 26 periods; one second of C.

## 4. Verdict
A Vernam/XOR layer with any of these five letter codes, directly or behind the cycle-22 transposition family, is **excluded for key lengths 1–26**, and English running keys score inside the shuffled-null range. **Negative.**

## 5. Limits
Only these five code tables (no original 1888 Baudot, no figure-shift codes, no 6- or 8-bit ASCII); key tape non-English and non-periodic (a true one-time pad) is untestable by design; running key only in model A; transposition family as in cycle 22. Tools: `tools/vernam.c`, `tools/vernam_controls.py`, `tools/vernam_score_rk.py` (needs `perms97.bin` from `tools/export_perms.py`).
