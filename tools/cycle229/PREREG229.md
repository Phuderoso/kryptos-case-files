# PREREG229 — Cycle 229 (audit): the I-330 NC bar's quadgram floor (I-335), n ≥ 11 vs n ≥ 12 vs 10, on fresh nulls with a low-n plant ladder; Part B: full-scale V nulls for the case 213 edges (I-337)

Filed 2026-11-21 (time = this commit), before any plant, null or K4 run of `kb229` other than the gate-T / smoke checks disclosed
below. Base: origin/main 2471b2f (c228 published). Case file 215. Slot: **audit** (I-334 / I-338: 229 must be an audit = I-335).

## Why
Case 213's only null pass of the house bar (null 209425, Q all.bin p 24, r10 row 78680, NC −5.29) had exactly **10** non-crib
quadgrams, the bar's floor. Voynich's independent n-quad recount (voynich-case-files 518a839 / d26217b, index 2252322; frozen
22:01:28 MST 2026-11-20) agrees (−5.2916, 4 hits / 1 collapsed text) and shows that over the printed B / C null decrypts the null
max is below −6.0 for every n ≥ 11 (n 11: −6.31, n 12: −6.24, n 14: −6.11); a floor of 20 would lose plant 13 (n 11). Her table is
built from printed lines only (B = running best, C = old all-letter candidates), not the full decrypt population. Decision taken after
c227 (I-335 / I-338): **no post-hoc change**. This file fixes the floor choice rule and its gates before the run.

## Tool
- `tools/cycle229/kb229.c` = `tools/cycle227/kb227.c` + one output-only addition: per (model, p, nq) over every scored V / Q hit with
  known ≥ 49 and ≥ 1 non-crib quadgram, the count, the count with NC ≥ −6.0, and the max NC (`Y` lines). Counting, decrypt (tie = '?'),
  P / M / S / T / C / X lines untouched.
- **Gate T (done before filing, disclosed):** on K4 bank Q+V geo a r10 and on null 209425 all.bin VQ geo a r10, every non-Y line of
  kb229 equals the published case 213 file (`data/cycle227/R/…`) after sorting, except `B` lines (running best: printed when a thread
  improves the max, so their set depends on thread timing; they are not used here). Null 209425 reproduces the −5.292 pass at nq 10
  (`Y model=Q p=24 nq=10 n=10 pass=4 max=-5.292`). **PASS.**
- Smoke (disclosed): `plant229.py` was run once with seed **1** (not the gate seed) to check that the rejection sampler reaches each
  target n; three seed-1 plants were run through kb229 and their P lines equalled the Python prediction. Seed 209558 not yet drawn.

## Part A — floor audit (I-335)
- **Bar (I-330, unchanged except the floor):** candidate iff known ≥ 49, NC ≥ −6.0 (mean log10 quadgram, `qg.bin` sha256 4a02ba4e…9f69,
  over quadgrams with no '?' and no crib position 21–33 / 63–73, 0-indexed), tie = '?', and nq ≥ F. F ∈ {10 (current), 11, 12}.
- **Nulls:** 16 fresh shuffled K4, seeds **209559–209574** (`random.Random(seed).shuffle`), run through the case 213 family with
  kb229: direct (GVQ geo a, GV geo b), Q behind bank.bin and all.bin on every 10th row (r10, as case 213), V geo a and V geo b behind
  bank.bin and all.bin at **full scale**. K4 is run through the same commands (reference only; raising the floor can only remove passes).
- **Counting:** null passes at each F counted as hits, **distinct decrypt texts** (per null), and null texts with ≥ 1 pass out of 16
  (Wilson 95 %). The null `Y` table (count / passes / max NC by nq, pooled) is printed beside K4's.
- **Low-n plant ladder (seed 209558, `plant229.py`):** 24 Q-model plants (kb227 alphabets, carved-index key, p 19–24, behind bank /
  all.bin alternating in pairs), target nq = 10 + ⌊pid / 4⌋ → four plants at each of n 10, 11, 12, 13, 14, 15; odd pids carry **one
  corrupted carved crib letter**; plaintext K1–K3 English or Jane Eyre. Rows / keys redrawn until known ≥ 49 and the decrypt of the true
  configuration (independent Python reimplementation of kb227's Q decrypt, tie = '?') has exactly the target n. Each plant is run with
  kb229 on its own row only. Measured nq / NC = kb229's P line; the Python prediction is a cross-check (agreement printed).
- **Gate P0 (recovery + bar power at the current floor):** ≥ 23/24 plants recovered (H line at the true configuration and period) and
  ≥ 23/24 clear the bar at F = 10 (Wilson printed). Fails → no floor adoption (the low-n bar itself is unproven).
- **Gate P(F):** among plants with n ≥ F, passes at F ≥ eligible − 1 (Wilson printed). Plants lost by construction (n < F) are listed
  as the floor's cost, not as failures.
- **Null criterion N(F):** 0 distinct null texts pass at F among the 16 fresh nulls **and** 0 in the published case 213 null P lines
  (`data/cycle227/R`). Floor 10 already fails N on the published record (null 209425), so it is not a candidate.
- **Decision rule:** adopt the **smallest F ∈ {11, 12}** with N(F), P(F) and P0 all satisfied. If neither: no adoption; the floor stays at
  10 with the case 213 caveat printed, and a quadgram-count-dependent bar (I-332 style) is queued. Nothing else is chosen after the run.
  Adoption applies from cycle 230 onward; no earlier verdict is relabelled (cases 212–214 had no K4 pass at any floor).
- **Scale statement:** 16 nulls bound the per-text null pass rate only to Wilson ≈ [0, 0.19] if 0/16; that limit is printed, not hidden.

## Part B — I-337 (full-scale V edges of case 213)
- Same 16 fresh nulls, V geo a / geo b behind bank.bin / all.bin at full scale (the Part A runs); K4 rerun with kb229 (case 213 numbers:
  V geo a bank p 19: 2, p 20: 2). Per cell p 17–24: K4 count, null counts, occupancy (Wilson), p_up = (1 + #nulls ≥ K4) / 17.
- **Labels:** K4 0 and ≤ 2/16 nulls non-zero → `EXACT-EXCL (discriminating)`; K4 0 and ≥ 3/16 → `EXACT-EXCL (non-discriminating)`;
  K4 > 0 with p_up > 0.05 → `INSUFFICIENT-DISCRIMINATION`; K4 > 0 with p_up ≤ 0.05 → read the decrypts (K4 P lines); no K4 bar pass →
  `NO-SIGNAL`. Q all.bin p 16 full scale (≈ 1–2 min per null) is **not** in this cycle (budget); stays in I-337.

## Seeds / budget / publication
Plants 209558, nulls 209559–209574; next free seed **209575**. `setsid timeout 420 bash run229.sh` in its own process group
(≈ 4–5 min expected). Analysis `analyze229.py` (no tuning after the run). Labels kept separate: EXACT-EXCL / NO-SIGNAL /
INSUFFICIENT-DISCRIMINATION. A real solution = 97 letters of coherent English with EASTNORTHEAST at 21–33 and BERLINCLOCK at 63–73.
