# Cycle 193 pre-registration — new family: the SANDWICH compound key (IDEAS I-199 via pointer I-201)

Written and pushed before any K4 or registered-null run. Timing only on the reserved shuffle seed 9191 (I-116) under **I-180** (81 routes =
all_s2048, `timeout 60`, the full registered pair set and tableau set): `cmp193` with tab4, 625 pairs, both models ≈ 0.12 s → C1 (all 165,782
routes) ≈ 250 s; whole run ≈ 6 min. Binary: `cmp193` from `tools/cycle193/cmp193.c` (`gcc -O3 -march=native -fopenmp -lm`), the core of
`cmp191`/`sw192probe` with mixed indices. Heavy budget ≤ 8 min (≈ 1.5 min used before this push: probe, meter, controls).

## Question (new family; checked against cases 119, 131, 176–179)
K3 was a transposition; K1/K2 were keyword substitutions on the KRYPTOS tableau. A layered build in K3's own order: **a keyword pass on the
plaintext, K3's transposition, then a second keyword pass on the carved text**, each pass on A–Z or on KRYPTOS. With x = T1idx(p), z = T2idx(c),
σ(y) = T2idx(T1[y]), plaintext i carved at S[i]:

  **S1:** z = s2·σ(s1·x + a[i mod m]) + b[S[i] mod n]   (s1, s2 = ±1; variant absorbed into the key sign)
  **S2:** the reverse index assignment, a[S[i] mod m] and b[i mod n] (first pass keyed by the destination cell).

Cases 176–179 put both arbitrary keys on the same side of the route (models P and C); cases 119 and 131 tried only named keyword pairs with a
transposition between the layers. With mixed indices the residue graph is different and m = n is no longer a single period, so pairs with
m = n are included. One-tableau stacks (A–Z>A–Z, KRYPTOS>KRYPTOS) with mixed indices are not covered by case 176 and are included.

## Method (exact)
As case 178: crib t is a bijection between a[i_t mod m] and b[S[i_t] mod n] (S1); on every cyclic component of the residue graph all 26 root
values are tried and propagated, every non-tree edge checked; tree components always satisfiable. A config fits iff every cyclic component
keeps ≥ 1 root value. Exactness re-checked before K4: `recount193.py` (independent, literal letter tables) vs `cmp193` on a uniform random text
(seed 19340), 6 probe routes, tab4: 36,549 fits, identical.
**Chance count (I-193):** E_config = Π_cyclic 26^(1−r_c) = exact expected solutions for uniform carved letters. **Meter, 40 uniform texts
(seeds 19340–19379), 81 routes:** two-tableau pairs match in every band (z −0.20, +0.50, +0.43, +0.06, +0.58 for e = 0–4; 0 fits where
E ≤ 0.14). One-tableau stacks are additive, so solutions come in bundles of 26 (a cyclic component passes for all 26 root values or none) and
are strongly correlated across forms and period multiples: pooled tab4 showed e = 3 at 105 vs 209 (all 105 from the two-tableau pairs, one-tableau
0 vs 104). Checked on 400 further texts (seeds 19380–19779): one-tableau e = 0–4 z −2.11, +0.28, −0.73, −1.44, +0.66 (e = 3: 624 vs 1,044;
e = 4: 104 vs 35), i.e. lumpy but centred on E. **Rule:** E stays the expectation for labels; for one-tableau cells the fit probability is
≤ E/26 (Markov on 26-bundles), so E ≤ 0.05 is conservative there; the low-power comparison against E is reported separately for one- and
two-tableau cells, and K4's rank among the shuffles is the decision reference for low-power totals.
Pairs: ordered (m, n), 2 ≤ m, n ≤ 26, **m = n included** (625; m is the first pass). Forms VV, VB, BV, BB. Models S1 and S2.

## Registered cells
- **C1** K4, tab4 (A–Z>KRYPTOS, KRYPTOS>A–Z, A–Z>A–Z, KRYPTOS>KRYPTOS), **all 165,782 routes**, S1 and S2, 4 forms, 625 pairs.
- **Grid** K4 + 19 shuffles (seeds 19311–19329, `nulls193.txt`), tab4 on all_s512 (324 routes).
- **C3** K4, 572 themed × {A–Z, KRYPTOS} pairs on all_s512, condensed on the fly (H summed over the tableau pairs of each file, `agg193`).
- **No direct cells:** on the identity route S1 = S2 = case 178's model P with m ≠ n (already `EXACT-EXCL` there, C2t/C2v); the identity is not in all.bin.
- **Recount** `recount193.py` vs `cmp193` (all fits) on slice191 (7 rows), tab4, texts K4, P1, P2, P6, n19311: fit sets and solution counts identical.
- **Power note for Voynich (descriptive, no decision weight):** G lines give, per (model, m, n), the band histogram of route configs; for the
  full-power C1 cells we report the share of configs per E_config band and the 80th-percentile E_config of a planted config (the analogue of
  their 80th-percentile plant p).

## Labels
Cell = (model, tableau pair, form, m, n) over its routes (C3: over all 572 pairs). Cell E ≤ 0.05 = full power: K4 0 fits → **`EXACT-EXCL`**; any
K4 fit in a full-power cell → decoded with `decode193.py` before any label; a solution needs a full coherent English decryption with
EASTNORTHEAST and BERLINCLOCK at the official positions, reproducible. E > 0.05 → **`LOW-POWER`** (totals vs E and vs the shuffles: p⁺ =
(1 + #nulls ≥ K4)/20, floor 0.05, rank flag only; I-182/I-203). If a full-power cell's H fit count exceeds its printed M lines, it is re-run
with full printing before labelling. Missing `END` = not run.

## Controls (`plant193.py`, seed 19300; passes applied literally letter by letter) — rehearsed 13/13, declared the registered control run
Positives (fit at row, tableau pair, reduced form, model, (m, n), plaintext reproduced by the decoder): P1 A–Z>KRYPTOS S1 Vig 7 / Vig 11 (row
12345); P2 KRYPTOS>A–Z S1 Beau 5 / Vig 13 (row 100000); P3 A–Z>KRYPTOS S2 variant 8 / Beau 12 (row 18944); P4 KRYPTOS>A–Z S1 Vig 6 / Beau 19
(row 165781); **P5 PALIMPSEST (A–Z, Vig) → route 12345 → ABSCISSA (KRYPTOS, Vig)**, decoded in full (97/97, both keywords recovered); P6
A–Z>A–Z S1 variant 3 / Vig 25 (row 51712); P7 KRYPTOS>KRYPTOS S1 Beau 4 / Beau 9 (row 12345); P8 A–Z>KRYPTOS S1 Vig 7 / Beau 7 (m = n,
row 100000); P9 KRYPTOS>A–Z S2 Beau 6 / Beau 10 (row 18944). Negatives (no fit with E_config ≤ 1e-4 at the row): N1 three passes (5 on the
plaintext index, 7 and 11 on the carved index); N2 random key; N3 = P1 with one wrong carved crib letter; **N4 a case-178 compound key** (both
keys on the plaintext index), not a sandwich. **Non-equivalence:** case 178's `cmp191` finds N4 but none of P1, P5, P8 at their rows.
**Rehearsal fix (disclosed, I-195):** N3's wrong letter was first put on slot 2, a pendant edge of P1's graph (outside the 2-core), where no crib
test can see it, so P1's cell still fitted; it was moved to slot 3, the first 2-core slot ≥ 2.

## Not covered (stated now)
One wrong crib letter; three or more passes; m or n > 26 or = 1; vocabulary tableaux; themed pairs beyond 1/512 of the routes; dropped/extra
letters; a different transposition between the passes than the K3-law decimations/routes.
