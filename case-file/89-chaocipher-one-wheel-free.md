# 89 — Chaocipher with one wheel left completely free (cycle 94)
> *The machine moves both wheels by the same clock. Find the clock and one wheel stops mattering.*

## 1. Why
[Case file 13](13-chaocipher.md) (cycle 14) tested Chaocipher only with **both** starting wheels drawn from 264 themed alphabets, and left "arbitrary starting alphabets" open since then: (26!)² states, and no crib-driven attack. This cycle closes half of that space exactly.

## 2. Reduction lemma (new, checked by controls)
In Rubin's algorithm the left wheel is rotated so that index *k* is at the zenith and then gets a fixed pluck-and-insert; the right wheel is rotated so index *k*+1 is at the zenith and gets another fixed pluck-and-insert. **Both moves depend only on the index *k* where the input letter sat, not on which letters are involved.** Consequences:
1. The wheel that holds the input letters (left when carved = encrypt(plaintext), right when carved = decrypt(plaintext)) together with the carved text fixes the whole index sequence *k*₀ … *k*₉₆.
2. The other wheel is then only relabeled: output letter *i* = W₀[*u*ᵢ], where *u*ᵢ is a computable index into the starting order W₀. **The plaintext is a simple substitution of a known stream.** W₀ can be anything (26! choices) at no cost.
3. Rotating the input wheel changes only *k*₀ and is absorbed by W₀, so rotations / the "relative offset" of cycle 14 are irrelevant.

Crib test: the 24 known letters fall on 24 values of *u*; they must map consistently (13 same-letter pairs equal) and injectively (263 different-letter pairs unequal). A random input wheel passes with probability around 26⁻¹¹; a pass is decisive.

## 3. Tools
`tools/cycle94/chaoarb.c` (direct), `tools/cycle94/chaoarb_tb.c` (transpose, then Chaocipher), `tools/cycle94/ctl94.py` (Rubin test vector + planted controls), `tools/cycle94/mkalpha94.py` (word-keyed alphabets).

## 4. Controls
- Rubin's published test vector: PASS (in `ctl94.py`).
- Six planted texts with the cribs at K4's positions: input wheel = a word-keyed alphabet, **rotated by a random amount**, output wheel **random**, both directions. Searching 900,527 alphabets: **6/6 recovered, each the only hit.**
- Transposition-first plant (themed alphabet 77, cycle 12 transposition 5,000, random output wheel): recovered as the only hit among 58 M runs.

## 5. Results ([data](../data/cycle94/results.txt))
| Input wheel enumerated (output wheel arbitrary) | Layers | Runs | K4 hits | Nulls |
|---|---|---|---|---|
| 900,527 word-keyed alphabets (367k English words × keyword+rest, keyword+rest from last letter, reversed) | direct, both directions | 1.8 M | **0** (fewest conflicts 10) | 5 shuffled K4: 0 hits, fewest conflicts 8–10 |
| 86,731 keyed alphabets (the set used in cycles 54–64) + 20,946 themed | direct, both directions | 215 k | **0** | — |
| 20 M uniformly random alphabets | direct, both directions | 40 M | **0** (fewest conflicts 8) | baseline itself |
| 86,731 + 20,946 alphabets × 96,630 cycle-12 transpositions and × 147,709 strip transpositions | transpose then Chaocipher | 5.3 × 10¹⁰ | **0** (not even the 13 equalities) | null: 0 / 1.7 × 10¹⁰ |

K4's conflict distribution matches the shuffled nulls and the random baseline: no signal.

## 6. Verdict
| Hypothesis | Status |
|---|---|
| Chaocipher, input wheel from 1.0 M keyed/word/themed alphabets, **other wheel any of 26!**, both directions | **excluded** |
| Same behind 244,339 transpositions (cycle 12 + strips) | **excluded** |
| Both wheels arbitrary | **crib-underdetermined in principle** (≈ 26!·26⁻¹¹ input wheels pass), but a random-wheel sample of 4 × 10⁷ never passed, and the lemma means any proposed wheel can be checked in microseconds |
| Chaocipher, then transposition, arbitrary output wheel | open (the transposition scrambles the *k*-driving input; needs the cycle 14 `ta` loop) |

Limits stated plainly: "keyed alphabet" means the constructions listed; K3-style grids of alphabets, two-word keys, and Chaocipher variants with other pluck positions were not tested.

## Cycle 95 addendum: other wheel-moving rules
The lemma needs only that a wheel's move depends on the index *k*, not on the letters. So I generalized the move: rotate so index *k*+*o* is at the zenith, pluck the letter at position *p*, re-insert it at position *q*, with *o* ∈ {0, 1, 2}, *p* ∈ 1–5, *q* ∈ {12, 13, 14}. That gives 45 rules per wheel and 2,025 (input, output) pairs. Rubin's Chaocipher is the pair (0, 1, 13) / (1, 2, 13). Enumerating both rules also covers both directions, because the input wheel is simply the one the carved letters are found in. Tool: `tools/cycle95/chaogen.c`, controls in `tools/cycle95/ctl95.py` (which also re-checks Rubin's test vector).

| Test | Runs | Result |
|---|---|---|
| Planted controls: 3 non-Rubin rule pairs, themed input wheel, random output wheel | 3 × 4.2 × 10⁷ | 3/3 recovered, each the only run that met even the 13 equalities |
| K4, 20,946 themed input wheels × 2,025 rule pairs | 4.2 × 10⁷ | **0** (not even the 13 equalities) |
| K4, 86,731 keyed input wheels × 2,025 rule pairs | 1.8 × 10⁸ | **0** |
| 2 shuffled-K4 nulls, themed wheels | 2 × 4.2 × 10⁷ | 0 |

**Verdict:** this generalized Chaocipher family (the rule grid above, keyed or themed input wheel, any output wheel) is **excluded**. Still open: rules outside the grid (two plucks per step, moves that depend on the letter itself, a Kryptos-tableau slide), word-keyed input wheels × the rule grid (≈ 3.6 × 10⁹ runs, about 40 minutes, checkpointable), and both wheels arbitrary.
