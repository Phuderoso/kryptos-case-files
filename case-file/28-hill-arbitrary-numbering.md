# 28 — Hill 2×2 with an arbitrary letter numbering (cycle 29)

> *The Hill man always numbers his letters A = 0 to Z = 25. Cycle 27 took him at his word. This time I let him number them any way he liked, all 26! ways at once, and asked the solver whether any of them would talk.*

## 1. Why this test
- [Case file 26](26-hill-behind-transposition.md) (cycle 27) ruled out Hill n = 2–4 on the A–Z and KRYPTOS numberings, directly and behind a transposition. A numbering is a hidden alphabet, exactly like the KRYPTOS-keyed alphabet of K1–K2, so the natural K1–K3-style variant is Hill on a **secret mixed alphabet**. That was listed as next idea (2) in cycle 28's journal.
- First guess (written down before running): with 11 crib blocks (22 equations mod 26) and about 20 unknown letter values plus 4 matrix entries, the system looked close to underdetermined, so many solutions were expected. That guess was wrong (see results).

## 2. Method (`tools/hill_mixed_sat.py`)
- Unknowns: a bijection σ: A–Z → Z₂₆ (one-hot, a full permutation) and the 2×2 decryption matrix M (any entries, singular ones included, so nothing is excluded in advance).
- Constraints: for each block (i, i+1) lying fully inside EASTNORTHEAST (21–33) or BERLINCLOCK (63–73), 0-indexed, σ(P) = M·σ(C) mod 26. Products are encoded with one-hot helper variables (exact, no approximation).
- Both block alignments (blocks starting at even or odd positions): 11 blocks each.
- Solver: CaDiCaL 1.5.3 via python-sat; all solutions enumerated (projected on M and σ of the crib letters) with blocking clauses. Unit scaling σ → u·σ maps solutions to solutions, so real solutions come in groups of 12.

## 3. Results ([report](../analysis/hill_mixed_report.txt))
| Text | alignment 0 | alignment 1 |
|---|---|---|
| **K4** | **0 solutions (UNSAT)** | **0 solutions (UNSAT)** |
| Shuffled null 1 | 0 | 0 |
| Shuffled null 3 | 0 | 0 |
| Control 1 (planted Hill, random σ, M = [7 24; 14 15], alignment 0) | 2 classes, one is the planted M and σ (up to scaling) | 0 |
| Control 2 (planted, M = [11 16; 21 17], alignment 1) | 0 | 1 class, exactly the planted M and σ |

Shuffled null 2 did not finish (alignment 0 unresolved after about 30 minutes; stopped and recorded as no result).

## 4. Verdict
| Hypothesis | Status |
|---|---|
| Hill 2×2 directly on the copper, **any** letter numbering, any matrix, either block alignment | **impossible** (proved UNSAT) |
| Hill 2×2 with arbitrary numbering behind a transposition | open (one SAT call per transposition; too slow for 165k here) |
| Hill n ≥ 3 with arbitrary numbering | open |

## 5. Honest limits
- Plaintext and ciphertext share one numbering (as in standard Hill). Two different numberings, one per side, were not tested; that model is looser.
- Only the 24 published crib letters are used; no assumption about the rest of the plaintext.
- The nulls are also UNSAT, so this is a structural exclusion, not a K4-specific signal: Hill 2×2 just doesn't fit 22 random-looking crib equations, while it always fits a genuine Hill text (2/2 controls).

## Reproduce
```
pip install --break-system-packages python-sat
python3 tools/make_hill_controls.py      # writes hctl_*.txt and hnull_*.txt
python3 tools/hill_mixed_sat.py K4       # about 4 minutes on one core
python3 tools/hill_mixed_sat.py hctl_1.txt
```
