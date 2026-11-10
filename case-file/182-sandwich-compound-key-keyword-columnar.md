# Case file 182 — The sandwich around a keyed columnar: a keyword pass, a keyword columnar, a second keyword pass (cycle 195)

**Status:** negative. **Type:** new family (194 was an audit). IDEAS [I-209](../IDEAS.md) via pointer I-208.
Pre-registered in [`tools/cycle195/PREREG195.md`](../tools/cycle195/PREREG195.md) (commits b9cf2a5, 8954c82, 0ed7949, 00e994f, 6b06ea1, ~17:55 PT)
with the bank generators, plants, checker, decoder, recount, aggregators, run script, null seeds and meter output, **after** the I-180 probe on
the reserved shuffle (seed 9191, I-116), the chance meter on 40 + 400 uniform random texts split by tableau type (I-193, I-205), a pre-K4
recount and the control rehearsal (14/14, one fix disclosed), and **before** any K4 or registered-null run. Solver: case 180's
[`cmp193.c`](../tools/cycle193/cmp193.c), **unchanged**; only the permutation bank is new.

**Result in one line:** if K4 were made by **a periodic keyword pass on the plaintext (period m), then a keyed columnar transposition (case
50's 1,837 keyword orders, either direction, or a double columnar of two themed keywords), then a second periodic keyword pass on the carved
text (period n)**, on A–Z and/or KRYPTOS in any order, Vig/Beau/variant, either index assignment (S1/S2), 2 ≤ m, n ≤ 26 incl. m = n, then
**every full-power cell has been tested exactly: single columnar 5,792 cells, 4 fits vs E 7.55; themed double columnar 5,760 cells, 10 fits vs
E 18.2; all 14 fits decode to gibberish → `EXACT-EXCL` (chance fits decoded and rejected).** 572 themed × {A–Z, KRYPTOS} tableau pairs on the
184 themed single columnars: 1,264 full-power cells, 2 fits vs 1.95, gibberish. Other cells **`LOW-POWER`**. 19 shuffles at chance; controls
14/14; recount identical (5 texts, 202,722 fits). **No solution.**

## 1. Why this, and why it is new
Cases 180–181 put K3's own law (decimations/routes) between two arbitrary keyword passes. A **keyed columnar** is the other transposition a
1990 hand cipher would use, and K3 is itself a double transposition. Prior-coverage grep (48 case files mention columnar; README; IDEAS):
- Case 50 (cycle 52): the same 1,837 orders, single and double, but **one** periodic/progressive key on **one** side.
- Case 119 (cycle 131): model M is this sandwich's S1, but only with **named** themed keyword pairs, behind the 165,065 bank, whose keyword
  columnars stop at width 8 (case 111 audit); case 120 hashed vocabulary pairs only for the transposition-last model Q.
- Cases 176–181: two **arbitrary** periodic keys, only behind the 165,782 K3-law routes. **None of the 3,674 single columnar rows is in that
  bank** (6 of the 16,928 double rows are, flagged in the index).
So two arbitrary periodic keys around a keyword columnar had not been tested.

## 2. Method (exact)
S1: z = s2·σ(s1·x + a[i mod m]) + b[C(i) mod n]; S2: a at the carved index C(i), b at the plaintext index (x = T1idx(p), z = T2idx(c),
σ(y) = T2idx(T1[y]); variant absorbed into the key sign). Exact bijection-graph test on every cyclic component of the residue graph (all 26
root values), E_config = Π 26^(1−r_c) per config (I-193); cell = (model, tableau pair, form, m, n) summed over a bank; full power iff cell
E ≤ 0.05.

**Banks** ([`gen195.py`](../tools/cycle195/gen195.py), [`sub195.py`](../tools/cycle195/sub195.py), from
[`data/cycle52/orders.txt`](../data/cycle52/orders.txt); hashes in [`sha195.txt`](../tools/cycle195/sha195.txt)). Write the plaintext row by
row under the keyword (width 4–14, short last row), read the columns in alphabetical keyword order (ties left to right), as `tools/dcol.c`.
- **col1:** 1,837 orders × {encryption map, inverse} = **3,674** rows.
- **col2:** ordered pairs of the 92 themed orders incl. the same word twice (K3-style double), × {map, inverse}, minus rows already in col1 =
  **16,928** rows.
- **col1_th:** the 184 themed rows of col1 (for the themed tableau pairs). `plant195.py` re-derives the columnar literally from the keyword and
  asserts it equals the bank rows (independent check of the generator).

**Meter (I-193 / I-205, 40 uniform texts, seeds 19540–19579, on 460 col1 and 529 col2 rows; [output](../tools/cycle195/meter195_out.txt)).**
Two-tableau at chance: col1 bands e = 0–5 z +1.74, +0.26, +1.25, −2.31, −0.63, +1.01; col2 +1.19, −0.65, −0.16, −0.90, +0.84 (band 5: 0 vs
0.87). One-tableau stacks lumpy again (additive, 26-bundles shared across forms and period multiples): col1 z −3.87, −5.26, −2.60 in bands 1–3
over 40 texts; over 400 further texts (19580–19979) z +0.93, −2.90, −1.89, −0.68 in bands 0–3 and one band-5 event (text 19850: one 26-bundle
in 4 equivalent cells). As in case 180, E stays the expectation; one-tableau fit probability ≤ E/26. Huge |z| printed in empty bands is a
float artefact of the meter script (SD ≈ 10⁻¹⁷); read as n/a.

## 3. Results (K4; [summary](../data/cycle195/summary195.txt), [decodes](../data/cycle195/decodes195.txt))
| Cell | Scope | Full-power cells | E in them | K4 fits | Verdict |
|---|---|---|---|---|---|
| C1 | tab4 (A–Z>KRYPTOS, KRYPTOS>A–Z, A–Z>A–Z, KRYPTOS>KRYPTOS), all 3,674 single keyed columnars, S1 + S2, 4 forms | 5,792 (181 (m, n) pairs per model × 32; 9 with m = n, 95 with lcm > 26, up to 140) | 7.55 (two-tableau 3.78; one-tableau 3.78, fits expected ≤ 0.15) | 4 (all two-tableau) | `EXACT-EXCL` (4 chance fits decoded, gibberish) |
| C2 | tab4, all 16,928 themed double keyed columnars | 5,760 (180 pairs per model × 32) | 18.2 (two-tableau 9.10) | 10 (all two-tableau) | `EXACT-EXCL` (10 chance fits decoded, gibberish) |
| C3 | 572 themed × {A–Z, KRYPTOS} pairs, 184 themed single columnars | 1,264 (158 pairs per model × 4 forms) | 1.95 | 2 | `EXACT-EXCL` on the themed rows (2 fits decoded, gibberish) |

**Full-power fits, all decoded with [`decode195.py`](../tools/cycle195/decode195.py):**
- **C1:** HAVE/inv S2 AZ>KA BB 17 × 4 (97/97, `wszdjctewwyq…`); SHOOK/enc S1 AZ>KA BB 4 × 16 (97/97, `sxfvmhryssuv…`); MIGHTY/enc S1 KA>AZ VV
  20 × 7 (65/97, `?fbjnagehpch…`); DISAPPOINTMENT/inv S1 AZ>KA VV 2 × 19 (97/97, `nfgabickbnwz…`).
- **C2:** LAYERTWO+UNDERGROUND/enc S2 AZ>KA VB 7 × 20 (65/97); DESPARATLY+SHADOW/enc S1 AZ>KA BV 17 × 3; CHAMBER+MESSAGE/enc S1 KA>AZ BV 16 × 3
  (E_config 8.4 × 10⁻⁸, the run's strongest, `igmhxpxkwjol…`); ILLUSION+VIGENERE/inv S2 AZ>KA VB 12 × 8; DIGETAL+POSITION/inv S2 AZ>KA VV
  14 × 6; COLUMNAR+BERLINCLOCK/inv S2 KA>AZ BV 5 × 22 (69/97); SECRET+VIGENERE/enc S1 KA>AZ VB 15 × 5; DARKNESS+WALL/inv S2 KA>AZ VB 13 × 7;
  BERLINWALL+CARTER/enc S2 AZ>KA BV 3 × 18 (91/97); ENIGMA+TOMB/inv S2 AZ>KA BV 10 × 10 (m = n). Every one is random letters around the cribs.
- **C3:** STONE/enc S1 LAYERTWO/K>A–Z BV 3 × 17 and the same row with XLAYERTWO/K>A–Z (the two alphabets differ by one letter's place; one
  coincidence seen twice), `zjjvfxtwyeeo…`, gibberish.

**Low-power cells.** C1 two-tableau 7,104 cells: solutions 16,161,938 vs E 16,205,353 (−0.27 %); one-tableau 15,723,848 (−3.0 %, the lumpy
meter). C2 two-tableau −0.10 %, one-tableau −1.6 %. C3 +0.04 %. Bands: C1 e = 4: 5 vs 7.9, e = 5: 0 vs 0.31, e ≥ 6: 0; C2 e = 4: 18 vs 37.5,
e = 5: 1 vs 1.39 (CHAMBER+MESSAGE, a full-power cell, above), e ≥ 6: 0; C3 e = 4: 39 vs 56.8, e ≥ 5: 0 vs 2.29. No low-power fit with
E_config ≤ 10⁻⁶.

**Grid** (K4 + 19 shuffles, seeds 19511–19529, tab4 on **all** of col1; [grid](../data/cycle195/grid195.txt)): full-power fits K4 4, nulls 0–6
(p⁺ 0.30); band-1 solutions p⁺ 0.25; band 2 p⁺ 0.35; printed fits e ≥ 3: 127 vs 86–131 (p⁺ 0.10); e ≥ 4: 5 vs 0–9 (p⁺ 0.25); low-power
solutions two-tableau p⁺ 0.50, one-tableau p⁺ 0.40. K4 is inside the shuffles; no rank flag.

## 4. Controls and checks
- **Planted controls 14/14** ([`plant195.py`](../tools/cycle195/plant195.py), seed 19500, passes applied literally; checker
  [`checkctl195.py`](../tools/cycle195/checkctl195.py); [output](../tools/cycle195/controls195.txt)). Positives found at their row, tableau
  order, reduced form, model and (m, n), plaintext reproduced: P1 KRYPTOS columnar S1 AZ>KA Vig 7 / Vig 11; P2 PALIMPSEST columnar KA>AZ Beau
  5 / Vig 13; P3 LODESTONE inverse S2 variant 8 / Beau 12; P4 ALEXANDERPLATZ (width 14) KA>AZ Vig 6 / Beau 19; **P5 PALIMPSEST (A–Z, Vig) →
  KRYPTOS keyed columnar → ABSCISSA (KRYPTOS, Vig): found at its row (plus the equivalent 20 × 8 multiple), and the only fit with E_config
  ≤ 10⁻⁶ of any cell in all 3,674 rows of col1; both keywords and all 97 letters recovered**; P6 double KRYPTOS+PALIMPSEST A–Z>A–Z, found at its row in all 16,928 rows of col2; P7
  KRYPTOS>KRYPTOS BERLIN inverse; P8 m = n = 7; P9 S2 Beau/Beau. Negatives clean: N1 three passes, N2 random key, N3 = P1 with one wrong carved
  crib letter (slot 3, on the 2-core: the cell no longer fits), N4 a case-178 compound key, **N5 a K3-route sandwich (all.bin 12345): no fit at
  any of the six columnar rows** (found at its own route row). Equivalent cells (period multiples, one-tableau BB = VV) listed, not counted.
- **Rehearsal fix (disclosed):** the first control run printed fits only at E_config ≤ 10⁻⁴; that hid P4, a width-14 plant whose own
  E_config is 0.0015 (the solver had found it). The control print threshold was set to the registered run's 0.002; negatives are still judged
  at ≤ 10⁻⁴. Lesson → I-214.
- **Recount identical:** [`recount195.py`](../tools/cycle195/recount195.py) (= recount193, literal letter tables, vectorised DFS, no shared
  code) on the 7 control rows × tab4 × 2 models × 4 forms × 625 pairs: before K4 on a uniform text 40,550 fits; registered K4 40,657, P1
  40,729, P5 40,300, P6 40,454, n19511 40,582: sets and solution counts identical.

## 5. Cost
Probe 16 s; meter 175 s; controls 2 × 18 s; pre-recount 7 s; registered run 17:55:43–17:57:23 PT (100 s: C1 3 s, C2 14 s, grid 59 s, C3 16 s,
recount 8 s). ≈ 5.6 min heavy. Outputs condensed: [C1 full-power cells](../data/cycle195/c1_k4_fullpower_cells.txt),
[C2](../data/cycle195/c2_k4_fullpower_cells.txt), [C3](../data/cycle195/c3_k4_fullpower_cells.txt), fits with E_config ≤ 10⁻⁴
([C1](../data/cycle195/c1_k4_fits_e4.txt), [C2](../data/cycle195/c2_k4_fits_e4.txt), [C3](../data/cycle195/c3_k4_fits_e4.txt)),
[run log](../data/cycle195/runlog195.txt).

## 6. Limits (not covered)
- **One wrong crib letter** (strict test only; the audit is I-212).
- Double columnar beyond themed × themed (3.4 M ordered pairs of case 50); themed tableau pairs behind the 3,490 non-themed single columnars;
  disrupted, Myszkowski or incomplete-row variants between the passes (I-213).
- m or n = 1 or > 26; three or more passes; dropped or extra letters (I-196).
- Low-power cells (E > 0.05) cannot be decided by 24 cribs.

## 7. Verdict
Keyword pass → keyed columnar (1,837 keyword orders either direction, or a themed double columnar) → keyword pass, on A–Z and/or KRYPTOS in any
order, Vig/Beau/variant, either index assignment, periods 2–26 including equal ones: **`EXACT-EXCL`** in every full-power cell (fits at or
below the chance rate, all decoded and rejected); **`LOW-POWER`** elsewhere. No K4 solution.
