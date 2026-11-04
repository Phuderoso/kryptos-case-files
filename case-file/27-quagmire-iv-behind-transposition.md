# 27 — Quagmire IV behind a transposition (cycle 28)

> *Two alphabets, two keywords, one on each side of the table. The man who taught K1 and K2 to talk only ever used one. I checked whether he'd brought a friend.*

## 1. Why this test
- K1 and K2 use one KRYPTOS-keyed alphabet on both sides (Quagmire III). Cycle 13 ([case file 12](12-strips-and-periodic-keys.md)) tested Quagmire I, II and III with any periodic key (p ≤ 16) behind about 244k transpositions: 0 survivors.
- What was **not** tested behind a transposition is **Quagmire IV**: a different keyed alphabet on the plaintext side and on the ciphertext side. [kryptosbot's findings page](https://www.kryptosbot.com/findings/) (status Sept 29, 2026) also lists "repeating keys with two different keyword-mixed alphabets" as only partly tested, even directly on the carved text.
- Cycle 11b ([case file 11](11-sat-families-and-phrase-alphabets.md)) covered **arbitrary** alphabet pairs directly on the copper (periods 1–7 impossible). This cycle restricts to themed keyword alphabets but undoes a transposition first, which SAT on arbitrary alphabets can't afford.

## 2. Method (`tools/q4_perm.c`, `tools/q4_alphabets.py`)
- **Alphabets:** 268 keyword alphabets (keyword letters, then the rest of A–Z) and their reverses, from 136 distinct theme words: K1–K3 keys and odd spellings, Berlin/World Clock, Egypt/Carter, CIA/Langley, sculpture materials, compass words, cipher vocabulary ([list](../analysis/q4_alpha_names.txt)). Every ordered pair with PA ≠ CA, neither plain A–Z (those cases were cycle 13's): 71,556 pairs.
- **Transpositions:** cycle 19's family, 165,065 including identity (all column orders w ≤ 8, K3-style single and double rotations, inverses).
- **Modes:** Vigenère-type (k = C − P, the same consistency test as variant Beaufort) and Beaufort (k = C + P); key indexed by plaintext position (substitute, then transpose) or carved position (transpose, then substitute).
- **Test:** exact. For period p = 1–16 the 24 crib key values must agree inside every residue class. 7.56 × 10¹¹ tests per text.
- **Chance level:** a random config at period p survives with probability about 26^−(24−p). At p = 16 that predicts about 0.2 chance survivors per text (survivors come in groups of 4, because reversed alphabets give equivalent Vigenère/Beaufort pairs); p ≤ 15 should give none.

## 3. Results ([report](../analysis/q4_perm_report.txt))
| Text | Survivors p = 1–15 | p = 16 |
|---|---|---|
| **K4** | **0** | **0** |
| Shuffled null 1 | 0 | 0 |
| Shuffled null 2 | 0 | 0 |
| Shuffled null 3 | 0 | 4 (one equivalent group, t = 122945; chance level as predicted) |
| Control 1: PALIMPSEST → SHADOW, Vigenère, key CLOCK, PT-indexed, transposition 5000 | recovered: only t = 5000, key CLOCK at p = 5 (and 10, 15) | |
| Control 2: BERLIN reversed → KRYPTOS, Beaufort, key LAYERTWO, carved-indexed, transposition 120000 | recovered: only t = 120000, key LAYERTWO at p = 8 (and 16) | |
| Control 3: LUCID → ABSCISSA, Vigenère, key IQLUSION, no transposition | recovered at identity, key IQLUSION at p = 8; also at t = 93174, which equals identity on all 24 crib positions (indistinguishable), plus one p = 16 group at t = 104722, which shares 20 of 24 crib positions | |

All hits of the controls sit on the planted transposition (or ones identical to it at the cribs) with the planted key word, so the tool finds what it should.

## 4. Verdict
| Hypothesis | Status |
|---|---|
| Quagmire IV (two different themed keyword alphabets) with a periodic key p ≤ 16, directly on the copper | **negative** (identity is in the family) |
| Same, behind or in front of the cycle 19 transposition family | **negative** (0 survivors; nulls at chance; 3/3 controls) |
| Quagmire IV with arbitrary (non-keyword) alphabets behind a transposition | **open** (too large for exact SAT per transposition here) |

## 5. Honest limits
- The alphabet list is themed, not exhaustive: a keyword not in it is untested. Two-word keyphrase alphabets (cycle 11b's 31k list) were not paired here; 31k² pairs × 165k transpositions is out of reach for exact enumeration.
- Periods 17–26 were skipped: at those periods chance survivors appear by the dozen and the test loses power.
- Transposition families outside cycle 19's set remain open.
