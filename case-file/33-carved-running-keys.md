# Case file 33 — Running keys the artist already carved, with and without a transposition

*Cycle 34, 2026-11-04. Status: **negative**; 5/5 planted controls recovered; K4 inside the shuffled-null range.*

## 1. Why this
Cycle 2 tried K0–K3 as running keys only straight across the carved text. Cycles 16 and 19 scored *any* English running key, but only on the plaintext side of a transposition (model A) and only by English-likeness of the 24 key letters, which says nothing about non-English keys such as the K1–K3 **ciphertext** or the KRYPTOS tableau itself. kryptosbot's public findings page (checked today) still lists "running keys combined with rearrangements" as tested only for a few source texts. The most "in plain sight" key a sculptor could use is text already on the copper: the solved passages, their ciphertext, the Morse of K0, or the tableau rows. With a named text, both layer orders become an exact test.

## 2. Model
- **Texts (12, each forward and reversed, read cyclically from every offset):** K1, K2 (as carved and with the S restored), K3 plaintexts; K1+K2+K3 plaintext; K1, K2, K3 ciphertexts and their concatenation (the letters carved right before K4); K0 Morse (same string as cycle 2); the KA tableau body read row by row; K0 + K1–K3 plaintext.
- **Substitutions (11):** Vigenère, Beaufort, variant Beaufort on the straight and the KRYPTOS alphabets; 5-bit XOR with the five letter codes of cycle 33.
- **Layer orders:** A = substitute in plaintext order, then transpose; B = transpose, then substitute in carved order.
- **Transpositions:** the 165,065 of cycle 22 (identity, every column order w ≤ 8, K3-style single and double rotations, inverses).
- A configuration survives only if all 24 crib letters match. About 1.1 × 10⁹ offset checks per text; 35 s of C (`tools/carved_rk.c`).

## 3. Results ([report](../analysis/carved_rk_report.txt))
| | Best crib matches | 24/24 |
|---|---|---|
| K4 | 11 (10 configurations) | **0** |
| 10 shuffled-K4 nulls | 10–11 | 0 |
| 5 planted controls (English + cribs, carved-text key, random transposition, both orders, Vigenère/Beaufort/variant/XOR) | 24 | **5/5**, planted configuration found each time |

The tableau control also hit equivalent offsets (reversed tableau with the mirror mode), as expected from the tableau's cyclic rows.

## 4. Verdict
No running key taken from the text already carved on Kryptos (K0–K3 plaintext or ciphertext, the tableau), in any of 11 substitutions, fits the cribs directly or with a transposition from the cycle-22 family, in either order. K4's best (11/24) is exactly the chance level of the shuffled copies. **Negative.**

## 5. Limits
Only these 12 texts (no K1 alternate 1988 plaintext, no Antipodes-only text, no physical left-to-right panel reading that crosses the tableau); key advances on every letter (no skipping at X, Q or ?); transposition family as in cycle 22; non-additive tableaux (Quagmire with two different keyed alphabets) not included.
