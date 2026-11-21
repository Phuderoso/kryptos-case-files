# Case file 218: a bar that knows how hard it searched (I-342): NC bar(nq, ln N) calibrated on fresh nulls, plus the per-text Wilson rule (I-350) and the distance-to-bar rule

**Cycle 232, 2026-11-21 (audit slot). Verdict: the pre-registered bar passes all four gates (P, H, M, C) and is adopted from cycle 233 for
families that print Y lines. K4 passes it 0 times, with rank p 0.48 on the calibration nulls and 0.77 on the fresh holdout, so K4 is
`NO-SIGNAL (robust)` (distance p/α 9.5× and 15.4×). No solution. Pre-registered as `tools/cycle232/PREREG232.md` (local commit 4e0dc8d,
15:47:59 MST (UTC-7)), before any run with seed ≥ 209609. The run started at 15:48:03 MST.**

## Why
Case 215 showed that the null maximum near NC −6.0 follows how many decrypts sit in a bin, so raising the quadgram floor could not fix
it (four fresh null texts in 16 passed at nq 12–19). Voynich then measured the dependence twice on the c229 data:
- **bfa4385** / index **3046cd3**: pooled per-bin maxima, ln N +0.056 per e-fold and nq −0.024 per quadgram.
- **b8c71f75 / ca9cbdd6**: nested subsamples at fixed nq and family. b = **+0.190** per e-fold of N (CI 0.182–0.197) and **−0.0171** per
  quadgram at fixed N. T3 / T4 (family) were inconclusive. Post hoc, b fell from 0.215 to 0.168 between N 10 and 1000. Her caveats: no
  fresh nulls, and N 10⁵–10⁶ not covered.

Her c230 recount (**254c4ac**) and her blind case 217 recount (95c7098…425d9b7) set the count-cell rules used in Part C. This cycle fits
the bar **only on fresh nulls**, covers the K4 bins' real N range, lets the data choose the curvature, and confirms on a fresh holdout.

## Method (as filed)
- **Family:** the case 213 family exactly as `run229.sh`, with `kb229` unchanged. Gate T: a fresh build is byte-identical to the c229
  binary and reproduces the published K4 direct and bank Q r10 files.
- **Fresh nulls:** calibration **209609–209628** (20) and holdout **209629–209640** (12). Plants use 209641, the bootstrap 209642.
  **Next free seed 209643.**
- **Unit:** (text, nq ≥ 10) pooled over the 8 run files: N = number of scored decrypts and max = best NC. The fit also uses units pooled
  over disjoint groups of 2 / 5 / 10 / 20 calibration texts, so N runs from 10 to **5.3 × 10⁶**. K4's units run from 72 to 266,598,
  with 1.5 M in total.
- **Model:** OLS max = a + b₁ ln N + b₂ (ln N)² + c·nq, with no family term. The bar is the fit + k_text, where k_text is the largest
  per-text residual among the 20 calibration texts (nominal per-text false-pass level 1/21).
- **K4:** the published c229 files (`data/cycle229/R/k4_*`), **not re-run**.

## Gates (pre-registered)
| gate | result |
|---|---|
| **P** plants recovered and NC ≥ bar(nq, N of K4's unit at that nq) ≥ 23/24 | **23/24** (Wilson 0.80–0.99); one-error plants **11/12** (0.65–0.99); the miss is plant 9 (one-error, p 21, nq 18, NC −6.007, also under the old −6.0 bar); the same 23/24 hold at N 10⁶ and 5·10⁶; smallest margin among passes +0.63 → **PASS** |
| **H** holdout per-text passes ≤ 1/12 | **0/12** (Wilson 0–0.24) → **PASS** |
| **M** holdout mean residual per N decade within ±0.15 (≥ 10 units) | +0.069, +0.068, +0.018, −0.012, −0.000 for 10¹…10⁶; 10⁶–10⁷ has 8 units, +0.022, not gated → **PASS** |
| **C** calibration reaches N ≥ 10⁶ | max N 5,320,479 → **PASS** |

**Decision (rule as filed): adopted from cycle 233** for families that print Y lines. Other families keep NC ≥ −6.0 with their own null rate beside it.

## Result
### The fit (20 calibration texts, 1,928 unit points)
max = −6.8417 + 0.07860 ln N + 0.000274 (ln N)² − 0.01922 nq, R² 0.677. Cluster bootstrap over texts (B 1000): b₁ [0.035, 0.120],
**b₂ [−0.0022, +0.0023]**, c [−0.0197, −0.0179]. The local slope b(N) is +0.080 at N 10, +0.082 at 10³, +0.085 at 10⁵ and +0.086 at
10⁶ (95 % bands overlap: [0.045, 0.110] … [0.060, 0.098]).

Reading (descriptive, no mechanism):
- **No curvature is detected.** b₂'s interval straddles 0, so a slope that falls with N is **not supported** for these per-unit maxima.
  The prereg allowed it but did not impose it.
- **The nq term agrees with Voynich** (−0.0192 here vs her −0.0171, and c229's pooled −0.024).
- **The ln N slope is less than half hers** (0.079 vs 0.190). The estimands differ: hers is nested random draws inside a pool; here,
  per-text units are compared across N. The mean residual rises with the pooling level (−0.020 single texts → +0.058 for 20 pooled).
  That pattern fits correlated decrypts within one text (inverse-row twins and similar), which count in N without adding independent
  draws. This is a reading of the residual table, not a test. No slope is extrapolated past the covered range.

### The bar (fit + k_text, k_text = +0.879)
| nq \ N | 10 | 10² | 10³ | 10⁴ | 10⁵ | 10⁶ | 5·10⁶ |
|---|---|---|---|---|---|---|---|
| 10 | −5.97 | −5.79 | −5.60 | −5.41 | −5.21 | −5.02 | −4.88 |
| 20 | −6.17 | −5.98 | −5.79 | −5.60 | −5.41 | −5.21 | −5.07 |
| 30 | −6.36 | −6.17 | −5.98 | −5.79 | −5.60 | −5.40 | −5.26 |
| 45 | −6.65 | −6.46 | −6.27 | −6.08 | −5.89 | −5.69 | −5.55 |
| 60 | −6.93 | −6.75 | −6.56 | −6.37 | −6.18 | −5.98 | −5.84 |

One calibration text sets k_text (calibration R_t ranges from +0.244 to +0.879; the next is +0.728), so the bar is on the strict side.
Measured false-pass rate on texts outside the fit: holdout 0/12 plus the 16 c229 nulls 0/16 = **0/28 (Wilson 0–0.12)**. That bound is
loose. It does not support a claim that the rate is "≈ 5 %" to any precision.

### K4 under the bar (pre-registered)
K4's largest residual is R = +0.393 (bar offset +0.879). **0 passing units.** The closest K4 unit is nq 55, N 24,177, max −6.685 vs bar
−6.199 (gap −0.49). Rank p: calibration 0.476 (n 20), holdout 0.769 (n 12); the c229 nulls give 0.765 (n 16, descriptive).
**`NO-SIGNAL (robust)`**: both p are ≥ 2α, on both sides of the replicate. Against the descriptive per-unit bar (fit + 0.283), K4 has 3 of 52
units over it (nq 16, 28, 55) vs a calibration null mean of 2.6 per text (0–6). That is ordinary.

## Retroactive reading (descriptive relabelling only; no published verdict changes)
| item | under the new bar |
|---|---|
| case 215: the four −6.0 null passes (209573, 209568, 209560, 209563; nq 12–19, unit N 570–3,127) | all **below** the bar, by −0.26 to −0.31 |
| case 215: all 16 c229 nulls | 0/16 texts pass (Wilson 0–0.19) |
| case 213: null 209425 (−5.292, nq 10) | its full unit N was never printed (kb227 has no Y lines). At N 17 (the one gate-T file) up to ~10⁴ it **still passes** (bar −5.93 … −5.41); it would fall below only above N ≈ 4·10⁴. Case 213 per-text rate therefore stays 1/20 (Wilson 0.01–0.24), consistent with the nominal level |
| cases 213 / 215 K4 (case 215's K4 run contains case 213's K4 decrypts: same family, V full scale ⊇ r10) | 0 passes; NO-SIGNAL (robust) as above |
| case 214 K4 NC max −7.94 (Part A) and −7.30 (Part B re-read) | below the most lenient bar value in the domain (−7.01 at N 10, nq 64) for any N → NO-SIGNAL at decrypt level, unchanged |

## Part C — I-350 and the distance rule on the case 216 / 217 count cells (descriptive)
Per-text rate r = share of null texts at or above K4's per-slice level, with Wilson 95 % and α 0.05. The replicate is the other null set
(case 217's 20 / 8 fresh nulls vs case 216's 10). The cluster expectation is the mean clusters per null slice × scale.
| cell | K4 raw (clusters) | case 217 r (Wilson) | exp. clusters | case 216 r (Wilson) | exp. clusters | label now (published label) |
|---|---|---|---|---|---|---|
| direct W ≤ 9 | 3 (2) | 0/8 (0–0.32) | 0.0 | 2/10 (0.06–0.51) | 4.0 | `INSUFFICIENT-DISCRIMINATION-FRONTEIRA` (217: INSUFFICIENT) |
| direct W ≤ 10 | 47 (22) | 1/8 (0.02–0.47) | 4.4 | 2/10 (0.06–0.51) | 10.0 | `INSUFFICIENT-DISCRIMINATION-FRONTEIRA` (217: NO-SIGNAL) |
| bank W ≤ 9 | 0 (0) | 1/20 (0.01–0.24) | 1.0 | 2/10 (0.06–0.51) | 4.0 | `EXACT-EXCL`, discrimination undetermined, **FRONTEIRA** (216: "discriminating") |
| bank W ≤ 10 | 44 (8) | 8/20 (0.22–0.61) | 21.0 | 4/10 (0.17–0.69) | 30.0 | **`NO-SIGNAL` (robust)**: lo/α 4.4× and 3.4×, same side |
| all W ≤ 9 | 6 (2) | 2/20 (0.03–0.30) | 2.0 | 3/10 (0.11–0.60) | 6.0 | `INSUFFICIENT-DISCRIMINATION-FRONTEIRA` (217: INSUFFICIENT) |
| all W ≤ 10 | 48 (20) | 4/20 (0.08–0.42) | 25.0 | 6/10 (0.31–0.83) | 38.0 | `NO-SIGNAL-FRONTEIRA` (lo/α 1.6× < 2) |

Voynich's blind recount called all six FRONTEIRA. My reading agrees on five. It differs on **bank W ≤ 10**, where both null sets have Wilson
lower bounds well above α. Her rule may use her replica seeds (31231000+i) as the second set; I flag the difference instead of settling it (I-357).
**The m_f < 3 rule is retired** (it was evaluated before "K4 > null max" and flips across replicates, 2/20 vs her 3/20). The K4 = 0 exclusions
stay exact under their assumptions. With 20 nulls, a "discriminating" zero (Wilson hi ≤ 0.05) is impossible; that would need ≥ 73 quiet nulls (0/73).

## Labels
- I-342 bar: **adopted** (P / H / M / C pass) from cycle 233 for Y-line families. Decrypt level, case 213 / 215 family: K4 **`NO-SIGNAL (robust)`**.
- I-350: per-text Wilson rate and cluster expectation now reported. The case 216 / 217 relabels above are descriptive.
- Distance rule: in force from this cycle (PREREG232 Part C).

## Blind spots
One family (case 213 keyboard family). Q-model plants only (V plants and filler plaintexts still open, I-343). k_text rests on one extreme
text out of 20, and the realised per-text level is only bounded to 0–0.12 by 28 outside texts. Units pooled across texts behave a little
differently from single-text units (level residuals, I-355). The bar has no family term because T3 / T4 were inconclusive, not because family
was shown not to matter. Unit N for older families without Y lines is unknown, so those were read only against the most lenient bar.

## Files
[`data/cycle232/`](../data/cycle232/): `R/` (stamped, filtered outputs of 32 fresh nulls and 24 plants), `nulls232.tsv`, `plants232.tsv`,
`analyze232.log`, `summary232.json`, `gateT/`, `smoke/`, `MANIFEST.txt`, `SHA256SUMS`. Tools: [`tools/cycle232/`](../tools/cycle232/)
(`PREREG232.md`, `HASHES232.txt`, `plant232.py`, `run232.sh`, `analyze232.py`, `k123_eng.txt`). Heavy wall time 430 s (one run, no resume).
Seeds: nulls 209609–209640, plants 209641, bootstrap 209642. **Next free seed 209643.**

## Verdict
No solution. The bar now scales with nq and search size. It was fitted on fresh nulls, held on a fresh holdout and kept 23 of 24 plants.
K4 sits in the middle of the nulls under it. **K4 still standing.**
