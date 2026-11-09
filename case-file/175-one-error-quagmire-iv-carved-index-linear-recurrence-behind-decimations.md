# Case file 175 — One letter off the walking key: case 174 under one carving error (cycle 188)

**Status:** negative. **Type:** audit (187 new family). IDEAS [I-185](../IDEAS.md) (part of I-003), with add-ons I-183 and I-184.
Pre-registered in [`tools/cycle188/PREREG188.md`](../tools/cycle188/PREREG188.md) (commits 15191b9, 3e71e19, 228f74e, f564fb8, ~14:24 PT)
with the plants, decoder, checker, run script, recount and null seeds, **after** the planted controls had been rehearsed (15/15, I-119) and
the top order timed under rule I-180 (81 routes, `timeout 60`, L ≤ 3), before any K4 or registered-null run. Add-on C (I-184) was
pre-registered separately in [`PREREG188b.md`](../tools/cycle188/PREREG188b.md) (commit 3aaaa61, ~14:30 PT) after the main run and before
any I-184 run. Timing used only the reserved shuffle, seed 9188 (I-116). New solver: [`lrk188.c`](../tools/cycle188/lrk188.c).

**Result in one line:** no Quagmire IV tableau — plaintext-side alphabet A, ciphertext-side alphabet B, one from the 144 themed alphabets
and the other from the 18,776 vocabulary alphabets — × Vig/Beau with an affine linear-recurrence key on the **carved** index fits K4
behind the K3-law decimations / routes **even if one of the 24 crib key values is wrong** (one mis-carved letter or one wrong crib
letter): **both directions 0 fits at L 1–2 on all 165,782 routes; L 3 on every 512th route (324) → `EXACT-EXCL` (one-error scope) on
that coverage.** 19 shuffles 0 in both directions; controls 15/15; audit build identical; independent recount 5/5 identical.
Add-ons: the cycle-187 direction-r D flag **NOT REPLICATED** on a second batch (I-183 closed); case 174's strict direction r extended
from 1/8 to **6/8** of the routes (0 fits, I-184 left with two eighths). **No solution.**

## 1. Why this
Case 174 excluded the carved-index Quagmire IV recurrence only under exact cribs. A single slip of the chisel, or one wrong crib letter,
would break every strict test of this kind. Cases 167, 169, 171 and 173 gave the plaintext-index versions their one-error audits; this
is the carved-index one (lrk183's method moved onto lrk186's per-route streams).

## 2. Method (exact)
k[j] = c₁k[j−1] + … + c_Lk[j−L] + d (mod 26), j = carved position, seed at carved positions 0…L−1, arbitrary weights; Vigenère
c = B[(A(p) + k) mod 26], Beaufort c = B[(k − A(p)) mod 26] (variant and rotations only shift d). One slot t has a free key value. By CRT,
a fit with slot t free exists mod 26 iff the 23 other slots are consistent mod 2 **and** mod 13 for the same t.
- **Mod 2:** lrk186's projected streams per route, dilated to Hamming distance 1 (V1 = V ∪ {v ⊕ e_r}); per candidate, st2(L) = the
  pair's word is a stream word (every t allowed), else A2(L) = the slots whose flip gives a stream word. Per-route hash join of V1 against
  the small side; candidates deduplicated and re-checked by linear scan (X line if not within distance 1).
- **Mod 13:** loop over c mod 13 with lrk186's basis table; slot t free = the rows other than t consistent (elimination, early exit).
  Exact shortcuts (off in the `-DSAFE=1` audit build): for mod-2-strict candidates a half-split prefilter (one bad row cannot sit in both
  halves of the 24 rows); GF(13) at L_max first (nesting holds for a fixed free slot). Audit build: every (A, B) pair against a per-route
  2^24 bitset of V1, no prefilter, no shortcut.
- **Chance rate** ≈ 25 · 26^(2L+1−24) per (route, pair, form): L 2 on the full set (≈ 9 × 10¹¹ pair-forms per direction) ≈ 3 × 10⁻¹⁴
  fits per text; L 3 on 324 routes ≈ 4 × 10⁻¹⁴. Full power everywhere.
- **Timing (I-180):** 81 routes, reserved shuffle, L 1–3: 3.4 s per direction (L 1–2: 0.06 s). L 3 on the full set would take ≈ 2 h per
  direction, so it was registered on all_s512 only.

## 3. Results ([`k4_runs188.txt`](../data/cycle188/k4_runs188.txt), [`nulls_counts188.txt`](../data/cycle188/nulls_counts188.txt), [`summary188.txt`](../data/cycle188/summary188.txt))
| Cell | Routes | Pairs per route | Orders | one-error mod-2 passes (top L) | K4 fits |
|---|---|---|---|---|---|
| C1 direction f | 165,782 (all, 8/8 chunks with END) | 2,703,744 | L 1–2, Vig + Beau | 10,271,635 | **0** |
| C2 direction r | 165,782 (all, 8/8 chunks with END) | 2,703,744 | L 1–2, Vig + Beau | 10,239,377 | **0** |
| C3 direction f | 324 (all_s512) | 2,703,744 | L 1–3 | 79,357 | **0** |
| C3 direction r | 324 (all_s512) | 2,703,744 | L 1–3 | 80,596 | **0** |

No X line, no missing END, no strict and no slot fit anywhere. **Grid** (I-152; K4 + 19 shuffles, seeds 18811–18829, all_s512, L 1–2):
F (fits) all zero in both directions (not scored). D (one-error mod-2 passes at L 2): direction f K4 20,205 vs 18,362–21,716
(mean 19,851.6, SD 1,003.4), p⁺ 0.40 / p⁻ 0.65; direction r K4 20,416 vs 17,912–21,699 (mean 19,915.8, SD 1,093.5), p⁺ 0.35 / p⁻ 0.70.
No rank flag. **Audit** ([`audit188.txt`](../data/cycle188/audit188.txt)): main vs SAFE on all_s20000 (9 routes), L 1–3, both directions,
H lines identical. **Recount** ([`recount188.txt`](../data/cycle188/recount188.txt)): brute-force order-1 carved-index streams (all
26³ (c, d, seed), numpy, no mod-2/mod-13 split, hits confirmed by direct Hamming distance ≤ 1) on a 44-row slice, 33 × 33 recount
alphabets × 2 forms: K4 0 / 0, P10 1 / 1, P11 1 / 1, n18811 0 / 0, n18812 0 / 0, identical sets.

## 4. Add-on B: I-183, second batch for the cycle-187 direction-r D flag ([`i183_counts188.txt`](../data/cycle188/i183_counts188.txt))
Case 174's direction-r D (strict mod-2 passes at L 3, `lrk186`) had K4 3,771 above all 19 nulls on all_s512 (p⁺ 0.05, z +2.39). On the
disjoint rows all.bin[256::512] (324 routes): **K4 3,092.** 40 parity-matched shuffles (primary, seeds 18841–18880): 2,713–4,029, mean
3,147.4, SD 280.0; **24 ≥ K4 → p_F 0.610**, z −0.20. **Verdict (registered): `NOT REPLICATED` → flag closed.** Descriptive (I-166): 20 plain
shuffles (18881–18900) mean 3,214.8, SD 227.2; filtered to parity agreement ≥ the median (49) n 11, mean 3,244.5; inflation (filtered −
matched) +97.2. Batch-to-batch (I-182): cycle 187's 19 nulls mean 3,098.8 / SD 280.8, here matched 3,147.4 / 280.0 and plain 3,214.8 / 227.2.
The centre and the spread held. K4 dropped from 3,771 to 3,092 on the new rows, so the flag again belonged to the row set. That is the fifth parity floor in a row that did not replicate.

## 5. Add-on C: I-184, case 174 direction r on further eighths ([`i184_runs188.txt`](../data/cycle188/i184_runs188.txt))
Strict, L 1–3, `lrk186` (cycle-187 binary), A vocabulary × B themed, residue classes all.bin[r::8]: r = 1…5 run (20,723 routes each,
mod-2 passes at L 3 205,458 / 204,696 / 201,539 / 197,655 / 203,005), **0 fits** in every class, END present, no X. Classes 6 and 7 were
stopped by the budget gate as registered. With case 174's class 0, direction r strict is now `EXACT-EXCL` on **6/8** of the routes.

## 6. Controls ([`controls_check188.txt`](../data/cycle188/controls_check188.txt), [`controls_planted188.txt`](../data/cycle188/controls_planted188.txt))
Independent string-level encryptor ([`plant188.py`](../tools/cycle188/plant188.py), seed 18800), each plant behind perm q of all.bin, one
carving error injected by shifting the B-index of the carved letter at a crib slot by δ. 11 positives found at q with the planted pair,
form, L and **the planted free slot**, the planted c listed mod 2 and mod 13, and the independent decoder ([`decode188.py`](../tools/cycle188/decode188.py):
CRT of the listed solutions, all 97 letters replayed) returning the planted plaintext except at the erroneous slot: f L1/L2/L3 (incl. an
error at a seed slot and a non-unit last weight); r L1/L2/L3 (incl. an error wrong mod 13 only, δ 2, and one wrong mod 2 only, δ 13, on a
seed row); an error-free progressive key (found as strict, t −1); A = B (KA × KA, δ 13); two recount plants. 4 negatives missed in both
directions: two wrong carved letters, random key + one error, alphabet outside both lists, order-4 plant. SAFE build H lines = main on
q−2…q+3 for every plant. **15/15.**

## 7. Limits
One-error L 3 covers 1/512 of the routes in each direction (the rest ≈ 2 h per direction now; needs a faster GF(13) stage, → I-187).
Two or more errors are out of scope. L 4 needs I-181. Strict direction r still lacks classes 6 and 7 (I-184, ≈ 64 s). Alphabet lists as
cases 170–174; vocabulary × vocabulary on the carved index not covered (I-188). All conclusions are conditional on the K3-law decimation /
route family and the official cribs at their positions (one slot may be wrong).
