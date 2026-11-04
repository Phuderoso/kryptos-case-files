# 20 — Fractionation: Polybius squares and Trifid (cycle 21)

> *Every hand cipher with a grid in it leaves a fingerprint in the alphabet it can print. I counted the copper's letters before I counted anything else.*

## 1. Census rule-out (fact)
K4's 97 carved letters use **all 26 letters**. Any cipher whose output comes from a 25-cell 5×5 square (Playfair, Bifid, two-square, four-square, letter Polybius) can therefore not be K4's **last** layer, unless another substitution follows it. Playfair is also excluded on the official alignment because it never encrypts a letter to itself, and two crib letters do: position 33 (S over S) and 74 (K over K), 1-indexed. ADFGX/ADFGVX output only 5 or 6 letters, so they're out too.

## 2. Trifid with an arbitrary cube (`tools/k4_trifid_sat.py`)
Delastelle's Trifid uses 27 symbols (a 3×3×3 cube), which fits 26 letters plus one extra sign such as the carved `?`. Each ciphertext symbol is three digits of the plaintext's coordinate stream, so wherever those plaintext positions are cribbed, two cube digits must be equal. I encoded the cube as an **arbitrary** bijection (one-hot, 27×27) and solved with CaDiCaL (pysat), periods 1–97, in both orientations (carved text as Trifid encryption of the plaintext, or the reverse).

| Text | Consistent periods (enc / dec orientation) |
|---|---|
| K4 | **0 / 97** and **0 / 97** |
| 5 shuffled-K4 nulls | 0 / 97 each |
| planted controls, periods 4, 7, 11, 23 | exactly the true period, nothing else |

The test is sharp: on planted text it finds the true period and rejects all 96 others, so the 24 cribs are enough to judge Trifid.

## 3. Trifid with a transposition (`tools/k4_trifid_trans.py`)
The cycle-19 transposition family (165,064: every column order w ≤ 8, K3-style single and double rotations w 2–49, inverses) × Trifid periods 1–20 × both orientations × both layer orders (transposition after or before the Trifid). An exact union-find prefilter (two symbols forced into one cube cell, or more than 9 symbols on one digit value of an axis) passes survivors to CaDiCaL.

- **K4:** 2 prefilter survivors, **0 SAT-consistent**.
- **3 shuffled-K4 nulls:** 0, 4 and 3 prefilter survivors, 0 consistent.
- **3 planted controls** (order A period 7, order B period 5, order A period 13 with a K3-style double rotation): each recovered at the true transposition, layer order and period.

## Verdict
**Negative** for Trifid with any cube, directly (all periods) and behind or in front of the cycle-19 transpositions (periods ≤ 20); 5×5-square fractionation is ruled out as a last layer by the letter census. Still open: Trifid periods 21–97 behind transpositions, fractionation followed by a further substitution, and Bifid on a 6×6 square with a substitution after it.
