# Case file 171 — One bad rivet, two hands: Quagmire IV with a linear-recurrence key under one wrong letter, behind K3's decimation law (cycle 183)

**Status:** negative. **Type:** audit (cycle 182 was a new family). IDEAS [I-165](../IDEAS.md) (the cycle-183 pointer I-167), part of
I-003. Pre-registered in [`tools/cycle183/PREREG183.md`](../tools/cycle183/PREREG183.md) (commits 450b985, 576eed7, 4360cef, 3edc9ad,
~11:56 PT) with the solver, plants, decoder, checker, recount, summarizer and null seeds, **after** the planted controls had been
rehearsed (14/14, I-119) and before any K4 or registered-null run. Smoke and timing used only the reserved shuffle, seed 9183 (I-116).

**Result in one line:** no Quagmire IV tableau (plaintext-side alphabet A, ciphertext-side alphabet B; one of the 144 themed alphabets
and one of the 18,776 vocabulary alphabets, both directions, Vig / Beau / variant, any rotations) with an affine linear-recurrence key
k[i] = c₁k[i−1] + … + c_Lk[i−L] + d (mod 26) on the plaintext index fits K4 behind any of the 165,782 K3-law decimations / routes **even
if one of the 24 crib letters (or the carved letter at its position) is wrong: 0 fits at L 1–4 on the full set, 0 at L 5 on 1/64 of the
routes → `EXACT-EXCL` (one-error scope)**. 19 shuffles 0; controls 14/14; brute-force recount identical; audit build identical. **No
solution.**

## 1. Why this
Case 170 excluded this family **strictly**; its N1 plant (one wrong carved letter) was, correctly, missed. Sanborn's carving has
known slips (K2's missing S, the K3 misspelling), so every strict exclusion of a high-impact family gets a one-error audit (I-003).
Cases 167 and 169 did this for the A–Z/KRYPTOS and Quagmire I–III versions; this is the Quagmire IV version.

## 2. Method (exact; [`lrk183.c`](../tools/cycle183/lrk183.c))
Conventions as cases 166–170 (cribs EASTNORTHEAST 21–33 and BERLINCLOCK 63–73, 0-indexed; plaintext position i carved at S[i];
Vig k = B(c) − A(p), Beau k = B(c) + A(p)). Slot t wild ⇔ its key value is a free unknown. Exact by CRT (cases 167/169): slot t free
fits mod 26 iff some v₂ passes GF(2) and some v₁₃ passes GF(13) **for the same t**; strict/strict is reported once (`t -1`).
- **Mod 2, dilated.** Case 170's 2²⁴ table T (bit L−1: some (c, d) mod 2 fits at order L) is dilated to Hamming distance 1 (I-161):
  SM[x] holds the slot mask {t : T[x ⊕ eₜ] at L_max} and the dilated L mask. The order-4 one-error pass set W1 has 8,198 words (order 5:
  32,718), still nested in L.
- **Method 0 (direction f, A = 144 themed).** U = ∪_A (W1 ⊕ pa_A), a 2²⁴ CSR map; per perm one lookup per B (18,776).
- **Method 1 (direction r, A = 18,776 vocabulary).** For each (c, d) mod 2 the passing words form an affine space V = w₀ + span(w_j);
  x is within one bit of V ⇔ σ(x) ⊕ (w₀ ≫ L) ∈ {0} ∪ {σ(eₜ)} (σ linear). So the case-170 hash join takes up to 25 probes per
  (B, (c, d)); duplicates are removed per perm.
- **Method 2 (audit, `-DSAFE=1`).** Every pair looked up in SM; no GF(13) prefilter; a 13-value loop on every slot (block 2 too).
- **GF(13).** Every candidate is re-checked against SM (`X` otherwise; none). Strict: lrk180's `solve0`. Per allowed slot t (all 24 if
  strict mod 2, else the slots whose flip passes mod 2): a **prefilter**, consistency of the in-block rows of both blocks that do not
  contain slot t (necessary, since the true key satisfies every such row); then exact: block-1 slot → v₁₃ ∈ Z₁₃ through `solve0`;
  block-2 slot → `solve0s` (case 169's exact shortcut: block 2 is fixed by propagation from block 1). The mod-2 side is confirmed with
  `solve0` / `solve0s` (`X` if not; none).
- **Chance rate** ≈ 24 · 26^(2L+2−24) per (perm, pair, form); 1.79 × 10¹² configurations per full set: L 4 ≈ 7 × 10⁻⁷, L 5 ≈ 4.5 × 10⁻⁴,
  L 6 ≈ 0.30 fits per text. Every registered cell has full power.
- **Not run (cost / I-151):** L 5 on the other 63/64 of the routes (≈ 7 min per direction with this code), L 6 (≈ 70 min per direction
  and ≈ 0.3 chance fits per text). Queued as I-168.

## 3. Results — K4 and 19 nulls ([`summary183.txt`](../data/cycle183/summary183.txt))
| direction | cell | K4 | 19 nulls (all_s64) | one-error mod-2 passes, K4 (diagnostic) | verdict |
|---|---|---|---|---|---|
| f (A themed × B vocabulary) | L 1–3 | **0 (full set)**, 0 (s64) | 0 each | 73,402,165 (full) | `EXACT-EXCL` |
| f | L 4 | **0 (full set)**, 0 (s64) | 0 each | 219,331,568 (full) | `EXACT-EXCL` |
| f | L 5 | **0 (all_s64, 2,591 routes)** | not run | 13,672,172 (s64) | `EXACT-EXCL` on 1/64 |
| r (A vocabulary × B themed) | L 1–3 | **0 (full set)**, 0 (s64) | 0 each | 73,198,863 (full) | `EXACT-EXCL` |
| r | L 4 | **0 (full set)**, 0 (s64) | 0 each | 219,056,254 (full) | `EXACT-EXCL` |
| r | L 5 | **0 (all_s64)** | not run | 13,664,700 (s64) | `EXACT-EXCL` on 1/64 |

No fit (strict or one-error), no overflow, no `X` line in any text. The audit build (method 2, no prefilter, 13-value loop on every
slot) gave identical H lines on K4 all_s2048 (81 routes), L 1–5, both directions. K4 lines: [`k4_runs183.txt`](../data/cycle183/k4_runs183.txt);
null lines: [`nulls_counts183.txt`](../data/cycle183/nulls_counts183.txt). There is nothing to decode.

**Grid (I-152 empirical rank).** The four fit cells are all-zero for all 20 texts (reported, not scored). D1 (direction f, one-error
mod-2 passes at L 4, all_s64) K4 3,435,762 vs 3,403,736–3,481,989, p⁺ 0.30 / p⁻ 0.75; D2 (direction r) K4 3,399,419 vs 3,399,415–3,457,728,
p⁺ 0.95 / p⁻ 0.10. **Grid p⁺ 0.30 / p⁻ 0.10.** K4 is an ordinary text (D2 sits low, one null below it; no flag).

## 4. Controls ([`controls_check183.txt`](../data/cycle183/controls_check183.txt), [`controls_planted183.txt`](../data/cycle183/controls_planted183.txt))
Independent string-level encryptor ([`plant183.py`](../tools/cycle183/plant183.py), seed 18300, plaintext as cycles 180–182); each
plant behind a perm q of all.bin, then the carved letter at the error slot's carved position shifted by a random non-zero amount;
searched on q ± 100 in both directions; audit build on q ± 20 compared with the main build on the same rows.
- **10/10 positives PASS** (planted A, B, form and L found at q in the planted direction; the wild slot is the planted one and no other;
  planted (c, d) mod 2 / mod 13 listed; string-level replay = plaintext except at the mis-carved position): P1 f L1 Vig KA × SHADOW/Z
  err 25; P2 f L3 Beau PALIMPSEST/K × BERLIN/Z err 66 (block 2); P3 f L5 Vig IQLUSION/Z × LODESTONE/K err 21 (a seed slot); P4 f L4 Beau
  ABSCISSA/Z × COMPASS/K, non-unit last weight, err 33; P5 f L2 Vig SHADOW/K × LODESTONE/K strict (`t -1`); P6 f progressive (c 1, d 3)
  BERLINCLOCK/K × MAGNETIC/Z err 73; P7 r L2 Beau MAGNETIC/Z × KA err 63; P8 r L4 Vig LODESTONE/Z × UNDERGRUUND/K err 30; P9 r L5 Beau
  CARTER/Z × PALIMPSEST/K err 70; P10 r L1 Vig AZ × KA err 22.
- **4/4 negatives PASS** (nothing at q in either direction): N1 two errors (66, 70), N2 random key, N3 a one-error plant with a pair
  outside the scope (TOMB/Z × SLOWLY/Z), N4 a one-error order-6 plant (outside L ≤ 5).
- Audit build: identical H lines and identical sets of fitting (L, form, q, A, B, slot) on all 14 windows.
- **Disclosed (budget):** the rehearsal before the push is the registered control run. Binaries (`lrk183` dae240ba…, `lrk183safe`
  5ed79c6d…) and `plants.json` (d0963307…) were unchanged afterwards; only the checker was re-run after the push. The rehearsal caught
  one checker issue (the audit comparison used full M-line text, which differs by design for block-2 slots), fixed before the push.
- **Independent recount** ([`recount183.py`](../tools/cycle183/recount183.py)): L 1 by enumerating all 26³ (c, d, seed) streams and
  looking up the 24-tuple and the 23-tuples with one slot removed; L 2 by numpy over all 26⁵ (c₁, c₂, d, k₂₁, k₂₂) with a mismatch
  count. No table, CRT, syndrome, dilation, prefilter or elimination. Slice all.bin[::4000] + the planted perms of P1, P6, P7, P10
  (46 rows); A, B ∈ the 33 recount alphabets (1,089 ordered pairs); see [`recount183.txt`](../data/cycle183/recount183.txt).
  **7/7 texts identical slot sets: RECOUNT MATCH**: P1 L1 KA × SHADOW/Z Vig slot 4, P7 L2 MAGNETIC/Z × KA Beau slot 13, P10 L1
  AZ × KA Vig slot 1, and **0 for K4, n18311, n18312** (and P6, whose BERLINCLOCK/K is not in the recount list) in both tools. A thin
  check at low order; the high-L cells rest on plants P3, P4, P8, P9.

## 5. Scope, blind spots, lessons
- **Excluded (one-error scope):** K4 = (one of the 165,782 K3-law decimations / routes) ∘ (Quagmire IV with A themed × B vocabulary or
  A vocabulary × B themed, any rotations, Vig / Beau / variant) with an affine mod-26 linear-recurrence key on the plaintext index,
  arbitrary weights and seed, order ≤ 4, with at most one wrong letter among the 24 crib positions; order 5 on 1/64 of the routes.
  Together with case 170: the strict and one-error versions of this family are closed at L ≤ 4.
- **Not covered:** L 5 on 63/64 of the routes and L 6 (I-168); two errors; vocabulary × vocabulary (I-163); the carved-index key (I-164);
  alphabets outside the lists; non-linear generators.
- **Lesson (method):** the Hamming-1 dilation fits both pair indexes without changing their shape. In the union map it only enlarges
  the stored set (×4 at order 4). In the syndrome join it becomes 25 probes per (B, (c, d)), because the one-bit neighbours of an affine
  space are its translates by σ(eₜ). The cost moves to GF(13): ~10⁹ one-error mod-2 survivors per direction at order 5, against ~10⁸ at
  order 4. A cheap necessary test (the rows that avoid the wild slot must be consistent) stops most of them before the 13-value loop.
- **Lesson (budget):** time the top order on the reserved shuffle before writing the scope. Order 6 cost 66 s on 1/64 in smoke, which
  is why L 5 is registered only on 1/64 and L 6 not at all.
- **Budget:** registered main run 233 s; rehearsal (= registered controls) 92 s and smoke ≈ 95 s before the push; ≈ 7.0 min heavy in
  total (6 threads, shared box). The recount ran niced, outside the budget.

## Reproduce
`gcc -O3 -march=native -fopenmp -o lrk183 tools/cycle183/lrk183.c` (and `-DSAFE=1 -o lrk183safe`); `tools/cycle183/run_cycle183.sh`
(W = scratch with run/{lrk183,lrk183safe,k4.txt,nulls183.txt,all_s2048.bin}, support/{all.bin,all_s64.bin,alpha172.txt,alpha_themed180.txt});
`summarize183.py out nulls183.txt`; controls `run_controls183.sh` (O=ctl); recount `mkslice183.py`, `lrk183safe CT slice183.bin
alpha_recount180.txt alpha_recount180.txt LAB 0 99 2 1 1 rc` (L 1 2 for P7), `recount183.py slice183.bin alpha_recount180.txt texts.txt
P7:44:MAGNETIC/Z`, `cmprecount183.py`. Inputs and md5s: [`inputs183.txt`](../data/cycle183/inputs183.txt).
