# Case file 149 — The rank-matched Gromark L 8 lineup, completed (cycle 161)

**Cycle 161, 2026-11-08. Audit of method** (IDEAS [I-062](../IDEAS.md); completes [case 147](147-rank-matched-nulls-gromark-l8.md), which
follows [case 143](143-gromark-one-error.md) and [case 145](145-structure-matched-nulls.md)).

## Question
Case 147 compared K4's one-error-feasible Periodic Gromark cases (relaxed model P, digit primers, L 8; K4 = 28) with 48 shuffles
matched on the crib-letter repetition profile **and** the crib-graph cycle rank r8 = 6, but only over primers 0–50 M for all nulls
(p 0.10). Two things were left open: the full-range comparison, and a loose end noticed **after the fact** — K4 has 13 of its
28 cases in the last primer quarter (75–100 M), above all 7 nulls that had reached it (max 6).

## Method
- **Same solver, same nulls.** `tools/cycle155/gromark1e.c` byte-identical to the cycle-159 copy; the rebuilt binary has the same
  sha256 (`c63bb0702dbe…99b1b6`). Nulls = `data/cycle159/nulls.txt` (unchanged). Runner = `tools/cycle159/run_cycle159.sh`, resumed in
  a copy of the cycle-159 work directory: it skipped the 122 finished chunks and ran the 70 left (q2 for 29 nulls, q3 for 41).
- **Pre-specification** (local checkpoint, written before any resumed result was read): primary = full 10⁸ count for all 48 nulls
  (it was a secondary statistic in case 147), K4 = 28, p_upper = (1 + #{null ≥ K4}) / (N + 1), Bonferroni ×4 because the L 8 row was
  picked post hoc among the four relaxed `LOW-POWER` rows of case 143. The q3 comparison is reported as **post hoc**, with ×4 (quarter
  choice) and ×16 (quarter and row).
- **Resume integrity** (`data/cycle161/consistency.txt`): the cycle-159 results file is an exact prefix of the completed one; 192 of
  192 (null, quarter) chunks, each exactly once, every chunk 25,000,000 primers; the cycle-159 primary (0–50 M, p 0.102) reproduces.

## Checks
- **K4 regression:** all 10⁸ L 8 primers rerun with the same binary: one-error cases 5 / 5 / 5 / 13 = **28**, as in cycle 155.
- **Planted controls** (`tools/cycle161/plant161.py`, primers forced into the resumed range): KA/Beau with a carved error at pos 29 →
  planted primer feasible (the changed letter stayed consistent under the free cipher alphabet); AZ/Vig with a wrong crib letter at
  pos 24 → recovered **only** as a one-error survivor, drop at pos 24 among its drops; clean KA/Vig → strict-feasible. **3/3.**
- **Independent recount** (`tools/cycle159/indep159.py`, pure Python, no shared code): 7 windows of 20,000 primers (5 around new null
  survivors in q2/q3, 2 around K4 q3 survivors) — strict / one / pairs **identical 7/7**.

## Results (`data/cycle161/summary_full_and_quarters.txt`)
| statistic | K4 | 48 rank-matched nulls: min / median / max, #zero | #null ≥ K4 | p_upper (resolution 0.020) | corrected |
|---|---|---|---|---|---|
| **primary: full 10⁸ primers** | **28** | 0 / 3.5 / 37, 13 zero | 3 (34, 35, 37) | **0.082** | Bonferroni ×4 (row) **0.33** |
| q0 (0–25 M) | 5 | 0 / 1 / 10 | 3 | 0.082 | — |
| q1 (25–50 M) | 5 | 0 / 0 / 13 | 5 | 0.12 | — |
| q2 (50–75 M) | 5 | 0 / 1 / 12 | 6 | 0.14 | — |
| **q3 (75–100 M), post hoc** | **13** | 0 / 1 / 11, 20 zero | 0 | **0.020** (floor) | ×4 quarter 0.082; max-over-quarters 0.041; ×4 row 0.16; ×16 0.33 |

Full-range sorted null counts: 0 ×13, 1 ×6, 2 ×2, 3 ×3, 4, 5 ×3, 6 ×6, 7 ×2, 8 ×2, 9 ×2, 10, 12, 18, 23, 27, 34, 35, 37.
Strict (all 24 cribs): K4 0, every null 0. The **max-over-quarters** correction asks how often a null's busiest quarter reaches 13:
once in 48 (rnull17, 13 in q1), so p = 2/49 = 0.041 before the row correction.
**Descriptive, post hoc:** all 28 K4 cases use the A–Z plain alphabet; nulls cluster too (rnull47 36 KA / 1 AZ, rnull06 23 / 0,
rnull10 18 / 0; `posthoc_alphabet_split.txt`). No weight.

## Verdict
- **No solution.** Over the full primer space K4 sits just inside the top 10 % of 48 rank-matched nulls (p 0.082; 0.33 after the
  row correction). Three nulls exceed it. **No count-level anomaly.**
- **Loose end closed.** K4's last quarter beats every null (13 vs max 11), but the comparison was chosen after seeing it; with
  the honest corrections it is 0.041 (quarter) and 0.16 (quarter and row), and the empirical p cannot go below the 0.020 floor with
  48 nulls. Chance survivors cluster by primer range in the nulls too (busiest null quarters 13, 12, 11, 10). **Not evidence.**
- **Labels:** relaxed Periodic Gromark digit L 8 under one error stays **`LOW-POWER`** as an exclusion (structure-matched shuffles leave
  up to 37 survivors) and **`NO-SIGNAL`** as an anomaly test. Decoding the 28 primers (I-051) is not promoted.

## Limits
- 48 nulls only (p resolution 0.020); r matched at L 8 only; other crib-graph structure not matched.
- L 9 digits and L 11–12 ranks still lack rank-matched nulls. Checkpoint: 48 profile + r9 = 7 shuffles generated
  (`nulls_r9_checkpoint.txt`; r9 = 7 holds for 91 % of profile-matched shuffles, so rank matching barely restricts at L 9).
  Exhaustive L 9 costs ≈ 10⁹ primers × 49 texts ≈ 23 core-hours → sampled design (I-063 → I-067).
- Heavy compute ~6.6 min (inside the ~8 min budget).

## Files
[tools/cycle161/](../tools/cycle161/) (`run_cycle161.sh`, `summarize161.py`, `plant161.py`, `README.md`) · [data/cycle161/](../data/cycle161/)
(`summary_full_and_quarters.txt`, `c_lines_resumed.txt`, `null_survivors_resumed.txt`, `consistency.txt`, `k4_regression.txt`,
`controls.txt`, `indep_windows.txt`, `posthoc_alphabet_split.txt`, `nulls_r9_checkpoint.txt`, `nulls_r9_generation.txt`, `timing.txt`) ·
[journal](../journal/2026-11-08-cycle161.md).
