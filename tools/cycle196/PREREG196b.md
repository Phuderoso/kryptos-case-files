# Cycle 196 pre-registration (b) — pooled reference for the grid rank flag (I-182 / I-203)

Written and pushed **after** the registered run of [PREREG196](PREREG196.md) and **before** any fresh-null run. Heavy so far ≈ 4.6 min.

**What triggered it.** The registered grid (K4 + 19 shuffles, seeds 19611–19629; tab2 on col1_s8 = 460 single keyed columnars, all 625 pairs,
one-error) gave, for two-tableau fits in bands e ≥ 3 (config U ≤ 26^−2.5, mostly LOW-POWER cells): **K4 12, nulls 1–8 (median 4), p⁺ 0.05**
(the rank floor; meter-expected U 5.61 per text). PREREG196 says a rank flag goes to a pooled reference, not a claim. Known before this file
(disclosed): 8 of K4's 12 are period-multiple / equivalent copies on two rows (CANNOT/enc row 328 and GAZING/enc row 2104, S2 KA>AZ VB, n 24 or
16 with m 2/4/8, config U 2.8 × 10⁻⁴ each, at the band edge); the cluster-aware count D (distinct row, model, tableau pair, form) is K4 6 vs
registered nulls 1–8 with 2 ≥ 6 (p 0.15) — D was computed after seeing the grid, so it is descriptive only.

**Registered test** ([`run_pool196.sh`](run_pool196.sh), [`pool196.py`](pool196.py)): 40 fresh shuffles (seeds 19631–19670,
[`nulls196b.txt`](nulls196b.txt), `random.Random(seed).shuffle(list(K4))`), the same cell (cmp194, tab2, col1_s8, all 625 pairs). Primary
statistic R = fits in bands e ≥ 3 from the B lines; pooled over the 19 registered + 40 fresh nulls, p_pool = (1 + #nulls ≥ K4)/60, binomial SE
printed (I-203). **Verdict:** p_pool ≤ 0.01 → "REPLICATED rank excess" (then decode K4's fits and a covariate-matched check before any
wording; never a solution claim by itself); otherwise **NOT REPLICATED** (flag closed). D reported beside it (descriptive). K4's e ≥ 3 grid fits
are decoded descriptively either way (they sit in LOW-POWER cells). Cost ≈ 65 s.
