# Case 230 — Audit: informative counts for case 228, when a one-error gate can test anything, rank vs parametric p, and reflected twins in Part H (cycle 244)

**Slot:** audit (I-410). Ideas **I-407** and **I-408** (tested here); Voynich's C130 / C131 / C133 questions answered; new **I-411–I-415**.
Pre-registered as [PREREG244](../tools/cycle244/PREREG244.md) (local commit fc2c5f9, 2026-11-28 10:34 MST, before any number of T1–T5). Base: origin/main **1d9a29d** (c243 published). Code: [`tools/cycle244/`](../tools/cycle244/) (`inf244.py`, `seat244.py`, `sweep244.py`, `twin244.py`, `h244.py`, `mknull244.py`, `run244.sh`, `HASHES244.txt`; `rk243.c` unchanged); results (stamped): [`data/cycle244/`](../data/cycle244/) (`SHA256SUMS`).
**Verdict: no solution; no label of any earlier case changes.** Case 228's "7 vs ≈ 33" is corrected to **7 vs 5.2 expected** (chance, rank p 0.31). The blanket "kb227 p ≥ 13 → one-error NOT TESTABLE" holds only for the direct layout; behind transpositions it is a per-layout property, and 8 of 24 one-error plant rows in cases 215 / 218 sit on untestable layouts. No label rested on a parametric p with the rank p at its floor. Part H's tie in case 229 is an exact Z27 identity; by class the gate is 10/10; 24 fresh nulls leave the bar at −4.884 and K4 at rank p 0.62.

## T1 — Case 228: how many of the 428 statistics could K4 win at all? (Voynich C131)
`inf244.py` rebuilt the 214 cells × {strict, one-error} from the `T` lines of all four scopes: **214 / 214 rows of `lowcells242.txt` reproduced, 0 mismatches**, K4 strict wins 7 (as published).
| quantity | value |
|---|---|
| statistics | 428 |
| informative (non-zero in K4 or in ≥ 1 null) | **82** (346 are 0 for all 13 texts) |
| unique-maximum statistics U | 68 |
| expected strict wins under exchangeability, U / 13 | **5.23** (case 228 wrote "≈ 33" = 428 / 13) |
| K4 strict wins | 7 (PA 31 one, PA 47 one, PA 49 strict, PA 51 strict / one, PA 52 strict ×2 — all low-constraint cells) |
| K4 mean mid-rank p over the 82 | 0.543 (exchangeable 0.5) |
| role rotation (each text as "K4" vs the other 12) | strict wins 0–11 (K4 7) → **rank p 0.308**; mean mid-rank p → **rank p 0.846** |
**Label: `NO-SIGNAL` confirmed** (both rank p ≥ 0.05). The published sentence read a deficit (7 vs 33) that a tie-dominated count cannot show; the right reference is 5.2 and K4 sits slightly above it, inside the spread of the nulls (null 209768 has 11). Addendum filed in case 228. Credit: Voynich (C131 question, 2026-11-26).

## T2 — When can a one-error gate test correction? (Voynich C130)
Rule (frozen): crib seat j sits in key class S[POS[j]] mod p; a plant's wrong seat is **PENDANT** (class size 1: the error is invisible), **TIE** (size 2: the class is blanked) or **MAJ** (≥ 3: outvoted). A (layout, p) with no class of size ≥ 3 is **NOT TESTABLE** for one-error correction.
| case (cycle) | one-error plants | PENDANT / TIE / MAJ | on NOT TESTABLE layouts | recovered + gate, pooled | on TESTABLE layouts |
|---|---|---|---|---|---|
| 215 (229) | 12 | 5 / 4 / 3 | 4 (plants 7, 11, 21, 23) | 12/12 | 8/8 |
| 218 (232) | 12 | 4 / 6 / 2 | 4 (plants 1, 7, 11, 19) | 11/12 | 7/8 (miss: plant 9, PENDANT on a testable layout) |
- **Independent agreement with C130:** case 218 counted here 4 PENDANT / 6 TIE / 2 MAJ and plant 9 PENDANT — exactly Voynich's numbers (her recount from the same published files, made first).
- **Census** (`seat244.txt`): the **direct** layout has no class of size ≥ 3 for every p 13–24 (so "p ≥ 13 → NOT TESTABLE" is exact there, which is where C130's census came from). Behind the bank, layouts with a MAJ seat are 98 % at p 13, 84 % at p 17, 60 % at p 21, 38–76 % at p 22–24; all.bin 95 % → 34 %. So the rule must be applied **per layout**, not per period.
- **Relabel (descriptive):** the 8 rows above read `NOT TESTABLE` in both gates; the pooled rates are kept beside. Both gates passed on their registered totals, which do not rest on those rows (case 218: 19/20 counting only testable rows and the clean plants; case 215: 20/20). No verdict changes. Addenda filed in cases 215 and 218. Rule adopted for every later one-error gate: report stratum and layout testability per plant, and draw ≥ 1 PENDANT and ≥ 1 TIE **on testable layouts** (I-413).

## T3 — Rank vs parametric p sweep (Voynich's question; her C131 lesson)
`sweep244.txt` lists the 14 places in cases 118–229 (plus this cycle) where a parametric p or z sits beside a rank p.
- **Rank p at its floor with a much smaller parametric p: 3** — case 165 C2 (Poisson 0.0038 vs rank 0.05), case 174 direction r (z +2.39 → 0.0084 vs 0.05), case 168 grid (Poisson tails called meaningless there). All three were decided on the rank scale and sent to replication; cases 166 and 175 then closed them **NOT REPLICATED**.
- Other discordance: case 166's fresh-40 z +1.82 (0.034) vs rank 0.073 — decided by rank. Case 167's single Poisson p⁻ 0.012 vs K4 5th of 20 — decided by rank. Case 184 says outright that Poisson z is no test on its heavy-tailed bands. Case 202 prints Poisson p only (0.38–1.00, overdispersed tenths make them anti-conservative; nothing below 0.05 to reverse). Case 221's normal-approximation MW was replaced by the exact p in c239.
- **Labels that rested on a parametric p with the rank p at its floor: 0 → no relabel.** The answer to Voynich: the house gates use rank or count bands; the parametric numbers were never the decider, and from now on both are printed with the rank one named as the decider.

## T4 — I-407: the Part H tie is an identity, not a coincidence (Voynich C133)
- **Algebra (frozen before the run):** in Z27 (g1), with key letters read through Y (M 1) and X fixed, reversing Y (index 25 − i) gives k' = 25 − k_B and Y^R[k'] = Y[k_B]. So **(g1, V, Y^R, M1) ≡ (g1, B, Y, M1)** and (g1, B, Y^R, M1) ≡ (g1, V, Y, M1), cell 26 ↔ 26. Run on the 24 implied letters of K4 and the 12 case-229 nulls over every S3b (X ∈ {AZ, KA}, Y with its reverse listed) — **0 of 1,497,652 triples differ** for both; g0, M0 and form R analogues differ in every triple (not identities).
- **A second identity, found in the gate data:** plant 13's top class holds (S1, g1, R, Y #7343) and (S1, g1, V, Y #7345). With X = Y both reversed, c' − p' = p − c, so **(g1, V, Y^R, M2) ≡ (g1, R, Y, M2)** and vice versa (0 of 62,413 sampled pairs differ; M1 and g0 versions differ everywhere).
- **Why it shows:** 57,602 of alpha.bin's 86,731 alphabets have their reverse in the list, 43,970 of them two rows away (Voynich's "Y + 2"; why the list is ordered that way was not traced). themed144 has none. Not a defect of the search; it inflates the config counts of cases 228 / 229 by structural twins (I-412).
- **Class rule** (identical 24 implied letters = one class; registered for every later Part H gate; post hoc for case 229): gate H **10/10** — plant 17's planted line is rank 2 as a line, rank 1 as a class; plant 13's twin was already harmless.

## T5 — I-408: 24 fresh Part H nulls
`rk243` unchanged on seeds 209783–209806, four scopes, 14 s. **Gate T PASS:** K4 −5.25975 and null 209771 −5.24922 reproduce case 229 exactly.
| set | n | max | mean | SD |
|---|---|---|---|---|
| fresh | 24 | −4.9139 | −5.2169 | 0.172 |
| case 229 | 12 | −4.8841 | −5.1874 | 0.139 |
| pooled | 36 | **−4.8841** | −5.2071 | 0.160 |
- **K4 Hmax −5.2598: rank p 0.622 among 36** (z −0.33, one-sided normal 0.63, concordant) → **`NO-SIGNAL`**, decided by rank.
- **PH36 = −4.88413**, registered as the Part H bar for later readings. The fresh nulls did not raise it. The ten case-229 English-key plants clear it by +0.094 (plant 19, *SKYBLUEIBREAT / UATINGCONTO*) to +1.007. The margin is real but thin for plain-English-poor keys; that is a power question, not settled by more nulls (→ I-411, Voynich's matched-size ladder).

## What this cycle does not cover
I-394 value audits (keys218 / 234 / 236 / 239), I-395, I-396 and the blind S18 check stay queued. K4 was re-run only as gate T5. The NOT TESTABLE census covers kb227's carved-index periodic key; other one-error families need their own census. The sweep is documentary over case files 118–229; older cases (< 118) were not swept.

## Labels
T1 `NO-SIGNAL` confirmed (case 228 sentence corrected). T2 8 rows `NOT TESTABLE` (descriptive relabel, no verdict change). T3 0 relabels. T4 identity confirmed; gate H 10/10 by class (post hoc). T5 `NO-SIGNAL`, PH36 −4.884. Compute < 1 min wall (setsid, timeout 300). Seeds 209783–209806; next free **209807**.
