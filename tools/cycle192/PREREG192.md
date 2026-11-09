# Cycle 192 pre-registration — audit: case 178 under one wrong crib letter (IDEAS I-197, pointer I-200)

Written and pushed before any K4 or registered-null run. Timing and pair selection only on the reserved shuffle seed 9191
(`random.Random(9191).shuffle(list(K4))`, I-116) under **I-180** (81 routes = all.bin[::2048], `timeout 60`): `cmp192` mode 0 with A–Z>KRYPTOS and
KRYPTOS>A–Z, all 600 pairs ≈ 0.36 s; on the candidate pairs ≈ 0.13 s → C1 on all 165,782 routes ≈ 265 s; whole run ≈ 7 min.
**Chance meter checked before K4 (I-193, one-error form):** 40 uniform random texts (seeds 19240–19279) on the 81 probe routes, all 600 pairs,
mode 1: the meter statistic S1 matches its exact expectation U per band e = round(−log26 U): band 1 194,326 vs 193,366 (text-level z +0.22),
band 2 2,170 vs 2,031 (+0.97), band 3 35 vs 35.2 (−0.03); 0 fits in bands ≥ 4 (U 1.29, 0.052, …). Fits ≤ U in every band ≥ 1.
**Planted controls rehearsed before this push: 13/13** (`plant192.py` seed 19200, `run_controls192.sh`, `checkctl192.py`); the rehearsal is the
registered control run. Two fixes in the rehearsal, before any K4 run (disclosed): (1) N3's second wrong letter (slot 17) sat in a pendant part
of the graph once slot 2 was deleted, so the two-error plant was a one-error plant and fitted; plant192 now picks wrong slots in the 2-core
(positives) and, for two-error negatives, a second slot in the core without the first and vice versa (I-195: different classes). (2) P4's
requested slot 0 was outside the core (invisible error, strict fit); now slot 4. Recount rehearsed on P1 (row 0 of slice191, m, n ≤ 12: 32
fits, identical). Binary: `cmp192` from `tools/cycle192/cmp192.c`, `gcc -O3 -march=native -fopenmp -lm`. Heavy budget ≤ 8 min (≈ 30 s used).

## Question (audit of case 178)
Case 178 excluded z = s2·σ(s1·x + a[i mod m]) + b[i mod n] (two arbitrary periodic keys on two different tableaux, A–Z then KRYPTOS or the
reverse, Vig/Beau/variant, key on the plaintext or carved index, behind the 165,782 K3-law decimations/routes) **strictly**: all 24 cribs exact.
Sanborn's K1–K3 carry errors. Does the exclusion survive **one** wrong carved or crib letter anywhere in the 24 crib positions?

## Method (exact; new solver `cmp192.c`)
A wrong letter at slot t is an edge whose bijection is unknown, i.e. a deleted edge. In a bijection graph, unlike case 177's additive graph,
a bridge between two cyclic parts constrains (each part keeps only some root values), so **every** slot is tried, not one per series class.
Deleting t only changes t's component K, and pendant trees never constrain, so the deletions of K are reduced to the distinct 2-cores of
K − t. Fit = all cyclic components consistent (strict), or exactly one component fails and some distinct core of it minus one slot is
consistent. **Chance count:** U = Σ_K Σ_d (E_G/E_K)·E_d (E as in case 178), capped at 1, bounds the fit probability; the statistic
S1 = Σ_K Σ_d sols(G∖K)·sols(d) has exact expectation U (meter above). A cell is full power iff its U, summed over routes (and tableau pairs),
is ≤ 0.05. Cells = (model, tableau pair or tableau-pair list, form, m, n) as in case 178.

## Pair selection (structure only, mode 2, text-free, fixed now)
C1 runs only the ordered pairs whose cell U estimated from all_s512 × 512 is ≤ 1 (P 138, C 118; 20× margin over the full-power threshold);
C3 pairs with 572·U_s512 ≤ 1 (254); C2t pairs with 20,592·U_direct ≤ 1 (166); C2v 75,292·U_direct ≤ 1 (138). All other cells: **`LOW-POWER`
(structural estimate)**, not run. The labels themselves use the exact U computed in the run.

## Registered cells (`run_cycle192.sh`, in this order)
- **C1** K4, A–Z>KRYPTOS and KRYPTOS>A–Z, **all 165,782 routes**, P and C, 4 forms, pairs_c1.
- **Grid** K4 + 19 shuffles (seeds 19211–19229, `nulls192.txt`), tab2 on all_s512 (324 routes), all 600 pairs.
- **C3** K4, 572 themed × {A–Z, KRYPTOS} pairs (both orders) on all_s512, pairs_c3.
- **Recount** `recount192.py` (independent: literal letter tables, all 25 deletions tried with no 2-core reduction or deduplication) vs
  `cmp192` on slice191 (7 rows), tab4 (incl. A–Z>A–Z, KRYPTOS>KRYPTOS), all 600 pairs, texts K4, P1, P2, P7, n19211: fit sets identical.
- **C2t** K4 direct, 20,592 themed × themed pairs, pairs_c2t. **C2v** K4 direct, 75,292 vocabulary × {A–Z, KRYPTOS}, pairs_c2v (lowest priority).

## Labels
Full-power cell (U ≤ 0.05) with 0 K4 fits → **`EXACT-EXCL` (one-error scope)**. Any fit in a full-power cell → decoded with `decode192.py`
(every consistent deletion printed) before any label; a solution needs a full coherent English decryption with EASTNORTHEAST and
BERLINCLOCK at the official positions (at most one crib letter off), reproducible. U > 0.05 → **`LOW-POWER`**; totals vs U and vs the
shuffles (p⁺ = (1 + #nulls ≥ K4)/20, rank flag only, I-152/I-182). Fits printed for U ≤ 0.002; if a full-power cell's fit count exceeds its
printed lines, that cell is re-run with full printing before labelling. Missing `END` = not run.

## Controls (`plant192.py`, seed 19200, passes applied literally letter by letter)
Positives = case 178's eight plants, each with ONE wrong carved crib letter (P1 slot 2, P2 15, P3 23, P4 4, P5 9, P6 19, P7 12, P8 6;
unequal shifts) plus P0 = P1 without error (strict, slot −1). Each must fit at its row, tableau pair, form, model and (m, n), and
decode192 must reproduce the planted plaintext at every determined position except the deleted slot's own position, with the planted
slot among the reproducing deletions or an equivalent slot named (I-195). Negatives (no fit with U ≤ 1e-4 at the planted row): N1 three
passes, N2 random key, N3 = P1 with two wrong letters (requested 2, 17 → used 2, 18 after the class check), N4 = P4 with two wrong letters (requested 0, 23 → used 4, 5).

## Not covered (stated now)
Two or more wrong letters; dropped or extra letters (I-196); the sandwich with a transposition between passes (I-199); themed pairs behind
the routes beyond all_s512 and vocabulary pairs behind the routes (I-198); m or n > 26; three or more passes.
