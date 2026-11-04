# 07 — Creative synthesis (cycle 9)

> *For eight cycles I knocked on every door in the building. This time the brief was different: think like a scientist. Work out first which door the architect would have used, then knock once, with a witness standing by (a planted control).*

## 1. The field, 2023–2026 (sources opened this cycle)
- **K4's plaintext is known, but not public.**
  - In Sept 2025 Jarett Kobek and Richard Byrne found the plaintext among Sanborn's papers at the Smithsonian's Archives of American Art. Sanborn confirmed it, and the files are sealed for 50 years. They did not find a method. Sources: [Scientific American](https://www.scientificamerican.com/article/a-solution-to-the-cias-kryptos-code-is-found-after-35-years/), [WIRED](https://www.wired.com/story/kryptos-code-reveal/).
  - The archive, including "the original K4 coding system", sold for $962,500 on 2025-11-20 ([RR Auction](https://content.rrauction.com/jim-sanborns-complete-kryptos-archive-sells-for-962500-at-auction/)).
  - The buyer is **Paradigm**. It now vets guesses by hash, at $1 per submission ([WIRED, 2026-06-12](https://www.wired.com/story/crypto-guys-bought-the-answer-to-the-cias-mysterious-kryptos-sculpture/)). *We submit nothing, per the case rules.*
- **The lot description has a telling detail:** "the original **scrambled texts** shown to the Department of Historical Intelligence" ([RR lot](https://www.rrauction.com/auctions/lot-detail/350761607302001-the-complete-secrets-of-kryptos-jim-sanborns-private-archive/)). This matches Sanborn's 2009 phrase, the text was "scrambled by a coding system that would unravel itself slowly" ([hint compilation](https://kryptools.com.about.ag/hints.htm)).
- **AI and LLMs:** Sanborn reports a flood of chatbot "solutions", all wrong: "AI lies, and does not have enough info" ([WIRED 2025](https://www.wired.com/story/plaintext-kryptos-code-artificial-intelligence/), [NYT via jimsanborn.net](https://jimsanborn.net/assets/press/A_Solution_to_the_C.I_A.%E2%80%99s_%E2%80%98Kryptos%E2%80%99_Sculpture_Goes_Up_for_Auction_-_The_New_York_Times.pdf)). **Lesson:** the only useful role for an LLM here is generating hypotheses and writing code that is then checked against the cribs, which is how this repo works.
- **The expert consensus I could verify:**
  - Bean (HistoCrypt 2021) ran Monte Carlo permutation tests. They give strong evidence of a **one-to-one letter correspondence (no transposition)**. He proposes the **Gromark** cipher (Gillogly suggested it in 1999–2004). His `gt.c` finds 39 base-10 primers fitting the cribs with *some* cipher alphabet. Sources: [paper](https://richardbean.id.au/papers/03_Bean_HistoCrypt2021.pdf), [code](https://github.com/RichardBean/k4testing).
  - Scheidt says English frequencies were **deliberately masked** ([NPR](https://thin.npr.org/4684720)). He also hinted at **changing the base** (2015/2020, quoted in Bean's paper; [2015 transcript](https://richardbean.id.au/misc/kryptos/scheidt2015.txt)).
  - *Not verified this cycle:* a "2025 letter" with further method details, and any exact Sanborn quote that the method is "not in K1–K3". I do not rely on either.

## 2. How K3 *should* have been solved, and what that implies for K4
- **K3 by insight.** K3 is 336 letters, and 336 = 24×14 = 8×42. It is a transposition, because its letter frequencies are plain English. The length invites grids, and two rotations solve it (`rot_dec(rot_dec(ct,24),8)`). The method is visible in the text's statistics and arithmetic.
- **The same diagnosis applied to K4:**
  - (a) K4 is 97 letters, and 97 is prime. Bean's statistics say no transposition, which agrees with the primality: no grid fits.
  - (b) It is *not* plain English by frequency, so there is a substitution with masking.
  - (c) Adding the '?' before OBKR gives 98 = 7×14. I tested that grid idea anyway (H11).
- **The W observation.** K4 has W at **21, 37, 49, 59, 75** (verified). W at 21 sits directly before EAST (22), and W at 75 directly after CLOCK (74). The segments between W's have lengths 20, 15, 11, 9, 15, 22, so both crib segments are 15 long.
  - **Measured** (`tools/w_bracket_test.py`): P(≥2 W in the 4 crib-boundary slots) = 0.013. But P(*any* letter doing that) = 0.20.
  - **Verdict:** suggestive, **not significant** once the look-elsewhere effect is counted. I still tested it, because it is cheap.

## 3. Lessons from puzzles that were brute-forced
- **Z340, 2020** ([arXiv 2403.17350](https://arxiv.org/abs/2403.17350)): a *statistical phenomenon* (bigram repeats at period 19) pointed to the structure. Computation (AZdecrypt over 655k transposition variants) finished the job, and encoder errors had hidden the near-miss for years. **Lesson:** diagnose first, then search a small space chosen by the phenomenon, and allow for encoder errors. *K4 analogue:* Bean's one-to-one result.
- **Chaocipher:** unbroken for 92 years. The method was revealed in 2010 from Byrne's family papers ([Rubin](https://www.chaocipher.com/ActualChaocipher/Chaocipher-Revealed-Algorithm.pdf)). It is a *dynamic* alphabet, which defeats periodic analysis. **Lesson:** a simple hand mechanism can sit outside every standard family. *K4 analogue:* the archive holds "the original K4 coding system".
- **Beale B2:** the key was a plain-sight document (the Declaration of Independence) used as a book cipher. **Lesson:** test plain-sight running keys (H9).
- **Dorabella, Voynich, Cicada:** many confident "solutions" never verified. **Lesson:** require a gate and a control. That is exactly the failure mode Sanborn describes in AI submissions.

## 4. Ranked hypotheses and exact tests (`tools/k4_creative.py`)
Every survivor must reproduce all 24 crib letters. Alphabets: AZ, KA, and the keyed PALIMPSEST/ABSCISSA/BERLINCLOCK alphabets, used as plain and cipher alphabets. Modes: Vigenère and Beaufort.

| Rank | Hypothesis (why plausible) | Tests | Survivors |
|---|---|---|---|
| 1 | **H1 Gromark base 10, primer 5** (Bean; Scheidt "base"), 25 alphabet pairs × 26 slides | 130,000,000 | **0** |
| 2 | **H2 Gromark base 5** (Berlin-clock base) and bases 2–9, primers 2–6 | 232,308,544 | **0** |
| 3 | H3 Gromark base 10, primer lengths 2,3,4,6 | 210,308,800 | **0** |
| 4 | H4 W = separator, keyword restarts after each W (any length 1–26) or progressive per segment | 2,600 | **0** |
| 5 | H5 W = nulls removed, then periodic P1–26 or Gromark b5/b10 | 21,451,300 | **0** |
| 6 | H6 each W-segment has its own Caesar shift | 50 | **0** |
| 7 | H7 progressive / stepped "clock-hand" key a+s·⌊i/m⌋ | 30,000 | **0** |
| 8 | H8 Mengenlehreuhr lamp count, from any start minute (step 1/5/15/60 min) | 1,152,000 | **0** |
| 9 | H9 running key from K1/K2/K3 plaintexts, ciphertexts, tableau (± reversed) | 487,400 | **0** |
| 10 | H10 ciphertext feedback / lagged self-key d=1..30 | 3,120 | **0** |
| 11 | H11 '?'+K4 = 98 = 7×14, K3-style rotations then periodic sub | 16,640 | **0** |
| 12 | Mengenlehreuhr row digits of a fixed time as the key | – | *reduces to period 4 → excluded in cycle 1* |
| 13 | World-Clock zone offsets as a repeating shift list | – | *reduces to period ≤24 → excluded in cycle 1* |
| 14 | **Gromark with an unknown keyed cipher alphabet** (Bean's 39 primers) | – | **OPEN**: this cycle only tested plain-sight alphabets |
| 15 | Dynamic-alphabet hand cipher (Chaocipher-like) driven by KRYPTOS | – | **OPEN**: needs a definite mechanism to test |

**Total:** 595,760,454 exact tests, **0 survivors**.

**Planted controls** (`analysis/k4_creative_control.txt`), each recovered at its exact parameters:
- H1: primer 31415, AZ→KA, slide 3.
- H2: base 5, KA Beaufort.
- H4: W-restart with SHADOWFORCES.
- H8: lamps from t0=600, step 5, ×7, +4.
- H9: running key from K3 plaintext at offset 200.
- H11: rotation (7,14) plus ABSCISSA.

## 5. Interpretation (labelled inference)
- **Gromark with any plain-sight alphabet is now excluded**, in bases 2–10 with primers 2–6. If Bean's Gromark is right, the cipher alphabet is something non-obvious. That fits Scheidt's "masking", and it moves the question to *how the alphabet was built* (rank 14).
- The W brackets around the cribs are worth remembering, but they are not statistically significant. Simple W-separator models fail.
- **Strongest remaining line:** Bean-style diagnosis says one-to-one, and the RR lot mentions a "coding system" plus "scrambled texts". Together they point to a hand substitution whose key state changes in a non-periodic way. That is a family I have not yet pinned to a definite, testable mechanism.
