# Case file 125 — Ciphertext-fed autokey with a keyed cipher alphabet and a free plaintext alphabet (cycle 137)

**Status:** negative, exact. **Type:** new structural idea (cycle 136 was a variant). It opens the Quagmire II / IV side of autokey that case file 124 left out, and it does so for **every** plaintext alphabet at once, not for a word list.

## Question
Cycles 19, 22, 133, 134 and 136 tested autokey only when the plaintext side used a known alphabet (A–Z, KRYPTOS, or the same vocabulary alphabet as the cipher side). Quagmire II and IV autokey, where the plaintext alphabet is a second, different mixed alphabet, stayed open. Searching pairs of word alphabets behind the bank would cost about 10⁴ times cycle 136.

Is there a way to leave the plaintext alphabet completely free and still test exactly?

## The trick
For a ciphertext-fed autokey the key letter is the earlier ciphertext letter of the same layer, which is always known once the transposition is fixed. Write the Vigenère form with three index maps:

`y(c_j) = x(p_j) + z(c_{j−L})  (mod 26)`

- `y` is the cipher-alphabet index (a keyed alphabet),
- `z` reads the key letter (the same keyed alphabet, plain A–Z or KRYPTOS),
- `x` is the plaintext-alphabet index, **any of the 26! alphabets**.

So `x(p_j) = y(c_j) − z(c_{j−L})` is a number we can compute at every crib. The crib letters do not need to be placed in `x`; we only need the computed numbers to behave like a permutation: equal plaintext letters must get equal numbers, and different letters different numbers. The 24 official cribs hold 13 distinct letters, so with all cribs active there are 11 equalities, each passing by chance with probability 1/26. A survivor needs at least 6.

With `x` free, Beaufort (`x = z − y`) is the same test as Vigenère (`x → −x`). Variant Beaufort (`x = y + z`) is a separate test. The primer never matters: positions `j < L` are simply not used.

## Search
Tool: [`tools/cycle137/ctfree.c`](../tools/cycle137/ctfree.c).

- Cipher/key alphabet pairs `(y, z)`: (W, W), (W, A–Z), (W, KRYPTOS), (A–Z, W), (KRYPTOS, W) for every one of 10,056 vocabulary words W (K1/K2 construction: unique letters, then the rest of A–Z). That is 50,280 pairs, each with two signs.
- Behind the 165,065-entry bank in both directions (330,130 permutations), with the key read at the carved index (transposition first) or at the plaintext index (model Q), lags 1–16: **1,060,428,127,680 exact tests** (≈1.06×10¹²). Wall time 337 s on 8 cores.
- Direct (no transposition), any lag at which the cribs still give at least 6 equalities, which is L 1–26.
- Nulls: two shuffled K4 texts (seeds 13701–13702) on every tenth bank entry (1.06×10¹¹ tests each), and in full for the direct pass.

## Results
| text | tests | consistent |
|---|---|---|
| K4, behind the bank | 1,060,428,127,680 | **0** |
| null 1 (1/10 of the bank) | 106,050,173,760 | 0 |
| null 2 (1/10 of the bank) | 106,050,173,760 | 0 |
| K4, direct, L 1–26 | 10,458,240 | **0** |
| nulls, direct | 10,458,240 each | 0 |

Planted controls (independently encrypted in Python, each with a **random** plaintext alphabet): 5/5 recovered.

- ctl1 carved, y = z = PALIMPSEST, Vigenère, L 7: found at the true permutation (and its bank duplicate), with the readable partial plaintext.
- ctl2 carved, y = KRYPTOS, z = A–Z, Beaufort, L 13: found.
- ctl3 model Q, y = BERLIN, z = KRYPTOS, variant, L 5: found.
- ctl4 carved, y = A–Z, z = CLOCK, Vigenère, L 16: found at the true permutation, plus 46 neighbouring columnar permutations that only swap 16-letter blocks (same lag as the block width); all of them read as the planted English, so this is the expected ambiguity, not noise.
- ctl5 direct, y = z = SHADOW, variant, L 12: found (also under SHADOWS, the same alphabet).

A direct control at L 30 was **not** found, as expected: at that lag only 3 crib equalities remain, below the 6-check threshold. That is why the direct pass stops at L 26.

## What this closes
Ciphertext-fed autokey in which the cipher side is a K1/K2-style keyed alphabet (or A–Z/KRYPTOS with a keyed key alphabet), and the plaintext side is **any** alphabet, with a primer of any letters: excluded direct for L 1–26 and behind 330,130 bank permutations for L 1–16, in both index orders. This includes Quagmire II and Quagmire IV CT-autokey with any second alphabet, which no earlier cycle could reach.

## Still open
- Plaintext-fed autokey with a free plaintext alphabet: the key letter is then a plaintext letter, usually unknown, so the same trick does not apply.
- Both alphabets free (the computed numbers then depend on an unknown `y`; the test loses its power).
- The key letter read through the plaintext alphabet (`x(c_{j−L})`) rather than through `y` or a fixed tableau.
- Lags 17–26 behind the bank, and lags above 26 direct (too few crib equalities; would need a language score).
