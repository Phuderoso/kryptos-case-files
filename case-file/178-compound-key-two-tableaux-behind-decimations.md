# Case file 178 — Two keywords, two tableaux: the compound key on A–Z and KRYPTOS behind K3's decimation law (cycle 191)

**Status:** negative. **Type:** new family (190 was an audit). IDEAS [I-190](../IDEAS.md) via pointer I-194.
Pre-registered in [`tools/cycle191/PREREG191.md`](../tools/cycle191/PREREG191.md) (commits 3c0c414, 33f5cf8, c796208, ~15:53 PT) with the solver,
plants, checker, decoder, recount, run script, null seeds and control texts, **after** the solver had been timed under rule I-180 on the reserved
shuffle (seed 9191, I-116), the chance meter checked on 40 uniform random texts (I-193) and the planted controls rehearsed (11/11), and **before**
any K4 or registered-null run. New solver: [`cmp191.c`](../tools/cycle191/cmp191.c). Checked new against cases 119, 176 and 177.

**Result in one line:** if K4 were enciphered by **two arbitrary periodic keys of lengths m and n on two different tableaux** (first pass on A–Z,
second on KRYPTOS, or the reverse; any mix of Vigenère, Beaufort and variant steps; key on the plaintext index or on the carved index), then **on all
165,782 K3-law decimations/routes every full-power cell has been tested exactly: 2,384 cells (166 ordered pairs × 8 tableau-order/form settings on
the plaintext index, 132 × 8 on the carved index; 94 / 70 pairs with lcm > 26, up to 105 / 90; 8 × 10, 10 × 8, 7 × 11, 11 × 7 among them)
returned 5 fits against 4.94 expected by chance, and all 5 decode in full to gibberish → `EXACT-EXCL` (chance fits decoded and rejected).**
The same holds for 572 themed × {A–Z, KRYPTOS} tableau pairs on every 512th route (2 fits vs 2.41 expected, gibberish), directly for 20,592
ordered themed × themed pairs (1 fit vs 4.89, gibberish) and for 75,292 vocabulary-keyed × {A–Z, KRYPTOS} pairs (0 fits vs 0.73). The other cells
are **`LOW-POWER`**: the cribs cannot pin them, and their solution totals equal the chance count (C1 −0.12 %). 19 shuffles at chance; controls
11/11 (including two one-tableau plants); recount identical (5 texts, 238,591 fits). **No solution.**

## 1. Why this
Case 176 stacked two keyword passes on **one** tableau; every such stack collapses to one additive key K[i] = a[i mod m] + b[i mod n]. But the
sculpture carries two alphabets: the plain A–Z and the KRYPTOS-keyed one of the tableau. K1 and K2 were enciphered on the KRYPTOS tableau; a
"layered, simple" K4 could run one keyword on one alphabet and a second keyword on the other, handing the letter over as a letter. With
x = T1idx(p), z = T2idx(c) and σ(y) = T2idx(T1[y]) (the map between the two alphabets), each letter obeys

  **z = s2 · σ(s1 · x + a[i mod m]) + b[i mod n]**  (s1, s2 = ±1: Vigenère/variant +, Beaufort −).

σ is not affine, so this is not a periodic key of period lcm(m, n) in any index space and none of the periodic, Quagmire or case-176 exclusions
covers it. Case 119 tried only **named** keyword pairs on mixed tableaux; here both keys are arbitrary.

## 2. Method (exact)
For a fixed route, model, tableau order and form, crib t ties a[u] and b[v] (u = pos mod m, v = pos mod n) by a **bijection**
b = F_t(a) = z_t − s2·σ(s1·x_t + a). The cribs therefore form a bipartite residue graph whose edges are bijections. On every connected component
with a cycle, `cmp191` tries all 26 values of one root, propagates along a BFS spanning tree and checks every non-tree edge as soon as both ends
are set. Components without a cycle are always satisfiable. A configuration fits iff every cyclic component keeps at least one root value. No
approximation is involved: the test is a complete enumeration of the key values the cribs touch.

**Chance count (I-193, extended to a non-additive cipher).** With independent uniform carved letters, each non-tree edge is hit with
probability exactly 1/26 for any root value, so a component with r independent cycles has exactly 26^(1−r) consistent root values on average,
and **E_config = Π_cyclic 26^(1−r_c)** is the exact expected number of solutions (an upper bound on the pass probability). `cmp191` prints fits,
solutions and E per cell (H) and per band e = round(−log26 E_config) (B). A cell is full power iff its E (summed over routes and, for C2/C3,
tableau pairs) is ≤ 0.05. **Meter check before K4:** 40 uniform random texts on 81 probe routes, text-level z per band −0.12, +0.56, −0.90,
−1.90, −0.20 (e = 0–4); 0 solutions where E ≤ 0.003.

Pairs: ordered (m, n), 2 ≤ m, n ≤ 26, m ≠ n (600; m is the first pass). Forms VV, VB, BV, BB (first letter = first pass). Models P (key on the
plaintext index: substitute then transpose) and C (key on the carved index: transpose then substitute).

## 3. Results (K4)
| Cell | Scope | Full-power cells | E in them | K4 fits | Verdict |
|---|---|---|---|---|---|
| C1 | A–Z>KRYPTOS and KRYPTOS>A–Z, all 165,782 routes, P + C, 4 forms | P 1,328 (166 pairs × 8), C 1,056 (132 × 8) | 3.22 + 1.72 | 3 + 2 | `EXACT-EXCL` (5 chance fits decoded, gibberish) |
| C3 | 572 themed × {A–Z, KRYPTOS} pairs (both orders), all_s512 (324 routes) | P 664 (166 × 4), C 520 (130 × 4) | 1.80 + 0.61 | 1 + 1 | `EXACT-EXCL` on 1/512 (2 fits decoded, gibberish) |
| C2t | direct, 20,592 ordered themed × themed pairs | 768 (192 × 4) | 4.89 | 1 | `EXACT-EXCL` (1 fit decoded, gibberish) |
| C2v | direct, 75,292 vocabulary-keyed × {A–Z, KRYPTOS} pairs | 664 (166 × 4) | 0.73 | 0 | `EXACT-EXCL` |

**Fits in full-power cells, all decoded with [`decode191.py`](../tools/cycle191/decode191.py) (unique solution each; [decodes](../data/cycle191/decodes191.txt)):**
C1 route 81496 C AZ>KA BB 13 × 6 (`tclftejsaynbixlb…`), route 116792 C AZ>KA BV 17 × 3 (`augbrfebqaljbjtl…`), route 31182 P AZ>KA BB 2 × 18
(91/97 letters, `oa?cjofiwswftqqa…`), route 44016 P AZ>KA BV 2 × 17 (`ckppnmoggddqiukd…`), route 134787 P KA>AZ BV 16 × 3 (`ftngazaumaudlgke…`);
C3 route 118272 C AGENCY/Z>AZ BV 16 × 3, route 161792 P AZ>TIMEZONE/Z VB 17 × 2; C2t ALEXANDERPLATZ/K>LAYERTWO/K VV 13 × 7. All eight full
decryptions are random letters around the cribs. Every one sits in a cell with E between 0.003 and 0.045 and has E_config 8 × 10⁻⁸ – 2 × 10⁻⁶,
i.e. exactly the kind of fit the 166–192 full-power pairs × thousands of configs should throw up by chance (8 observed vs 12.97 expected over
C1, C2t, C2v and C3). Every full-power cell with a fit had its fit printed (H count = printed M lines).

**Low-power cells.** C1: 7,216 cells, solutions 704,061,790 vs E 704,873,420 (−0.12 %); C3 +0.08 %; C2t −1.8 %; C2v −3.0 % (keyed vocabulary
alphabets and K4's letter frequencies are not the uniform model). K4's band totals: e = 3:
5,190 vs 5,119; e = 4: 225 vs 176; e = 5: 4 vs 6.7; e ≥ 6: 0 vs 0.23.

**Grid** (K4 + 19 shuffles, seeds 19111–19129, A–Z>KRYPTOS / KRYPTOS>A–Z on all_s512; [grid](../data/cycle191/grid191.txt)): fits with
e ≥ 3: K4 7, nulls 4–12 (p⁺ 0.85); e ≥ 4: K4 0, nulls 0–1; solutions e = 1: K4 8,166, nulls 7,754–10,721 (p⁺ 0.45); e = 2: K4 226, nulls
214–289 (p⁺ 0.85). K4 is inside the shuffles everywhere.

## 4. Controls and checks
- **Planted controls 11/11** ([`plant191.py`](../tools/cycle191/plant191.py), seed 19100, passes applied literally letter by letter; checker
  [`checkctl191.py`](../tools/cycle191/checkctl191.py)). Positives found at their row, tableau order, reduced form, model and (m, n), and the
  decoder reproduces the planted plaintext at every determined position: P1 A–Z>KRYPTOS P Vig 7 + Vig 11; P2 KRYPTOS>A–Z C Beau 5 + Vig 13;
  P3 A–Z>KRYPTOS C variant 8 + Beau 12; P4 KRYPTOS>A–Z P Vig 6 + Beau 19; P5 direct PALIMPSEST (A–Z) then ABSCISSA (KRYPTOS); P6 direct KRYPTOS
  (Beau, KRYPTOS) then BERLINCLOCK (Vig, A–Z); **one-tableau plants (I-190 requirement)** P7 A–Z>A–Z C variant 3 + Vig 25 and P8 KRYPTOS>KRYPTOS
  P Beau 4 + Beau 9 (26 solutions each: the additive shift). Negatives clean: N1 three passes (5, 7, 11), N2 random key, N3 = P1 with one wrong
  carved crib letter.
- **I-195 handling (equivalent cells).** Fits at equivalent cells were listed, not counted as failures: period multiples (P3 at 8 × 24 and
  16 × 12; P5 at 20 × 8), model P = C on the identity route (P6), one-tableau form equivalents (P7 BB = VV), and P8's period-36 key also fitting
  m | 36, n | 36 cells such as 2 × 18 on other tableau orders, because the crib positions 27–33 and 63–69 are 36 apart (parallel crib edges).
- **Recount identical:** [`recount191.py`](../tools/cycle191/recount191.py) (literal letter-level two-pass tables, vectorised DFS over the 26 root
  values; shares no code with `cmp191`) on 7 routes × 4 tableau orders (incl. the one-tableau A–Z>A–Z and KRYPTOS>KRYPTOS) × 2 models × 4 forms ×
  600 pairs: fit sets and solution counts identical for K4 (47,711), P1 (47,756), P2 (47,476), P7 (47,778) and n19111 (47,870).
- **Meter:** see §2; K4's own band totals are in §3.

## 5. Cost
Probe 0.11 s on 81 routes; registered run 15:54:02–15:57:25 PT (203 s: C1 99 s, grid 5 s, C3 25 s, C2t 10 s, recount 29 s, C2v 35 s); with
probe, meter and controls ≈ 3.7 min heavy. The direct C2 outputs (19 GB of per-cell lines) were reduced by [`agg191.c`](../tools/cycle191/agg191.c)
(all 1,499 files had `END`) and deleted; the aggregated tables are in [summary191](../data/cycle191/summary191.txt).

## 6. Limits (not covered)
- **One wrong crib letter** (strict test only; the audit is I-197).
- **A transposition between the two passes** (first key on the plaintext index, second on the carved index: the "sandwich", I-199). Models P and
  C put both keys on the same side of the route.
- Themed or vocabulary tableau pairs behind the routes beyond 1/512 (themed) and direct (vocabulary) (I-198); vocabulary × vocabulary pairs.
- Three or more passes; m or n > 26; dropped or extra letters (I-196).
- Low-power pairs (too few independent crib cycles: E > 0.05 per cell) cannot be decided by 24 cribs.

## 7. Verdict
Two arbitrary periodic keys on two different tableaux, A–Z and KRYPTOS in either order, Vig/Beau/variant, key on the plaintext or carved index,
behind any of the 165,782 K3-law decimations/routes: **`EXACT-EXCL`** in every full-power cell (fits at the chance rate, all decoded and
rejected); **`LOW-POWER`** elsewhere. No K4 solution.
