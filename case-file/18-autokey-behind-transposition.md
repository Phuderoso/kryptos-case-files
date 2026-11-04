# 18 — Autokey behind a transposition (cycle 19)
> *A repeating key leaves fingerprints. An autokey wipes them with the message itself. So I asked whether somebody had wiped them behind a shuffled grid.*

## 1. Why this
Open lead from cycles 11b and 18: SAT ruled out ciphertext-autokey (lag ≤ 35) applied **directly** to the carved text, and cycle 18 ruled out **periodic** keys behind 98-symbol grids. Autokey **behind a transposition** was only sampled by annealing in cycle 5 (double columnar 5–9, lag 1–7). An autokey is the simplest non-repeating key a sculptor could run by hand, and it would explain why every periodic test fails.

## 2. Test (`tools/k4_autokey_trans.py`)
Exact algebra, no guessing of keywords and no scoring by English: for each transposition and lag L, the autokey relation either reproduces all 24 known plaintext letters or it doesn't.
- **Transpositions (165,064 for 97 letters; 162,966 for 98 with the `?`):** all column orders for widths 2–8; K3-style single rotations (widths 2–49, columns read up or down, left or right); all pairs of those (double rotations, as in K3); plus every inverse.
- **Keys:** ciphertext-fed autokey (lag 1–21) and plaintext-fed autokey (lag 1–21; only lags ≤ 9 are actually checkable, see limits).
- **Tableaux:** KRYPTOS-keyed and straight alphabets; Vigenère, Beaufort, variant Beaufort.
- **Orders:** Model A, autokey then transpose (97 letters, and 98 with the `?` landing at either end); Model B, transpose then ciphertext-autokey (97).
- **Hit rule:** every checkable crib letter matches, with ≥ 12 checks (ciphertext-fed) or ≥ 6 (plaintext-fed).

## 3. Controls (`analysis/autokey_trans_control.txt`)
English plaintext with both cribs, random transposition, tableau, mode and lag, encrypted and fed back in: 3 of 3 ciphertext-autokey plants (Model A lag 12, Model B lags 4 and 20) and 1 plaintext-autokey plant (lag 8) recovered with their exact transposition (the lag-20 plant also matched one neighbouring column order, 18 of 18 checkable letters, a known side effect of the early crib letters falling in the primer). A second plaintext-autokey plant at lag 12 was **not** recoverable: only 1 crib letter is checkable at that lag, so the test is blind there (see limits). **PASS within stated coverage.**

## 4. Results (`analysis/autokey_trans_report.txt`, `analysis/autokey_trans_nulls.txt`)
| Text | Full-consistency hits | Best partial (CT-fed, of 24) |
|---|---|---|
| K4 | **0** | 9 |
| shuffled K4 (3 seeds) | 0, 0, 0 | 9, 8, 9 |

K4's best partial matches equal shuffled-copper nulls in every model.

## 5. Verdict
| Hypothesis | Status |
|---|---|
| Ciphertext-autokey (lag 1–21, KA/AZ, three modes) before or after columnar w ≤ 8 or K3-style single/double rotations | **negative** |
| Same with the `?` as a 98th symbol (autokey first) | **negative** |
| Plaintext-autokey, lag ≤ 9, behind the same transpositions (autokey first) | **negative** |
| Plaintext-autokey lag ≥ 10, or with transposition first | **not tested** (too few crib pairs for exact algebra; needs English scoring) |
| Autokey with an arbitrary mixed alphabet behind a transposition | open |

Honest limits: the plaintext-fed test only sees crib letters whose key letter is also a crib letter, so it is weak by design. Overlap with cycle 5 (annealing, narrower) is small; this cycle is exhaustive and exact on its families.
