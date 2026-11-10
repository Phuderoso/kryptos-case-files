# Cycle 194 pre-registration — audit: the sandwich compound key under ONE wrong crib letter (IDEAS I-204 via pointer I-207)

Written and pushed **before** any K4 or registered-null run. Timing only on the reserved shuffle seed 9191 (I-116) under **I-180**.
Binary: `cmp194` from [`cmp194.c`](cmp194.c) (`gcc -O3 -march=native -fopenmp -lm`) = case 179's one-error solver `cmp192` with case 180's
mixed indices (`cmp193`). Heavy budget ≤ 8 min; ≈ 0.6 min used before this push (probe, structure pass, meter 23 s, controls 6 s, recount check).

## Question (audit of case 180; checked against cases 177, 179, 180)
Case 180 excluded the sandwich (keyword pass a, period m → K3-law decimation/route → keyword pass b, period n; A–Z>KRYPTOS, KRYPTOS>A–Z,
A–Z>A–Z, KRYPTOS>KRYPTOS; Vig/Beau/variant; S1 = a at the plaintext index, b at the carved index; S2 the reverse; 2 ≤ m, n ≤ 26 incl. m = n)
only under the **strict** test. A single wrong carved or crib letter in the crib window (K1–K3 all carry slips) breaks every crib cycle
through its edge. Does a one-error sandwich survive?

## Method (exact)
A wrong letter at slot t = an edge with an unknown bijection = a deleted edge. As in case 179 (I-202): every slot tried; deletions with the
same 2-core of K − t deduplicated; fit iff all cyclic components consistent (strict), or exactly one component K fails and some distinct core
of K − t is consistent. Strict part checked identical to `cmp193` (probe81, tab4, 625 pairs, both models). Independent recount
[`recount194.py`](recount194.py) (literal letter tables, all 25 deletions, no reduction) identical to `cmp194` on a uniform random text
(seed 19440, slice191 row 1, all 1,250 model-pairs, 7,355 fits).
**Chance bound (I-193 one-error form):** U = Σ_K Σ_d (E_G/E_K)·E_d (capped at 1) bounds P(fit); statistic S1 has exact expectation U.
**Meter, 40 uniform texts (seeds 19440–19479), all_s2048, 625 pairs, metered apart (I-205)** ([checks](prereg_checks194.txt)):
two-tableau bands 1–4: S1 vs U 234,721 vs 234,486 (z +0.09), 2,253 vs 2,303 (−0.50), 27 vs 38.1 (−2.11), 3 vs 1.30 (+1.01); 0 fits in bands ≥ 5
(U 0.054, 0.002, …). One-tableau (additive) bands 1–2: 91,104 vs 117,243 (z −3.39), 676 vs 1,152 (−1.22); band 3: 0 vs 19.0 — lumpy as in
case 180 (26-bundles; the 400-text check there centred these bands), and in every band of both types **fits ≤ U**, which is what the labels
use. Not re-run at 400 texts (budget).
**One-tableau forms:** in A–Z>A–Z and KRYPTOS>KRYPTOS BB = VV and BV = VB exactly (a → −a), so those run forms VV and VB only; equivalents listed.

## Pair selection (text-free, fixed here)
Structure-only pass (mode 2) on all_s512 of the reserved shuffle ([struct](struct512_r9191.txt)); cell U estimate = U_s512 × 165,782/324.
Registered: pairs with estimate ≤ 0.05 → [`pairs_fp.txt`](pairs_fp.txt), **116 per model**. (≤ 1 would be 136 per model, ≈ 470 s on all
routes, over budget.) Pairs not run are `LOW-POWER` by that estimate; labels use the exact U computed in the run.

## Registered cells ([run script](run_cycle194.sh))
- **C1a** K4, A–Z>KRYPTOS + KRYPTOS>A–Z, 4 forms, S1 + S2, pairs_fp, **all 165,782 routes** (est. ≈ 246 s).
- **C1b** K4, A–Z>A–Z + KRYPTOS>KRYPTOS, VV/VB, S1 + S2, pairs_fp, all routes in 8 chunks of 20,723 rows; a chunk starts only if the run's
  elapsed time ≤ 390 s (budget gate; unrun chunks reported as not covered).
- **Grid** K4 + 19 shuffles (seeds 19411–19429, [`nulls194.txt`](nulls194.txt)), tab2 + tab1s on all_s2048 (81 routes), all 625 pairs.
- **Recount** `recount194.py` vs `cmp194` (all fits) on slice191 (7 rows), pairs_fp, texts K4, P1, P4, P7, n19411: fit sets identical.
- Not registered (budget): themed pairs behind the routes (case 180's C3), pairs with estimated cell U > 0.05.

## Labels
Cell = (model, tableau pair, form, m, n) over all routes. Cell U ≤ 0.05 = full power (one-error scope): K4 0 fits → **`EXACT-EXCL`
(one-error)**; any fit there is decoded with [`decode194.py`](decode194.py) under every consistent deletion before any label (all fits with
config U ≤ 0.05 are printed, so every fit of a full-power cell is printed). A solution needs a full coherent English decryption with
EASTNORTHEAST and BERLINCLOCK at the official positions, reproducible. U > 0.05 → **`LOW-POWER`** (totals vs U, and K4's rank among the
shuffles: p⁺ = (1 + #nulls ≥ K4)/20, floor 0.05, rank flag only; I-182/I-203: a flag goes to a pooled 19 + 40 reference, not a claim).
Missing `END` = not run.

## Controls ([`plant194.py`](plant194.py) from case 180's plants, seed 19300) — rehearsed 15/15, declared the registered control run
Positives (fit at row, tableau pair, reduced form, model, (m, n); deletion of the planted slot reproduces the planted plaintext at every
determined position except the corrupted one): P1–P9 = case 180's P1–P9 (incl. **P5 PALIMPSEST → route 12345 → ABSCISSA**, P8 m = n, P6/P7
one-tableau stacks, P3/P9 model S2), each with one wrong carved crib letter (+7) on a 2-core slot (requested slot moved to the next 2-core
slot, computed independently by leaf peeling). P0 = P1 without error (strict fit). **PD = P1 with the wrong letter on pendant slot 0:
expected strict fit and reported as an undetectable error** (the strict decryption is wrong on that edge's residue class, 8 positions).
Negatives (no fit with U ≤ 1e-4 at the row): N1 three passes, N2 random key, N3 = P1 with two wrong letters (slots 1 and 3, each in the
other's remaining 2-core, shifts +7 / +11), N4 a case-178 compound key.
**Rehearsal notes (disclosed):** (1) the checker first required PD's strict decryption to be wrong only at the corrupted crib position; a
pendant error sets that edge's whole residue class from the wrong letter, so PD now must reproduce the rest under deletion of its slot and
reports the residue-class damage. (2) P4's wrong letter (slot 4) leaves its component consistent with a different root value (a bijection
cycle keeps a value with probability ≈ 1 − 1/e when r = 1), so `cmp194` reports it as a strict fit; deletion 4 reproduces the plant. (3) The
solver reports the first slot of a deduplicated 2-core (P2 2 for 15, P3 4 for 23, P6 10 for 21, P7 11 for 12; I-195).
