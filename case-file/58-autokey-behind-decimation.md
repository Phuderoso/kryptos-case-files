# Case file 58 — Autokey behind K3's law (cycle 60)

**Question.** Cycle 59 showed K3's double rotation is one decimation (every 192nd letter around 337 slots) and built
the K4 analogue: 159,712 decimation permutations (M = 97–112 slots, any stride and start, both directions) not in the
cycle-12 family. Only periodic Quagmire III keys were run behind them. Autokey is the next K1–K3-adjacent family
(Sanborn's era, one keyword primer, no visible period), so: does any **autokey** layer on either side of a decimation
reproduce the 24 crib letters?

**Method (exact, [`tools/autokey_exact60.c`](../tools/autokey_exact60.c)).** For every decimation, alphabet, lag
L = 1–96, mode (Vigenère c = p + k, Beaufort c = k − p, variant c = p − k, in the alphabet's index space):

- **Model A** — autokey first, decimation last: the intermediate letter at PT position j is the carved letter at
  perm[j]. CT-fed: key = intermediate letter L back. PT-fed: key = plaintext letter L back.
- **Model B** — decimation first, autokey on the carved order. CT-fed: key = carved letter L back. PT-fed: key = the
  plaintext letter that the decimation put L slots earlier.

The primer is never guessed: only crib positions whose key letter is known give a constraint (n of them). A test hits
when all n agree. CT-fed hits also print the fully determined decryption of every position ≥ L. Alphabets: the 264
themed keyword alphabets (A–Z, KRYPTOS-keyed and 262 others, `data/tw_alpha.bin`) for N = 97; the first 41 for the
98-symbol run.

**Extra family.** K3's law over **98 symbols** with the `?` as symbol 0 (idea from cycle 59): 154,186 decimations,
M = 98–112, cribs shifted by one ([`tools/autokey_gen60.py`](../tools/autokey_gen60.py)).

**Controls.** Four planted autokey encryptions of an English 97-letter text with the cribs in place, behind random
decimations from the same family:

| control | plant | result |
|---|---|---|
| actl0 | A, CT-fed, Vig, L 7, themed alphabet #5 | recovered, n = 24, decryption printed in full past L |
| actl1 | A, PT-fed, Beau, L 4, KRYPTOS alphabet | recovered, n = 16 |
| actl2 | B, CT-fed, variant, L 11, alphabet #40 | recovered, n = 21, decryption printed |
| actl3 | B, PT-fed, Vig, L 2, A–Z | **not testable**: n = 0 (the decimation scatters every crib letter's neighbours) |

actl3 is a power limit, not a bug: model B with a PT-fed key is only testable when a decimation leaves crib letters
within L carved slots of each other. That corner stays open.

**Results ([`data/cycle60/results60.txt`](../data/cycle60/results60.txt)).** Highest constraint count with a hit:

| run | A/CT | A/PT | B/CT | B/PT |
|---|---|---|---|---|
| K4, 97, 264 alphabets | n 5 (12 hits; chance ≈ 10.6) | n 5 (18) | n 5 (29) | n 6 (1; chance ≈ 1.8) |
| shuffled K4 (null0), same | n 5 (11) | n 5 (5) | n 6 (1) | n 6 (3) |
| `?`+K4, 98, 41 alphabets | n 5 (2) | n 5 (7) | n 5 (6) | n 5 (4) |
| `?`+null0, 98, same | n 5 (2) | n 4 | n 6 (2) | n 5 (9) |

Every K4 histogram is the chance curve (hits ≈ tests × 26⁻ⁿ) and matches its shuffled null; nothing reaches n ≥ 7,
while the three testable controls come back at n 16–24. **Negative**: no autokey (any lag 1–96, any primer, three
modes, 264 themed alphabets) sits on either side of a K3-law decimation of K4 or of `?`+K4 (41 alphabets).

**Not covered.** Arbitrary (non-themed) alphabets; PT-fed autokey after the decimation where n is small; autokey with
two different alphabets; the `?` placed anywhere other than symbol 0.
