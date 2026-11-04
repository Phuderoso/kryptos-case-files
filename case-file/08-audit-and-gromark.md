# 08 — Audit of cycles 1–9, and Bean's Gromark lead (cycle 10)

> *Before chasing the next suspect, I re-read my own notebook with a red pen. Then I went after the one lead with a real pedigree: Richard Bean's Gromark.*

## A. Audit (`tools/audit_cycle10.py` → `analysis/audit_cycle10.txt`)
| # | Assumption | Check | Result |
|---|---|---|---|
| 1 | K4 text: 97 letters, OBKR…KCAR | matched against the tail of Elonka's panel transcript and both Antipodes copies | **PASS** |
| 2 | Crib indexing | code uses a 0-based dict `KN` = 21..33 EASTNORTHEAST, 63..73 BERLINCLOCK, i.e. 1-based **22–34 / 64–74**. The ciphertext under them is FLRVQQPRNGKSS / NYPVTTMZFPK, Sanborn's published pairs | **PASS** |
| 3 | Alphabet KA | KRYPTOSABCDEFGHIJLMNQUVWXZ = keyed("KRYPTOS") | **PASS** |
| 4 | Vigenère direction and K3 rotation | K1, K2 and K3 all decrypt correctly with the same code | **PASS** |
| 5 | Mode definitions | the same in every tool: vig c=p+k, beau c=k−p, varbeau c=p−k | **PASS**, with one gap: cycle 9 H9 (running keys) skipped variant Beaufort. Variant Beaufort only matters when the key is fixed (words, running keys). **Rerun: 243,700 tests, 0 survivors**, so the conclusion is unchanged |
| 6 | "Pure transposition impossible" | the cribs need E×3; K4 has E×2. This is the only shortfall, and it alone proves the claim | **PASS** |
| 7 | Cycle 9 W positions and segments | W at 21, 37, 49, 59, 75 (1-based); segment lengths sum to 97 with the 5 W's | **PASS** |
| 8 | Control strength | **Limitation, not a bug.** Every control plants a member of the family being searched, at the true crib positions. So controls prove the code and gate work. They do not prove a family would be *found* if K4 used an unlisted variant | documented |

No other off-by-one was found. Earlier tables stand. The only correction is the H9 note in 07.

## B. Bean's Gromark lead
**Model (Hall 1969, ACA).** The key digits come from a primer expanded by lagged Fibonacci: k_n = k_{n−L} + k_{n−L+1} (mod base). Encryption is c_i = CA[(PA⁻¹(p_i) + k_i) mod 26].

**1. Reproduction.**
- I compiled Bean's own [`gt.c`](https://github.com/RichardBean/k4testing) and ran it: **39 primers** (base 10, length 5).
- My independent solver (`tools/gromark_alphabet.py`) found **the same 39**. It treats the problem as a constraint graph with unknown plain and cipher alphabets, using union-find with offsets mod 26 plus an injectivity check.
- Reproduction confirmed.

**2. Partial alphabet recovery, standard ACA style** (plain alphabet = A–Z, cipher alphabet unknown):
- **0 of the 39 primers are feasible.** This was extended over bases 5–10 and primer lengths 4–6 (`tools/gromark_extend.py`): **0 feasible with an A–Z plain alphabet in every case**.
- The same holds for a KA plain alphabet and for the "count left" direction.
- Control: primer 27182 with cipher alphabet = ACA-columnar(SHADOW) was recovered as the unique hit, along with its partial cipher alphabet `.E...FM..CK..OGNVS.JQYW...`, which matches the planted alphabet letter for letter.
- **Result:** if K4 is a Gromark at all, it is not the textbook ACA Gromark. *Both* alphabets would have to be mixed.

**3. Base 5, the Berlin-clock base:** 0 primers feasible even with *any* alphabets, for primer lengths 4–6.

**4. Keyword-derived alphabets.** `tools/gromark_keyword.py`:
- **Candidates:** 66,081 distinct alphabets. They come from AZ, KA, ZA, plus keyed, reversed-keyed and ACA-columnar alphabets for every word of 3–14 letters in the 5-book Gutenberg vocabulary and the cycle-7 plain-sight words.
- **Search:** each alphabet was tried as the plain alphabet *and* as the cipher alphabet, against all 39 primers. That is **1.7×10¹¹ (PA, CA, primer) combinations**, checked exactly by hashing normalised crib vectors.
- **Hits: 0.**
- Control: PA = keyed(LANTERN), CA = ACA-columnar(COMPASS), primer 27182 was recovered uniquely, and its decrypt scores −4.01 per character (English range).
- **Logic:** the 39 primers are *exhaustive* for base 10, length 5. Any alphabet pair that works must sit on one of them, so this search covers every keyword alphabet in that vocabulary.

**5. English readability.** No candidate survived, so there was nothing to score. The scoring code is in place and validated by the control.

## Interpretation (labelled)
- **Fact:** Bean's 39 are reproduced. **Fact:** the standard-plain Gromark is impossible for bases 5–10 with primers of length 4–6.
- **Inference:** a Gromark explanation now needs two independently mixed alphabets that don't come from any ordinary keyword. That is less "simple, memorable, pencil-and-paper" than Scheidt described. It lowers my prior on Gromark, but doesn't kill it.
- **Open:**
  - alphabets made from multi-word keyphrases or other non-dictionary keys;
  - Gromark variants with other key generators (e.g. base conversion of a keyword number, which the "change the base" hint might mean);
  - Bean's own seriated and other hypotheses.
