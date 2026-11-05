# Case file 82 — The halfabet (mod-13 key inside the two halves of a keyed alphabet)

**Cycle 85, 2026-11-05. New family (diversity rule).**

## The idea

K1–K3 use the KRYPTOS-keyed alphabet as one 26-letter ring. A natural, hand-friendly twist is to cut that ring into two
13-letter halves and let the key turn each half on its own: a plaintext letter stays in its own half and moves `k` places
(mod 13) inside it. It is Porta's opposite (Porta always *crosses* halves, case file 31). We call it the halfabet.

Two ways to cut the alphabet `A` (any ordering):

- **split 0:** first 13 letters / last 13 letters;
- **split 1:** even positions / odd positions (interleaved).

Two ways to move inside a half (half-index `i`, key `k` in 0–12):

- **var 0 (additive):** `c = H[(i + k) mod 13]`;
- **var 1 (reflective, Beaufort-like):** `c = H[(k − i) mod 13]`.

## Key-free screen

Whatever the key, every crib pair (plaintext letter, ciphertext letter) must sit in the **same half**. That is about a
2⁻²⁴ filter, so it can be run over every alphabet and every transposition before any key is guessed. Survivors are then
checked for a consistent periodic key of length 1–26, with the key indexed by plaintext position (substitute, then
transpose) or by ciphertext position (transpose, then substitute).

## Scope

- 86,731 alphabets (`alpha.bin`: A–Z, KA, reversals, 264 themed keyword alphabets and the large keyword list) × 2 splits;
- 165,065 transpositions (cycle 19 family, identity included) — same model as case file 31: plaintext letter `j` pairs
  with carved letter `ct[t[j]]`;
- var 0/1 × both layer orders × periods 1–26.

That is 2.9 × 10¹⁰ screened (alphabet, split, transposition) triples per text. Tool: `tools/cycle85/halfabet.c`, runner
`tools/cycle85/run85.sh` (8 parallel chunks; 4 min 53 s wall for K4 plus 5 nulls on 8 cores).

## Results

| text | same-half survivors (split 0 / split 1) | periodic keys found, by period |
|---|---|---|
| **K4** | 1,104 / 774 | **L ≤ 24: 0**; L 25: 11; L 26: 266 |
| shuffled null 1 | 567 / 726 | L 25: 8; L 26: 209 |
| shuffled null 2 | 383 / 674 | L 25: 7; L 26: 154 |
| shuffled null 3 | 519 / 982 | L 25: 1; L 26: 330 |
| shuffled null 4 | 575 / 882 | L 25: 1; L 26: 286 |
| shuffled null 5 | 678 / 587 | L 24: 2; L 25: 6; L 26: 155 |

At L 25–26 there are about as many key slots as cribs, so a "key" fits by chance; K4 sits inside the null range there.

### Planted controls (`tools/cycle85/mkctl85.py`, `analysis/cycle85/controls85.json`)

| control | alphabet, perm, split, var, order | true key | recovered |
|---|---|---|---|
| A | #2, perm 1234, split 0, var 0, sub→trans | L 7 `3,7,1,12,5,0,9` | **yes, exact** (plus the equivalent rotated alphabet #0) |
| B | #40000, perm 99001, split 1, var 1, trans→sub | L 11 `4,4,11,2,8,6,0,10,1,3,7` | **yes, exact** (plus an equivalent alphabet #39998) |
| C | #1 (KA), identity, split 0, var 1, trans→sub | L 5 `6,2,9,11,5` | **yes, exact** (identity is order-blind; a duplicate identity perm also fires) |

Controls ran on the alphabet chunk holding their true alphabet (10,842 alphabets × all 165,065 transpositions); each
true configuration was found at its true period, with nothing else below L 15.

## Verdict

**Negative.** No halfabet with a periodic key of length ≤ 24, on any of 86,731 keyword alphabets, either split, either
variant, directly or behind any of 165,065 transpositions in either order, fits the 24 known plaintext letters.

A note so nobody over-reads it: K4's split-0 survivor count (1,104) is above all five nulls (383–678). Survivors are
heavily clustered (equivalent rotated alphabets and near-identical transpositions fire together), so these counts are
not independent trials, and split 1 shows the reverse (K4 774 inside 587–982). It is recorded, not claimed.

## Still open

Halfabet with a running key or autokey; halfabet with an arbitrary (non-keyword) split (SAT); 13-letter halves in a
K3-style grid; halfabet on top of Playfair or Bifid.
