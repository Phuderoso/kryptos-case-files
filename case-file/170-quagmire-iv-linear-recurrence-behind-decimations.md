# Case file 170 — Two hands on one wheel: Quagmire IV with a linear-recurrence key behind K3's decimation law (cycle 182)

**Status:** negative. **Type:** new family (cycle 181 was an audit). IDEAS [I-155](../IDEAS.md) (the cycle-182 pointer I-162), plus the
cheap audit add-on [I-160](../IDEAS.md). Pre-registered in [`tools/cycle182/PREREG182.md`](../tools/cycle182/PREREG182.md) (commits
b7527cc, d3bb43b, 4f42b3b, 553efc3, ~11:28 PT) with the solver, plants, decoder, checker, recount, summarizer, null seeds and the I-160
replication rule, **after** the planted controls had been rehearsed (14/14, I-119) and before any K4 or registered-null run. Smoke and
timing used only the reserved shuffle, seed 9182 ([I-116](../IDEAS.md)).

**Result in one line:** no affine linear-recurrence key k[i] = c₁k[i−1] + … + c_Lk[i−L] + d (mod 26), arbitrary weights and seed, on
the plaintext index, read through a **Quagmire IV** tableau (plaintext-side alphabet A ≠ ciphertext-side alphabet B) with one alphabet
from the 144 themed alphabets and the other from the 18,776 vocabulary alphabets (both directions, 5.4 M ordered pairs, Vigenère /
Beaufort / variant, any rotations), fits K4 behind any of the 165,782 K3-law decimations / routes: **0 fits at L 1–6 (full set) →
`EXACT-EXCL`**. 19 shuffles 0; controls 14/14; numpy recount 6/6 identical; audit build identical. Add-on: case 169's D2 rank floor
**did not replicate** (I-160: plain p_F 0.073, parity-matched p_F 0.143) and is closed. **No solution.**

## 1. Why this
Cases 168/169 used **one** keyed alphabet per tableau (Quagmire I/II/III, the K1/K2 construction). Quagmire IV, with two different
keyed alphabets, is the natural next ACA form and was the explicit blind spot of case 168. Case 172 had excluded Quagmire IV with
*periodic* keys behind the same decimations (every ordered vocabulary pair, p ≤ 14); a recurrence key is a different, non-periodic key.

## 2. Method (exact; [`lrk182.c`](../tools/cycle182/lrk182.c))
Conventions as cases 166–169: cribs EASTNORTHEAST 21–33 and BERLINCLOCK 63–73 (0-indexed); plaintext position i is carved at S[i];
Vig k = B(c) − A(p), Beau k = B(c) + A(p). Direction **f**: A ∈ themed (`alpha_themed180.txt`, 144) × B ∈ vocabulary (`alpha172.txt`,
18,776). Direction **r**: A ∈ vocabulary × B ∈ themed. 2,703,744 pairs per direction; pairs with A = B repeat case 168 and were kept.
- **Mod 2 factorises.** The 24 crib key bits are w = parity_B(carved letter) ⊕ parity_A(crib letter) = cp_B(perm) ⊕ pa_A (constant), so
  the case-168 table T (2²⁴ entries, bit L−1 = "some (c, d) mod 2 fits at order L") still decides mod 2.
- **Nesting.** An order-L solution is an order-(L+1) solution with c_{L+1} = 0 (fewer in-block equations, identical propagation), mod 2
  and mod 13. So the order-6 pass set W₆ (5,462 words, 3.3 × 10⁻⁴ of 2²⁴) contains every lower order; the program checks this on T.
- **Method 0 (direction f, small A list).** U = ∪_A (W₆ ⊕ pa_A) is precomputed as a 2²⁴ CSR map word → A list (787 k entries); per perm
  one lookup per B returns exactly the passing A's. ≈ 18,776 lookups per perm instead of 2.7 M.
- **Method 1 (direction r, large A list).** For each (c, d) mod 2 at order 6 the passing words form an affine space w₀ + span(w_j)
  whose low 6 bits are the free seed (crib slots 21–26). So x ∈ V ⇔ σ(x) = w₀ ≫ 6, with σ(x) = (x ⊕ Σ x_j w_j) ≫ 6 linear. Pair
  test = hash join per (c, d) on σ(pa_A) ⊕ (w₀ ≫ 6) (precomputed for all 18,776 A) against σ(cp_B) (144 B per perm × 128 (c, d)).
- **Method 2 (audit, `-DSAFE=1`).** Every pair looked up in T, and no nesting shortcut in GF(13). Methods 0, 1 and 2 must give identical
  H lines.
- **GF(13).** Every mod-2 pass is re-checked against T (`X` line otherwise; none). lrk180's `solve0` mod 13 at order 6 first; lower L
  only if order 6 has a mod-13 solution (exact by nesting). Fit ⇔ mod 2 and mod 13 both solvable at that L.
- **Chance rate** ≈ 26^(2L+2−24) per (perm, pair, form); 1.79 × 10¹² configurations per full set: L 5 ≈ 2 × 10⁻⁵, **L 6 ≈ 0.013** fits
  per text. **Dead-on-arrival line (I-151):** L 7 ≈ 8.6 chance fits per pass (`LOW-POWER` by construction) → not run; vocabulary ×
  vocabulary (3.5 × 10⁸ pairs) and the carved-index key → not run (cost), queued.

## 3. Results — K4 and 19 nulls ([`summary182.txt`](../data/cycle182/summary182.txt))
| direction | cell | K4 | 19 nulls (all_s64) | mod-2 passes, K4 (diagnostic) | verdict |
|---|---|---|---|---|---|
| f (A themed × B vocabulary) | L 1–5 | **0 (full set)**, 0 (s64) | 0 each | 48,731,858 (full) | `EXACT-EXCL` |
| f | L 6 | **0 (full set)**, 0 (s64) | 0 each | 146,024,932 (full) | `EXACT-EXCL` (chance ≈ 0.007) |
| r (A vocabulary × B themed) | L 1–5 | **0 (full set)**, 0 (s64) | 0 each | 48,699,837 (full) | `EXACT-EXCL` |
| r | L 6 | **0 (full set)**, 0 (s64) | 0 each | 145,856,585 (full) | `EXACT-EXCL` (chance ≈ 0.007) |

No fit, no overflow, no `X` line in any text; the audit build (method 2, no shortcut) gave identical H lines on K4 all_s64 in both
directions. K4 lines: [`k4_runs182.txt`](../data/cycle182/k4_runs182.txt); null lines: [`nulls_counts182.txt`](../data/cycle182/nulls_counts182.txt).
There is nothing to decode.

**Grid (I-152 empirical rank).** The four fit cells are all-zero for all 20 texts (reported, not scored). D1 (direction f, order-6 mod-2
passes, all_s64) K4 2,279,282 vs 2,269,422–2,292,696, p⁺ 0.55 / p⁻ 0.50; D2 (direction r) K4 2,276,735 vs 2,264,891–2,298,656,
p⁺ 0.70 / p⁻ 0.35. **Grid p⁺ 0.55 / p⁻ 0.35.** K4 is an ordinary text here.

## 4. Add-on: I-160 replication (pre-registered, PREREG182 §B; [`i160_counts182.txt`](../data/cycle182/i160_counts182.txt))
Case 169's D2 (one-error carved-index mod-2 passes, L 1–3, all_s64, 18,776 alphabets × q1/q2/q3) had K4 18,432 above all 19 nulls.
Recomputed with the same binary: **18,432** (q1 6,211 / q2 6,455 / q3 5,766).
- **40 fresh plain shuffles** (seeds 18241–18280): 14,897–19,437, mean 17,218.7, SD 841.4; **2 ≥ K4 → p_F 0.073**, z +1.44.
- **20 parity-matched shuffles** (seeds 18281–18300, letters permuted within K4's A–Z parity classes, I-146): 16,722–19,622, mean
  17,533.2, SD 753.4; **2 ≥ K4 → p_F 0.143**, z +1.19. Built-in check: q1 depends only on the A–Z parity pattern, so it is identical
  (6,211, SD 0) in every matched shuffle, as it must be.
- **Decision (registered): `NOT REPLICATED` → flag closed.** By type (description only): the q2 excess persists somewhat (2–3 of 40 /
  2 of 20 ≥ K4), q1 and q3 are ordinary. Together with case 168's non-replication (p_F 0.12) the carved-index mod-2 near-miss line is
  closed as a chance upper-tail draw on the same letters at the same positions.

## 5. Controls ([`controls_check182.txt`](../data/cycle182/controls_check182.txt), [`controls_planted182.txt`](../data/cycle182/controls_planted182.txt))
Independent string-level encryptor ([`plant182.py`](../tools/cycle182/plant182.py), seed 18200, plaintext as cycles 180/181); each
plant behind a perm q of all.bin, searched on q ± 500 in both directions and with the audit build.
- **10/10 positives PASS** (planted A, B, form and L found at q in the planted direction, planted (c, d) mod 2 / mod 13 listed,
  string-level replay = plaintext): P1 f L1 Vig KA × SHADOW/Z; P2 f L3 Beau PALIMPSEST/K × BERLIN/Z; P3 f L5 Vig IQLUSION/Z ×
  LODESTONE/K; P4 f L6 Beau ABSCISSA/Z × COMPASS/K with a non-unit last weight; P5 f L2 Vig SHADOW/K × LODESTONE/K; P6 f progressive
  key (c 1, d 3) BERLINCLOCK/K × MAGNETIC/Z; P7 r L2 Beau MAGNETIC/Z × KA; P8 r L4 Vig LODESTONE/Z × UNDERGRUUND/K (B themed only);
  P9 r L6 Beau CARTER/Z × PALIMPSEST/K; P10 r L1 Vig AZ × KA.
- **4/4 negatives PASS** (missed at q in both directions): N1 = P2 with one wrong carved letter (strict family), N2 random key,
  N3 a pair outside the scope (TOMB/Z × SLOWLY/Z), N4 an order-7 plant (outside L ≤ 6).
- Audit build H lines identical to methods 0 / 1 on all 14 control windows. The rehearsal before the push gave the same 14/14
  (same `plants.json` md5); nothing was changed between rehearsal and the registered run.
- **Independent recount** ([`recount182.py`](../tools/cycle182/recount182.py), numpy brute force over every (c, d) ∈ Z₂₆², and every
  (c₁, c₂, d) ∈ Z₂₆³ at the L 2 spots; no table, CRT, syndrome or nesting). Slice all.bin[::4000] + the planted perms of P1, P5, P7
  (45 rows); A, B ∈ the 33 recount alphabets (1,089 ordered pairs). **6/6 texts identical fit sets**: P1 L1 KA × SHADOW/Z Vig, P5 L2
  SHADOW/K × LODESTONE/K Vig, P7 L2 MAGNETIC/Z × KA Beau, and **0 for K4, n18211, n18212** in both tools ([`recount182.txt`](../data/cycle182/recount182.txt)).
  Disclosed: the recount (slice of 45 rows, K4 and two nulls included) ran during the rehearsal, before the push, with the pushed tools
  unchanged. It is a thin check at low order; the high-L cells rest on plants P3, P4, P8, P9.

## 6. Scope, blind spots, lessons
- **Excluded:** K4 = (one of the 165,782 K3-law decimations / routes) ∘ (Quagmire IV with A themed × B vocabulary or A vocabulary × B
  themed, any rotations, Vig / Beau / variant) with an affine mod-26 linear-recurrence key on the plaintext index, arbitrary weights
  and seed, order ≤ 6, all 24 crib letters exact. Includes progressive, Fibonacci-type and periodic keys of period ≤ 6 through those
  tableaux.
- **Not covered:** L ≥ 7 (`LOW-POWER` at 7); vocabulary × vocabulary pairs (I-163); the key on the carved index (I-164); one wrong letter
  (I-165, the natural audit via I-161's Hamming-1 dilation); alphabets outside the lists; non-linear generators.
- **Lesson (method):** when one side of a two-alphabet test is a per-perm quantity and the other a constant, put the constant side into
  the precomputation. A union map (small constant side) or a per-(c, d) syndrome hash join (large constant side) turns 2.7 M pair
  lookups per perm into ≈ 19 k. The whole full-set run took 78 s for 1.8 × 10¹² configurations. Nesting in L removes all but one
  GF(13) solve per mod-2 pass.
- **Lesson (statistics):** the covariate-matched null was cheap to build by permuting within parity classes, and it has a free
  self-test (q1 must come out constant). Voynich's C092 note (~11:33 PT) proposed the same construction independently.
- **Budget:** registered main run 78 s, I-160 197 s, controls 40 s; rehearsal 39 s and smoke ≈ 15 s before the push; ≈ 6.1 min heavy
  in total (6 threads, shared box). The recount ran niced, outside the budget.

## Reproduce
`gcc -O3 -march=native -fopenmp -o lrk182 tools/cycle182/lrk182.c` (and `-DSAFE=1 -o lrk182safe`); `tools/cycle182/run_cycle182.sh`
and `run_i160_182.sh` (W = scratch with run/{lrk182,lrk182safe,lrk181,k4.txt,nulls182.txt}, support/{all.bin,all_s64.bin,alpha172.txt,
alpha_themed180.txt}); `summarize182.py out nulls182.txt i160`; controls `run_controls182.sh`; recount `mkslice182.py`, `recount182.py
slice182.bin alpha_recount180.txt texts.txt P5:43:SHADOW/K P7:44:MAGNETIC/Z`, `cmprecount182.py`. Inputs and md5s: [`inputs182.txt`](../data/cycle182/inputs182.txt).
