# 25 — Interrupted key: the key restarts at every X (cycle 26)

> *K2 used X as a full stop. A clerk who restarts his key word at every full stop leaves no period for the analyst to measure. That's an old trick, it's simple, and nobody had walked it past K4 in these files. So I did.*

## Why this hypothesis (inference, labelled)
- **Fact:** in K2's plaintext `X` separates sentences ([case file 02](02-solved-sections.md)); K1 and K2 use one KRYPTOS-keyed tableau with a real-word key ([case file 10](10-style-profile.md)).
- **Inference:** an *interrupted key* (the key word starts over after each sentence break) is a classic hand-cipher tweak that keeps K1/K2's tableau and word key but destroys the fixed period every earlier periodic test assumed. Cycles 1–25 tested strict periods only.
- **Rules tested:** (1) key restarts after each plaintext X; (2) key restarts after each ciphertext X (K4 carries two X's: `UOXOG`, `ZXTJ`); (3) the key does not advance on a plaintext X; (0) plain periodic, as a reference.

## Test A — dictionary key words (`tools/xreset.c`)
369,351 English words of 3–20 letters ([dwyl/english-words](https://github.com/dwyl/english-words) `words_alpha.txt`) × AZ and KA tableaux × Vigenère/Beaufort/variant × 4 rules × every starting phase of the key = **83,693,688 full decryptions**, each scored against the 24 official crib letters (EASTNORTHEAST at 22–34, BERLINCLOCK at 64–74, 1-indexed).

| Text | best rule 0 | rule 1 | rule 2 | rule 3 | runs ≥ 20/24 |
|---|---|---|---|---|---|
| **K4** | 9 | 8 | 8 | 8 | **0** |
| 20 shuffled K4 nulls | 8–9 | 8–9 | 7–9 | 8–9 | 0 |
| control 1 (SHADOW, KA, Vig, rule 1) | 13 | **24** | 11 | 16 | key recovered |
| control 2 (PALIMPSEST, KA, Beau, rule 2) | 15 | 15 | **24** | 15 | key recovered |
| control 3 (ABSCISSA, AZ, variant, rule 3) | 16 | 16 | 12 | **24** | key recovered |

Each control recovered its exact key, tableau, mode and rule, with the full plaintext. The planted plaintext is invented example text, labelled as such in `tools/xreset_controls.py`.

## Test B — any key, not just words (`tools/xreset_generic.py`)
With no X inside the cribs, an interrupted key keeps period-P structure *inside* each crib block, but the phase between the two blocks becomes free (any number of restarts may fall between letters 35 and 63). For each tableau, mode and P = 1–26 I counted the phases at which **some** key fits all 24 crib letters.
- **K4:** the smallest consistent key length is **24**; 36 consistent (tableau, mode, P, phase) cases in total.
- **20 shuffled nulls:** smallest 23–24; totals 36–56. K4 is at the null floor.
- **Control 1:** consistent from **P = 6** (its true length), 110 cases.

## Verdict
**Negative.** An interrupted key restarting at X (either side) or pausing on X, with the KRYPTOS or straight tableau, is excluded for every English dictionary word as key, and for **any** key of length ≤ 23. Lengths 24–26 survive only as the nulls do (the 13-letter crib block then constrains almost nothing).

**Limits:** single-alphabet tableaux only (no Quagmire I/II/IV with two different alphabets); the cribs are taken at the carved positions (no transposition layer); restarts at markers other than X (W, Q, word boundaries) were not tested.
