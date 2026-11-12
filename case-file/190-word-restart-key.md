# 190 — Word-restart key: the key word starts over at every plaintext word (cycle 203)

> *A clerk who restarts his key at every word leaves no period to measure. Case 25 walked the X-restart past K4 in cycle 26 and left word boundaries on the "untested" list. Tonight that door got opened and checked.*

**IDEAS:** I-256 (via I-257). **Pre-registration:** [`tools/cycle203/PREREG203.md`](../tools/cycle203/PREREG203.md), local commit `b972fc0` (2026-11-12 03:47 PT), before any K4 run.
**Code:** [`wr203.py`](../tools/cycle203/wr203.py), [`run203.py`](../tools/cycle203/run203.py), [`sat203.py`](../tools/cycle203/sat203.py). **Results:** [`results203.json`](../tools/cycle203/results203.json), [`results203_sat.json`](../tools/cycle203/results203_sat.json), logs `runlog203_*.txt`.

## Why this family (inference, labelled)
- **Fact:** K1 and K2 use one KRYPTOS-keyed tableau and a real key word ([case 10](10-style-profile.md)); case 25 tested a key restarting at X and listed word-boundary restarts as untested; a grep over `case-file/` found no later test (case 89 restarts at W only).
- **Inference:** restarting the key at every word is a simple hand-cipher tweak that keeps K1/K2's tableau and key word but destroys the period every periodic test (and case 187's lag panel) assumed.

## Rules tested
- **R1 (word restart):** key index = position of the letter inside its plaintext word, mod L.
- **R2 (word-wise key):** one key letter per word, the key advancing one step per word.
- **QIII-R1:** R1 with an unknown keyed alphabet (Quagmire III, any of 26! alphabets), Vigenère form and Beaufort form, by SAT (pysat Glucose 4).

Tableaux AZ and KA (KRYPTOSABCDEFGHIJLMNQUVWXZ), Vigenère / Beaufort / variant, L = 1–26, cribs at the carved positions (EASTNORTHEAST 22–34, BERLINCLOCK 64–74, 1-indexed), no transposition layer. Primary segmentations: EASTNORTHEAST, EAST|NORTHEAST, EASTNORTH|EAST, EAST|NORTH|EAST × BERLINCLOCK, BERLIN|CLOCK; the word holding each crib's first letter may have started earlier (free offset 0..L−1). Secondary: every boundary set inside the cribs whose fully internal words have ≥ 2 letters (377 × 144 sets), L 1–13.

## Controls (passed before K4 was read)
| Control | Result |
|---|---|
| C1: planted R1, KA Vigenère, key ABSCISSA, L 8 (invented example text) | true config survives; crib-implied key letters = ABSCISSA (2 survivors at L 8) |
| C2: planted R2, AZ Beaufort, key PALIMPSEST, L 10 | true config survives with the right key letters (150 survivors: R2 is weak once words are short) |
| C3: planted QIII-R1, random alphabet, L 8 | SAT at the true config |
| C4: 1,000 shuffled K4 (seed 203203) for R1 / R2; 3 shuffles for QIII (time budget) | below |

## Results
**R1, direct tableaux (exact under the stated assumptions).**
| Text | survivors at L ≤ 19 | L 20–22 | L ≥ 23 |
|---|---|---|---|
| **K4, primary** | **0** | **0** | 2 / 184 / 414 / 692 at L 23 / 24 / 25 / 26 |
| K4, secondary (any boundaries, L ≤ 13) | **0** | — | — |
| 1,000 nulls (fraction with any survivor) | 0 | 0.001 / 0.013 / 0.161 | 0.875, 1.0, 1.0, 1.0 |

Every K4 survivor at L ≥ 23 keeps both cribs unsegmented and needs BERLINCLOCK to sit ≥ 10 letters deep inside a single word (minimum offset 10); with the I-256 design bound (offset ≤ 3) there are **0 survivors at any L**. The test discriminates at L ≤ 19 (no null survives there) and loses power from L 22 up.

**R2, direct tableaux:** **0 survivors** for K4 at every L and segmentation; also 0 in all 1,000 nulls (one key letter for a 4–13-letter crib word is almost never consistent), while C2 is recovered. Exact, but the null shows the cribs alone kill R2 for almost any text, so this says little about K4 specifically.

**QIII-R1 (unknown alphabet, SAT):** K4 is **UNSAT for every primary segmentation and offset at L ≤ 10 (Vigenère form) and L ≤ 7 (Beaufort form)**; SAT from L 11 (Vig) and L 8 (Beau). Three shuffled nulls first turn SAT at L 6, 7, 11 (Vig): K4 sits inside that range, so above those lengths the family is **underdetermined**, not supported.

## Verdict
- **EXCLUDED (exact, under these assumptions):** word-restart key (R1) on the straight or KRYPTOS tableau, Vigenère / Beaufort / variant, any key (not only dictionary words) of length 1–22, any English segmentation of the cribs and, at L ≤ 13, any segmentation with internal words of ≥ 2 letters; word-wise key (R2) for every L. Quagmire III word-restart for L ≤ 10 (Vig) / ≤ 7 (Beau).
- **NO-DISCRIMINATION / open:** R1 L ≥ 23 (only with absurd word offsets); QIII-R1 above the UNSAT lengths (underdetermined, SAT like the nulls); Quagmire I/II/IV (two different alphabets); restarts combined with a transposition layer; restarts at other markers (sentence, line); a dropped or wrong crib letter.
- The dictionary key-word step was not needed: no direct survivor at a discriminating L.
- **Budget note:** the registered runs took 84 s (direct, 1,000 nulls) and 351 s (SAT); with the 128 s SAT smoke the cycle's heavy compute was ≈ 9.5 min, a little over the 8-minute target (disclosed). The QIII null sample is 3, so its comparison is descriptive only.

**No solution; K4 status unchanged.**
