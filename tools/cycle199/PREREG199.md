# PREREG199 — I-220 chunk 1: two-tableau indel compound key behind the NON-M = N decimations

Written 2026-11-10 ~19:45 PT, before any K4 or shuffled-K4 run with this scope. Run so far: the reserved shuffle (seed 19790, timing
probe) and the planted controls below (rehearsal 6/6, `controls199_rehearsal.txt`).

## Why
Case 184 ran solver B (two tableaux A–Z/KRYPTOS either order, bijection graph, `cmp197`) behind the pure decimations M = N only
(decM98 4,116 + decM96 3,072 perms); the rest of the families (dec98 166,142 + dec96 165,786 perms) was left open (I-220).
`[speculation]` model as in PREREG197 (one dropped / one extra carved letter, two periodic keys on two tableaux).

## Cost correction (disclosed)
I-220 estimated ≈ 700 s for the whole remainder. The probe on the reserved shuffle says otherwise: ≈ 36 ms/perm (dec98) and
≈ 26 ms/perm (dec96) single-thread on non-M = N perms, ≈ 10,300 core-s in total (≈ 25 min on 7 threads). Also found: the M = N perms
are exactly dec98 q 0–4115 and dec96 q 0–3071 (checked by byte comparison), and `cmp197`'s q range is half-open [qlo, qhi).
Per I-229 the registered stage is cut to the budget: **chunk 1 = dec98 q 4116–28115 and dec96 q 3072–27071 (24,000 perms each,
≈ 14 % of the remainder)**. Chunks 2–7 stay queued (I-232).

## Run (`run_cycle199.sh`)
`cmp197` from tools/cycle197 unchanged, compiled with `-fopenmp` (7 threads; it has an OpenMP loop, earlier cycles' builds may have
been single-threaded), registered pair lists `pairsB_del.txt` / `pairsB_ins.txt` (chosen by the cycle-197 structure pass on the M = N
subsets; pairs that would be full-power on non-M = N perms but were not selected stay a blind spot), print threshold E_config ≤ 0.002.

## Classification (registered)
- A cell = (kind, model, tableau pair, form, m, n). Its E for the chunk is printed by the run. Because the chunk is part of a bank, a cell
  is **full-power for the bank only if E_chunk × (bank / chunk) ≤ 0.05** (dec98 factor 166,142/24,000 = 6.92, dec96 165,786/24,000 = 6.91);
  cells with E_chunk ≤ 0.05 but above that are reported as full-power *within the chunk only*.
- `EXACT-EXCL` (chunk scope) if every fit in full-power cells is decoded (every equivalent d) and none reads as English (≥ 3 real
  words off the cribs, quadgram score vs plants). Fit totals compared with the summed E. Cells above 0.05: `LOW-POWER`, 20 strongest fits decoded.
- Real solution only as in the routine: full 97-letter coherent English with both cribs, reproducible.

## Controls (post-run must equal rehearsal)
P7n dec98 q 10000 del d 60 model C AZ>KA VB TIME+KRYPTOS; P8n dec96 q 20000 ins d 10 model P KA>AZ VV SHADOW+LIGHT; P9n dec98 q 27000
del d 33 model P KA>AZ BB ABSCISSA+CLOCK; negatives N7n/N8n/N9n = the same plants with two crib-slot letters shifted by 7: must not fit
at the planted cell. Encryption independent of `cmp197` (`plant199.py`, plant197's `make`, `lib197`). Each plant runs on its own perm only.

## Nulls and grid
19 shuffled-K4 texts (seeds 19951–19969) and K4 on every 64th perm of the chunk (375 + 375 perms, `dec98_c1s64` / `dec96_c1s64`).
Statistic (I-217 style): number of distinct clusters (kind, perm, model, tableau, form) with a fit at E_config ≤ 26^−3; K4 rank of 20;
floor 0.05, descriptive only (rank 1 → pooled follow-up later, not a signal). I-230's two-direction meter check is not part of this run (still queued).
