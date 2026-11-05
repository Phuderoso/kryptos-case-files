# Case file 54 — Interrupted key: a keyword that restarts wherever the encipherer chooses (cycle 56)

**Why this family.** The ACA "interrupted key" is the smallest possible step beyond K1/K2: the same keyword on the
same keyed tableau, except that the key goes back to its first letter at chosen points (every plaintext word, every
X separator, every sentence) instead of running on periodically. It needs nothing that K1–K3 don't already show, and
it breaks the periodicity that every periodic test in this repo relies on. It was not in the repo or in kryptosbot's
published list (Sept 29, 2026). New family for the coverage table (diversity rule).

**Model (exact).** One mixed alphabet A (A–Z, KRYPTOS, or any of the 86,731 keyword/keyphrase alphabets in
`data/alpha.bin`); the row for key letter k is A shifted to start at k, as on the Kryptos tableau. Vigenère
a(c) = a(p) + a(k), Beaufort a(c) = a(k) − a(p), variant a(c) = a(p) − a(k). The key index advances by one per letter
and wraps after the last key letter, but at any interruption point it returns to 0. Interruption points are unknown,
so the solver (`tools/intkey.c`) allows all of them: a bitmask dynamic program over the key index (continue j → j+1
mod L, or restart j → 0), with the index free at the start of each crib. Only the 24 crib letters are used.

**Keys.** `tools/words56.py`: themed K1–K3/Kryptos vocabulary (cycle 52 list) + K1–K3 plaintext words + the 10,000
most frequent English words (lengths 3–14) from five Gutenberg novels: 10,056 single words over all 86,731 alphabets;
two-word keyphrases from the first 3,000 words (9 million phrases, ≤ 31 letters) over 298 themed alphabets
(A–Z, KRYPTOS and the first 296 entries of cycle 55's themed list; `tools/intkey2.c`).

**Run** (`tools/run_cycle56.sh`, about 4.5 minutes): 2.6 × 10⁹ single-word tests and 8.0 × 10⁹ phrase tests per text.

| Text | Single words (all alphabets) | Two-word phrases (298 alphabets) |
|---|---|---|
| **K4** | **0** | **0** |
| 5 shuffled-K4 nulls | 0, 0, 0, 0, 0 | 0, 0, 0, 0, 0 |
| CTL1 KA, Vigenère, SHADOW, restart at every word | found (also SHADOWS, SHADOWFORCES) | found |
| CTL2 alphabet #5000, Beaufort, PALIMPSEST, 12 random restarts | found (unique) | — (alphabet not in the 298) |
| CTL3 KA, variant, BURIEDSTONE, restart at every word | — (phrase, not a word) | found (+ BURIEDSTO… prefixes) |
| CTL4 A–Z, Vigenère, LANGLEY, never interrupted | found (unique) | found |

Controls 4/4 recovered. Extra hits in the controls are keys that share the planted key's prefix: with free restarts the
cribs only see the key letters they reach, so a key is certified only up to that point.

**Verdict.** Negative for an interrupted keyword or two-word keyphrase from this vocabulary on any of these tableaux.
**Still open:** arbitrary (non-keyword) alphabets; keys outside the vocabulary; interruption behind a transposition;
interruption that also changes the alphabet (that becomes the split key of case file 52 with more segments).
