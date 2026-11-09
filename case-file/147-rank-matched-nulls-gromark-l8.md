# Case file 147 — Cycle-rank-matched nulls for the Periodic Gromark L 8 one-error survivors (cycle 159)

**Cycle 159, 2026-11-08. Audit of method** (IDEAS [I-057](../IDEAS.md); follows [case 143](143-gromark-one-error.md) and [case 145](145-structure-matched-nulls.md)).

## Question
Cycle 155 found **28** one-error-feasible digit primers for K4 in the relaxed Periodic Gromark model P at L 8 (arbitrary cipher
alphabet, free group offsets, A–Z/KRYPTOS plain, Vig/Beau). Cycle 157 showed that chance survivor counts follow the **cycle rank r** of
the crib graph (cipher-letter nodes ↔ group-offset nodes), and that the only four profile-matched nulls with K4's r = 6 gave 1, 2, 2, 5.
Is K4's 28 genuinely above its rank-matched baseline (then the 28 primers deserve decoding, I-051), or was four nulls simply too few?

## Method
- **Nulls** (`tools/cycle159/mknulls159.py`): shuffles of K4's 97 letters accepted only if the 24 crib cipher letters have K4's
  repetition profile (3-2×8-1×5, 14 distinct) **and** r = 6 at L 8. 48 accepted of 19,350 shuffles (135 profile-matched; 36 % of
  those also had r = 6). Data: `data/cycle159/nulls.txt` (r at L 9/11/12 listed for reference).
- **Test:** the unchanged cycle-155 program, model P, all 10⁸ digit primers at L 8 in four quarters of 25 M. Statistic = one-error-
  feasible (primer, plain alphabet, form) cases, summed as in cycles 155/157 (K4: 28 = 5 + 5 + 5 + 13 by quarter).
- **Budget stop and pre-specification.** The first run (null-major order) projected ~13 min wall, so it was stopped at 125 s and
  restarted **quarter-major**. Before any result of the restart was read, the primary statistic was fixed (local checkpoint) as the
  count over the primer range completed by **all** nulls; that range turned out to be primers 0–49,999,999 (K4 = **10**).
  Secondary: 0–75 M (19 nulls; K4 15) and the full range (7 nulls; K4 28).
- **p-value:** p_upper = (1 + #{null ≥ K4}) / (N + 1). The L 8 row was singled out post hoc among the four relaxed `LOW-POWER` rows
  of case 143 (digits L 8, L 9; ranks L 11, L 12), so a Bonferroni ×4 adjustment is also reported.

## Checks
- **Planted controls** (`plant159.py`, model P L 8, random alphabet and offsets, 600 k-primer windows): carved error AZ/Vig → planted
  primer recovered with the corrupted crib (pos 33) among its drops; wrong crib letter KA/Beau → recovered with drop at pos 26; carved
  error KA/Vig → recovered with drop at pos 29; clean AZ/Beau → planted primer strict-feasible. **4/4.** (The full 11/11 control set of
  cycle 155 applies; the tool is unchanged.)
- **Independent recount** (`indep159.py`, pure Python, all 24 drops, no shared code): 12 windows of 20,000 primers (8 around null
  survivors, 2 around K4 survivors, 2 random): strict / one / pairs **identical 12/12**; K4 survivors 82560397 and 19575014 reproduce.
- **Nulls re-verified** by an independent method (cycle rank = edges − GF(2) rank of the incidence matrix, no union-find):
  **48/48** are permutations of K4 with its profile and r8 = 6; K4 r8 = 6 confirmed.

## Results (`data/cycle159/`)
| statistic | K4 | rank-matched nulls: N, min / median / max, #zero | #null ≥ K4 | p_upper (resolution) | Bonferroni ×4 |
|---|---|---|---|---|---|
| **primary: primers 0–50 M** | **10** | 48, 0 / 1 / 21, 19 zero | 4 | **0.102** (1/49 = 0.020) | 0.41 |
| secondary: 0–75 M | 15 | 19, 0 / 4 / 25 | 3 | 0.20 (0.05) | 0.80 |
| secondary: full 10⁸ | 28 | 7, 0 / 6 / 23 | 0 | 0.125 (0.125) | 0.50 |
| full 10⁸ pooled with cycle-157 r = 6 nulls (1, 2, 2, 5) | 28 | 11, 0 / 5 / 23 | 0 | 0.083 (0.083) | 0.33 |

Primary sorted null counts: 0 ×19, 1 ×7, 2 ×2, 3 ×7, 4 ×3, 5 ×2, 6, 7, 7, 8, 11, 15, 16, 21. Strict (all 24 cribs): K4 0, all nulls 0.
Per quarter (`per_quarter.txt`): K4 5 / 5 / 5 / 13; nulls q0 median 1 (max 10), q1 0 (13), q2 2 (9, N 19), q3 0 (6, N 7).

## Verdict
- **No solution.** No count-level anomaly: on the pre-specified common range K4 ranks around the top 10 % of 48 rank-matched nulls
  (p = 0.10, Bonferroni 0.41). The rank-matched baseline is heavy-tailed (0 to 21 on half the range), so cycle 157's "1, 2, 2, 5"
  understated it. The four-null contrast that motivated I-057 does **not** replicate at the 5 % level.
- **Label:** relaxed digit primers L 8 under one error stays **`LOW-POWER`** as an exclusion (nulls with K4's structure also leave
  survivors, up to 21 on half the range), and the anomaly question is answered **no signal at the count level** (consistent with chance).
  Decoding the 28 primers (I-051) is not promoted; it stays P3.
- **Not settled:** K4's quarter q3 (primers 75–99.99 M) holds 13 of its 28 cases, above all 7 nulls run there (max 6). This was noticed
  after the fact, on 7 nulls, in one of four quarters, so it carries no evidential weight; finishing the remaining 70 chunks
  (q2 for 29 nulls, q3 for 41, ~6 min, resumable) closes it (I-062).

## Limits
- Full-range comparison only for 7 nulls (budget); L 9 digits and L 11–12 ranks not rerun with rank matching (I-062).
- r is matched only at L 8; other structure (how cycles fall on plaintext letters, injectivity of the 14 letters) is not matched,
  which is part of why the baseline is wide.
- Heavy compute ~8.3 min (slightly over the ~8 min budget, mostly the stopped null-major start).

## Files
[tools/cycle159/](../tools/cycle159/) (`mknulls159.py`, `plant159.py`, `run_cycle159.sh`, `summarize159.py`, `indep159.py`) ·
[data/cycle159/](../data/cycle159/) (`nulls.txt`, `nulls_generation.txt`, `c_lines.txt`, `null_survivors.txt`,
`summary_primary_0-50M.txt`, `summary_secondary_0-75M.txt`, `summary_secondary_full.txt`, `per_quarter.txt`, `structure_check.txt`,
`controls.txt`, `indep_windows.txt`, `indep_windows_list.txt`, `timing.txt`) · [journal](../journal/2026-11-08-cycle159.md).
