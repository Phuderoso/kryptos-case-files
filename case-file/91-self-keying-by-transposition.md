# 91 — Self-keying by transposition (cycle 98)
> *What if K4 brought its own key: the message, or its ciphertext, written out again in a grid's order and added to itself?*

## 1. Idea
A "layers of something simple" scheme that no earlier case file covers. The key for position *i* is not a book, a keyword or an autokey lag, but the text itself read through a permutation σ, such as a K3-style grid, a decimation or a route:

- **Model C (ciphertext keys itself):** `P[i] = dec(C[i], C[σ(i)])`. Ciphertext autokey is the special case σ(i) = i − L. Decryption is direct, so every crib letter is a check: 24 exact checks per configuration.
- **Model P (plaintext keys itself):** `C[i] = enc(P[i], P[σ(i)])`. Easy to encipher by hand: write the plaintext out a second time in the grid's order and add. To decipher, walk each cycle of σ: one crib letter fixes its whole cycle, and every other crib on the cycle plus the cycle's closure is a check, so each configuration gets 24 checks. A crib-free cycle stays unknown (`?`).

Tableaux: straight A–Z and KRYPTOS-keyed (index arithmetic on the alphabet). Modes: Vigenère (c = p + k), Beaufort (c = k − p), variant (c = p − k).

## 2. Permutations (each used as σ and as σ⁻¹)
- 165,065 transpositions (columnar w 2–8, K3-style rotations, inverses, identity; the cycle 19 family)
- 159,712 K3-law decimations (cycle 59), 6,070 spiral/diagonal/K3-grid routes (cycle 61)
- 9,409 affine maps i ↦ a·i + b mod 97 and reflections i ↦ b − i (this includes "the ciphertext read backwards" and every cyclic shift, which differs from autokey because it wraps)

That is 340,256 permutations × 2 directions × 2 tableaux × 3 modes = **4,083,072 configurations per model**, about 3 seconds in C (`tools/cycle98/selfkey.c`).

## 3. Controls and nulls (`analysis/cycle98_selfkey_report.txt`)
- **Planted:** an English 97-letter plaintext carrying both cribs, enciphered with 4 Model P and 4 Model C configurations (all 4 permutation families, both tableaux, all 3 modes). **8 of 8 recovered** with all 24 checks. Model P returns the readable plaintext with `?` only on crib-free cycles. Model C plants come back with the exact text; because Model C only reads σ at the 24 crib positions, many permutations in the 165k family agree there (one control returned 240 distinct near-identical texts), so a real hit would need English scoring to pick its grid, not to be found.
- **Shuffled K4 ×5:** Model C best 7–10 of 24 checks; Model P at least 15 failed checks. No hits.

## 4. Result on K4
| Model | Best on K4 | Nulls | Hit threshold |
|---|---|---|---|
| C (ciphertext self-key) | 9 / 24 | 7–10 / 24 | ≥ 20 / 24 |
| P (plaintext self-key) | 17 failed checks at best | 15–16 failed | ≤ 1 failed with ≥ 8 checks |

**0 hits.** K4 sits squarely inside the null distribution.

## 5. Verdict
| Hypothesis | Status |
|---|---|
| K4 = plaintext + plaintext read through a columnar/K3 rotation, decimation, route or affine map (A–Z/KRYPTOS tableau, Vig/Beau/variant) | **negative** |
| K4 deciphers as ciphertext minus ciphertext read through the same permutations | **negative** |
| Self-key on a mixed (non-KRYPTOS) alphabet; self-key + periodic keyword; a self-key and a transposition in sequence; σ outside these families (e.g. Myszkowski, turning grille) | open |

Caveat: Model P with Vigenère has a parity weakness on odd cycles (closure gives `2·P = S`, a mod-2 ambiguity), so closure checks there are weaker than 1/26. The shuffled nulls measure the real false-positive level, and K4 does not exceed it.
