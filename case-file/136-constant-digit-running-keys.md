# Case file 136 — Running keys from the digits of mathematical constants (cycle 148)

**Idea.** A K1–K3-era cipher clerk who wants a long, non-repeating key without carrying a book might use a famous constant: pi, e, the golden ratio. If K4's second layer were a running key read from such a digit stream, the cribs would pin down the start offset and shift exactly.

**Model.** key[i] = stream[o+i] + c (mod 26), with free start o (0..~10,000) and free shift c. Streams: 8 constants (pi, e, sqrt2, sqrt3, sqrt5, phi, ln2, Euler gamma) x 5 derivations (single digits; non-overlapping pairs mod 26 in two phases; pairs kept only when < 26 in two phases) = 40 streams. Vigenère, Beaufort and variant over A–Z and KRYPTOS tableaux; direct, and behind the 165,065-transposition bank in both directions and both layer orders.

**Method.** Exact, not scored: a (gap, difference) index on the two lowest crib positions yields every candidate (o, c); each is verified on all 24 crib letters. Tools in `tools/cycle148/`.

**Controls.** Five planted keys (direct, behind a bank transposition, carved order, inverse) all recovered at 24/24 with the full English plaintext. Two shuffled-ciphertext nulls run identically.

**Result.** Direct K4: best 9/24. Behind the bank (1.58 x 10^8 configs, 2.8 x 10^10 candidates per text): K4 best 10/24, nulls best 10/24, zero hits at >= 20. **Negative**: K4 behaves exactly like shuffled text.

**Not covered.** Digit streams in other bases or groupings (triples, letter-number codings A=1..26 with carries), keys read backward, constants beyond these eight, keystream stepping by a decimation.
