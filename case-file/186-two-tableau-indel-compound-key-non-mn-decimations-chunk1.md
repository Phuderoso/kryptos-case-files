# Case file 186 — The rest of the decimations, first slice: case 184's two-tableau indel stack behind non-M = N decimations (cycle 199)

**Status:** negative, partial coverage (chunk 1 of ≈ 7). **Type:** coverage completion of case 184 (I-220 via pointer I-226).
Pre-registered in [`tools/cycle199/PREREG199.md`](../tools/cycle199/PREREG199.md) as a **local commit dbc3e00 (2026-11-10 19:44:28 PT)**
before any K4 or shuffled-K4 run. The GitHub connector was unreachable for this whole run, so nothing could be pushed before the run; the
pre-registration is published together with the results, with its local commit time stated here. That is weaker than a public
timestamp, and this file says so.

**Result in one line:** if K4 were case 184's model with **two tableaux** (A–Z>KRYPTOS or KRYPTOS>A–Z, Vig/Beau per pass, two periodic keys,
one dropped or one extra carved letter) **behind a K3-law decimation with skipped slots (M ≠ N)**, then on **chunk 1** (dec98 q 4116–28115 and
dec96 q 3072–27071, 48,000 of the 331,928 non-M = N perms, 14.5 %): cells at full power for the whole bank (E_chunk × 6.9 ≤ 0.05)
**drop 1,744 cells, 1 fit vs E 0.585; extra 2,016 cells, 2 fits vs E 0.528**; cells at full power for the chunk only: drop 256 cells 8 vs 8.98,
extra 112 cells 1 vs 1.91. **All 12 decoded under every equivalent d: gibberish** (off-crib quadgram −7.9 to −8.4; English ≈ −4.5).
`EXACT-EXCL` (chunk scope) on the full-power cells, `LOW-POWER` on the rest (drop 112 cells 28 vs 37.6, extra 352 cells 354 vs 583.6, at or
below chance). **No solution.**

## What was found before the run (disclosed)
- **The I-220 cost estimate was wrong.** ≈ 700 s was extrapolated from M = N perms; on the reserved shuffle (seed 19790) the non-M = N perms
  cost ≈ 36 ms (drop) / 26 ms (extra) per perm single-threaded, ≈ 10,300 core-seconds in total. Per I-229 the registered stage was cut to a chunk.
- **The M = N perms are exactly dec98 q 0–4115 and dec96 q 0–3071** (checked by byte comparison against decM98/decM96), so the non-M = N
  remainder is a clean index range.
- `cmp197`'s q range is half-open [qlo, qhi) — my first control rehearsal ran zero perms and "missed" every plant. Caught before registration.
- `cmp197` has an OpenMP loop; this cycle compiled it with `-fopenmp` (7 threads). Same source, same output (controls identical).

## Controls (6/6, post-run identical to the rehearsal)
P7n dec98 q 10000 drop d 60, carved index, AZ>KA VB, TIME + KRYPTOS; P8n dec96 q 20000 extra d 10, plaintext index, KA>AZ VV, SHADOW + LIGHT;
P9n dec98 q 27000 drop d 33, plaintext index, KA>AZ BB, ABSCISSA + CLOCK: each found at its planted cell. N7n/N8n/N9n (the same plants with two
crib-slot letters shifted by 7): no fit at the planted cell. Encryption by plant197's `make` (`lib197`, independent of `cmp197`).
Scope: recovery within the registered pair lists only.

## Nulls and grid (descriptive)
19 shuffles (seeds 19951–19969) and K4 on every 64th perm of the chunk (375 + 375). Cluster count at E_config ≤ 26^−3: **K4 0**, nulls
0,0,0,0,0,0,1,1,1,1,1,1,2,2,2,2,3,3,3 (p⁺ 1.00, p⁻ 0.35). K4 sits at the low end, which is consistent with chance (the floor is 1/20). The I-230 two-direction check was not applied.

## Recount
Independent Python recount (`recount197.py`, BFS, no union-find) on the first 40 perms of each sample bank: identical per-cell fit counts
(drop 0 fit cells; extra 1 cell, C AZ>KA VV 20 × 2, 8 fits, in both). A small recount, because the budget ran out; it checks the build, not the chunk.

## Blind spots
- Pair lists were chosen by cycle 197's structure pass **on the M = N subsets**. Pairs that would be full power on M ≠ N perms but were not selected
  were not run (I-234).
- Chunks 2–7 (dec98 q 28116–170257, dec96 q 27072–168857) are not run (I-232).
- No one-error version here (I-227). Themed alphabets were not run (I-225).

## Compute
Probe ≈ 2.5 min (incl. a 60 s timeout), registered run 19:44:28–19:49:38 PT (310 s), controls/recount ≈ 40 s: heavy ≈ 8.8 min, slightly over budget.

## Files
`tools/cycle199/`: PREREG199.md, run_cycle199.sh, run_controls199.sh, plant199.py, ctl199.txt, controls199_rehearsal.txt / _post.txt,
summarize199.py, summary199.txt, k4_decodes199.txt, runlog199.txt; `data/cycle199/` recount outputs. Solver: `tools/cycle197/cmp197.c`.
