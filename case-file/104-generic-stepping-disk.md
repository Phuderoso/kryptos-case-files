# 104 — The generic stepping disk: how many step sizes does K4 need? (cycle 116)

**Question.** Cycles 106–107 (Alberti disk), 111 (M-209) and 114–115 (Kryha) each tested one machine that turns a
ring by a cumulative shift. All of them died on the same evidence: the 22 adjacent differences inside the two cribs.
Here the question is asked once for the whole family. Take any device with a fixed plain alphabet F, a cipher
alphabet M, and a ring shift s_{i+1} = s_i + d_i, where each step d_i comes from a step set S, in any order and with
no period. How small can S be and still fit K4?

**Method.** For an alphabet pair and a sense σ, the crib residues r_k = σ(M⁻¹(c_k) − F⁻¹(p_k)) force the 22 adjacent
steps. S must contain that set D, so m = |D| is the smallest step set any such machine needs. The 30-letter gap
between the cribs must also be crossable: 30 steps from D must sum to r_63 − r_33. If not, m is raised by 1. Layer
order is "substitution first, then transposition" (model A), so the cribs stay adjacent. Space: the identity (direct)
plus the 165,065-transposition bank, × 2,356 K1–K3-style keyword alphabet pairs × 2 senses, about 7.8 × 10⁸
configurations per text. Code: `tools/cycle116/stepset116.c`.

**Results** (`data/cycle116/`).

| text | direct min m | global min m over the bank | configs at that m |
|---|---|---|---|
| **K4** | 10 | **6** | 4 (one transposition, #119606; two mirror pairs of alphabets × 2 senses) |
| 16 shuffled nulls | 10 (all) | 7 in 14, 6 in 2 | 62–132 at 7; 4 and 24 at 6 |
| planted, \|S\| = 3 | 10 | **3** | 24, true setting m = 3 |
| planted, \|S\| = 4 | 10 | **4** | 24, true setting m = 4 |
| planted, \|S\| = 6 | 10 | 6 | 4, true setting m = 6 (indistinguishable from nulls) |

**Reading.**
- **Direct:** with any keyword alphabet pair, K4 needs at least **10** different step sizes (shuffles: 10 as well).
  This excludes every keyword-alphabet stepping machine with at most 9 step values used without a transposition.
  That includes the Kryha V1 (steps 5–13, 9 values), progressive keys (1 value) and any "turn by one of a few
  amounts" disk.
- **Behind the bank:** K4's best is m = 6. That is at the null level (2 of 16 shuffles also reach 6). A machine with
  **|S| ≤ 5** and keyword alphabets is excluded behind every bank transposition (controls with |S| = 3 and 4 are found
  at exactly their size, below every null). For |S| ≥ 6 the cribs cannot tell K4 from noise.
- The 24 crib letters are the limit: 22 steps can show at most 22 values, and random data already needs about 13 of 26.

**Still open.** Free (non-keyword) alphabets; transposition-first order (cribs scattered); |S| ≥ 6 behind
transpositions, which would need a language score on the 73 non-crib letters.
