# 81 — Playfair with an arbitrary square under a periodic key (cycle 83)

> *Cycle 82 only questioned Playfairs who kept their square in a dictionary. This time the square could be anything at all — any 25 letters, any order — and I let a SAT solver look for one.*

## Why this idea (and not the "halfabet")
Cycle 82 left two cheap next steps. The **halfabet** (a key acting mod 13 inside each half of the KA alphabet) keeps every letter in its own half, so it is a key-free yes/no screen on the 24 crib letters, very close to cycle 32's Porta screen (which asked the opposite question: must every letter cross halves?). It would close quickly, but it is one narrow member of a family the repo has already probed. **Arbitrary-square Playfair** is the biggest hole cycle 82 left open: 25!/25 squares can't be enumerated, the word-square test said nothing about them, and a proof here covers every square anyone could have used, keyword or not. So cycle 83 extends cycle 82 (allowed by the diversity rule) with that one idea. The halfabet stays on the list.

## Model
Plaintext → **Playfair** on a 5×5 square holding **any 25 of the 26 letters in any arrangement** (the omitted letter is free; it just can't be one of the crib letters) → **periodic Vigenère / Beaufort / variant** (c = q + k, c = k − q, c = q − k) on the **KA or A–Z tableau**, period p. Pairs start at even or at odd positions (0-indexed; both alignments). The cribs are EASTNORTHEAST at 22–34 and BERLINCLOCK at 64–74 (1-indexed), the repo's convention.

## Exact test (SAT, `tools/cycle83/sat83.py`)
The square, the omitted letter and the p key letters are all free variables (CaDiCaL 1.5.3 via PySAT). Constraints:
- **all 13 Playfair pairs that touch a crib**: 11 pairs with both letters known, plus the 2 half pairs at the crib edges, where the unknown plaintext partner is a free letter. Each must follow the row, column or rectangle rule into the inner letters that the key produces;
- for p ≤ 13 the key is fixed at **every** position, so all 97 inner letters must be in the square, and the two letters of every inner pair must differ (Playfair never outputs a doubled pair);
- symmetry break: Playfair doesn't change under cyclic shifts of rows or columns, so E is fixed at cell (0,0).

**Divisibility.** A key of period p is also a key of period kp, so UNSAT at p = 4, 5, 6 covers every p from 1 to 6. 12 configurations (2 tableaux × 3 modes × 2 alignments) per period.

**Encoding note.** With only the 11 full crib pairs, K4 KA/Vigenère/even was still SAT at p = 7 and 8. Adding the 2 half pairs made p = 7 UNSAT. The half pairs carry real information, so they are in every run below.

## Results (`analysis/cycle83/`)
| Text | p = 4 | p = 5 | p = 6 | p = 7 |
|---|---|---|---|---|
| **K4** | **12/12 UNSAT** | **12/12 UNSAT** | **12/12 UNSAT** | 1/1 run UNSAT (KA, Vigenère, even); 11 configs pending |
| shuffled-K4 nulls (3 runs) | — | — | 3 UNSAT, 1 stopped unfinished at the budget | — |

Solver time: 961 s of CPU over 44 finished instances (7–65 s each, ~8 cores).

## Planted controls (4/4)
`mkctl83.py` builds controls from a **random** square (random omitted letter outside the crib alphabet), random keys, K1–K3-style English with the cribs in place, and an independent Python Playfair. Configurations: p 4 KA/Vig/even, p 5 AZ/Beau/odd, p 6 KA/variant/odd, p 6 AZ/Vig/even.
- **4/4 SAT** at their true configuration (no false UNSAT: the encoding is sound for these cases).
- In **4/4 the solver's witness key is exactly the planted key**. So at p ≤ 6 the cribs fix the outer key, and a SAT witness would hand over the key directly.
- The witness square, which comes from the cribs alone, already deciphers **69–89 of the 97 letters** back to the planted plaintext, e.g. control 0: `…EASTNORTHEASTGXTHISGASHISLASTMUSXAWEQTHIRTBERLINCLOCKESFIFTYSEVENMINUTES…`.

## Verdict
**Negative (proof, within range).** Playfair with **any** 5×5 square, followed by a periodic Vigenère, Beaufort or variant key on the KA or A–Z tableau with **period 1–6**, both pair alignments, can't produce K4's 24 crib letters. Controls show the test is sound and that it recovers the key when a solution exists. Shuffled nulls are also UNSAT at p = 6, so this exclusion is generic: Playfair plus a short key is too rigid to fit chance text. **p = 7 is one config in twelve; p = 8 is not run**. Both are checkpointed for cycle 84 (`run83.sh`, resumable). The 8-minute budget ran over: about 13 minutes of wall time including the encoding trials, spent to finish p ≤ 6. It was not stretched further.

## Audit note on case file 80
Case file 80 says the cribs give 22 inner letters in the even alignment and **20** in the odd one. Both alignments give 11 full crib pairs (22 letters). The cycle 82 code (`pfv82.c`) already used all of them, so only the text was wrong. Results are unaffected.

## Still open
p = 7 (11 configs) and p = 8 (closing p ≤ 8 by divisibility); p ≥ 9 with arbitrary squares (crib-underdetermined: needs annealing on the full text with quadgrams); outer keys on other mixed alphabets; Playfair behind or in front of a transposition; seriated / two-row Playfair; the halfabet (mod-13 key on the KA halves).

## Cycle 84 addendum: p = 7 and p = 8 (resumed)
Same encoder (`tools/cycle83/sat83.py`), resumed with `tools/cycle84/run84.sh` under an 8-minute budget. Raw results: `analysis/cycle84/results_c83_c84.jsonl`.

**Two new planted controls** (`mkctl84.py`, random squares, seed 8401): p 7 AZ/Beaufort/even and p 8 KA/Vigenère/odd. **2/2 SAT, and both witness keys equal the planted keys** (`XADWASO`, `GZYXIDQX`). Controls are now 6/6 across p 4–8, so the encoding is sound at the longer periods too.

| K4 | done | result |
|---|---|---|
| p = 7 | 4/12 (KA Vig even, KA Vig odd, KA Beau even, KA Beau odd) | 4 UNSAT (16–22 s each) |
| p = 8 | 5/12 (KA Vig odd, KA Beau odd, KA variant odd, AZ Vig odd, AZ Vig even) | 5 UNSAT (267–404 s each) |

p = 8 is about 20 times harder than p = 7 for the solver, so the budget went mostly to p 8. **Still pending:** p 7 KA variant ×2, AZ ×6 (8 configs); p 8 KA Vig even, KA Beau even, KA variant even, AZ Beau ×2, AZ variant ×2 (7 configs); nulls at p 7 and the unfinished p 6 null. Rerunning `run84.sh` resumes exactly there. No verdict for p 7–8 until all 12 configs of each period are done.
