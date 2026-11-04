# 36 — Hex inside hex, mod-26 version: lifted digit regrouping

*Cycle 37, 2026-11-04. Status: **negative**.*

## Why
Cycle 36 took Phuderoso's "hex inside hex" hunch literally (letters → digit pairs → regrouped → letters) and showed it cannot carry an arbitrary plaintext, because regrouped pairs are often not letters. Its own next-ideas list asked for the version that *is* valid for any text: reduce each regrouped pair **mod 26**. That makes the cipher a genuine two-layer scheme in plain sight, a number layer under a letter layer, with the digit shuffle as the K3-style transposition.

## Model (`HYPOTHESIS`)
1. Plaintext letter → number n in A–Z or KRYPTOS order, 0- or 1-based.
2. n → two digits in base b (b = 10 decimal, b = 16 hex).
3. The 194-digit stream is transposed at **digit level**: every rotation 1–193, reversal, odd/even split, plain columnar widths 2–40, keyword-keyed columnar for 22 themed words (KRYPTOS, PALIMPSEST, ABSCISSA, BERLIN, CLOCK, SHADOW, LUCID, MEMORY, SANBORN, SCHEIDT, LANGLEY, EASTNORTHEAST, BERLINCLOCK, HEX, DIGIT, REGROUP, LAYER, IQLUSION, UNDERGRUUND, DESPARATLY, EGYPT, CARTER) read both ways, and the inverse of each: 363 permutations.
4. Digits regrouped into pairs, pair value v (0 to b² − 1), cipher letter = A[(v − z) mod 26].

Decryption loses nothing to guesswork: each carved letter has 4 (decimal) or 10 (hex) possible lifted pair values, the un-transposed digits must form pairs that are letters, and the 24 crib letters are fixed. Each of 8 schemes × 363 permutations = **2,904 configurations** was solved exactly with z3.

## Results
| Text | Configurations | Satisfiable |
|---|---|---|
| K4 | 2,904 | **0** |
| Shuffled K4, seeds 1–3 | 2,904 each | 0, 0, 0 |
| Planted control 11 (KA, 1-based, hex, keyword ABSCISSA columnar, inverse) | 2,904 | 1, the planted one |
| Planted control 12 (KA, 1-based, hex, rotation 136) | 2,904 | 8, all rotation 136 (an even digit rotation is a plain letter rotation, so every scheme fits) |
| Planted control 13 (KA, 0-based, decimal, rotation 147) | 2,904 | 1, the planted one |

The test has power (each planted plaintext is found and almost nothing else fits), and K4 fits nothing, same as its shuffled copies. Raw output: [`analysis/cycle37_liftregroup.txt`](../analysis/cycle37_liftregroup.txt). Code: [`tools/liftregroup.py`](../tools/liftregroup.py), run with [`tools/run_cycle37.sh`](../tools/run_cycle37.sh).

## Limits
- One letter layer only: a periodic or running key applied *after* the regroup is not covered.
- Bases 10 and 16 only; digit-level transpositions limited to the family above (no double columnar, no K3 double-rotation on digits).
- Cipher numbering uses the same alphabet as the plaintext numbering.

## Verdict
Lifted digit regrouping, the strongest any-text reading of "hex inside hex", does not produce K4 under these 2,904 configurations. **Negative.**
