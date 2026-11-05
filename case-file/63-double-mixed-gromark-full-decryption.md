# Case file 63 — Gromark with both alphabets mixed, decrypted in full (cycle 65)

**Why this test.** Our coverage table and kryptosbot's research questions both list "a Gromark cipher with keyed
alphabets on both sides" as open. Case file 08 reproduced Richard Bean's 39 primers (base 10, primer length 5) that
survive the cribs when *both* alphabets are arbitrary, and case file 11 confirmed them with SAT. But nobody here had
asked the next question: for those 39 primers, is there *any* pair of alphabets that turns all 97 letters into English?
Feasibility only uses the 24 crib letters; the other 73 had never been read. This is a new test of an open family, so
it satisfies the diversity rule set in cycle 64.

**Model.** Key digits k_i from a primer of length L by lagged Fibonacci, k_{i+L} = k_i + k_{i+1} (mod 10).
c_i = CA[(PA⁻¹(p_i) + k_i) mod 26], with PA and CA two **independent, arbitrary** permutations (Beaufort and the
reversed-direction forms are the same model with PA reversed, so they are covered). No transposition layer.

**Method.** [`tools/c65.c`](../tools/c65.c).
1. *Census.* For each primer, a weighted union-find on 52 nodes (PA⁻¹ of the crib plaintext letters, CA⁻¹ of the crib
   ciphertext letters) with offsets mod 26, plus an injectivity check inside each component. K4 at L = 5 gives exactly
   Bean's **39** feasible primers.
2. *Full decryption by hard-constrained annealing.* For each feasible primer, simulated annealing over (PA, CA) maximises
   the quadgram score of the whole 97-letter decryption. Every state satisfies all 24 crib equations by construction:
   moves either swap two alphabet letters that touch no crib, or shift a whole crib component by a constant (the free
   letters it displaces take the vacated slots). Score = mean natural-log quadgram probability (planted English scores
   −4.0 to −4.2; random text about −7.9).

## Census of feasible primers (base 10)
| Text | L = 4 | L = 5 | L = 6 | L = 7 |
|---|---|---|---|---|
| **K4** | 3 | **39** | 412 | 3,834 |
| 6 shuffled K4 nulls | 14–618 | 75–6,712 | 484–64,366 | 5,335–618,806 |
| 4 planted controls | 0–178 | 10–1,439 | 6–17,497 | 192–170,731 |

K4 sits at the low end of the null range. That only reflects how many letters repeat among K4's crib-position
ciphertext letters; the planted controls span the same range, so the count is **not evidence for or against** Gromark.
Every planted primer was among its control's feasible set (4/4).

## Full-decryption results (L = 5 unless noted)
| Text | Feasible primers | Restarts | Best score | Best text |
|---|---|---|---|---|
| CTL1 (planted, primer 14802) | 1,439 | 6 | **−4.21** | THEROADTURNSSHARPLYTOEASTNORTHEAST… exact |
| CTL2 (80128) | 12 | 6 | **−4.04** | ITWASHIDDENUNDERSTONE… (one letter off: MALLS for FALLS) |
| CTL3 (60948) | 81 | 6 | **−4.14** | …UNTILYOUSEE → ANTILHOUSEE (two letters off) |
| CTL4 (02190) | 10 | 6 / 12 | −5.03 (missed) / **−4.04** in 4 of 4 seeds | ITWASHIDDEN… |
| **K4** | 39 | 6, then 12 × 4 seeds | **−5.03** | LJACUTINGOBRANTWOMEWZ… (primer 88254), gibberish |
| NULL0 / NULL2 / NULL5 | 478 / 524 / 75 | 6 (NULL5 also 12 × 2) | −5.08 / −5.21 / −5.07 | gibberish |
| **K4, L = 6** | 412 | 8 | −4.95 | OGSTLYGOVERYSANSORSUN… gibberish |

Controls: **4/4 recovered** at 12 restarts (3/4 at 6 restarts; the miss is why K4 was rerun at 12 restarts × 4 seeds).
The letter slips in the controls are plaintext letters that never meet a crib, so their alphabet slot is only fixed by
English statistics. All outputs: [`data/cycle65/`](../data/cycle65/); reproduce with
[`tools/run_cycle65.sh`](../tools/run_cycle65.sh) (controls from [`tools/gen65.py`](../tools/gen65.py); about 6 minutes
on 8 cores).

## Verdict
- **Fact:** none of Bean's 39 double-mixed Gromark primers (base 10, L = 5) yields readable English with any alphabet
  pair the annealer can find; K4's best (−5.03) sits with the shuffled nulls (−5.07 to −5.21) and a full 1.0 nat per
  quadgram below every recovered planted English text. **Negative.**
- **Fact:** at L = 6 (412 primers), the best is −4.95, also gibberish. **Limit:** no equal-size null was run at L = 6,
  and annealing is a search, not a proof; a solution the annealer misses in 48 restarts per primer cannot be excluded.
- **Not covered:** L ≥ 7 (3,834+ primers), other bases, Gromark behind a transposition, a one-letter anomaly inside the
  Gromark, and periodic Gromark (primer re-seeded by a keyword).
