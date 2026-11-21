# PREREG232 — Cycle 232 (audit): I-342 null-calibrated NC bar as a function of nq and ln N, on fresh nulls; I-350 per-text rates; the distance-to-bar rule

Filed 2026-11-21 (time = this commit, MST = UTC-7), **before** any fresh-null, plant or K4 run with seed ≥ 209609. Base: origin/main 36b2871
(c231 published). Case file 218. Slot: **audit** (I-341 / I-347: 232 audit = I-342).

## Inputs cited (Voynich desk, public voynich-case-files)
- **bfa4385** (c229 recount, index **3046cd3**, `audits/kryptos/c229-nq-vs-search-size/`): per-bin null max falls with nq (R² 0.65), ln N alone R² 0.10;
  joint pooled partials ln N +0.056 / e-fold, nq −0.024 / quadgram.
- **b8c71f75 / ca9cbdd6** (`audits/kryptos/c229-subsample-i342/`, PREREG sha 78af9769…, tool 5185d776…): at fixed nq and family
  b = **+0.190** NC per e-fold of N (CI 0.182–0.197), at fixed N **−0.0171** per quadgram; family composition tests T3 / T4 **inconclusive**;
  post hoc the slope falls 0.215 → 0.168 from N 10 to 1000; replicas were the same 16 nulls; N 10⁵–10⁶ **not covered**. Her estimand
  (nested draws inside pools, N < 2000) differs from per-bin maxima; neither slope is extrapolated here.
- **254c4ac** (c230 recount, index 4d3050f) and her case 217 blind recount (95c7098…425d9b7, replica seeds 31231000+i) for the count-cell rules.

## Disclosed before filing (no fresh seed used)
- **Gate T:** `kb229.c` (sha f727ed9e…) rebuilt (`gcc -O3 -march=native -fopenmp`) is byte-identical to the c229 binary (b0b29ffa…); on K4
  direct geo a and K4 bank Q r10 its sorted S/T/M/P/Y/N lines equal the published `data/cycle229/R` files (md5 equal). These are reference
  re-runs of already published K4 outputs, used only as the gate.
- **Smoke:** `plant232.py` run once with seed **1**; the 24 seed-1 plants went through kb229; the analysis script was dry-run on a
  directory of **symlinks to the published c229 nulls** (cycled, standing in for the fresh seeds) to test the code path. Its numbers are not
  results and are not reported as such; the bar form, gates and decision rule below were written before that dry run and not changed after
  it except two code fixes: a numpy scalar conversion, and plant recovery accepting the H line at a divisor of the true period (kb229
  prints H at the primitive period; seen on seed-1 plant 2, p 12 → H at p 6).

## Part A — I-342 bar (fresh nulls only)
- **Family / commands:** case 213 family exactly as `run229.sh` (direct GVQ geo a / GV geo b; Q behind bank / all.bin r10; V geo a / b behind
  bank / all.bin full scale), `kb229` unchanged, print level −6.0. `run232.sh` (resumable, skips finished files).
- **Fresh nulls:** shuffled K4 (`random.Random(seed).shuffle`), **calibration seeds 209609–209628 (20)**, **replicate / holdout seeds
  209629–209640 (12)**. Plants seed **209641**, bootstrap RNG seed **209642**. Next free seed **209643**.
- **Unit:** U = (text, nq), nq ≥ 10, pooled over the 8 run files, models and p: N_U = Σ n of the Y lines, max_U = max of their max.
  Domain N_U ≥ 10 (K4's smallest unit is N 72).
- **Covering the real N range:** fit points = single-text units **plus** units pooled across disjoint groups of calibration texts
  (g = 2, 5, 10, 20, same nq) — the max over the union of independent null decrypt sets — so N reaches ~10⁶–5·10⁶ (K4 units: 72 … 266,598;
  K4 total 1.5 M).
- **Form (curvature allowed, no family term, no extrapolation):** OLS  max_U = a + b₁·x + b₂·x² + c·nq, x = ln N. Local slope b(N) = b₁ + 2b₂x
  is reported at N 10, 10³, 10⁵, 10⁶ with a cluster bootstrap over calibration texts (B 1000). Whether b decreases with N is **read from
  the data**, not imposed. Mean residual by pooling level is printed.
- **Bar:** bar(nq, N) = fit(nq, N) + k_text, k_text = max over the 20 calibration texts of R_t = max over the text's single-text units of
  (max_U − fit). Nominal per-text false-pass level 1/21 ≈ 0.048. Descriptive per-unit bar: fit + k05 (95th percentile of single-text residuals).
  A decrypt is a bar candidate iff known ≥ 49, nq ≥ 10, tie = '?', NC ≥ bar(nq, N of its unit).
- **Gates:** **P** plants: ≥ 23/24 recovered (P line of the true configuration at the true p, H line at p or a divisor) **and** NC ≥ bar(nq, N_ref)
  with N_ref = K4's own unit N at that nq (largest K4 unit N if K4 has no unit there); Wilson printed; also reported at N 10⁶ and 5·10⁶.
  Plants: 24 Q-model (kb227 conventions), nq bands 10–11 / 12–14 / 15–19 / 20–29 / 30–44 / ≥ 45 (4 each), p 8–24, behind bank / all.bin,
  **odd pid one corrupted crib letter (one-error)**, plaintext K1–K3 / Jane Eyre. **H** holdout: per-text passes ≤ 1/12 (Wilson printed).
  **M** misfit: holdout units (single + pooled g 2 / 4 / 12) mean residual |·| ≤ 0.15 NC in every N decade with ≥ 10 units. **C** coverage:
  calibration max N ≥ 10⁶.
- **Decision:** all four pass → the bar is **adopted from cycle 233** for families that print Y lines (others keep NC ≥ −6.0 with the null
  rate beside it). Otherwise not adopted; numbers reported descriptively. Nothing is tuned after the run.

## Part B — K4 under the bar (pre-registered) and retroactive reading (descriptive only)
- **K4 = the published c229 files** (`data/cycle229/R/k4_*`, case 215; deterministic, same tool and commands; **not re-run**). Statistic
  R_K4 = max over K4 units of (max_U − fit); K4 passes iff R_K4 ≥ k_text. Rank p = (1 + #null texts with R_t ≥ R_K4) / (n + 1), on calibration
  (n 20) and holdout (n 12) separately; the c229 nulls (n 16, not in the fit, already seen) are a descriptive third set.
- Retroactive relabelling is **descriptive only**: case 215's four −6.0 null passes and its 16 nulls under the new bar; cases 213 / 214 K4 NC maxima
  against the most lenient bar value in the domain; case 216 / 217 count cells under the I-350 and distance rules. No published verdict changes.

## Part C — I-350 and the distance-to-bar rule (agreed with Voynich; from this cycle on)
1. **I-350:** every null comparison reports the **per-text hit rate with Wilson 95 %** and a **cluster-level expectation** (mean clusters per null text
   × scale) instead of "null-equivalent ×20/n" (which was an expectation driven by 2–3 texts).
2. **Order of rules:** the old few-firing-nulls rule (m_f < 3 → INSUFFICIENT / NO-SIGNAL) was evaluated **before** "K4 > null max" (otherwise case 217
   direct W ≤ 9 would read EXCESS). **m_f < 3 is unstable across replicates** (Voynich's replica seeds 31231000+i: all W ≤ 9 fires in 3/20 →
   NO-SIGNAL where the fresh set gave 2/20 → INSUFFICIENT) and is **replaced** by the Wilson per-text rule: with r = fraction of null texts at or
   above K4's per-slice level, Wilson [lo, hi]: **EXCESS** iff hi ≤ α; **NO-SIGNAL** iff lo ≥ α; else **INSUFFICIENT-DISCRIMINATION**. For K4 = 0 the
   exclusion is exact under its stated assumptions; "discriminating" iff hi(any-hit rate) ≤ α, "non-discriminating" iff lo > α, else undetermined.
   α = 0.05.
3. **Distance to the bar:** for a p-value, distance = α/p (signal side) or p/α (no-signal side); for counts / EXACT-EXCL, the Wilson bound of the null
   rate against the K4 rate (lo/α or α/hi). **Robust** (and only then a mechanism reading) iff distance ≥ 2× **and** the same side on a
   fresh-null replicate; otherwise the label carries the suffix **FRONTEIRA** and no causal reading. Count ratios are descriptive only (heavy tails,
   null firing rates of 65–80 %). Retroactive application = descriptive relabelling only.
4. Labels stay separate: `EXACT-EXCL` (under stated assumptions) / `NO-SIGNAL` / `INSUFFICIENT-DISCRIMINATION` / `FRONTEIRA` suffix. Small null samples
   do not support tail claims: with 20 nulls a Wilson upper bound below 0.05 is impossible, and that is printed, not hidden.

## Part D — publication
`k123_eng.txt` (needed by plant229/230/232) is published in `tools/cycle232/` with its sha in `HASHES232.txt`. The fresh-null outputs (filtered
to S/T/M/P/Y/N lines) go to `data/cycle232/R/` with `SHA256SUMS` so Voynich can replicate I-342 on nulls she did not see.

## Budget
`setsid timeout 480 bash run232.sh` in its own process group (≈ 32 × 11.5 s + plants ≈ 6.3 min). If it times out, the run resumes once
(`resume`) for the remaining texts; any text still missing is listed and the scope (calibration / holdout counts) is stated as run.
A real solution = 97 letters of coherent English with EASTNORTHEAST at 21–33 and BERLINCLOCK at 63–73, reproducible.
