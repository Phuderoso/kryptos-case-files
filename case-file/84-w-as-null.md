# Case file 84 — W as a null: the 92-letter W-free text (cycle 88)

**Idea.** In K1–K3, X separates sentences. K4's five Ws are spread unusually evenly (cycle 87, [case file 83](83-w-split-equal-frequencies.md)),
and none of them falls inside a crib: they sit at positions 20, 36, 48, 58 and 74 (0-indexed), i.e. one letter before
EASTNORTHEAST and one letter after BERLINCLOCK. If W is a null or separator, the real ciphertext is 92 letters and the
cribs move to EASTNORTHEAST at 20–32 and BERLINCLOCK at 60–70. Nothing in the repo had tested that text before.

**Tests (exact, crib-consistency; code in `tools/cycle88/`, numbers in `data/cycle88/results.txt`).**
1. 239,149 permutations of 92 letters (identity; keyword columnar widths 2–8, every column order; K3-law decimations
   of [case file 57](57-k3-as-decimation.md) re-derived for 92 letters, M = 92–107, every coprime step and start; all inverses) × periodic key
   p 1–24 × Vigenère/Beaufort × plaintext and ciphertext alphabet each A–Z or KRYPTOS × both layer orders.
2. No transposition: Quagmire III over the 86,731 themed keyed alphabets × Vigenère/Beaufort × p 1–20.

**Results.**
| | p ≤ 20 | p 21 | p 22 | p 23 | p 24 |
|---|---|---|---|---|---|
| K4 W-free, test 1 | 0 | 0 | 42 | 367 | 1,046 |
| 3 shuffled nulls, test 1 | 0 | 0–1 | 33–52 | 278–363 | 848–1,191 |
| K4 W-free, test 2 | 0 | — | — | — | — |

Test 2 nulls 0/3. Planted controls: 3/3 recovered in test 1 (both layer orders, both alphabets), 1/1 in test 2.
At p ≥ 22 the cribs no longer constrain the key and K4 sits inside the null range.

**Verdict.** Treating W as a null does **not** open K4 to periodic substitution, with or without a columnar or
K3-style decimation layer, for keys up to 21 letters. **Negative.**

**Still open:** W as a *word separator* (blocks enciphered separately, key restarting at each block); W-free text with
Myszkowski, routes or Playfair; W as null *and* one carving anomaly.
