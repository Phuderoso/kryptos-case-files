# Case file 120 — Two keyword layers then a transposition, full vocabulary (cycle 132)

**Status:** negative, exact. **Type:** variant/extension of case file 119 (closes its main open gap for one model).

## Question
Cycle 131 tested two stacked keyword layers behind the transposition bank only for themed × themed keyword pairs,
because each configuration needed a scan of all 330,130 permutations. The open row said "vocabulary pairs behind
transpositions". Could K4 be: keyword 1 (Vig/Beau/variant, A–Z or KRYPTOS tableau) → keyword 2 (same choices) →
one of the bank transpositions, with arbitrary dictionary words as keys?

## Method
For model Q (both layers at the plaintext position, transposition last) the letters the ciphertext must show at
σ(21..33), σ(63..73) are fixed by the keywords alone. Each permutation and inverse is precomputed into a 24-letter
signature and hashed; each configuration is one exact lookup. Search: 10,056 × 10,056 ordered pairs × 2 tableaux ×
3 directions per layer = 3.64×10⁹ configurations, each equivalent to 330,130 permutation tests (≈1.2×10¹⁵ exact
tests).

## Results
| text | configs | survivors |
|---|---|---|
| K4 | 3,640,432,896 | **0** |
| null 1 (shuffled K4) | 3,640,432,896 | 0 |
| null 2 (shuffled K4) | 3,640,432,896 | 0 |

Controls: 3/3 planted model-Q ciphertexts with vocabulary keywords (HARBOR+WINDOW, MIRROR+GARDEN with an inverse
permutation, KRYPTOS+QUESTION) recovered with exactly one survivor each.

## What this excludes and what it doesn't
Excluded: any pair of repeated words from the 10,056-word list as two stacked Vig/Beau/variant layers on A–Z or
KRYPTOS tableaux, followed by any of the 165,065 bank transpositions (either direction).
Not excluded: models M and P (transposition first or between the layers) with vocabulary pairs — the hash trick does
not apply there because the key is read at the carved position; phrases; keys outside the list; transpositions
outside the bank.

## Next
The same signature hash makes **any** plaintext-position substitution followed by a bank transposition cheap: e.g.
keyword + autokey, Quagmire III with vocabulary keywords, Gromark with vocabulary primers — all at one lookup per
key.
