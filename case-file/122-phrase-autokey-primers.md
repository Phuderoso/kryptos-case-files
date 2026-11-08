# Case file 122 — Phrase-primer plaintext- and ciphertext-autokey behind a transposition (cycle 134)

**Status:** negative, exact. **Type:** variant of cycle 133 (the same model-Q autokey families, now with phrase primers long enough that the first crib sits inside a ciphertext-fed primer).

## Question
Cycle 133 tested Quagmire III PT-autokey and a repeating keyword stacked with PT-autokey, model Q behind the 165k bank, but only with single vocabulary primers of length 3–10. Longer primers were left open: the crib-signature hash needs n = 24 − 2L determined letters and is underpowered for L ≥ 11, and a ciphertext-fed primer has to reach position 21 before any crib letter of the intermediate text is determined (no vocabulary word is longer than 14). Could K4 use a *phrase* primer — two vocabulary words joined, or three themed words — so that:

1. **PT-autokey at L 11–22**, where a few crib-to-crib chains still exist and a derived primer can be looked up even though the hash filter is weak?
2. **CT-autokey at L 22–28**, where the primer finally overlaps `EASTNORTHEAST` at index 21?

## Method
Each of the 330,130 permutations (both directions of the 165,065-entry bank) is known as an intermediate text I. The 24 official cribs (`EASTNORTHEAST` at 21–33, `BERLINCLOCK` at 63–73) are then walked back along the autokey chains to *derive* the primer. Most settings fail the first extra chain check (about 25/26) and never reach the dictionary. A derived primer, possibly with a few unknown letters, is matched against:

- the 762 leftover vocabulary words of length 11–14 (skipped in cycle 133);
- every concatenation of two vocabulary words (88,336,835 of length 11–22 and 1,484,370 of length 22–28);
- every concatenation of three themed words in those same length bands (460,272 and 465,786).

After removing the 62 singles that also split as two words and the three-themed strings that coincide with a two-word join, the unique primer sets are 88,797,091 (PT, L 11–22) and 1,950,051 (CT, L 22–28). Tool: [`tools/cycle134/qphrase.c`](../tools/cycle134/qphrase.c).

| family | W | settings | L |
|---|---|---|---|
| Q — Quagmire III, alphabet = keyed(W) | 10,056 vocabulary words | 3 directions | PT 11–22 and CT 22–28 |
| KA — repeating themed W, then autokey of that layer | 97 themed words | 2 tableaux × 3 × 3 directions | same |
| AK — autokey of the plaintext, then repeating themed W | 97 themed words | same 18 settings | same |

Equivalent configurations: Q-PT 2.679×10¹², Q-CT 5.883×10¹⁰, KA/AK-PT 3.101×10¹¹, KA/AK-CT 6.810×10⁹ (total 3.055×10¹²), each checked against 330,130 permutations ≈ **1.008×10¹⁸ exact tests**. The inner loop actually walks (W, setting, L, perm) and looks the derived primer up, 2.111×10¹¹ such tests per text. Wall time 678 s (8 cores) for K4 plus two nulls.

PT primers of length 23–28 and three-themed phrases of length 29–42 were not scanned (the former have no primer-independent I-signature and no extra crib-residue conflict cheap enough for the full vocabulary pass in the time budget; the latter would need one extra length slot each at full vocabulary cost). Stacks used the 97 themed repeating keywords, not the whole 10,056-word list.

## Results
| text | inner-loop tests | consistent derived primers | phrase survivors |
|---|---|---|---|
| K4 | 211,131,340,200 | **0** | **0** |
| null 1 (shuffled K4, seed 13401) | 211,131,340,200 | 4 | 0 |
| null 2 (shuffled K4, seed 13402) | 211,131,340,200 | 0 | 0 |

The four consistent primers on null 1 did not match any phrase. K4 produced no crib-consistent derivation at all.

Controls (`plant.py`, independently encrypted in Python): 4/4 planted model-Q ciphertexts recovered.

1. QIII PT-autokey, alphabet PALIMPSEST, primer NORTHEAST+BERLIN (L = 15), Beaufort, perm 4242.
2. Keyword SHADOW (A–Z, variant) then PT-autokey primer CLOCK+KRYPTOS (L = 12, A–Z, Vigenère), inverse of perm 99999.
3. PT-autokey primer EAST+BERLIN+CLOCK (L = 15, KRYPTOS, Beaufort) then keyword LAYER (KRYPTOS, Vigenère), perm 160000. A dual writing of the same two operations (variant then Beaufort) also matches, as expected.
4. QIII CT-autokey, alphabet KRYPTOS, primer ALEXANDERPLATZ+NORTHEAST (L = 23), Vigenère, perm 12345. At this length only primer[21:23] is pinned by the first two crib letters, so 5,510 crib-consistent L = 23 phrases share those two letters; an independent decrypt with the planted primer restores all 97 letters of the English control plaintext.

Some neighbouring bank entries are stored inverses of each other and are reported as the other direction of the same mapping; that does not add a new key.

## What this excludes and what it doesn't
Excluded: any vocabulary-keyed Quagmire III alphabet with a phrase PT-autokey primer of length 11–22 or a phrase CT-autokey primer of length 22–28 (two vocabulary words, three themed words, or a leftover single word of length 11–14), and any *themed* repeating keyword stacked with the same phrase primers (either order, A–Z or KRYPTOS tableau, Vigenère / Beaufort / variant), followed by any of the 165,065 bank transpositions (either direction).

Not excluded: CT-fed primers shorter than 22 (still blind: the primer does not reach the first crib); PT phrase primers of length 23–28 and three-themed phrases of length 29–42; stacks whose repeating keyword is a non-themed vocabulary word; transposition-first models (the key would sit at the carved position); Quagmire I, II or IV autokey; a running-key layer in place of the autokey; keys outside the phrase set; transpositions outside the bank.

## Next
Cycle 132's leftover index — bucketing permutations by the carved crib positions modulo the key length — is the way into transposition-first models (key at the carved position). Cycle 135 should open a new family or that structural idea rather than another variant of 133/134. Quagmire I/II/IV autokey, and vocabulary (not just themed) repeating keywords with phrase primers, remain on the stack side.
