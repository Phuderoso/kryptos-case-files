# Case file 117 — The periodic Gromark (cycle 129)

**Family:** ACA Periodic Gromark (new to this repo; cycles 10, 11, 11b and 65 tested ordinary Gromark, where the key is pure digits).

## The cipher
The ACA rule (cryptogram.org, Periodic Gromark): write the keyword-mixed alphabet under the keyword (repeats removed) and read it off by columns in key order; that is the cipher alphabet. The keyword's numerical key is the primer, extended by chain addition (next digit = sum of the first two digits of the current window, mod 10). The text is cut into groups as long as the keyword; group g starts the cipher alphabet at the position of keyword letter g, and each letter is shifted further by its digit. The keyword offsets push the key off the 0–9 window, so the "any digit key" proof of cycle 11 does not cover it.

Our generator reproduces the ACA's ENIGMA worked example letter for letter: `WINTRYSHOWERS...` → `RHNAAX NRUZBN IUARXC ... TLUD`.

## What was tested
- **Keywords:** the themed list from `tools/dcol_gen.py`, the 10,056-word vocabulary of cycle 56 and every ordered pair of themed words, 3–12 distinct letters: 17,164 keywords.
- **Alphabets:** cipher alphabet = ACA columnar (the rule), plain keyword-mixed, or KRYPTOS; plaintext alphabet A–Z or KRYPTOS. That gives 102,984 key streams.
- **Layers:** direct, and behind all 165,065 bank transpositions (both directions), key before (model A) or after (model B) the transposition, Vigenère (ACA) or Beaufort form.
- **Size:** 1.36 × 10¹¹ exact tests against all 24 crib letters.

## Result
| text | survivors |
|---|---|
| K4 | **0** |
| shuffled null 1 | 0 |
| shuffled null 2 | 0 |
| planted controls | 4/4 recovered (direct ACA; model A with KRYPTOS alphabets; model B Beaufort; model A through an inverse perm) |

With no free parameters once the keyword is fixed, the chance of a false survivor is about 10⁻²³ per test, so zero survivors on the nulls is expected and any K4 hit would have meant something. There is none. **Negative.**

## What stays open
- The periodic Gromark with a keyword that is not in the lists: both the alphabet and the offsets are then unknown, which suits a SAT model (cipher alphabet arbitrary, L offsets, primer of length L).
- Behind width ≥ 9 arbitrary column orders rather than the bank.
- Primers of other bases (the ACA notes base-10 only).
