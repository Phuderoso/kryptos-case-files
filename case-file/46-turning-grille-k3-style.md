# 46 — Turning grille 10×10, K3-style reading, tested exactly (cycle 47)

> *The grille man works with a sheet of card and a pair of scissors. Twenty-five windows, turn it a quarter, read what shows, turn again. Ninety-seven letters fit in his hundred squares with three left dark. I gave him the K3 treatment — write the message across the grid, read it through his windows — and a repeating key on either side. He never matched the 24 letters we already know.*

## Why
The coverage table listed **turning grilles and disrupted columnar** as "everything open". A turning (Fleissner) grille is the period-classic hand transposition that K3's "write in a grid, read in another order" method generalises, and 97 letters fit a 10×10 grid with 3 empty cells. **New family** for the diversity rule.

## Method (`tools/grille_exact.py`, `tools/run_cycle47.sh`)
- **Convention A (K3-like):** plaintext written row-major into the 10×10 grid, cells 97–99 empty; a grille with 25 holes (one in each of the 25 four-cell rotation orbits, 4²⁵ ≈ 1.1 × 10¹⁵ grilles) read rotation by rotation, holes in row-major order, empty cells skipped.
- **Key:** periodic Vigenère or Beaufort (variant covered by sign), A–Z or KRYPTOS numbering, applied before the transposition (key index = plaintext position) or after it (key index = ciphertext position).
- **Exact search without enumerating grilles:** a cell read in rotation r gets ciphertext index 25r − (empty cells read earlier) + (cells before it read in the same rotation). So each crib block needs only a rotation label per crib cell plus one offset per label. Both blocks are enumerated exactly with key-consistency pruning, joined, and a dynamic program over the free orbits checks that a real grille produces the implied counts. Every survivor is re-verified by encrypting through the grille.
- A first attempt as one big z3 model (`tools/grille_sat.py`) timed out on all four planted controls at 150 s and was dropped; its generator/encryptor is kept and used for the controls.

## Results (`analysis/cycle47_grille_A.txt`)
| Text | Key after transposition | Key before transposition |
|---|---|---|
| K4 | **0 grilles** for L 1–5 (all 8 settings); L = 6 timed out | **0 grilles** for L 1–4; L 5–6 timed out |
| 3 shuffled nulls (one L each, 1–3, all 8 settings) | 0 | 0 |
| planted controls | QX (Beaufort, A–Z, L 2) recovered | PALIM (Vigenère, KRYPTOS, L 5) recovered |

Power: with L ≤ 5 the 24 cribs carry about (24 − L) × 4.7 ≈ 89 bits against about 50 bits of grille freedom, so a random text should almost never fit; the nulls agree.

**Verdict.** No 10×10 turning grille read K3-style, with a periodic key of length ≤ 5 after it or ≤ 4 before it, fits K4. **Negative** in that range.

## What this does not cover
Convention B (plaintext written through the holes, grid read row-major — the classic Fleissner direction); longer keys (the Python search times out; a C port is the obvious next step); counter-clockwise turning or a different hole-reading order; other placements of the three empty cells (e.g. at the start, or the `?` as a 98th letter); grille combined with running keys.
