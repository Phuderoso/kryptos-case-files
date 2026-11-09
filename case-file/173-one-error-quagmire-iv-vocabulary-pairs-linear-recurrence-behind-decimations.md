# Case file 173 — One bad rivet, both hands from the long list: one-error audit of case 172 (cycle 185)

**Status:** negative (budget-limited coverage). **Type:** audit slot (cycle 184 was a new family). IDEAS [I-172](../IDEAS.md) (the
cycle-185 pointer I-174). Pre-registered in [`tools/cycle185/PREREG185.md`](../tools/cycle185/PREREG185.md) (commits a007631, 1c28933,
00bad71, 1a0fd13, ~12:55–12:56 PT) with the solver, plants, decoder, checker, recount, summarizer and null seeds, **after** the planted
controls had been rehearsed (14/14, I-119) and the top order timed (I-169), before any K4 or registered-null run. Smoke and timing
used only the reserved shuffle, seed 9185 (I-116).

**Result in one line:** no Quagmire IV tableau with **both** alphabets from the 18,776-alphabet vocabulary (352,538,176 ordered pairs,
Vig / Beau) with an affine linear-recurrence key on the plaintext index fits K4 behind the K3-law decimations / routes **with at most
one wrong letter among the 24 crib positions**: **0 fits at L 1 on the full set (165,782 routes), L 1–2 on 1/8, L 1–3 on 1/64 →
`EXACT-EXCL` on that coverage.** 19 shuffles 0; controls 14/14; brute-force recount 6/6 identical; audit build identical. One
diagnostic rank flag (D1 at the floor, §3), registered for replication, not a signal. **No solution.**

## 1. Why this
Case 172 closed the vocabulary × vocabulary family strictly at L 1–4, and its one-wrong-letter plant was (correctly) missed. Every
strict exclusion in this series has been followed by its one-error audit, because a single mis-carved letter or a wrong crib letter
would hide a true solution from a strict test (I-003). Pairs with A or B themed (≈ 1 %) repeat case 171; A = B repeats Quagmire III
one-error (case 169); both kept.

## 2. Method (exact; [`lrk185.c`](../tools/cycle185/lrk185.c) = case 171's `lrk183.c` verbatim apart from the header line)
Conventions as cases 166–172. Case 171's direction-r path with **both** lists = the vocabulary: the strict mod-2 table dilated to
Hamming distance 1 (I-161), a 25-probe syndrome join per (B, (c, d) mod 2) on σ(pa_A) ⊕ (w₀ ≫ L) (the one-bit neighbours of an
affine space are its translates by σ(eₜ)), duplicates removed per route; then per allowed wild slot a GF(13) prefilter on the in-block
rows avoiding the slot and the exact CRT wildcard (block-1 13-value loop through `solve0`, block-2 `solve0s`). Strict fits reported once.
Audit build `-DSAFE=1`: every pair looked up, no prefilter, 13-value loop on every slot.
- **Chance rate** ≈ 24·26^(2L+2−24) per (route, pair, form); 1.17 × 10¹⁴ configurations per full set: L 1 ≈ 10⁻¹³, L 2 ≈ 10⁻¹⁰,
  L 3 ≈ 6 × 10⁻⁸ fits per text. Full power everywhere.
- **Timing line (I-169)**, reserved shuffle, all_s64, 6 threads: L_max 1 1.5 s, L_max 2 6.6 s, **L_max 3 ≈ 37.7 s** (1.1 × 10⁸
  one-error mod-2 candidates, ≈ 25× the strict count). Full set: L 1 ≈ 1.6 min, L ≤ 2 ≈ 7 min, L ≤ 3 ≈ 40 min. The control rehearsal
  then cost 180 s (the audit build, every pair, ≈ 1.6 s per route), so the registered scope was cut to fit 8 minutes: C1 L 1–3 on 1/64,
  C2 L 1–2 on 1/8, C3 L 1 on the full set in eight resumable chunks, in that priority order.

## 3. Results — K4 and 19 nulls ([`summary185.txt`](../data/cycle185/summary185.txt))
| cell | routes | K4 fits | one-error mod-2 survivors (K4, per form) | verdict |
|---|---|---|---|---|
| C3 L 1 | **165,782 (full set, 8/8 chunks)** | **0** | 511,744,522 | `EXACT-EXCL` |
| C2 L 1–2 | 20,723 (all_s8) | **0** | 64.1 M (L 1), 230.8 M (L 2) | `EXACT-EXCL` (1/8) |
| C1 L 1–3 | 2,591 (all_s64) | **0** | 8.2 M, 29.2 M, 112.8 M | `EXACT-EXCL` (1/64) |
| grid L 1–3 | 81 (all_s2048) | **0**; 19 nulls 0 each | 3,838,120 at L 3 | — |

Vig and Beau both 0 in every cell; no overflow and no `X` line in any text; nothing to decode. The audit build gave H lines identical
to the main build on K4 all_s20000 (9 routes, L 1–3). K4 lines: [`k4_runs185.txt`](../data/cycle185/k4_runs185.txt); null lines:
[`nulls_counts185.txt`](../data/cycle185/nulls_counts185.txt).

**Grid (I-152 empirical rank).** Fit cell all-zero for all 20 texts (not scored). **D1** (one-error mod-2 survivors at L 3, all_s2048):
K4 **3,838,120** vs nulls 3,291,720–3,678,035 (mean 3,493,537, SD 109,192; K4 +3.2 SD), **p⁺ 0.05 (floor) / p⁻ 1.00**. This is a
**rank flag on a diagnostic**, not a signal: D1 counts parity coincidences between carved letters and alphabet parities, no fit exists
behind it, and the same statistic has floored before and not replicated (cases 168/169 → I-160, case 177 → I-133). Descriptive only:
on the 2,591 routes of C1, K4's L 3 count (112.8 M) is below the reserved shuffle's (113.5 M), one comparison. Registered for one
pre-registered replication with the covariate-matched null primary (Voynich C093 / I-166) as **I-176**. Grid p⁺ 0.05 / p⁻ 1.00.

## 4. Controls ([`controls_check185.txt`](../data/cycle185/controls_check185.txt), [`controls_planted185.txt`](../data/cycle185/controls_planted185.txt))
Independent string-level encryptor ([`plant185.py`](../tools/cycle185/plant185.py), seed 18500, plaintext as cycles 180–184); each plant
behind a route q of all.bin, then the carved letter at the error slot shifted by a random non-zero amount; main build on q ± 100, audit
build on q−2…q+3 against the main build on the same rows.
- **10/10 positives PASS** (planted A, B, form and L found at q; wild slot = the planted slot and no other; planted (c, d) mod 2 / mod 13
  listed; replay = plaintext except at the mis-carved letter): P1 L1 Vig MEDITERRANEAN/Z × SAINTLY/K err 25; P2 L2 Beau MERCHANT/Z ×
  OBLIQUE/Z err 66 (block 2); P3 L3 Vig NOVEMBER/Z × PLIGHT/K err 21 (a seed slot); P4 L3 Beau ITALIAN/K × RATTLING/K non-unit last weight
  err 33; P5 L2 Vig WHIP/K × KNIGHTS/Z strict (`t -1`); P6 progressive (c 1, d 3) MOUTHS/Z × HESITATING/K err 73; P7 L2 Vig SAINTLY/K ×
  SAINTLY/K (A = B) err 63; P8 L1 Vig LAYER/Z × TOMB/Z err 22; P9 L2 Beau SLOWLY/Z × EGYPT/Z err 70; P10 L1 Beau KA × SHADOW/K err 30.
  P1–P7 use only alphabets outside the themed list.
- **4/4 negatives PASS** (nothing at q): N1 two errors (66, 70); N2 random key; N3 a random alphabet outside the vocabulary; N4 an
  order-4 one-error plant (outside L ≤ 3).
- Audit build: identical H lines and fitting-slot sets on all 14 windows.
- **Disclosed (budget, as in cycles 183–184):** the rehearsal before the push is the registered control run. Binaries (`lrk185`
  0120f084…, `lrk185safe` d372a4c7…) and `plants.json` (36337da9…) unchanged afterwards; only the checker was re-run after the push.
- **Independent recount** ([`recount185.py`](../tools/cycle185/recount185.py), recount183 logic: L 1 by enumerating all 26³ streams with
  set lookups of the 24-tuple and its 23-tuples; L 2 by numpy over all 26⁵ at P9's row with A = SLOWLY/Z; no table, CRT, syndrome,
  dilation, prefilter or elimination). Slice all.bin[::4000] + the planted routes of P8, P9, P10 (45 rows, md5 aa0693d9…); A, B ∈ the
  33 recount alphabets. lrk185 method 1 ran on the slice with the **full** vocabulary on both sides and was restricted to recount-list
  pairs. **6/6 texts identical: RECOUNT MATCH** (P8 L1, P9 L2, P10 L1 one config each, wild slot as planted; **0 for K4, n18511, n18512**
  in both tools); see [`recount185.txt`](../data/cycle185/recount185.txt).

## 5. Scope, blind spots, lessons
- **Excluded (one-error scope):** K4 = (K3-law decimation / route) ∘ (Quagmire IV, A and B any ordered pair from the 18,776 vocabulary
  alphabets, Vig / Beau / variant) with an affine mod-26 linear-recurrence key on the plaintext index, at most one wrong letter among the
  24 crib positions: order 1 on all 165,782 routes, order ≤ 2 on every 8th route, order ≤ 3 on every 64th route.
- **Not covered:** L 2 on 7/8 of the routes, L 3 on 63/64, L 4 (I-175: needs a faster GF(13) stage); two errors; the carved-index key
  (I-164); alphabets outside the vocabulary; non-linear generators.
- **Lesson (budget).** I-169 timed the solver, but the control rehearsal turned out to be the expensive part: the audit build checks every
  one of 3.5 × 10⁸ pairs per route, ≈ 1.6 s per route, and 14 plants × 6 routes cost 180 s, four times the smoke. In a vocabulary ×
  vocabulary scope the audit window belongs in the timing line too (now part of I-169's wording).
- **Lesson (method).** At one error the work moves almost entirely into GF(13): ≈ 25 × the strict mod-2 survivors, each with up to 24
  slot prefilters. A single cheap necessary test — a wrong letter can spoil only one block, so block 1 *or* block 2 must be consistent on
  its own — would stop nearly all of them with two eliminations instead of 24 (I-175).
- **Budget:** smoke ≈ 52 s, rehearsal (= registered controls) 180 s, registered main run 240 s: **472 s ≈ 7.9 min heavy** (6 threads,
  shared box). Recount niced, outside the budget.

## Reproduce
`gcc -O3 -march=native -fopenmp -o lrk185 tools/cycle185/lrk185.c` (and `-DSAFE=1 -o lrk185safe`); `tools/cycle185/run_cycle185.sh`
(W = scratch with run/{lrk185,lrk185safe,k4.txt,nulls185.txt}, support/{all.bin,all_s8.bin,all_s64.bin,all_s2048.bin,all_s20000.bin,
alpha172.txt}); `summarize185.py out nulls185.txt`; controls `run_controls185.sh` (O=ctl); recount `mkslice185.py`, `lrk185 CT
slice185.bin alpha172.txt alpha172.txt LAB 0 999 1 1 2 q4r`, `recount185.py slice185.bin alpha_recount180.txt texts.txt P9:43:SLOWLY/Z`,
`cmprecount185.py recount.txt texts.txt rc alpha_recount180.txt P9:43:SLOWLY/Z`. Inputs and md5s: [`inputs185.txt`](../data/cycle185/inputs185.txt).
