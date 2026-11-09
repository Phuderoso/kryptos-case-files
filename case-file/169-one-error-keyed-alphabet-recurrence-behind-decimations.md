# Case file 169 — A forged signature in a borrowed hand: case 168 under one wrong letter (cycle 181)

**Status:** negative (audit holds). **Type:** audit / variant (cycle 180 was a new family). IDEAS [I-156](../IDEAS.md) (the cycle-181
pointer I-157; Firefly's standing one-error priority I-003). Pre-registered in [`tools/cycle181/PREREG181.md`](../tools/cycle181/PREREG181.md)
(commits 83545e7, c03aee3, 3e08a19, 45dda94, ~11:00 PT) with the solver, plants, decoder, checker, recount, summarizer and null
seeds, **after** the planted controls had been rehearsed on both builds (I-119) and before any K4 or registered-null run. Smoke and
timing used only the reserved shuffle, seed 9181 ([I-116](../IDEAS.md)).

**Result in one line:** [case 168](168-linear-recurrence-keyed-alphabets-behind-decimations.md)'s exclusion **survives one wrong
letter**. No affine linear-recurrence key k[i] = c₁k[i−1] + … + c_Lk[i−L] + d (mod 26), arbitrary weights and seed, read through a
keyword-keyed tableau (18,776 vocabulary alphabets × Quagmire I / II / III × Vigenère / Beaufort / variant), fits K4 behind any of
the 165,782 K3-law decimations / routes **with any one of the 24 crib letters (or the carved letter at its position) allowed to be
wrong**: **0 fits at L 1–6 on the plaintext index (full set), 0 at L 1–2 on the carved index (full set) and 0 at L 3 on the carved
index (1/8 of the routes) → `EXACT-EXCL`** (one-error scope). 19 shuffles 0 in every cell; controls 17/17; numpy recount 4/4
fitting-slot sets identical; audit build identical. **No solution.**

## 1. Why this
Case 168 needed all 24 crib key values exact. The sculpture has known carving quirks (IQLUSION, the missing S / UNDERGRUUND,
DESPARATLY), and case 168's own negative N1 (one wrong carved letter) was correctly *missed* by the strict test, which is the
point: a strict zero says nothing about a key that is right except for one bad rivet. Case 167 closed that gap for the A–Z / KRYPTOS
tableaux; this file closes it for the keyword tableaux of case 168.

## 2. Method (exact; [`lrk181.c`](../tools/cycle181/lrk181.c))
Repo conventions as cases 166–168: cribs EASTNORTHEAST 21–33 and BERLINCLOCK 63–73 (0-indexed); plaintext position i is carved at
S[i]; A = plaintext-side alphabet, B = ciphertext-side; Vig k = B(c) − A(p), Beau k = B(c) + A(p); types q1 (A keyed, B = A–Z),
q2 (A = A–Z, B keyed), q3 (A = B keyed). `alpha172.txt` (18,776 alphabets; 56,326 (alphabet, type) pairs).
- **Wildcard by CRT (case 167).** Slot t wrong ⇔ its key value is a free unknown. Since Z₂₆ ≅ Z₂ × Z₁₃, a fit with t free exists iff
  some v₂ passes GF(2) and some v₁₃ passes GF(13) for the same t.
- **M0, key on the plaintext index, L 1–6 (full set).** Case 168's 2²⁴ mod-2 table (in-block equations + propagation across the
  gap, per L) is **dilated to Hamming distance 1**: T₁[w] = T[w] ∨ ⋁ₜ T[w ⊕ 2ᵗ]. Still one lookup per (perm, alphabet, type).
  Survivors get their allowed slots (all 24 if w passes strictly). GF(13): block-1 slots (21–33) try every v₁₃ through lr178's solve0;
  block-2 slots (63–73) need one solve with that slot's in-block rows dropped and the propagation check ignoring it. This is exact,
  because propagation from block 1 fixes all of block 2, so "free value at t" ⇔ "the other ten block-2 slots match". The same
  shortcut mod 2 re-checks the table on every fit (`X` line on disagreement; none).
- **M1, key on the carved index (seed at carved 0…L−1, any offset), L 1–2 full set, L 3 on `all_s8.bin`.** The 2^(2L+1) mod-2 streams
  projected on the crib slots' carved positions (`pext`) go into a per-thread 2²⁴ bitset **with their 24 one-bit neighbours**; one
  lookup per (alphabet, type); then per weight vector c mod 13 the 24 rows (linear in seed and d) are eliminated, and if
  inconsistent, each allowed slot's row is left out. This is only done for slots up to the first inconsistent row, since leaving out
  a later row cannot repair it (exact).
- **Audit build** `-DSAFE=1` switches both shortcuts off. It gave identical H/O lines on all 17 control windows and on K4 (all_s64,
  every cell) ([`safe_audit181.txt`](../data/cycle181/safe_audit181.txt)).
- **Chance rate** per (perm, pair, form) ≈ 24·26^(2L+2−24); 1.87 × 10¹⁰ configurations per full set: M0 L 5 ≈ 2 × 10⁻⁶,
  **M0 L 6 ≈ 0.003 fits per text**; M1 L ≤ 3 < 10⁻¹⁰. Every run cell has full power.
- **Dead-on-arrival line (I-151), declared before the run:** M0 L 7 gives ≈ 2.1 chance fits per full set (`LOW-POWER` by
  construction) at ≈ 18 min per full pass → not run. M1 L 3 on the full set (≈ 190 s per text) and M1 L 4 themed → not run, queued (I-159).

## 3. Results — K4 and 19 nulls ([`summary181.txt`](../data/cycle181/summary181.txt))
| model | cell | K4 | 19 nulls (all_s64) | one-error mod-2 passes, K4 (diagnostic) | verdict |
|---|---|---|---|---|---|
| M0 plaintext index | L 1–5 | **0 (full set)**, 0 (s64) | 0 each | 24,346,369 (full) | `EXACT-EXCL` |
| M0 plaintext index | L 6 | **0 (full set)**, 0 (s64) | 0 each | 72,102,370 (full) | `EXACT-EXCL` (chance ≈ 0.003) |
| M1 carved index | L 1–2 | **0 (full set)**, 0 (s64) | 0 each | 277,429 (full) | `EXACT-EXCL` |
| M1 carved index | L 3 | **0 (all_s8, 20,723 routes)**, 0 (s64) | 0 each | 107,239 (s8) | `EXACT-EXCL` on 1/8 of the routes |

No strict fit, no one-error fit, no overflow, no `X` line in any text. K4 lines: [`k4_runs181.txt`](../data/cycle181/k4_runs181.txt); null
lines: [`nulls_counts181.txt`](../data/cycle181/nulls_counts181.txt). There is nothing to decode.

**Grid (pre-registered, I-152 adopted: empirical rank, no Poisson tails).** All four fit cells are all-zero for all 20 texts, so they are
reported and not scored. Diagnostics (all_s64): D1 (M0 one-error mod-2 passes L 5–6) K4 1,403,785 vs 1,395,005–1,429,960, p⁺ 0.80 /
p⁻ 0.25. D2 (M1 one-error mod-2 passes L 1–3) **K4 18,432 vs 15,575–18,207, above all 19 → p⁺ 0.05 (the floor)**. Grid p⁺ 0.05 / p⁻ 0.25.
**Reading of the D2 floor (as pre-registered: a rank flag, not a signal).** D2 is the Hamming-1 dilation of case 168's D2, the
same statistic that sat at the floor there and **did not replicate** on 40 fresh shuffles (p_F 0.12). The two are computed from the
same K4 letters at the same carved positions, so a second floor is not independent evidence. Split by type (post hoc, description
only): q1 K4 6,211 vs null mean 5,634 (SD 594, 3/19 ≥), **q2 6,455 vs 5,642 (SD 302, 1/19 ≥)**, q3 5,766 vs 5,744 (10/19 ≥). In
case 168 the excess sat in q1. Here it sits in q2, where A = A–Z and the keyed alphabet acts on K4's carved letters. These are
mod-2 near-misses with **no fit anywhere behind them**. A pre-registered replication on fresh shuffles is queued (I-160). The
covariate-matched version (shuffles that keep K4's letter multiset *and* the parity pattern at the crib carved positions, I-146) is
the right null for this kind of count.

## 4. Controls ([`controls_check181.txt`](../data/cycle181/controls_check181.txt), [`controls_planted181.txt`](../data/cycle181/controls_planted181.txt))
Independent string-level encryptor ([`plant181.py`](../tools/cycle181/plant181.py), seed 18100; plaintext as cycle 180); each plant
behind a perm q of all.bin, the carved letter at the error slot changed by a random non-zero shift; searched on q ± 500.
- **12/12 positives PASS.** Each was found at its q with the planted alphabet, type, form and L, **with the planted error slot as the
  only fitting slot** (strict plants: one `t −1` line), the planted (c, d) listed (M0), and a string-level replay equal to the planted
  plaintext except at the mis-carved letter. The plants were: P1 M0 L3 q3 Vig SHADOW/Z err 25 (`…EASTMORTHEAST…`); P2 M0 L5 q1 Beau
  BERLIN/K err 66 (block-2 shortcut); P3 M0 L6 q2 Vig ABSCISSA/Z err 21 (first seed slot); P4 M0 L2 q3 Beau SHADOW/K err 73; P5 M0
  L4 q3 strict; P6 M0 L6 KA non-unit last weight err 33 (start of the gap); P7 M1 L1 err 64; P8 M1 L2 q1 Beau LODESTONE/K err 22;
  P9 M1 L3 q2 MAGNETIC/Z err 29; P10 M1 L3 strict; P11 progressive key (c 1, d 3) err 30; P12 M1 L3 q1 SHADOW/K err 73.
- **5/5 negatives PASS:** two-error plants (M0 slots 66 + 70, M1 slots 22 + 68), random keys (M0, M1), and a one-error plant made
  with an alphabet not in the list. All were missed at their q.
- **Rehearsal before the push** (I-119) caught two issues, fixed before the push. A carved-index strict fit was printed once per
  slot; it is now one line. The M1 decoder replayed only the printed mod-2 stream, which is not identified off the cribs when
  c ≡ 0 (mod 2), the cycle-179 lesson again; it now re-enumerates every matching stream. No rule changed.
- **Independent recount** ([`recount181.py`](../tools/cycle181/recount181.py), numpy brute force: no CRT, no table, no `pext`, no
  elimination, no shortcut; one-error fits by explicit seed variants and a crib-mismatch count ≤ 1). Slice: all.bin[::4000] + the
  planted perms of P4, P7, P8, P11 (46 rows). Alphabets: the 33 of `alpha_recount180.txt`. Texts: K4, n18111, n18112, P4, P7, P8, P11.
  Cells: M0 L 1 and M1 L 1 everywhere, M0 L 2 (P4) and M1 L 2 (P8) at the planted row and alphabet. **4/4 fit lines identical with
  identical fitting-slot sets** (P11 slot 30, P4 slot 73, P7 slot 64, P8 slot 22), and **0 fits for K4, n18111 and n18112 in both
  tools** ([`recount181.txt`](../data/cycle181/recount181.txt)). This is a thin check. It confirms the dilated table, the slot
  attribution and both shortcuts at low order; the high-L cells rest on plants P3, P5, P6 and P9–P12.

## 5. Scope, blind spots, lessons
- **Excluded (one-error scope):** K4 = (one of the 165,782 K3-law decimations / routes) ∘ (Quagmire I, II or III tableau from any of
  the 18,776 vocabulary-keyed alphabets, Vig / Beau / variant, any rotation) with an affine mod-26 linear-recurrence key, arbitrary
  weights and seed, order ≤ 6 on the plaintext index or ≤ 2 on the carved index (≤ 3 on every 8th route), **with at most one wrong
  letter among the 24 crib positions** (errors off the crib positions do not enter the test). Includes progressive, Fibonacci-type and
  periodic keys of period ≤ L through those tableaux.
- **Not covered:** M0 L 7 (`LOW-POWER` by construction, ≈ 2 chance fits per pass) and L 8; M1 L 3 on the other 7/8 of the routes and
  M1 L ≥ 4 (I-159); two or more errors; insertions / deletions (they shift the transposition); Quagmire IV (I-155); alphabets outside
  the list; non-linear generators.
- **Lesson (method):** a precomputed pass table turns a one-error audit into a **Hamming-1 dilation**. That is one extra 2²⁴ pass at
  build time and the same single lookup per configuration, so the audit costs ≈ 1.5–2× the strict run, not 24×. Two exact
  shortcuts (block-2 slots need no value loop; skip-tests stop at the first inconsistent row) halve the GF(13) stage, and a
  `-DSAFE` build that turns them off is the cheap way to prove they changed nothing.
- **Lesson (statistics):** a diagnostic that is a monotone image of an earlier flagged diagnostic will re-flag on the same text. Count it
  once (the case-168 replication already answered it) and test it, if at all, against a null that holds the shared covariate fixed.
- **Disclosed:** `summarize181.py` as pushed read the H-line fields at the wrong indices and crashed on the first run; the indices were
  fixed after the main run (no rule, cell or threshold changed; the raw H lines are in the data files).
- **Budget:** registered main run 437 s (7.3 min, 6 threads, shared box), controls 24 s, SAFE audit 13 s. Rehearsal (both builds,
  ≈ 91 s) and smoke (≈ 47 s) came before the push. The recount ran single-core and niced, outside the budget.

## Reproduce
`gcc -O3 -march=native -fopenmp -o lrk181 tools/cycle181/lrk181.c` (and `-DSAFE=1 -o lrk181safe`); `tools/cycle181/run_cycle181.sh`
(W = scratch with run/{lrk181,k4.txt,nulls181.txt}, support/{all.bin,all_s8.bin,all_s64.bin,alpha172.txt}); `summarize181.py out
nulls181.txt`; controls `run_controls181.sh`; recount `mkslice181.py`, `recount181.py slice.bin alpha_recount180.txt texts.txt
P4:42:SHADOW/K P8:44:LODESTONE/K`, `cmprecount181.py`. Inputs and md5s: [`inputs181.txt`](../data/cycle181/inputs181.txt).
