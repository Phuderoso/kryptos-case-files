# Case file 145 — Structure-matched nulls for the Gromark one-error tests (cycle 157)

**Cycle 157, 2026-11-08. Variant / audit of method** (IDEAS [I-052](../IDEAS.md); feeds [I-004](../IDEAS.md), [I-051](../IDEAS.md)).

## Why
Cycle 155 ([case 143](143-gromark-one-error.md)) labelled four Periodic Gromark rows `LOW-POWER` because K4's one-error survivor counts
(28 digit primers at L 8, 11 at L 9, rank strings at L 11–12) sat inside a null range of 0 to 1.15 × 10⁶. The six shuffled nulls had
13–19 distinct cipher letters under the cribs (K4: 14), so the range mixed texts of very different structure. I-052 asked whether nulls with
**K4's exact repetition profile** give a calibrated baseline. In the free-alphabet model the ciphertext enters only through the partition of
the 24 crib positions by cipher letter, so profile-matched shuffles differ from K4 only in which positions share a letter.

## Method
- **Nulls** (`tools/cycle157/mknulls157.py`): shuffles of K4 accepted only if the crib letters have profile 3-2-2-2-2-2-2-2-2-1-1-1-1-1
  (14 distinct). 20 accepted of 2,915 (0.69 %). Data: `data/cycle157/nulls.txt`.
- **Test**: the unchanged cycle-155 program (`tools/cycle155/gromark1e.c`, model P: arbitrary cipher alphabet, L free group offsets,
  A–Z/KRYPTOS plain, Vig/Beau, exact leave-one-out with certificate pruning). Every matched null over all digit primers L 2–8 and all
  keyword-rank primers L 8–11 (full sets). K4 L 8 digits and L 11 ranks rerun as a regression; other K4 rows are the cycle-155 zeros.
- **Structure statistic** (`structure157.py`): the crib graph joins each crib's cipher-letter node to its group-offset node
  (group = (pos div L) mod L). Every independent cycle (cycle rank r = edges − nodes + components) is one mod-26 equation on the digit
  stream, so r should govern how many primers pass by chance. Not run: L 9 digits and L 12 ranks (10⁹ and 4.8 × 10⁸ primers per text;
  out of budget).

## Checks
- K4 L 8 digit and L 11 rank survivor lines are **identical to cycle 155** (45 lines; regression).
- Profile of every null recomputed independently: 20/20 match, all are true permutations of K4.
- Pure-Python recount (`tools/cycle155/indep_check.py`, no shared code: tries all 24 drops, BFS) of the full L 4 run for every null:
  **20/20 identical**. 35 sampled L 8 null survivors (2 per null) each **confirmed** one-error-feasible in Python.
- Planted-key controls for the solver are cycle 155's (11/11; tool unchanged). This cycle builds a null model, so the nulls are the subject.

## Results (`data/cycle157/results.txt`, `structure.txt`) — one-error-feasible primers
| primers | K4 | 20 matched nulls: min / median / max (# zero) | p (upper) | reading |
|---|---|---|---|---|
| digits L 2–7 | 0 | 0 / 0 / 0 (20) | — | chance survivors absent at K4's structure: the cycle-155 `EXACT-EXCL` rows also have **power** |
| ranks L 8, 9, 10 | 0 | 0 / 0 / 1, 0 / 0 / 0, 0 / 0 / 0 | — | same |
| **digits L 8** | **28** | 0 / 60 / 586 (2) | 0.571 | profile-matched: K4 at chance |
| ranks L 11 | 6 | 0 / 0 / 10 (16) | 0.143 | profile-matched: K4 at chance |

Strict (all 24 cribs): K4 0 everywhere; matched nulls 0–7 at L 8 digits, 0 elsewhere.

**Profile matching is not enough: the cycle rank decides.** With the same profile, L 8 counts still range from 0 to 586. Split by r:

| L 8 digits | n | one-error counts | K4 |
|---|---|---|---|
| r = 5 | 14 | 0, 2, 20, 56, 64, 65, 90, 93, 99, 113, 125, 153, 397, 586 (median 93) | — |
| **r = 6 (K4's)** | 4 | **1, 2, 2, 5** | **28** |
| r = 7 | 2 | 0, 2 | — |

At L 11 (rank primers) K4 has r = 6; the 11 r = 6 nulls give 0, 0, 0, 0, 0, 0, 0, 2, 2, 6, 10 (K4 6, p = 3/12 = 0.25); r = 7–8 nulls give 0.
The cycle-155 nulls had r = 1–7 at L 8 (null2, with 10⁶ survivors, has r = 1), which explains their huge spread.

## Verdict
- **No solution; no labels upgraded to a claim.** The cycle-155 `EXACT-EXCL` rows stand, and at K4's structure the test has power there
  (matched nulls almost always 0, so a true key would stand alone).
- **L 11 rank primers:** K4 6 inside the r-matched null range → `NO-SIGNAL` at the count level (stage 2 already excluded every ACA keyword).
- **L 8 digit primers:** against profile-matched nulls K4 is at chance (p 0.57), but against the **four** nulls that also match its cycle
  rank, K4's 28 is above all of them (1–5). With four nulls the smallest attainable p is 0.2, so this is **not** evidence; the row stays
  `LOW-POWER`, now with a concrete question (I-057): is K4 really ~10× over its r-matched baseline? If a larger r-matched sample confirms
  it, the 28 primers move up the decoding queue (I-051); if not, the row can be closed as chance.
- **Method:** for union-find / SAT feasibility tests, nulls should be matched on the **cycle rank of the crib graph at each period**, not
  only on the repetition profile. Profile matching removes the 10⁶ outliers but leaves a 0–586 spread.

## Limits
- 20 nulls; only 4 share K4's L 8 cycle rank (rejection sampling on r is the fix, I-057).
- L 9 digits and L 12 ranks not run (cost); model G not rerun (all zeros already).
- r is a first-order statistic; injectivity of the alphabet (14 letters must get distinct values) and how the cycles fall on the
  plaintext letters also matter (r = 5 nulls span 0–586).

## Files
[tools/cycle157/](../tools/cycle157/) (`mknulls157.py`, `run_cycle157.sh`, `summarize157.py`, `structure157.py`, `indep157.sh`) ·
[data/cycle157/](../data/cycle157/) (`results.txt`, `structure.txt`, `nulls.txt`, `c_lines.txt`, `k4_survivors.txt`,
`null_survivors.txt`, `indep_check.txt`, `indep_L4.txt`, `indep_single.txt`, `sample_survivors.txt`, `timing.txt`) ·
[journal](../journal/2026-11-08-cycle157.md).
