# Case file 172 — Both hands from the long list: Quagmire IV with two vocabulary alphabets and a linear-recurrence key, behind K3's decimation law (cycle 184)

**Status:** negative. **Type:** new family slot (cycle 183 was an audit). IDEAS [I-163](../IDEAS.md) (the cycle-184 pointer I-170); I-130
costed and declared dead on arrival (§5). Pre-registered in [`tools/cycle184/PREREG184.md`](../tools/cycle184/PREREG184.md) (commits
ca93e91, 003d8dc, 8b61feb, 464d905, ~12:26–12:27 PT) with the solver, plants, decoder, checker, recount, summarizer and null seeds,
**after** the planted controls had been rehearsed (14/14, I-119) and the top order timed (I-169), before any K4 or registered-null run.
Smoke and timing used only the reserved shuffle, seed 9184 (I-116).

**Result in one line:** no Quagmire IV tableau with **both** alphabets from the 18,776-alphabet vocabulary (plaintext-side A,
ciphertext-side B, 352,538,176 ordered pairs, Vig / Beau, any rotations and the variant via the affine family) with an affine
linear-recurrence key k[i] = c₁k[i−1] + … + c_Lk[i−L] + d (mod 26) on the plaintext index fits K4 behind any of the 165,782 K3-law
decimations / routes at **L 1–4: 0 fits on the full set → `EXACT-EXCL`**. 19 shuffles 0; controls 14/14; brute-force recount identical;
second join path and audit build identical. **No solution.**

## 1. Why this
Case 170 closed Quagmire IV with a recurrence key when one hand was one of the 144 themed alphabets (5.4 M ordered pairs). A K1/K2-style
tableau can be keyed by any word, on either side, so the natural next step is both hands from the long list: 3.5 × 10⁸ ordered pairs per
route. About 99 % of these pairs are new (96 of the 144 themed alphabets are in the vocabulary; pairs with A = B repeat Quagmire III,
case 168; both kinds are kept).

## 2. Method (exact; [`lrk184.c`](../tools/cycle184/lrk184.c) = case 170's `lrk182.c` verbatim apart from the header line)
Conventions as cases 166–171 (cribs EASTNORTHEAST 21–33 and BERLINCLOCK 63–73, 0-indexed; plaintext position i carved at S[i];
Vig k = B(c) − A(p), Beau k = B(c) + A(p)). Mod 2 the 24 crib key bits are w = parity_B(carved letter) ⊕ parity_A(crib letter).
- **Method 1 (registered main run).** For each (c, d) mod 2 at order L_max = 4 the passing words form an affine space w₀ + span(w_j);
  a hash join per (c, d) on σ(pa_A) ⊕ (w₀ ≫ 4) for all 18,776 A, one σ(cp_B) lookup per (B, (c, d)) per route (18,776 × 32 probes).
- **Method 0 (second join path, audit).** CSR union map ∪_A (W₄ ⊕ pa_A): 18,776 × 342 words = 6.4 M entries, small enough at L 4.
- **Method 2 (audit build, `-DSAFE=1`).** Every one of the 3.5 × 10⁸ pairs looked up in the table; no GF(13) nesting shortcut.
- **GF(13).** Every mod-2 pass is re-checked against the table, then lrk180's `solve0`; fit ⇔ mod 2 and mod 13 both solvable at that L
  (nested in L, exact).
- **Chance rate** ≈ 26^(2L+2−24) per (route, pair, form); 1.17 × 10¹⁴ configurations per full set: L 3 ≈ 3 × 10⁻⁹, L 4 ≈ 2 × 10⁻⁶ fits per
  text. Every registered cell has full power.
- **Timing line (I-169), reserved shuffle, all_s64, 6 threads:** L_max 3 1.2 s, **L_max 4 4.4 s**, L_max 5 25.5 s (≈ 27 min full set) →
  L ≤ 4 registered on the full set; L 5 not run (I-171).

## 3. Results — K4 and 19 nulls ([`summary184.txt`](../data/cycle184/summary184.txt))
| cell | K4 | 19 nulls (all_s512, 324 routes) | mod-2 survivors, K4 full set (diagnostic) | verdict |
|---|---|---|---|---|
| L 1 | **0 (full set)** | 0 each | 21,026,632 | `EXACT-EXCL` |
| L 2 | **0 (full set)** | 0 each | 76,564,787 | `EXACT-EXCL` |
| L 3 | **0 (full set)** | 0 each | 300,013,596 | `EXACT-EXCL` |
| L 4 | **0 (full set)** | 0 each | 1,190,953,754 | `EXACT-EXCL` |

Vig and Beau both 0 in every cell; no overflow and no `X` line in any text. Method 0 and method 1 gave identical H lines on K4 all_s64
(2,591 routes); the audit build gave identical H lines to method 1 on K4 all_s2048 (81 routes). K4 lines:
[`k4_runs184.txt`](../data/cycle184/k4_runs184.txt); null lines: [`nulls_counts184.txt`](../data/cycle184/nulls_counts184.txt). Nothing to decode.

**Grid (I-152 empirical rank).** The fit cell is all-zero for all 20 texts (reported, not scored). D1 (mod-2 passes at L 4, all_s512) K4
2,339,902 vs 2,231,666–2,405,237 (mean 2,327,717, SD 43,009), p⁺ 0.40 / p⁻ 0.65. **Grid p⁺ 0.40 / p⁻ 0.65.** K4 is an ordinary text.

## 4. Controls ([`controls_check184.txt`](../data/cycle184/controls_check184.txt), [`controls_planted184.txt`](../data/cycle184/controls_planted184.txt))
Independent string-level encryptor ([`plant184.py`](../tools/cycle184/plant184.py), seed 18400, plaintext as cycles 180–183); each
plant behind a route q of all.bin, searched on q ± 200 with methods 1 and 0; audit build on q−2…q+3 against method 1 on the same rows.
- **10/10 positives PASS** (planted A, B, form and L found at q; planted (c, d) mod 2 / mod 13 listed; string-level replay = plaintext):
  P1 L1 Vig MEDITERRANEAN/Z × SAINTLY/K; P2 L2 Beau MERCHANT/Z × OBLIQUE/Z; P3 L3 Vig NOVEMBER/Z × PLIGHT/K; P4 L4 Beau ITALIAN/K ×
  RATTLING/K, non-unit last weight; P5 L4 Vig WHIP/K × KNIGHTS/Z; P6 progressive (c 1, d 3) MOUTHS/Z × HESITATING/K; P7 L2 Vig
  SAINTLY/K × SAINTLY/K (A = B); P8 L1 Vig LAYER/Z × TOMB/Z; P9 L2 Beau SLOWLY/Z × EGYPT/Z; P10 L1 Beau KA × SHADOW/K. P1–P7 use only
  alphabets outside the themed list, i.e. the part of the space that case 170 never saw.
- **4/4 negatives PASS** (nothing at q): N1 = P3 with one wrong carved letter (slot 30), N2 random key, N3 a random alphabet outside
  the vocabulary, N4 an order-5 plant (outside L ≤ 4).
- Method 0 and the audit build: identical H lines on all 14 windows.
- **Disclosed (budget, as in cycle 183):** the rehearsal before the push is the registered control run. Binaries (`lrk184` 92ae4b82…,
  `lrk184safe` e7a28859…) and `plants.json` (298cb2d3…) were unchanged afterwards; only the checker was re-run after the push.
- **Independent recount** ([`recount184.py`](../tools/cycle184/recount184.py), recount182 logic: numpy brute force over every (c, d) ∈ Z₂₆²,
  and every (c₁, c₂, d) ∈ Z₂₆³ at P9's row with A = SLOWLY/Z; no table, CRT, syndrome or nesting). Slice all.bin[::4000] + the planted
  routes of P8, P9, P10 (45 rows); A, B ∈ the 33 recount alphabets. lrk184 ran on the slice with the **full** vocabulary on both sides
  and was restricted to recount-list pairs. **6/6 texts identical: RECOUNT MATCH** (P8 L1, P9 L1 and L2, P10 L1; **0 for K4, n18411,
  n18412** in both tools); see [`recount184.txt`](../data/cycle184/recount184.txt). **Disclosed:** the first comparison reported a
  mismatch on P9 because the comparison script kept lrk184's L 3–4 lines at the L 2 row (the C run used L_max 4, cycle 182's used 2).
  The script was fixed to keep only L 1 and the listed L 2 row (commit with the data); the solver and the recount were not touched.
  P9's planted second-order stream also satisfies a first-order recurrence at the crib slots, which both tools found.

## 5. I-130 declared dead on arrival (not run)
Gromark with both alphabets free behind the decimations: the 24 crib equations u(p) + k = v(c) (mod 26), with u and v unknown
permutations, form a graph on the crib letters (13 plaintext letters + the distinct carved letters). Only its independent cycles are
checks. For K4 over all_s64 the cycle rank is **0 on 1,182 / 2,591 routes**, 1 on 998, 2 on 359, 3 on 48, 4 on 4 (mean 0.72). On a
rank-0 route every primer passes (only injectivity limits it), so over 10^L primers the chance count is far above one for every L, and an
exact feasibility count cannot tell K4 from a shuffle: `LOW-POWER` by construction. Only a full-decryption score (case 63's route,
behind 165,782 routes) could, and that is not affordable. I-130 is closed with that label.

## 6. Scope, blind spots, lessons
- **Excluded:** K4 = (one of the 165,782 K3-law decimations / routes) ∘ (Quagmire IV with A, B any ordered pair from the 18,776
  vocabulary alphabets, any rotations, Vig / Beau / variant) with an affine mod-26 linear-recurrence key on the plaintext index, arbitrary
  weights and seed, order ≤ 4. With cases 168 and 170: every keyed-tableau recurrence over this vocabulary is closed strictly at L ≤ 4
  (themed pairs to L 6).
- **Not covered:** L 5 (I-171, full power but ≈ 27 min); one wrong letter (I-172); the carved-index key (I-164); alphabets outside the
  vocabulary (phrase-keyed, reversed); non-linear generators.
- **Lesson.** One measured timing at the top order (4.4 s at L 4, 25.5 s at L 5 on 1/64) decided the scope before the rules were written,
  as I-169 asks. A second one, the cycle rank of the crib graph, settled I-130 in a fraction of a second without a run: before building a
  two-free-alphabet solver, count how many real checks the cribs leave.
