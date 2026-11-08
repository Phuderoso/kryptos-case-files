# Case file 116: one primer, two jobs (Sequence Transposition + Gromark from the same digits)

**Cycle 128, 2026-11-08. Variant of case file 115. Verdict: negative.**

## Why
In the ACA's Sequence Transposition and in the Gromark, the digit stream is generated the same way, from a 5-digit primer by chain addition. A hand cipherer who already has that stream on the worksheet could use it twice: once to sort letters into ten columns, and once as the Gromark key that shifts each letter. That is "several layers of something simple", with one secret serving both layers, like K3's single keyword setting both the grid and the reading.

## What was tested (exact)
- Every primer from 00000 to 99999 and every one of the 10! column read orders.
- The digit substitution before the transposition (digit at the plaintext position) or after it (digit at the carved position).
- Plaintext alphabet A–Z or KRYPTOS, Vigenère or Beaufort form, and **any cipher alphabet**: the 24 crib letters must fit one consistent one-to-one cipher alphabet.

## Controls and nulls
- 4/4 planted controls (independent encryptor; ENIGMA- and SHADOW-keyed cipher alphabets, KRYPTOS/KRYPTOS, A–Z/A–Z) were recovered at the true primer, model, alphabet and form, with the true column order among the survivors. A primer with only even digits leaves five columns empty, so those columns can be reordered freely and give equivalent survivors.
- Shuffled K4: 3 and 10 survivors.

## Result
**K4: 1 survivor** (primer 76707, model B, A–Z, Vigenère), which is fewer than either null. Its partial decryption from the 19 cipher letters the cribs pin down is gibberish: `?BP?GI?LWMC?HKU?N?LKC[EASTNORTHEAST]UVPUEFLB?Y??SNFJLONM?UB?YXM??[BERLINCLOCK]DA?ZFT??FWSJ?G?JYI?JRFM`. Negative.

## Still open
Separate primers for the two jobs (10¹⁰ pairs, too many to search exactly; this needs a smarter model such as SAT), the inverse transposition direction, and primers longer than five digits.
