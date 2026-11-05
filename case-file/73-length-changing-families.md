# 73 — Length-changing families: the counting lemma, and nulls outside the cribs (cycle 75)

**Type:** new family/structure (diversity rule: cycle 74 was an audit, so 75 must be new).

## Part A — expanding schemes: a counting lemma (proof, no search)
Sanborn's clues are positional: carved letters 22–34 (1-based) *are* EASTNORTHEAST and 64–74 *are* BERLINCLOCK,
13 and 11 carved slots. Any scheme whose ciphertext for a crib needs more than one symbol per plaintext letter is
impossible as K4's final layer, whatever the key, alphabet or re-lettering step, unless a later transposition
moves symbols (then the clue would not name contiguous carved runs).

| Scheme (symbols per crib) | EASTNORTHEAST needs | BERLINCLOCK needs | slots | verdict |
|---|---|---|---|---|
| Pollux (one digit per Morse symbol or gap) | ≥ 39 | ≥ 44 | 13 / 11 | impossible |
| Morbit (one digit per pair of Morse symbols/gaps) | ≥ 20 | ≥ 22 | 13 / 11 | impossible |
| Fractionated Morse (cycle 73, three per letter) | ≥ 39 | ≥ 44 symbols = 15 letters | 13 / 11 | impossible (cycle 73) |
| Polybius, ADFGX/ADFGVX, Nihilist substitution, Grandpré, any 2-symbol coordinate output | 26 | 22 | 13 / 11 | impossible |
| Straddling checkerboard (≥ 1 digit per letter; 2 for all but ~8 letters) | > 13 unless all 13 crib letters are 1-digit letters | > 11 likewise | 13 / 11 | impossible: the two cribs use 13 distinct letters, a checkerboard has at most 8 one-digit letters |

Independently, **97 is prime**, so no uniform k-symbols-per-letter expansion (k ≥ 2) produces 97 symbols.
Morse lengths are computed by `tools/cycle75/nulls75.py` (`lemma()`), output in `analysis/cycle75_k4.json`.

The checkerboard row is a counting argument too: the two cribs together use 13 distinct letters
(A B C E H I K L N O R S T); a checkerboard has at most 8 single-digit letters. (EASTNORTHEAST alone uses exactly 8,
E A S T N O R H, so it could fit by itself; BERLINCLOCK adds B, L, I, C, K and cannot.)

## Part B — length-reducing: null letters anywhere outside the crib spans (exact search)
The surviving length-changing structure is the opposite one: the carved text is *longer* than the plaintext because
null letters were dropped in (a K2-style "in plain sight" trick). Cycle 9 (case file 07) tested only W as the null.
Here nulls may sit **anywhere** outside the two crib runs, in any number: `a` in slots 1–21, `b` in 35–63, `c` in 75–97.
The key runs over the plaintext stream (nulls skipped), so crib 1 sits at plaintext index 21−a and crib 2 at 63−a−b.
The phase `a` never changes consistency, and `c` is irrelevant; only `b` (0–29) matters.

- **Fixed tableau:** A–Z or KRYPTOS alphabet × Vigenère/Beaufort/variant × period 1–26 × b 0–29 (4,680 configurations),
  exact crib check.
- **Arbitrary alphabets:** each key class mod p its own unknown substitution (the most general periodic substitution),
  exact injectivity check, p 1–26 × b 0–29.

### Controls (planted, `tools/cycle75/controls75.py`, `analysis/cycle75_controls.json`)
English plaintext with both cribs at the official **carved** positions after random null insertion:
KA Vigenère p 7 key SHADOWS with (a, b, c) = (4, 9, 6); AZ Beaufort p 11 with (2, 0, 9); arbitrary alphabets
p 5 with b 12; arbitrary alphabets p 6 with b 20. **4/4 recovered** at the planted (p, b); control 0 decrypted back
to all 78 planted plaintext letters from the recovered key and the planted null slots.

### Result for K4 (`analysis/cycle75_k4.json`, baselines `analysis/cycle75_baseline.json`, 500 shuffles)
- **Fixed tableau:** 0 consistent configurations at p ≤ 23 for any number and placement of nulls. Survivors only at
  p 24–26 (72), where 24 crib letters barely touch the key; shuffled K4 gives the same (mean 74.8, minimum p 22–24).
  **Excluded p ≤ 23; p 24–26 untestable by the cribs.**
- **Arbitrary alphabets:** p ≤ 5 impossible for every null arrangement. p 6 survives only at b ≡ 5 (mod 6)
  (b = 5, 11, 17, 23, 29); 41.6% of shuffled texts also have p 6 survivors and 1.2% even reach p 5, so this is
  chance. p ≥ 7: cribs give no power. **Negative for p ≤ 5, chance at 6, untestable above.**

## Verdict
Every expanding scheme is closed by counting. Null insertion outside the cribs does not rescue a periodic
tableau cipher (p ≤ 23). Open: nulls **plus** a transposition layer, and nulls with a non-periodic (running/autokey) key;
the cribs cannot test arbitrary-alphabet periods ≥ 7 with or without nulls.
