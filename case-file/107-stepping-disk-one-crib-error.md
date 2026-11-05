# 107 — Stepping disk with one wrong crib letter (cycle 119)

**Question.** Cycle 116 ruled out any cumulative-shift "stepping disk" (Alberti-with-steps, Kryha, progressive key, …) with keyword alphabets and a step set of size ≤ 9 direct, or ≤ 5 behind the 165,065-permutation bank. Those tests assume all 24 crib letters are right. If one crib letter is wrong — a carving slip under a crib, or a wrong assumed plaintext letter — do the exclusions still hold?

**Code.** [`tools/cycle119/stepset119.c`](../tools/cycle119/stepset119.c), driver [`run119.py`](../tools/cycle119/run119.py). For each (permutation, alphabet pair, sense), drop each crib letter in turn, discard the one or two adjacent steps that touched it, and take m1 = the smallest remaining number of distinct steps. This is a **lower bound** on the step-set size a machine needs under a one-crib error (the merged two-step constraint and the 30-letter gap test of cycle 116 are ignored, so it can only under-count). About 6 minutes wall time for K4 + 8 nulls + 4 planted controls on 8 cores. Outputs in [`data/cycle119/`](../data/cycle119/).

**Controls.** Clean planted machines with |S| = 3, 4, 5 recover m0 = |S| at their true setting. After flipping the intermediate letter that feeds one crib (the carved cell the crib test actually reads), m1 recovers to ≤ |S| in every trial. So the leave-one-out score finds a real one-error machine when one is there.

## Results

| Text | direct m1 | bank: perms with min m1 ≤ 4 | ≤ 5 | ≤ 6 | global min m1 |
|---|---|---|---|---|---|
| K4 | 9 | 0 | 1 | 158 | 5 |
| null 0..7 (8 shuffles) | 7–9 | 0 | 0–2 each (4 of 8 nulls hit 5) | all | 5 or 6 |
| planted \|S\|=3 clean | — | true perm at m1=3 | — | — | 3 |
| planted \|S\|=4 clean / with one crib flip | — | true perm at m1=4 | — | — | 4 |

K4's only m1 = 5 configuration: permutation 104010, alphabet pair 707, both senses, by dropping crib index 19 (m0 was 7). That is as rare as the same score on shuffled copies.

## Verdict
- **Direct: |S| ≤ 8 still excluded** under a one-crib error (m1 = 9; cycle 116 had |S| ≤ 9 with no error).
- **Behind the bank: |S| ≤ 4 still excluded** (K4 never reaches m1 ≤ 4; nulls neither).
- **Behind the bank: |S| ≤ 5 does *not* survive.** Cycle 116's exclusion relied on a perfect crib. With one wrong crib letter, K4 reaches m1 = 5 once, indistinguishably from the nulls. From |S| = 6 up, the cribs already could not tell signal from noise in cycle 116.

**Negative for |S| ≤ 4 (and for direct |S| ≤ 8), with planted controls. Softens cycle 116's |S| ≤ 5 claim behind the bank to: only under a perfect crib.**
