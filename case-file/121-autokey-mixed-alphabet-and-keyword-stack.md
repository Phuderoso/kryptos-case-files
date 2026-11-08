# Case file 121 — Plaintext-autokey with a mixed alphabet or a keyword stack, then a transposition (cycle 133)

**Status:** negative, exact. **Type:** new structural idea (cycle 132's crib-signature hash applied to autokey-style key-at-plaintext substitutions that cycles 19 and 22 left open: mixed alphabets, and a repeating keyword stacked with an autokey).

## Question
K1 and K2 are Quagmire III (one KRYPTOS-keyed alphabet, a repeating English word). Cycle 19 tested ciphertext- and plaintext-fed autokey behind the bank only on the A–Z and KRYPTOS *shift* tableaux, and cycle 22 closed the plaintext-autokey chains for any primer on those same tableaux (where the cribs give at least six checks). Cycle 131/132 stacked two *repeating* keywords and left "keyword + autokey" open. Could K4 be:

1. **Quagmire III autokey** — a vocabulary-keyed mixed alphabet (the K1/K2 construction: unique keyword letters, then the rest of A–Z) with a vocabulary primer, the key then continuing with the plaintext itself — followed by a bank transposition?
2. **A repeating vocabulary keyword stacked with a plaintext-autokey**, either order, on the A–Z or KRYPTOS tableau, then a bank transposition?

Both are key-at-plaintext substitutions (model Q of cycle 131), so cycle 132's hash applies.

## Method
For primer length L ≤ 10 no official crib sits inside the primer region (the first crib letter is at index 21), so the letters the ciphertext must show at the determined crib positions depend on the alphabet or repeating keyword, on L and on the setting, but *not* on the primer letters. Each of the 330,130 permutations (both directions) is reduced to those n = 24 − 2L letters and hashed; a hit is decrypted in full from the primer and checked against all 24 crib letters (`EASTNORTHEAST` at 21–33, `BERLINCLOCK` at 63–73). Tool: [`tools/cycle133/qak.c`](../tools/cycle133/qak.c).

Search, for every ordered pair (W, R) with R of length 3–10 (9,294 of the 10,056 words):

| family | settings |
|---|---|
| Q — Quagmire III PT-autokey, alphabet = keyed(W), primer = R | 3 directions (Vigenère / Beaufort / variant) |
| KA — repeating W, then PT-autokey of that layer's output with primer R | 2 tableaux (A–Z, KRYPTOS) × 3 × 3 directions |
| AK — PT-autokey of the plaintext with primer R, then repeating W | same 18 settings |

3 + 18 + 18 = 39 settings. 10,056 × 9,294 × 39 = 3.645×10⁹ configurations, each equivalent to 330,130 permutation tests (≈1.20×10¹⁵ exact tests). Wall time 49 s (8 cores), because one hash lookup serves every primer of a given length.

Ciphertext-fed autokey (key continues with the substitution's own output) is **blind** on this vocabulary: the longest word has length 14, and a CT primer must reach position 21 before any crib I-letter is determined. Primers of length 11–14 (762 words) are underpowered for the hash filter (n ≤ 2) and were skipped (7,662,672 pairs).

## Results
| text | configs | survivors |
|---|---|---|
| K4 | 3,644,958,096 | **0** |
| null 1 (shuffled K4, seed 13301) | 3,644,958,096 | 0 |
| null 2 (shuffled K4, seed 13302) | 3,644,958,096 | 0 |

Controls (`plant.py`, independently encrypted in Python): 4/4 planted model-Q ciphertexts recovered with their planted keys when each first-keyword row was searched against the full 10,056-word list (362,466 configs per row). No other keyword/primer pair survived any control.

1. QIII, alphabet KRYPTOS, primer BERLIN, Vigenère, perm 12345.
2. Keyword SHADOW (A–Z, variant) then PT-autokey primer CLOCK (A–Z, Vigenère), inverse of perm 99999.
3. PT-autokey primer EAST (KRYPTOS, Beaufort) then keyword MIRROR (KRYPTOS, Vigenère), perm 160000. A dual writing of the same two operations (variant then Beaufort) also matches, as expected.
4. QIII, alphabet PALIMPSEST, primer LAYER, Beaufort, perm 4242.

Some neighbouring bank entries are stored inverses of each other and are reported as the other direction of the same mapping; that does not add a new key.

## What this excludes and what it doesn't
Excluded: any vocabulary-keyed Quagmire III alphabet with a vocabulary PT-autokey primer of length 3–10, and any vocabulary repeating keyword stacked with a vocabulary PT-autokey primer of length 3–10 (either order, A–Z or KRYPTOS tableau, Vigenère / Beaufort / variant), followed by any of the 165,065 bank transpositions (either direction).

Not excluded: ciphertext-fed autokey (blind here); primers of length 11 and up, including two-word phrases (the filter needs more determined letters, or a different index); transposition-first models (the key would sit at the carved position); Quagmire I, II or IV autokey; a running-key layer in place of the autokey; keys outside the 10,056-word list; transpositions outside the bank.

## Next
Two-word phrase primers would push L into 11–20 (where PT-autokey is weak but no longer empty) and, for three themed words or long pairs, past 21, where ciphertext-fed autokey finally sees the first crib. Cycle 132's other leftover — bucketing permutations by carved crib positions modulo the key length — is the way into transposition-first models.
