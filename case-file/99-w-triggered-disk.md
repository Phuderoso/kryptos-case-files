# 99 — The disk that turns at every W (cycle 107)

**Question.** Cycle 106 left one strict special case of the Alberti disk open: the inner ring turns by a fixed step *d* every time a W is carved, so the five carved Ws (positions 20, 36, 48, 58, 74, 0-based) split K4 into six stretches, each one plain substitution, each the previous one turned by *d*. This is the "W as separator" idea (cycle 9) turned into a mechanism. A sister case: the disk turns at every X in the *plaintext* (unknown positions, so each crib block is one substitution and the two blocks differ by a free offset).

**Model.** Both rings arbitrary: τ(c) = π(p) + s (mod 26), π and τ unknown bijections, s = d · (number of Ws before the letter). Beaufort is the same model with −d once the rings are free.
- **Direct:** EASTNORTHEAST sits inside the single stretch between the Ws at 20 and 36, and E→F (pos 21) vs E→K (pos 30) breaks it at once. **Direct W-turn and direct X-turn models are impossible.**
- **Behind a transposition** (165,065 permutations from `tools/export_perms.py`): model A = substitution first, then transposition (Ws counted in the pre-transposition stream); model B = transposition first, then substitution (Ws counted in carved order); W turning before or after itself; d = 1…25 (d = 0 counted separately as plain substitution); model X with block offset 1…25. Exact weighted union-find with injectivity; strength = number of redundant (checking) equations.

**Results** (`tools/cycle107/wturn.c`, raw output `data/cycle107/`):

| text | model A best checks | model B best checks | model X | plain substitution |
|---|---|---|---|---|
| K4 | 0 | **3** (one transposition, #121558, every d) | none | none |
| 32 shuffled nulls (non-W letters shuffled, W positions kept) | 0–2 | 2 (30 nulls), 3 (2 nulls) | none | none |
| 6 planted controls (random rings, d, 4–5 Ws) | 6–7 on the true permutation | 3–6 on the true permutation, ranked first or tied first in the full search | — | — |

K4's best (3 checks) is reached by 2 of 32 nulls (p ≈ 0.06–0.1) and is the weakest planted control's score. With KRYPTOS / A–Z rings fixed on #121558 (all d, start settings, Vig/Beau), best 7 of 24 crib letters and noise English (−7.7 per quadgram).

**Verdict.** Direct: **impossible**. Behind 165,065 transpositions: **negative / at null level**; model A and model X find nothing with any checking strength. Caveat: with free rings each stretch carries few crib letters, so model B is only weakly judged by the cribs (controls score 3–6). Shuffled nulls kept the carved W positions, because shuffling the Ws changes how finely they cut the cribs and makes raw counts incomparable (first-pass nulls with shuffled Ws were discarded for that reason).
