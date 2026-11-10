# Case file 180 — The sandwich: a keyword pass, K3's transposition, a second keyword pass (cycle 193)

**Status:** negative. **Type:** new family (192 was an audit). IDEAS [I-199](../IDEAS.md) via pointer I-201.
Pre-registered in [`tools/cycle193/PREREG193.md`](../tools/cycle193/PREREG193.md) (commits d97bfad, efa3629, 52ff355, 965b989, ~16:53 PT) with the
solver, plants, checker, decoder, recount, aggregator, run script, null seeds and control texts, **after** the solver had been timed under rule
I-180 on the reserved shuffle (seed 9191, I-116), the chance meter checked on 40 + 400 uniform random texts (I-193) and the planted controls
rehearsed (13/13, one plant fix disclosed), and **before** any K4 or registered-null run. New solver: [`cmp193.c`](../tools/cycle193/cmp193.c).
Checked new against cases 119, 131 and 176–179.

**Result in one line:** if K4 were made by **a periodic keyword pass on the plaintext (period m), then one of the 165,782 K3-law
decimations/routes, then a second periodic keyword pass on the carved text (period n)**, each pass on A–Z or on KRYPTOS (both orders and both
one-tableau stacks), Vig/Beau/variant, with the first key at the plaintext index and the second at the carved index (S1) or the reverse (S2), then
**every full-power cell has been tested exactly: 5,024 cells (157 ordered pairs (m, n) × 16 tableau/form settings × 2 models; 8 pairs with m = n,
82 with lcm > 26, up to 105) returned 5 fits against 9.61 expected by chance, and all 5 decode to gibberish → `EXACT-EXCL` (chance fits decoded
and rejected).** The same holds for 572 themed × {A–Z, KRYPTOS} tableau pairs on every 512th route (3 fits vs 2.32, gibberish). Other cells are
**`LOW-POWER`**. 19 shuffles at chance; controls 13/13; recount identical (5 texts, 236,679 fits). **No solution.**

## 1. Why this
K3 is a transposition; K1 and K2 are keyword substitutions on the KRYPTOS tableau. Cases 176–179 tested two arbitrary keys **on the same side**
of the route (both before or both after the transposition). The simplest layered build in Sanborn's own vocabulary puts the transposition
**between** two keyword passes. With x = T1idx(p), z = T2idx(c), σ(y) = T2idx(T1[y]) and plaintext i carved at S[i]:

  **S1:** z = s2 · σ(s1 · x + a[i mod m]) + b[S[i] mod n]   **S2:** z = s2 · σ(s1 · x + a[S[i] mod m]) + b[i mod n]

(s1, s2 = ±1; variant is absorbed into the key sign). The two key residues now live in different index spaces, so the crib graph differs from
cases 176–179, and **m = n is not a single period** (so those pairs are included). One-tableau stacks (A–Z>A–Z, KRYPTOS>KRYPTOS) are additive but,
with mixed indices, not covered by case 176. Cases 119 and 131 tried only **named** keyword pairs with a transposition between the layers.
**Non-equivalence shown:** case 178's solver `cmp191` does not find the sandwich plants P1, P5, P8 at their rows, but finds a case-178 plant
(N4), which `cmp193` in turn rejects.

## 2. Method (exact)
As in case 178: crib t is a bijection between a[u] and b[v] (S1: u = i mod m, v = S[i] mod n). On every cyclic component of the residue graph
`cmp193` tries all 26 root values, propagates along a BFS tree and checks each non-tree edge; tree components are always satisfiable. A config
fits iff every cyclic component keeps a root value. Exactness re-checked against the independent [`recount193.py`](../tools/cycle193/recount193.py)
on a uniform random text before K4 (36,549 fits identical) and on the registered recount (§4).

**Chance count (I-193).** E_config = Π_cyclic 26^(1−r_c) is the exact expected number of solutions for uniform carved letters. **Meter, 40
uniform texts (seeds 19340–19379) on 81 probe routes:** two-tableau pairs match in every band (z −0.20, +0.50, +0.43, +0.06, +0.58 for e = 0–4).
**One-tableau stacks are lumpy:** they are additive, so a cyclic component passes for all 26 root values or for none (bundles of 26), and fits are
shared across forms and period multiples. Pooled over tab4, band e = 3 showed 105 solutions vs 209 (z −10), all 105 from two-tableau pairs and 0
vs 104 from one-tableau stacks. On 400 further texts (seeds 19380–19779) the one-tableau bands centre on E (z −2.11, +0.28, −0.73, −1.44, +0.66;
e = 3: 624 vs 1,044, e = 4: 104 vs 35). E stays the expectation; for one-tableau cells the fit probability is ≤ E/26, so E ≤ 0.05 is conservative
there. New rule I-205: meter additive and non-additive cells separately. Pairs: 2 ≤ m, n ≤ 26 incl. m = n (625). Forms VV, VB, BV, BB.

## 3. Results (K4)
| Cell | Scope | Full-power cells | E in them | K4 fits | Verdict |
|---|---|---|---|---|---|
| C1 | tab4 (A–Z>KRYPTOS, KRYPTOS>A–Z, A–Z>A–Z, KRYPTOS>KRYPTOS), all 165,782 routes, S1 + S2, 4 forms | S1 2,512 + S2 2,512 (157 pairs × 16 each) | 4.81 + 4.81 | 2 + 3 | `EXACT-EXCL` (5 chance fits decoded, gibberish) |
| C3 | 572 themed × {A–Z, KRYPTOS} pairs, all_s512 (324 routes) | S1 624 + S2 624 (156 pairs × 4) | 1.16 + 1.16 | 1 + 2 | `EXACT-EXCL` on 1/512 (3 fits decoded, gibberish) |

No direct cells: on the identity route S1 = S2 = case 178's model P (already `EXACT-EXCL` there); the identity is not in all.bin.

**Fits in full-power cells, all decoded with [`decode193.py`](../tools/cycle193/decode193.py) ([decodes](../data/cycle193/decodes193.txt)):**
C1 route 11343 S1 AZ>KA BV 23 × 2 (73/97 letters, `tppdmfnpdhi…`), route 68647 S1 KA>AZ BV 19 × 4 (75/97), route 44016 S2 AZ>KA BV 2 × 17
(97/97, `ckppnmoggddqiukd…`, the same decryption as case 178's route-44016 fit: on that route the two parity classes coincide), route 132931 S2
AZ>KA BV 14 × 5 (97/97, `tqfwhyoahyil…`), route 159516 S2 AZ>KA VV 10 × 9 (4 solutions, 97/97, `xyeyjvqukror…`); C3 row 316 S1 A–Z>TIMEZONE/Z
VB 17 × 2, row 236 S2 A–Z>CENTRALINTELLIGENCE/Z BB 4 × 22, row 241 S2 GRANITE/K>KRYPTOS VV 4 × 15. All are random letters around the cribs; each
has E_config 8.4 × 10⁻⁸ in a cell with E 0.005–0.016. Every full-power cell with a fit had its fit printed (H count = printed M lines).

**Strongest fit of the run (low-power cell).** Route 3870 S2 AZ>KA BV 14 × 9, E_config 1.2 × 10⁻¹⁰ (band e = 7, where the whole of C1 expected
0.016 solutions). Decoded: 56/97 letters, `…tzeglezncp EASTNORTHEAST ?qe??w… BERLINCLOCK krrxhatlxl…`, gibberish → rejected. Post hoc
(descriptive, no decision weight): 1,000 fresh shuffles (seeds 19400–20399) on route 3870 gave 0 fits with E_config ≤ 10⁻⁹. A 1-in-60 event over
the run, closed by its decryption (I-206). The other low-power fits with E_config ≤ 10⁻⁶ (routes 116361, 161443, 93408, and route 74155's
one-tableau KRYPTOS>KRYPTOS bundle of 26 in four equivalent cells) are gibberish too.

**Low-power cells.** C1 two-tableau 7,488 cells: solutions 734,340,560 vs E 734,694,650 (−0.05 %); one-tableau 7,488 cells: 717,641,470 vs
734,694,650 (−2.3 %, the lumpy meter of §2); C3 +0.28 %. K4's C1 bands: e = 4: 384 vs 363; e = 5: 115 vs 13.6 (104 of them one route's
one-tableau 26-bundle, see above; two-tableau 11); e = 6: 0 vs 0.44; e = 7: 1 vs 0.016; e ≥ 8: 0.

**Grid** (K4 + 19 shuffles, seeds 19311–19329, tab4 on all_s512; [grid](../data/cycle193/grid193.txt)): solutions e = 1 K4 15,440, nulls
12,809–20,042 (p⁺ 0.45); e = 2 488 vs 235–815 (p⁺ 0.40); fits e ≥ 3 6 vs 4–17 (p⁺ 0.90); e ≥ 4 2 vs 0–2 (p⁺ 0.10). K4 is inside the shuffles; no
rank flag.

**Power note (descriptive, for the Voynich desk's 80th-percentile question).** In the 157 full-power (m, n) pairs per model, a planted config's
own E_config is at worst 26⁻⁴ and at the 80th percentile (weak end) 26⁻⁶ (≈ 3 × 10⁻⁹); shares by band e = 5–9 ≈ 0.10 each. Every plant in a
full-power cell is found (exact test, power 1); what limits the search is cell-level E summed over 165,782 routes, not weak plants.

## 4. Controls and checks
- **Planted controls 13/13** ([`plant193.py`](../tools/cycle193/plant193.py), seed 19300, passes applied literally letter by letter; checker
  [`checkctl193.py`](../tools/cycle193/checkctl193.py)). Positives found at their row, tableau order, reduced form, model and (m, n), plaintext
  reproduced: P1 A–Z>KRYPTOS S1 Vig 7 / Vig 11; P2 KRYPTOS>A–Z S1 Beau 5 / Vig 13; P3 A–Z>KRYPTOS S2 variant 8 / Beau 12; P4 KRYPTOS>A–Z S1 Vig 6
  / Beau 19; **P5 PALIMPSEST (A–Z, Vig) → route 12345 → ABSCISSA (KRYPTOS, Vig): both keywords and all 97 letters recovered**; P6 A–Z>A–Z S1
  variant 3 / Vig 25; P7 KRYPTOS>KRYPTOS S1 Beau 4 / Beau 9; P8 A–Z>KRYPTOS S1 Vig 7 / Beau 7 (m = n); P9 KRYPTOS>A–Z S2 Beau 6 / Beau 10.
  Negatives clean: N1 three passes, N2 random key, N3 = P1 with one wrong carved crib letter, N4 a case-178 compound key. Equivalent cells (period
  multiples, one-tableau form equivalents BB = VV) were listed, not counted (I-195).
- **Rehearsal fix (disclosed):** N3's wrong letter was first placed on slot 2, a pendant edge of P1's graph (outside the 2-core): no crib test
  can see an error there, so P1's cell still fitted. It was moved to slot 3, the first 2-core slot ≥ 2, before the push.
- **Non-equivalence:** `cmp191` (case 178) finds N4 at its row and none of P1, P5, P8.
- **Recount identical:** `recount193.py` (literal letter-level tables, vectorised DFS; no shared code) on 7 routes × tab4 × 2 models × 4 forms ×
  625 pairs: K4 47,163, P1 47,535, P2 47,363, P6 47,241, n19311 47,377 fits, sets and solution counts identical.

## 5. Cost
Probe 0.12 s on 81 routes; meters 50 s; controls 3 × 3 s; registered run 16:54:25–16:57:08 PT (163 s: C1 126 s, grid 6 s, C3 23 s, recount 8 s);
post-hoc route-3870 check 23 s. ≈ 4.1 min heavy. C3 was condensed on the fly (H summed over tableau pairs per file, `agg193`); published:
[per-cell C1 table](../data/cycle193/c1_k4_cells.txt), [C1 fits with E_config ≤ 10⁻⁴](../data/cycle193/c1_k4_fits_e4.txt),
[summary](../data/cycle193/summary193.txt), [run log](../data/cycle193/runlog193.txt).

## 6. Limits (not covered)
- **One wrong crib letter** (strict test only; the audit is I-204). A wrong letter on a pendant edge is invisible to any crib test.
- Three or more passes; m or n = 1 or > 26; dropped or extra letters (I-196).
- Themed pairs behind the routes beyond 1/512; vocabulary-keyed tableaux behind the routes (I-198).
- Transpositions other than the K3-law decimations/routes between the passes.
- Low-power cells (E > 0.05: too few independent crib cycles) cannot be decided by 24 cribs.

## 7. Verdict
Keyword pass → K3-law decimation/route → keyword pass, on A–Z and/or KRYPTOS in any order, Vig/Beau/variant, either index assignment, any periods
2–26 including equal ones: **`EXACT-EXCL`** in every full-power cell (fits at or below the chance rate, all decoded and rejected); **`LOW-POWER`**
elsewhere. No K4 solution.
