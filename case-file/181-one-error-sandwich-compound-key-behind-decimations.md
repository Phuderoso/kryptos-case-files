# Case file 181 — One bad letter in the sandwich: case 180 under a single wrong crib letter (cycle 194)

**Status:** negative. **Type:** audit (193 was a new family). IDEAS [I-204](../IDEAS.md) via pointer I-207; part of I-003.
Pre-registered in [`tools/cycle194/PREREG194.md`](../tools/cycle194/PREREG194.md) (commits e688934, 5a8ecb7, c1f7462, e5a653c, ~17:20 PT) with
the solver, plants, checker, decoder, recount, run script, pair list and null seeds, **after** the I-180 probe on the reserved shuffle (seed
9191, I-116), the one-error chance meter on 40 uniform random texts metered apart by tableau type (I-193, I-205), an exactness recount on a
random text and the control rehearsal (15/15, notes disclosed), and **before** any K4 or registered-null run. New solver:
[`cmp194.c`](../tools/cycle194/cmp194.c) (case 179's one-error core `cmp192` with case 180's mixed indices).

**Result in one line:** if K4 were made by **a periodic keyword pass on the plaintext (period m), one of the 165,782 K3-law
decimations/routes, and a periodic keyword pass on the carved text (period n)** (case 180's sandwich: A–Z>KRYPTOS, KRYPTOS>A–Z, A–Z>A–Z,
KRYPTOS>KRYPTOS; Vig/Beau/variant; index assignments S1 and S2) **and one of the 24 crib positions carried a wrong carved or crib letter**,
then **every registered cell keeps full power under one error and has been tested exactly: 3,712 cells (116 ordered pairs per model, incl.
7 with m = n and 49 with lcm > 26, up to 84; × 8 two-tableau settings and × 4 distinct one-tableau settings; × 2 models) gave 3 fits against a
bound of 3.67, and all 3 decode in full to gibberish → `EXACT-EXCL` (one-error scope, chance fits decoded and rejected).** Pairs not run
(509 per model, estimated cell U > 0.05) are **`LOW-POWER`**. 19 shuffles at chance; controls 15/15; recount identical. **No solution.**

## 1. Why this
Case 180 needed all 24 crib letters exact. K1–K3 carry slips (PALIMPCEST, IQLUSION, DESPARATLY, the dropped S of K2), and one wrong letter
on a cyclic crib edge kills the planted config. Cases 177 and 179 did this audit for keys on one side of the route; this file does it for
the sandwich, where the two keys live in different index spaces.

## 2. Method (exact)
A wrong letter at slot t is a deleted edge. As in case 179 (I-202): every slot of the failing component tried, deletions with the same 2-core
of K − t deduplicated; fit iff all cyclic components are consistent, or exactly one component K fails and some distinct core of K − t is
consistent. The strict part of `cmp194` is identical to `cmp193` (probe81, tab4, 625 pairs, both models: all 20,000 cell counts equal).
**One-tableau forms:** in A–Z>A–Z and KRYPTOS>KRYPTOS the cipher is additive and BB = VV, BV = VB exactly (a → −a), so those run VV and VB only.

**Chance bound (I-193, one-error form).** U = Σ_K Σ_d (E_G/E_K)·E_d (capped at 1) bounds P(fit); S1 = Σ_K Σ_d sols(G∖K)·sols(d) has exact
expectation U. **Meter before K4** (40 uniform texts, seeds 19440–19479, 81 routes, all 625 pairs, both models;
[checks](../tools/cycle194/prereg_checks194.txt)), **metered apart (I-205):**

| Band e = round(−log26 U) | two-tableau fits / S1 vs U (text z) | one-tableau fits / S1 vs U (text z) |
|---|---|---|
| 1 | 143,947 / 234,721 vs 234,486 (+0.09) | 2,610 / 91,104 vs 117,243 (−3.39) |
| 2 | 1,812 / 2,253 vs 2,303 (−0.50) | 14 / 676 vs 1,152 (−1.22) |
| 3 | 27 / 27 vs 38.1 (−2.11) | 0 vs 19.0 |
| 4 | 3 / 3 vs 1.30 (+1.01) | 0 vs 0.65 |
| ≥ 5 | 0 vs 0.054 | 0 vs 0.027 |

Two-tableau S1 tracks U; the one-tableau bands run low, the lumpy 26-bundle pattern of case 180 (centred there at 400 texts; not re-run here,
budget). In every band of both types **fits ≤ U**, which is all the labels use.

**Pair selection (text-free, fixed before K4).** A structure-only pass (mode 2) on all_s512 of the reserved shuffle estimated each pair's cell
U; pairs with estimate ≤ 0.05 were registered ([`pairs_fp.txt`](../tools/cycle194/pairs_fp.txt), 116 per model). Estimate ≤ 1 (136 per model,
case 179's rule) would have cost ≈ 470 s on all routes, over the 8-minute budget. In the run every registered cell's exact U was ≤ 0.030.

## 3. Results (K4; [summary](../data/cycle194/summary194.txt), [cells](../data/cycle194/c1_k4_cells.txt))
| Cell | Scope | Full-power cells | U in them | K4 fits | Verdict |
|---|---|---|---|---|---|
| C1a | A–Z>KRYPTOS, KRYPTOS>A–Z, 4 forms, all 165,782 routes, S1 + S2 | S1 928 + S2 928 (116 pairs × 8) | 1.22 + 1.22 | 2 + 1 | `EXACT-EXCL` one-error (3 chance fits decoded, gibberish) |
| C1b | A–Z>A–Z, KRYPTOS>KRYPTOS, VV/VB (= BB/BV), all routes (8 chunks, all run), S1 + S2 | S1 928 + S2 928 (116 × 4 × 2 tableaux) | 0.61 + 0.61 | 0 + 0 | `EXACT-EXCL` one-error |

**Fits, all decoded with [`decode194.py`](../tools/cycle194/decode194.py) under every consistent deletion
([decodes](../data/cycle194/decodes194.txt)):**
- route 136483, S1, A–Z>KRYPTOS, VB, 2 × 16, config U 7.6 × 10⁻⁷ (deletion 2 or 10): `aybfhbwjvetrwgyeeevlj EAITNORTHEAST ljnzuq…`
- route 130922, S1, A–Z>KRYPTOS, VB, 11 × 6, U 4.9 × 10⁻⁸ (deletion 9 or 13): `txspjudqoceuoterdblkg EASTNORTHTAST qtpoiz…`
- route 3870, S2, A–Z>KRYPTOS, BV, 7 × 9, U 2.2 × 10⁻⁹ (deletion 12 or 14): `oesvozhrtectzeglezncp EASTNORTHEASY rqjleb… BERLINCLOCK krrxhaylxq…`

All three are random letters around the cribs (97/97 decrypted). **3 fits vs a bound of 3.67.** Route 3870 is the route of case 180's loudest
fit (S2 A–Z>KRYPTOS BV 14 × 9): the 7 × 9 one-error fit carries the same fragments (`tzeglezncp`, `krrxha?lx?`), i.e. the same chance
coincidence seen through a period-7 key with one slot dropped, not a second event. Closed with I-206.

**Grid** (K4 + 19 shuffles, seeds 19411–19429, tab2 + tab1s on all_s2048, all 625 pairs; [grid](../data/cycle194/grid194.txt)): one-error
fits in bands ≥ 1 pooled K4 3,760, nulls 3,621–3,877 (p⁺ 0.20); ≥ 2: 36 vs 30–64 (p⁺ 0.95); ≥ 3: 0 vs 0–2 (p⁺ 1.00). By type: two-tableau
≥ 1 3,700 vs 3,563–3,791 (p⁺ 0.20); one-tableau ≥ 1 60 vs 36–88 (p⁺ 0.55). K4 sits inside the shuffles; no rank flag.

## 4. Controls and checks
- **Planted controls 15/15** ([`plant194.py`](../tools/cycle194/plant194.py), case 180's plants (seed 19300) with one wrong carved crib letter
  (+7) on a 2-core slot; checker [`checkctl194.py`](../tools/cycle194/checkctl194.py); [result](../data/cycle194/controls194.txt)). P1 A–Z>KRYPTOS
  S1 7 × 11 slot 5; P2 KRYPTOS>A–Z S1 5 × 13 slot 15; P3 A–Z>KRYPTOS S2 8 × 12 slot 23; P4 KRYPTOS>A–Z S1 6 × 19 slot 4; **P5 PALIMPSEST → route
  12345 → ABSCISSA slot 9**; P6 A–Z>A–Z 3 × 25 slot 21; P7 KRYPTOS>KRYPTOS BB 4 × 9 slot 12 (found as VV); P8 m = n 7 × 7 slot 6; P9 S2 BB 6 × 10
  slot 0: all found at their cell, and deleting the planted slot reproduces the planted plaintext everywhere except the corrupted letter.
  P0 (no error) fits strictly. **PD (wrong letter on pendant slot 0) fits strictly, as expected, and is reported as an undetectable error**:
  the strict decryption is wrong at 8 positions, the whole residue class that edge sets. Negatives clean: N1 three passes, N2 random key,
  N3 = P1 with two wrong letters (slots 1 and 3, each in the other's remaining core, +7 / +11), N4 a case-178 compound key.
- **Rehearsal notes (disclosed in PREREG194):** PD's check first expected damage only at the corrupted crib position and was corrected to the
  residue class; P4's wrong letter left its one-cycle component consistent with a different root value (probability ≈ 1 − 1/e for r = 1),
  so the solver reports P4 as a strict fit and the planted deletion reproduces it; reported slots are the first of a deduplicated 2-core
  (P2 2 for 15, P3 4 for 23, P6 10 for 21, P7 11 for 12; I-195). Equivalent cells (period multiples, swapped models in one-tableau stacks)
  are listed, not counted.
- **Recount identical.** Before K4: [`recount194.py`](../tools/cycle194/recount194.py) (literal letter tables, all 25 deletions, no 2-core
  reduction; no shared code) on a uniform random text, 1 route, all 1,250 model-pairs: 7,355 fits identical. Registered (slice191, 7 rows,
  pairs_fp): K4 0, P1 0, P4 0, P7 4, n19411 0, identical (thin: those plants sit on other rows). Added after the run (descriptive, it changes
  no label): K4 on the same 7 rows with all 1,250 model-pairs: **47,759 fits identical** ([recount](../data/cycle194/recount_all194.txt)).

## 5. Cost
Probe, structure pass, meter (23 s), controls (6 s) and the pre-K4 recount ≈ 45 s; registered run 17:20:59–17:27:14 PT (375 s: C1a 208 s,
C1b 140 s, grid 12 s, recount 15 s); post-run recount 7 s. ≈ 7.1 min heavy. Raw outputs condensed to the per-cell table and fit lines (32 MB
scratch, nothing raw published).

## 6. Limits (not covered)
- Pairs with estimated cell U > 0.05 under one error (509 per model; 20 per model between 0.05 and 1 might be decidable on exact U) → I-210.
- Themed × {A–Z, KRYPTOS} pairs behind the routes under one error (case 180's C3) → I-210; two or more wrong letters; dropped/extra letters (I-196).
- Three or more passes; m or n = 1 or > 26; vocabulary tableaux; transpositions other than the K3-law decimations/routes between the passes (I-209).
- A wrong letter on a pendant crib edge is invisible to every crib test (it only damages one residue class of the decryption).

## 7. Verdict
Keyword pass → K3-law decimation/route → keyword pass, on A–Z and/or KRYPTOS in any order, Vig/Beau/variant, either index assignment,
**with at most one wrong crib letter**: **`EXACT-EXCL`** in all 3,712 registered cells (116 period pairs per model, every one full power under
one error; fits at the chance rate, all decoded and rejected); **`LOW-POWER`** for the pairs not run. No K4 solution.
