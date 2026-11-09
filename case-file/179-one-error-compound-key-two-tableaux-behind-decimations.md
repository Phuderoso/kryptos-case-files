# Case file 179 — One bad letter, two tableaux: case 178 under a single wrong crib letter (cycle 192)

**Status:** negative. **Type:** audit (191 was a new family). IDEAS [I-197](../IDEAS.md) via pointer I-200; part of I-003.
Pre-registered in [`tools/cycle192/PREREG192.md`](../tools/cycle192/PREREG192.md) (commits ac2bf1d, c824f09, c44bb43, e1b9ac5, ~16:23–16:24 PT)
with the solver, plants, checker, decoder, recount, run script, null seeds and pair lists, **after** the I-180 probe on the reserved shuffle
(seed 9191, I-116), the one-error chance meter on 40 uniform random texts (I-193) and the control rehearsal (13/13), and **before** any K4 or
registered-null run. New solver: [`cmp192.c`](../tools/cycle192/cmp192.c).

**Result in one line:** if K4 were enciphered by **two arbitrary periodic keys on two different tableaux** (case 178's family: A–Z then
KRYPTOS or the reverse, Vig/Beau/variant, key on the plaintext or carved index, behind any of the 165,782 K3-law decimations/routes) **and one
of the 24 crib positions carried a wrong carved or crib letter**, then **every cell that keeps full power under one error has been tested
exactly: 1,744 cells (116 ordered pairs × 8 settings on the plaintext index, 102 × 8 on the carved index; 54 / 44 pairs with lcm > 26, up to
84 / 72) gave 1 fit against a bound of 2.44, and it decodes in full to gibberish → `EXACT-EXCL` (one-error scope).** The same holds for 572
themed × {A–Z, KRYPTOS} pairs on every 512th route (2 fits vs 1.42, gibberish), directly for 20,592 themed × themed pairs (3 vs 1.73,
gibberish) and for 75,292 vocabulary × {A–Z, KRYPTOS} pairs (0 vs 0.27). Other cells are **`LOW-POWER`**. 19 shuffles at chance; controls
13/13; recount identical (5 texts, 297,153 fits). **No solution.**

## 1. Why this
Case 178 needed all 24 crib letters exact. K1–K3 carry carving and key slips, and a single wrong letter breaks every crib cycle through its
edge, so a real two-tableau key with one slip in the crib window would have been thrown out. Case 177 did this audit for the additive
one-tableau stack; this file does it for the non-additive two-tableau cipher.

## 2. Method (exact)
A wrong letter at slot t is an edge whose bijection is unknown, i.e. a **deleted edge** (b = z_t − s2·σ(s1·x_t + a) with z_t free imposes
nothing). **New point:** in case 177's additive graph a consistent component always admits all 26 shifts, so bridges never constrain and one
deletion per series class suffices. In a bijection graph a component keeps only *some* root values, so a **bridge between two cyclic parts
does constrain**, and deleting different members of one series class can give different systems. `cmp192` therefore tries **every** slot of
the failing component, reduced only by an exact equivalence: pendant trees never constrain, so deletions with the same 2-core of K − t
are the same test (deduplicated by edge mask). A config fits iff all cyclic components are consistent, or exactly one component K fails and
some distinct 2-core of K − t is consistent (26 root values per sub-component, as in `cmp191`).

**Chance count (I-193, one-error form).** For any subgraph H, E[sols(H)] = Π 26^(1−r) (case 178). The fit event is a union over (K, d), so
**U = Σ_K Σ_d (E_G/E_K)·E_d** (capped at 1) bounds the fit probability, and the statistic S1 = Σ_K Σ_d sols(G∖K)·sols(d) has exact expectation U.
**Meter check before K4** (40 uniform random texts, 81 routes, all 600 pairs; [data](../data/cycle192/prereg_checks192.txt)): S1 vs U per band
e = round(−log26 U): 194,326 vs 193,366 (text-level z +0.22), 2,170 vs 2,031 (+0.97), 35 vs 35.2 (−0.03); 0 fits in bands ≥ 4 (U 1.29, 0.05, …);
fits ≤ U in every band. A cell is full power iff its U (summed over routes and tableau pairs) is ≤ 0.05.

**Pair selection (fixed before K4, text-free).** A structure-only pass (mode 2) on all_s512 of the reserved shuffle estimated each pair's
cell U; only pairs with estimated cell U ≤ 1 (20× the threshold) were run: C1 P 138 / C 118, C3 254, C2t 166, C2v 138. Labels use the exact U
computed in the run. Unrun pairs are `LOW-POWER` by that structural estimate.

## 3. Results (K4; [summary](../data/cycle192/summary192.txt), [C1 cells](../data/cycle192/c1_k4_full.txt))
| Cell | Scope | Full-power cells | U in them | K4 fits | Verdict |
|---|---|---|---|---|---|
| C1 | A–Z>KRYPTOS and KRYPTOS>A–Z, all 165,782 routes, P + C, 4 forms | P 928 (116 × 8), C 816 (102 × 8) | 1.18 + 1.26 | 1 + 0 | `EXACT-EXCL` one-error (1 chance fit decoded, gibberish) |
| C3 | 572 themed × {A–Z, KRYPTOS}, all_s512 (324 routes) | P 464 (116 × 4), C 408 (102 × 4) | 0.66 + 0.76 | 0 + 2 | `EXACT-EXCL` one-error on 1/512 (2 fits decoded, gibberish) |
| C2t | direct, 20,592 themed × themed | 552 (138 × 4) | 1.73 | 3 | `EXACT-EXCL` one-error (3 fits decoded, gibberish) |
| C2v | direct, 75,292 vocabulary × {A–Z, KRYPTOS} | 464 (116 × 4) | 0.27 | 0 | `EXACT-EXCL` one-error |

**Fits in full-power cells, all decoded with [`decode192.py`](../tools/cycle192/decode192.py), every consistent deletion printed
([decodes](../data/cycle192/decodes192.txt)):** C1 route 33989 P AZ>KRYPTOS VB 2 × 15 (deletion 2 or 18, `nnyyjzhqukjlmqgdcwzrk…`); C3
route 0 C KRYPTOS>WONDERFULTHINGS BB 15 × 3 (deletion 0 or 16), route 187 C KRYPTOS>THEPOINT BV 15 × 3 (deletion 8); C2t MESSAGE>CARTER BV
11 × 7 (deletion 1), EASTNORTHEAST>INTERPRETATU BV 16 × 2 (deletion 12 or 15), WEBSTER>MAGNETIC VV 19 × 2 (deletion 4 or 13, 75/97 letters).
All six read as random letters around the cribs. **6 fits vs a bound of 5.86** over the four cell families: what chance should throw up.
Every full-power fit was printed (fit count = printed lines).

**Low-power cells (run).** C1 304 cells: 36 fits vs U 59.9; C3 20 vs 28.2; C2t 36 vs 48.7; C2v 4 vs 6.0 (U is an upper bound, union over
deletions). K4's C1 bands: e = 3: 20 vs 25.7; e = 4: 16 vs 34.9; e = 5: 1 vs 1.75; e ≥ 6: 0 vs 0.07.

**Grid** (K4 + 19 shuffles, seeds 19211–19229, tab2 on all_s512, all 600 pairs; [grid](../data/cycle192/grid192.txt)): fits in bands ≥ 1:
K4 11,150, nulls 10,977–11,393 (p⁺ 0.65); ≥ 2: 119 vs 103–151 (p⁺ 0.80); ≥ 3: 2 vs 1–11 (p⁺ 0.90); ≥ 4: 0 vs 0–1. K4 sits inside the shuffles.

## 4. Controls and checks
- **Planted controls 13/13** ([`plant192.py`](../tools/cycle192/plant192.py), seed 19200, passes applied literally; checker
  [`checkctl192.py`](../tools/cycle192/checkctl192.py); [result](../data/cycle192/runlog192.txt)). Case 178's eight plants, each with one wrong
  carved crib letter (P1 slot 2, P2 15, P3 23, P4 4, P5 9, P6 19, P7 12, P8 6), all found at their cell and decoded back to the planted
  plaintext with the planted slot as a reproducing deletion; P0 (no error) fits strictly. Negatives clean: N1 three passes, N2 random key,
  N3 = P1 with wrong slots 2 and 18, N4 = P4 with 4 and 5.
- **I-195 handling.** The solver reports the first slot of a deduplicated 2-core (P2 reported 2 for planted 15, P3 10 for 23, P5 1 for 9, P6 4
  for 19): those slots give the same 2-core, and the decoder shows only the planted slot reproduces the plaintext at every position. Equivalent
  cells (P5/P6 on the identity route in both models, P7 in the one-tableau form equivalents and swapped periods, P8 at 2 × 18 through the cribs'
  36-letter offset) listed, not counted.
- **Rehearsal fixes (before registration, disclosed in PREREG192):** N3's second slot first sat in a pendant tree once slot 2 was deleted
  (it fitted as a one-error text), and P4's requested slot 0 was outside the 2-core (an invisible error). Wrong slots are now drawn from the
  2-core, and two-error negatives use slots each in the other's remaining core.
- **Recount identical:** [`recount192.py`](../tools/cycle192/recount192.py) (literal letter tables, all 25 deletions per config tried with no
  2-core reduction or deduplication; shares no code with `cmp192`) on 7 routes × 4 tableau orders × 2 models × 4 forms × 600 pairs: fit sets
  identical for K4 (59,311), P1 (59,526), P2 (59,492), P7 (59,530), n19211 (59,294).

## 5. Cost and add-on
Probes, meter and controls ≈ 30 s; registered run 16:24:20–16:29:30 PT (310 s: C1 160 s, grid 16 s, C3 66 s, recount 43 s, C2t 6 s, C2v 18 s);
≈ 5.7 min heavy. Outputs reduced on the fly (`agg192.awk`); 31 MB total, nothing raw kept beyond the tables. **I-199 timing probe (I-200
add-on, reserved shuffle only):** `cmp191` with mixed indices ([`sw192probe.c`](../tools/cycle192/sw192probe.c); a on the plaintext index,
b on the carved index, and the reverse; tab4 incl. one-tableau stacks; 600 pairs) takes 0.10 s on 81 routes → ≈ 205 s on all routes
([probe bands](../data/cycle192/swprobe192.txt)). Feasible for cycle 193; its meter must be checked on uniform texts first.

## 6. Limits (not covered)
- Two or more wrong letters; dropped or extra letters (I-196).
- The sandwich (I-199), themed/vocabulary pairs behind the routes beyond 1/512 / direct (I-198), vocabulary × vocabulary, three passes,
  m or n > 26.
- Low-power cells: 116 / 102 pairs keep full power under one error, against 166 / 132 under the strict test; the rest cannot be decided by
  23 good cribs.

## 7. Verdict
Two arbitrary periodic keys on A–Z and KRYPTOS (either order), Vig/Beau/variant, key on the plaintext or carved index, behind any of the
165,782 K3-law decimations/routes, **with at most one wrong crib letter**: **`EXACT-EXCL`** in every cell that keeps full power (fits at the
chance rate, all decoded and rejected); **`LOW-POWER`** elsewhere. No K4 solution.
