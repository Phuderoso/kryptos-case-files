# Case file 57 — K3's rotation is a decimation (cycle 59)

## The audit question

Cycle 58 asked which K3-style constructions the cycle-12 transposition family (96,630 permutations, the backbone of
about twenty cycles) leaves out. The first answer turned out to be a simple fact about K3 itself.

## Finding: K3 is "read every 192nd letter"

K3's published method is a double rotation (336 letters in rows of 24, rotate clockwise, rows of 8, rotate clockwise).
[`tools/k3_as_decimation.py`](../tools/k3_as_decimation.py) checks, on the transcribed K3 text, that this is exactly

    PT[i] = CT[(192·(i+1) − 1) mod 337],   i = 0..335

that is, a single step of +192 around a circle of 337 = 336 + 1 slots. Every one of the 335 gaps is 192 mod 337.
This is a known observation in the community, but this repo had never used it: in K3-style terms, a
"double rotation" for K4 need not need 97 to factor at all. The natural K4 analogue is a **decimation**: put the text
on a circle of M ≥ 97 slots (slots ≥ 97 empty, like K3's 337th slot), and read every s-th slot from a start a.

## What was tested

- Family ([`tools/decimation_gen.py`](../tools/decimation_gen.py)): perm[j] = (a + s·j) mod M, M = 97…112,
  gcd(s, M) = 1, every start a, empty slots skipped; both directions (perm and inverse).
  **160,204 distinct permutations, of which only 492 were already in the cycle-12 family; 159,712 are new.**
- Layer ([`tools/periodic_exact59.c`](../tools/periodic_exact59.c)): one periodic key, Quagmire III (same keyed
  alphabet both sides, as K1/K2), Vigenère and Beaufort (variant Beaufort has the same consistency as Vigenère),
  key indexed by plaintext position or by carved position (both layer orders). Exact: all 24 crib letters must fit.
- Runs: 264 themed single-word alphabets, p ≤ 16; A–Z and KRYPTOS alphabets, p ≤ 26; all 20,946 themed alphabets
  (single words and two-word stacks), p ≤ 12.

## Results ([raw](../data/cycle59/results59.txt))

| Text | 264 alphabets, p ≤ 16 | A–Z/KRYPTOS, p ≤ 21 | A–Z/KRYPTOS, p 22–26 | 20,946 alphabets, p ≤ 12 |
|---|---|---|---|---|
| K4 | **0** | **0** | 20 / 39 / 668 / 516 / 28,910 | **0** |
| 3 shuffled-K4 nulls | 0, 0, 0 | 0, 0, 0 | 4–33 / 35–69 / 578–653 / 525–554 / 28,498–28,851 (K4 at or near the edges, i.e. chance) | not run (time) |
| Planted control 1 (M 98, s 31, KRYPTOS Vig, key ABSCISSA, key by PT position) | recovered, p 8 | recovered, p 8 | — | — |
| Planted control 2 (M 103, s 40, KRYPTOS Vig, key PALIMPSEST, key by carved position) | recovered, p 10 (key PA?IMPSEST, one class unconstrained) | — | — | — |

Periods 22–26 are uninformative: K4 sits inside the null range, and the test has no power there.

**Verdict: negative.** A K3-style decimation of K4 followed or preceded by a periodic Quagmire-III key of period ≤ 12
(any of 20,946 themed alphabets), ≤ 16 (264 single-word alphabets) or ≤ 21 (A–Z/KRYPTOS) does not fit the cribs.

## Limits and what is still open

- Only one substitution layer of the periodic kind. Every other family the repo has run "behind the cycle-12
  transpositions" (autokey, running keys, Porta, Hill, Quagmire IV, the one-letter anomaly, Ragbaby, Portax) has
  **not** been run behind decimations; this is now the most obvious structural gap in the coverage table.
- K3's own law includes its `?` (336 + `?` = 337 symbols with the `?` kept as plaintext). A K4 version with the `?`
  carved before OBKR as symbol 0 (98 symbols, M = 99) was not modelled separately.
- Two-step decimations (different strides for two passes) collapse to one decimation only when M is the same; mixed
  M was not tried.
- No null run on the 20,946-alphabet test (time budget); K4's 0 there is uninformative about chance rates but the
  controls show the test can see a planted key.
