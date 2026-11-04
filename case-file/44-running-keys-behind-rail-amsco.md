# 44 — Running keys behind rail fence, Redefence and AMSCO (cycle 45)

> *Last cycle the zigzag men only faced a keyword. This time I made them stand next to the books: Carter's diary, the Gospel on the lobby wall, the words already cut into the copper. Every page, every line-up. Not one of them had the twenty-four letters on him.*

## Why
Cycle 44's case file named this as the cheap next step, and kryptosbot's findings page (still dated Sept 29, 2026) lists "running keys combined with rearrangements" as tested only for a limited set of source texts. Our earlier running-key cycles (34–36) used the 165k columnar/route/K3-rotation family only; cycle 44's 1.87M rail fence, Redefence and AMSCO permutations had never met a running key. This is a variant cycle (cycles 43 and 44 satisfied the diversity rule with new families).

## Method (`tools/run_cycle45.sh`, `tools/bookrk.c` unchanged from cycle 35, `tools/rk_railamsco_controls.py`)
- **Transpositions:** cycle 44's files, 1,873,954 permutations incl. identity (rail fence rails 2–48, Redefence 3–7 rails in any rail order, AMSCO widths 2–9 in any column order, both start sizes and row conventions; each with its inverse).
- **Key texts (28, 730,978 letters):** cycle 34's carved texts (K1–K3 plaintexts and ciphertexts, K0 Morse, KA tableau rows, combinations; forward and reversed), Carter & Mace, *The Tomb of Tut·ankh·Amen* vol. I (K3's source, cycle 35 OCR) forward and reversed, KJV Gospel of John (the lobby motto's source) forward and reversed.
- **Substitutions (29):** 24 additive tableaux (Vigenère/Beaufort/variant × A–Z/KRYPTOS plain, cipher and key numbering, which covers Quagmire I–III on KRYPTOS) plus 5 five-bit XOR codes; both layer orders (key indexed by plaintext position, or by carved position).
- **Test:** exact. For each (permutation, layer order, substitution, text) the 24 crib constraints are ANDed as shifted bitsets over every key offset; "depth" = how many constraints some single offset satisfies together. 2.53 × 10⁹ configurations, ≈ 7.9 × 10¹³ key placements for K4.
- **Nulls:** 3 shuffled K4s on two of the eight chunks (chunk 0: rail, Redefence, AMSCO w 2–4; chunk 5: AMSCO w 9), about a quarter of the family each.
- **Controls:** 3 planted English texts with the cribs at the official positions, encrypted under a running key from these texts behind a Redefence (7 rails) and two AMSCO w 9 permutations, mixed tableaux and both layer orders; each run on a 20,000-permutation slice around the planted one.

## Results (`analysis/cycle45_rk_railamsco_summary.txt`)
| Text | Permutations | Full fits (24/24) | Best depth |
|---|---|---|---|
| K4 | all 1,873,954 | **0** | 9 (6 configs, all KJV John reversed) |
| 3 shuffled nulls | 468,490 each | 0 | 8–10 |
| 3 planted controls | 20,000-perm slice each | 3/3 recovered at the planted permutation, text, mode and offset | 24 |

Control notes: control 2 also fits K1–K3 combined texts at the matching offset (they contain K3's plaintext, so that is the same key); control 3 also fits three AMSCO column orders that differ from the planted one only in columns no crib touches (the same limit cycle 44 reported).

**Verdict.** No running key from the carved texts, Carter vol. I or the Gospel of John, under any of 29 substitutions, in front of or behind any rail fence, Redefence (≤ 7 rails) or AMSCO (w 2–9) permutation, fits the 24 crib letters. K4's best (9) sits inside the null range (8–10). **Negative.**

## What this does not cover
The bigger plain-sight texts (KJV New Testament, National Security Act 1947, Reagan's Berlin speech, Elliot Smith 1923), about 2.4M letters, would take roughly four cycles behind this family; given cycles 34–36 already found them silent behind the columnar family, they are low priority. Redefence 8+ rails, AMSCO w ≥ 10, non-additive running-key systems, and non-English key texts remain open.
