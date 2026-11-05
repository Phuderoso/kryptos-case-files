# Case file 66 — Doppelkasten: two-square applied twice with the same squares (cycle 68)

**Why this test.** Case file 65 closed the single two-square (both squares arbitrary) as a direct layer: K4 0/48. The
natural "several simple layers" next step is the German Army's WWII **Doppelkastenschlüssel**: the same pair of squares
used for two passes over the same digraphs. Two simple layers, one key, and the composition is *not* itself a
two-square, so case file 65 says nothing about it. (Idea 3 in the cycle 67 journal.)

**Model.** Exactly cycle 67's geometry and conventions (shapes 2×13 / 13×2 / 6×6, pair offset 1 or 2, square pairings
(S2,S1) horizontal, (S1,S2) vertical, plus (S1,S1), (S2,S2) as a superset, output order (u,v) or (v,u)) — 48
configurations — but every crib pair goes through two passes: (p1,p2) → (m1,m2) → (c1,c2), with the emitted order of
pass 1 fed to pass 2. The intermediate letters m1, m2 are free one-hot variables. Assumption: on 6×6 the intermediate
must be a letter (no digit cells in the middle). The textbook Doppelkasten's special same-row rule is covered only as far
as the geometry gives it (as in case file 65).

**Exact test.** CNF (PySAT, CaDiCaL): cell, row and column indicators for both squares, one-hot intermediates whose
row/column are tied to the squares, row/column equalities for both passes on all 11 crib pairs. UNSAT is a proof that no
pair of squares fits; SAT only means the 22 crib letters do not pin the squares down.

**Controls and nulls.** 48 planted controls (one per configuration, Moby-Dick text with the cribs at the official
positions, random squares, encrypted twice; 6×6 non-crib pairs that would hit a digit cell get random letters, a crib pair
forces a retry). Shuffled-K4 nulls, seeds 6800–6823; 20 of 24 finished inside the cycle's time budget, the other 4 were
stopped (not cherry-picked: they were simply the last to be scheduled).

## Results
| Text | Satisfiable configurations |
|---|---|
| **K4** | **14 / 48** (34 UNSAT) |
| 20 shuffled nulls | 0, 0, 4, 4, 6, 6, 8, 8, 10, 10, 10, 12, 12, 12, 12, 16, 16, 20, 22, 24 (median 10–12; 5 of 20 nulls ≥ K4) |
| Planted controls | **48 / 48** satisfiable at their own configuration |

K4's 14 open configurations: 2×13 (offset 1, S1/S2, swapped), (offset 2, S1/S2, swapped), (offset 2, S2/S2, straight);
13×2 (offset 1, S2/S1, straight), (offset 2, S2/S1, straight), (offset 2, S2/S2, swapped); 6×6 offset 1: S2/S1 straight,
S1/S2 swapped, S2/S2 both orders; 6×6 offset 2: S2/S1 straight, S1/S2 swapped, S1/S1 both orders. Every one of them is
also satisfiable for 25–75 % of shuffled nulls. Full bit-strings in `analysis/cycle68/`.

## Reading
- **34 of 48 configurations are excluded for K4** (UNSAT proofs; controls show the encoding accepts genuine Doppelkasten
  text). 10 of those 34 are satisfiable for at least one null, so those exclusions have demonstrated power; the other 24
  are rejected by every null too (as in case file 65, the crib pairs over-constrain them).
- **14 configurations stay open**, and K4 sits at the null median, so **there is no signal** in which ones survive. Two
  passes with free intermediates give the solver enough slack that 11 crib pairs cannot decide them.
- Closing them needs whole-text evidence: anneal the two squares against quadgrams with the 22 crib letters as hard
  constraints (as cycle 65 did for Gromark), gated by planted controls, and compare K4 with shuffled nulls.

**Verdict: partly excluded (34/48 exact), 14/48 open and crib-underdetermined; no evidence for Doppelkasten.**

Code: [`tools/dk68_sat.py`](../tools/dk68_sat.py) (needs `tools/ts67_sat.py`), [`tools/ctl68.py`](../tools/ctl68.py).
