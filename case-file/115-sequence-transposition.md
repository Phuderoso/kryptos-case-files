# Case file 115: Sequence Transposition behind or ahead of a periodic key

**Cycle 127, 2026-11-08. New family. Verdict: negative for periods ≤ 14.**

## Why
The ACA's Sequence Transposition sends each plaintext letter to one of ten columns, chosen by a digit stream. The stream comes from a 5-digit primer extended by chain addition, the same generator as the Gromark. The columns are then read in a keyword order. It's a transposition driven by a running digit key, the kind of layering of simple parts that the user's hunch points to (a digit key inside a letter transposition). The repo had covered Gromark as a substitution but never this transposition.

## What was tested (exact)
- Every primer from 00000 to 99999 and **every one of the 10! column read orders**, so every keyword under either the 0-9 or the 1-0 labelling convention is included.
- A periodic key before the transposition (model A) or after it (model B), A–Z or KRYPTOS alphabet, Vigenère/variant or Beaufort, every period from 1 to 14, checked against all 24 crib letters.
- About 2.4 × 10⁹ search nodes for K4 (depth-first search with crib pruning; the equivalent of 3.6 × 10¹¹ order × primer pairs times 8 key setups).

## Controls and nulls
- 4/4 planted controls built with an independent encryptor were recovered at their exact primer, order, model, alphabet, form and period. They were GUMMYBEARS/69315 (A–Z Vigenère p7, key before), CHARTHOUSE/42983 (1-0 labelling, KRYPTOS Beaufort p6, key after), BROADCLOTH/75639 (KRYPTOS Vigenère p10, key after) and KRYPTOSABC/00427 (A–Z Beaufort p10, key before). The only extras are echoes of the true answer: a two-column swap at a multiple of the true period, or swaps of columns that hold no crib letters.
- One shuffled K4 over all 100,000 primers: 0 survivors. (A second null was skipped to stay inside the time budget.)

## Result
**K4: 0 survivors** for any primer, any column order and any periodic key of length ≤ 14 in either layer order.

## Still open
- Periods 15–18, about 8× more search nodes. This would be checkpointed by primer ranges across cycles.
- The inverse direction (the sculptor applying the decryption routine).
- A non-periodic second layer: a Gromark digit key using the *same* primer stream as the transposition, which would be the "one key, two jobs" variant and cheap to test next.
- Primers longer than 5 digits.
