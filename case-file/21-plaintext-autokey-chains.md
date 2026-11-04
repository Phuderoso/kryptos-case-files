# 21 — Plaintext autokey behind a transposition, done properly (cycle 22)
> *Cycle 19 said the plaintext-fed autokey was half blind past lag 9. It was wrong about why. The message that keys itself also chains itself, and a chain can be followed.*

## 1. Audit of cycle 19
Cycle 19 checked a plaintext-autokey crib letter only when the letter **L places earlier** was also a crib letter, so it called lags ≥ 10 untestable. That undersold the algebra. With a fixed tableau, `P[i] = dec(C[i], P[i−L])`, so one known letter fixes its **whole residue chain** mod L in both directions (the primer only matters before position L). Any two crib letters on the same chain give an exact check, however far apart. Cycle 19 also never tried plaintext autokey with the transposition first (Model B).

## 2. Test (`tools/ptak_chain.c`, `tools/export_perms.py`)
- **Transpositions:** cycle 19's 165,064 (all column orders w 2–8, K3-style single and double rotations, inverses) plus the identity: 165,065.
- **Models:** A = autokey then transpose; B = transpose then autokey (cribs scattered by the grid).
- **Keys:** plaintext-fed autokey, every lag 1–96, any primer; KRYPTOS-keyed and straight tableaux; Vigenère, Beaufort, variant Beaufort.
- 190,154,880 exact chain tests, 15 s in C. A hit needs every check to match and at least 6 checks (false-positive rate about 26⁻⁶ per test).
- **Coverage, Model A:** checks per lag = 24 − (residue classes the cribs occupy). Lags 1–23 and 35–47 give ≥ 6 checks; 24–34 and 48–96 are blind (0–5). In Model B coverage depends on the grid. See `analysis/ptak_chain_coverage_modelA.txt`.

## 3. Controls (`analysis/ptak_chain_controls.txt`)
English plaintext with both cribs, random grid from the family, tableau and mode, planted at lags 3, 12, 20, 30, 45 and 52, alternating models: **5 of 6 recovered** with their exact grid and lag (8–21 checks). The lag-52 Model A plant was missed, as the coverage table predicts (1 check). Five shuffled-K4 nulls: 0 hits; their most-checked fully consistent configurations reach 4 or 5 checks.

## 4. Results (`analysis/ptak_chain_report.txt`)
| Text | Hits (≥ 6 checks) | Most checks among fully consistent |
|---|---|---|
| K4 | **0** | 4 (11 configs) |
| shuffled K4 ×5 | 0 | 4–5 |

## 5. Verdict
| Hypothesis | Status |
|---|---|
| Plaintext autokey (any primer), lag 1–23 or 35–47, autokey then columnar w ≤ 8 / K3-style rotation | **negative** |
| Same with the transposition first (Model B), wherever the grid gives ≥ 6 checks | **negative** |
| Plaintext autokey applied directly to the carved text, same lags | **negative** |
| Lags 24–34 and 48–96 (Model A) | **blind to algebra**; needs English scoring of the chains |
| Arbitrary mixed alphabets with plaintext autokey | open (SAT candidate) |

Honest limits: 97-letter grids only (the `?` variant was not rerun); fixed tableaux only.
