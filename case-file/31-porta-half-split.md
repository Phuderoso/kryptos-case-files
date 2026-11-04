# Case file 31 — Porta: the reciprocal tableau, behind the themed transpositions

*Cycle 32, 2026-11-04. Status: **negative** for periodic keys of length 1–26; **no signal** for running keys from six books; controls recovered.*

## 1. Why this
Porta (Giovan Battista della Porta, 1563) had never been tested in this file. It is the classic "simple thing" an artist could do by hand: 13 key values, each one swapping the first half of an alphabet with the second half. It is reciprocal, so encrypting and decrypting are the same act, a property Scheidt-style "masking" lectures like. With a KRYPTOS-keyed alphabet in place of A–Z it is a natural sibling of K1/K2's tableau.

## 2. The structural shortcut
In any Porta-type cipher a letter in one half always enciphers to a letter in the *other* half, **whatever the key**. So for a given transposition and alphabet, all 24 crib pairs must cross halves. That test needs no key at all, so it covers periodic keys, running keys, autokeys and random keys alike. Only configurations that pass go on to key tests.

## 3. Model
- Transpositions: the 96,630 of cycle 12 (identity, columnar w ≤ 8 all orders, keyword columnar 9–20, routes, K3 rotations incl. one-dropped-letter), each direction.
- Alphabets: the 20,946 themed orderings (AZ, KA, reverses, keyed/columnar alphabets of the plain-sight words and word pairs). Halves = first 13 / last 13 letters of the ordering.
- Two Porta variants (H1[i] ↔ H2[(i+k) mod 13] and H1[i] ↔ H2[(k−i) mod 13]); key indexed by plaintext position or by carved position.

## 4. Results ([report](../analysis/porta_report.txt))
| Test | K4 | Shuffled-K4 nulls | Planted controls |
|---|---|---|---|
| Half-cross survivors (any key) | 14 | 12–553 (10 nulls) | 267 / 1,175 |
| Periodic key, L ≤ 12 | 0 | 0 in all 10 | 2/2 recovered (PALIMPSEST L=10, CLOCK L=5) |
| Periodic key, L 13–26 | 0 | — | — |
| Running key (6 books) on survivors | best 12/24 | 12–13 | 24/24 at exact offset |

Period 27+ "hits" are empty: the two crib blocks then share no key residue, so any key fits. They are reported but carry no information.

## 5. Verdict
Porta (both variants, both key-index frames) with any of the themed alphabets, behind any of the cycle-12 transpositions, is **excluded for key lengths 1–26**. With a non-periodic key only 14 configurations remain (fewer than most shuffled nulls), and English running keys from the six local books score at chance on them. The 14 cluster on one column order (col7 0635142) with PALIMPSEST-derived alphabets; these alphabets are near-duplicates, so the cluster is one configuration seen several times, not a pattern.

## 6. Limits
Halves are always the first/last 13 of the ordering (an interleaved split such as odd/even positions is untested). Running-key corpora are only six books. Transposition family as in cycle 12, nothing larger.
