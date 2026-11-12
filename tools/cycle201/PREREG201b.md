# PREREG201b — second registered run of I-238 with a multiplicity-correct clean-item gate (fresh seeds)

Written 2026-11-11 ~19:51 PT, after run 1 (PREREG201, seeds 21000, outputs kept unchanged in `run1/`).

**What happened in run 1.** G1, G1b, G3, G4, G5 passed. **G2 failed as registered:** 2 of 48 configurations had a clean-plant
false-disfavour rate of 0.085 (17/200) against the bar 0.081 (JE C1 P 8 and JE C1 P 23); the pooled rate over 9,600 clean plants was
0.0502. The bar was wrong: a per-configuration 0.05 + 2 SE bar applied to 48 configurations fails a perfectly calibrated test with
probability ≈ 0.69 (P(X ≥ 17 | n 200, p 0.05) = 0.024 per configuration). Under PREREG201's own rule run 1 is **broken, no verdict**,
and it is reported that way. Its descriptive numbers were seen before this file was written; they are disclosed in case 188.

**Run 2 (this registration).** Same code, same models, same conditioning levels, same statistics, same verdict rule (a confirmatory cell
P 8 / 13 / 23 stays `STAT-DISFAVOURED` iff max q_rev over the 16 model × conditioning configurations < 0.05, else `LOW-POWER
(model-sensitive)`), **fresh seed base 22000** for every random draw. Only G2 changes: **G2b = pooled false-disfavour rate over the
48 × 200 clean plants ≤ 0.0544 (0.05 + 2 SE) and every configuration < 22/200 (Bonferroni 0.05/48)**. The run-1 G2 is still computed
and printed beside it. Secondary statistics (q_raw, q_col, dilution) remain descriptive and cannot create or keep a label this cycle.
If run 2 breaks a gate, the cycle closes with no verdict. There is no third run.
