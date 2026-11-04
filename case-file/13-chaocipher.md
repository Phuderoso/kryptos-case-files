# 13 — A dynamic alphabet: Chaocipher on K4 (cycle 14)
> *Every key I've tried so far sat still while the letters walked past it. This one moves with every step. The question was whether it had ever been on K4's street.*

## 1. Why this, why now
Cycle 13 closed the "one transposition + one periodic or small-digit key" story for every transposition family tested so far, and ended on: *what's left wants a key that doesn't repeat.* [Case file 07](07-creative-synthesis.md) (hypothesis 15) listed a Chaocipher-like dynamic alphabet as **open, needs a definite mechanism**. Chaocipher is that mechanism: a hand cipher by J. F. Byrne (1918), unbroken until the algorithm was published in 2010 ([Rubin, *Chaocipher Revealed: The Algorithm*](https://www.chaocipher.com/ActualChaocipher/Chaocipher-Revealed-Algorithm.pdf)). Two mixed alphabets (cipher "left", plain "right") are permuted after every letter, so the key never repeats and periodic tests (all of cycles 1–13 and the SAT proofs in [case file 11](11-sat-families-and-phrase-alphabets.md)) say nothing about it. It also fits the [style profile](10-style-profile.md): a hand method, keyword alphabets of the KRYPTOS kind, and a "change" at every step.

**HYPOTHESIS C1.** K4 = Chaocipher with two starting alphabets taken from Kryptos' own keyword alphabets (KRYPTOS, PALIMPSEST, ABSCISSA, SHADOW, BERLINCLOCK, …), possibly combined with one transposition.
**Falsification:** the 24 crib letters (EASTNORTHEAST at 22–34, BERLINCLOCK at 64–74, 1-based) must all appear at the official positions.

## 2. Tool (`tools/c/chao.c`, controls in `tools/chao_control.py`)
- Algorithm exactly as Rubin: find the letter, read the other alphabet at the same index; left alphabet rotated so the cipher letter is at the zenith and the letter at zenith+1 moved to the nadir; right alphabet rotated so the plain letter is at the zenith, one further step, then zenith+2 moved to the nadir.
- Start state: left = alphabet *a*, right = alphabet *b*, plus the relative offset of the two wheels (26 values). Both directions: carved = encrypt(text), or carved = decrypt(text) (the device run backwards).
- Alphabets: the 264 themed single-word alphabets from cycle 12 (`data/tw_alpha.bin`: AZ, KA, ZA, AK, then keyword/reversed/column forms of PALIMPSEST, ABSCISSA, SHADOW, LUCID, MEMORY, POSITION, BERLIN, CLOCK, BERLINCLOCK, EGYPT, LAYERTWO, …).
- Three layer orders: Chaocipher alone; transpose then Chaocipher (`tb`); Chaocipher then transpose (`ta`). Transpositions are cycle 12's 96,630 (columnar ≤ 8 in every order, keyword columnar, routes, K3 double rotations incl. one omitted letter) and cycle 13's 147,709 strip transpositions.

## 3. Controls ([chao_control.txt](../analysis/chao_control.txt))
- Rubin's published test vector: WELLDONEISBETTERTHANWELLSAID → OAHQHCNYNXTSZJRRHJBYHQKSOUJY, and back. **PASS.**
- Planted text with the cribs at K4's positions, Chaocipher with left = KRYPTOS alphabet, right = PALIMPSEST keyword alphabet, offset 7: recovered as the **only** 24/24 hit alone, after a cycle-12 transposition (`tb`), and before one (`ta`). **PASS** (3/3).

## 4. Results
| Test | Runs | Result |
|---|---|---|
| Chaocipher alone, 264 × 264 alphabets × 26 offsets × 2 directions ([report](../analysis/chao_plain_report.txt)) | 3,624,192 | best **9/24**; histogram identical to three shuffled-K4 nulls (9, 8, 8 best). **Chance.** |
| Transpose, then Chaocipher: first 100 themed alphabets (all pairs) × 96,630 cycle-12 transpositions ([report](../analysis/chao_transposed_report.txt)) | 5.0 × 10¹⁰ | **0** pass even EASTNORTHEAST |
| Same × 147,709 strip transpositions | 7.7 × 10¹⁰ | **0** |
| Chaocipher, then transpose: first 16 themed alphabets (AZ, KA, ZA, AK, KRYPTOS, PALIMPSEST ×3, ABSCISSA ×3, SHADOW ×3, LUCID ×2) × 96,630 transpositions | 1.3 × 10⁹ | **0** |

A random start state matches all 24 cribs with probability about 26⁻²⁴, so any hit would have been decisive; none came.

## 5. Verdict and limits
| Hypothesis | Status |
|---|---|
| C1: Chaocipher with themed keyword starting alphabets, no transposition | **negative** (at chance) |
| C1 + transposition (cycle 12–13 families), themed alphabets as listed | **negative** |
| Chaocipher with **arbitrary** starting alphabets | **open**: (26!)² states can't be enumerated; would need a crib-driven state-recovery attack (the published known-plaintext attacks need long contiguous plaintext, and K4 gives 13 + 11 letters) |
| Other dynamic-alphabet hand ciphers (different permutation rule, one wheel only, Kryptos-tableau "slides") | **open** |

Gaps worth stating plainly: `ta` used only 16 alphabets (cost: a sequential decrypt per transposition), `tb` 100 of 264; strip transpositions weren't used in `ta` because they are only defined on the crib positions.
