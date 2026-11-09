# Case file 174 — The key that walks the stone: Quagmire IV with a linear-recurrence key on the carved index (cycle 187)

**Status:** negative. **Type:** new family (184 new, 185 audit, 186 no result). IDEAS [I-164](../IDEAS.md) via the pointer I-179.
Pre-registered in [`tools/cycle187/PREREG187.md`](../tools/cycle187/PREREG187.md) (commits d5d3d0a, ba084b5, 25ed522, ~13:53 PT) with
the plants, decoder, checker, run script, recount and null seeds, **after** the planted controls had been rehearsed (15/15, I-119) and
the top order timed under rule I-180 (81 routes, `timeout 60`, L ≤ 3), before any K4 or registered-null run. Timing used only the
reserved shuffle, seed 9187 (I-116). Solver: cycle 186's [`lrk186.c`](../tools/cycle186/lrk186.c), unchanged.

**Result in one line:** no Quagmire IV tableau — plaintext-side alphabet A, ciphertext-side alphabet B, one from the 144 themed
alphabets and the other from the 18,776 vocabulary alphabets — × Vig/Beau with an affine linear-recurrence key on the **carved** index
fits K4 behind the K3-law decimations / routes: **direction f (A themed × B vocabulary) 0 fits at L 1–3 on all 165,782 routes;
direction r (A vocabulary × B themed) 0 fits at L 1–3 on every 8th route → `EXACT-EXCL` on that coverage.** 19 shuffles 0 in both
directions; controls 15/15; audit build identical; independent recount 5/5 identical. One diagnostic rank flag (direction r mod-2
passes, §3), booked for a second batch under I-182, not a signal. Add-on: the case 173 D1 flag **NOT REPLICATED** (I-176 closed). **No solution.**

## 1. Why this
Cases 170–173 put the recurrence key on the plaintext index (key after the transposition is undone). The other natural order is
transposition first, then key, so the key runs along the carved letters (M1). Cases 168 and 170 covered this order only for Quagmire
I–III (one alphabet); with two different alphabets the crib-side mask moves with every route, so case 170's precomputed table cannot
be used. That is why `lrk186.c` was written (cycle 186).

## 2. Method (exact)
k[j] = c₁k[j−1] + … + c_Lk[j−L] + d (mod 26), j = carved position, seed at carved positions 0…L−1, arbitrary weights. Vigenère
c = B[(A(p) + k) mod 26], Beaufort c = B[(k − A(p)) mod 26]; variant and rotations of A or B only shift d. Mod 2: the 2^(2L+1) streams
projected on the carved crib positions give a per-route word set; a pair's word is cp_B ⊕ pp_A; per route the larger side is hashed and
probed with every stream word ⊕ the small side (each pair once). Candidates re-checked by linear scan (X line if not found). GF(13):
lrk180's loop over c mod 13 with (seed, d) linear; shortcut at L_max first (exact by nesting). Audit build `-DSAFE=1`: every pair
against the per-route 2^24 bitset, no shortcut.
- **Chance rate** ≈ 26^(2L+1−24) per (route, pair, form); 8.96 × 10¹¹ configurations per direction on the full set → L 3 ≈ 8 × 10⁻¹³
  fits per text. Full power everywhere.
- **Timing (I-180):** 81 routes, reserved shuffle: 0.18 s per direction at L 1–3. Registered run 13:54:09–14:00:42 PT; C1 249 s.
  Heavy total ≈ 410 s (6.8 min) with controls, timing, grid, audit, C2, recount and the I-176 add-on.

## 3. Results ([`k4_runs187.txt`](../data/cycle187/k4_runs187.txt), [`nulls_counts187.txt`](../data/cycle187/nulls_counts187.txt), [`summary187.txt`](../data/cycle187/summary187.txt))
| Cell | Routes | Pairs per route | Orders | mod-2 passes (L 3) | K4 fits |
|---|---|---|---|---|---|
| C1 direction f | 165,782 (all, 8/8 chunks with END) | 2,703,744 | L 1–3, Vig + Beau | 1,608,469 | **0** |
| C2 direction r | 20,723 (all.bin[::8]) | 2,703,744 | L 1–3, Vig + Beau | 198,416 | **0** |

No X line, no missing END. **Grid** (I-152; K4 + 19 shuffles, seeds 18711–18729, all_s512, 324 routes): F (fits) all zero in both
directions (not scored). D (mod-2 passes at L 3): direction f K4 2,954 vs 2,793–3,539 (mean 3,134.1, SD 221.0), p⁺ 0.75 / p⁻ 0.30;
**direction r K4 3,771 vs 2,659–3,685 (mean 3,098.8, SD 280.8), p⁺ 0.05 (floor), z +2.39.** That is a rank flag on a parity
statistic with no fit behind it. Parity floors in this series have failed to replicate three times (I-133, I-160, and I-176 below).
Under I-182 it is not certified on one batch. It goes to a second batch (I-183).
**Audit** ([`audit187.txt`](../data/cycle187/audit187.txt)): main vs SAFE on all_s20000, both directions, H lines identical.
**Recount** ([`recount187.txt`](../data/cycle187/recount187.txt)): brute-force order-1 carved-index streams (numpy, no mod-2/mod-13
split) on a 44-row slice, 33 × 33 recount alphabets × 2 forms: K4 0 / 0, P10 1 / 1, P11 1 / 1, n18711 0 / 0, n18712 0 / 0, identical sets.

## 4. Add-on B: I-176 replication ([`i176_counts187.txt`](../data/cycle187/i176_counts187.txt))
Case 173's D1 (one-error mod-2 survivors at L 3, `lrk185`, vocabulary × vocabulary) had K4 above all 19 nulls on all.bin[::2048]
(K4 3,838,120; +3.2 SD). On the disjoint rows all.bin[1024::2048]: **K4 3,309,381.** 40 parity-matched shuffles (primary, seeds
18741–18780): 3,232,286–3,733,053, mean 3,525,817.4, SD 102,903.6; **39 ≥ K4 → p_F 0.976**, z −2.10. **Verdict (registered):
`NOT REPLICATED` → flag closed.** Descriptive (I-166): 20 plain shuffles (18781–18800) mean 3,488,296.0, SD 132,935.0; filtered to
parity agreement ≥ the median (49) n 11, mean 3,456,640.0; inflation (filtered − matched) −69,177. Batch-to-batch (I-182): case 173's
19 nulls mean 3,493,537, SD 109,192 vs these 20 plain 3,488,296 / 132,935. The null centre is stable. K4's own value fell by 529 k
on the new rows, so the flag belonged to the old row set, not to K4. (K4 near the bottom here is the opposite tail and was not
tested; p⁻ would be 0.049 post hoc, description only.)

## 5. Controls ([`controls_check187.txt`](../data/cycle187/controls_check187.txt), [`controls_planted187.txt`](../data/cycle187/controls_planted187.txt))
Independent string-level encryptor ([`plant187.py`](../tools/cycle187/plant187.py), seed 18700), each plant behind perm q of all.bin.
11 positives found at q with the planted pair, form and L, the planted (c, d) listed mod 2 and mod 13, and the independent decoder
([`decode187.py`](../tools/cycle187/decode187.py): CRT of the listed solutions, all 97 letters replayed) returning the planted
plaintext exactly: f L1/L2/L3 incl. a seed-slot plant (a crib at carved position < 2) and a non-unit last weight; r L1/L2/L3 incl. a
seed slot and a progressive key; A = B (KA × KA); two recount plants. 4 negatives missed in both directions: one wrong carved letter,
random key, alphabet outside both lists, order-4 plant. SAFE build H lines = main on q−2…q+3 for every plant. **15/15.**

## 6. Limits
Direction r covers 1/8 of the routes (the other 7/8 ≈ 3.6 min → I-184). L 4 needs the faster GF(13) stage (I-181). Strict only:
one wrong letter is out of scope (an audit slot, I-185). Alphabet lists as cases 170–172; vocabulary × vocabulary on the carved index
not covered. All conclusions are conditional on the K3-law decimation / route family and the official cribs at their positions.
