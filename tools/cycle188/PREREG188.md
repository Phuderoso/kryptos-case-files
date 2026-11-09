# Cycle 188 pre-registration — one-error audit of case 174: carved-index Quagmire IV with a linear-recurrence key behind K3's decimation law (IDEAS I-185), with the I-183 add-on

Written and pushed before any K4 or registered-null run. Timing only on the reserved shuffle seed 9188
(`random.Random(9188).shuffle(list(K4))`, I-116), under rule **I-180** (top registered order only, 81 routes, `timeout 60`):
`lrk188` L 1–3 on `all_s2048.bin` 3.4 s per direction (f and r, 0 fits, mismatch 0); L 1–2 0.06 s per direction. No order above 3
was timed. Extrapolation: L 1–2 on the full set ≈ 130 s (f) / 115 s (r); L 3 on the full set ≈ 2 h per direction (not registered).
**Planted controls rehearsed before this push (I-119): 15/15** (33 s); the rehearsal is declared the registered control run (as in
cycles 183–187): binaries `lrk188` (md5 57e3f6e6…, built from `tools/cycle188/lrk188.c` 1092f956… with
`gcc -O3 -march=native -fopenmp`), `lrk188safe` (`-DSAFE=1`, e4da6cd5…), `plant188.py` (seed 18800, b25b1b99…), `checkctl188.py`
(dae25e10…), `decode188.py` (11a94742…) are unchanged after it. Recount rehearsed on the planted text P10 only (3.1 s, MATCH).
**Heavy budget:** ≤ 8 min in total including controls and timing (≈ 45 s spent before this push).

## Question (audit slot: 187 was a new family)
Case 174 excluded (strict) Quagmire IV — plaintext-side A, ciphertext-side B — × Vigenère / Beaufort with an affine linear-recurrence key
k[j] = c₁k[j−1] + … + c_Lk[j−L] + d (mod 26) on the **carved index** j (seed at carved positions 0…L−1) behind the 165,782 K3-law
decimations / routes. Does that exclusion survive **one** carving error (one mis-carved letter at a crib slot's carved position, or one
wrong crib letter)? Direction **f** = A themed (`alpha_themed180.txt`, 144, 255a21fa…) × B vocabulary (`alpha172.txt`, 18,776, 92793b74…);
direction **r** = A vocabulary × B themed. Variant and rotations are covered (k → k + e only changes d).

## Method (exact; new solver `lrk188.c`)
One slot t's key value is a free unknown. By CRT a fit with slot t free exists mod 26 iff the 23 other slots are consistent mod 2 and
mod 13 for the same t. Mod 2: lrk186's projected streams with a Hamming-1 dilation (I-161 / lrk183 moved to the carved index):
V1 = V_Lmax ∪ {v ⊕ e_r}; per candidate, st2(L) = w ∈ V_L (every t allowed) or A2(L) = {t : w ⊕ e_r[t] ∈ V_L}. Method 1 = per-perm hash join
of V1 against the small side, candidates deduplicated and re-checked by linear scan (X if not within distance 1). GF(13): loop over c mod 13
with lrk186's basis table; slot t free = rows except t consistent (elimination). Exact shortcuts (off in `-DSAFE=1`): a half-split
prefilter for mod-2-strict candidates (one bad row cannot sit in both halves) and GF(13) at L_max first (nesting holds for a fixed free slot).
Audit build = method 2 (every (A, B) pair against a per-perm 2^24 bitset of V1), no prefilter, no shortcut.
**Chance rate** per (perm, pair, form) ≈ 25 · 26^(2L+1−24): L 2 on the full set (9 × 10¹¹ pair-forms per direction) ≈ 3 × 10⁻¹⁴ fits
per text; L 3 on all_s512 ≈ 4 × 10⁻¹⁴. Every registered cell has full power.

## Registered cells
- **C1** K4, direction f, L 1–2, **full set** (8 contiguous chunks of 20,723 rows, last to 165,782; a chunk without `END` = not run).
- **Grid** K4 + 19 nulls `random.Random(s).shuffle(list(K4))`, s = **18811…18829** (`nulls188.txt`, 04389628…), L 1–2, both directions,
  `all_s512.bin` (324 perms, 2a8c7ba2…).
- **Audit** K4 L 1–3 main vs SAFE on `all_s20000.bin` (9 rows, 46533f11…), both directions: H lines must be identical.
- **Recount** (independent numpy brute force, `recount188.py`): order 1 on the carved index, one error, slice = all.bin[::4000] + planted
  rows of P10, P11 (`slice188.bin`, 44 rows, 61abeaff…), 33 × 33 ordered pairs of `alpha_recount180.txt` × 2 forms, texts K4, P10, P11,
  n18811, n18812 (`rc_texts.txt`, aea00c92…); must equal `lrk188` (A = B = recount list, L 1) fit sets exactly.
- **C3** K4, directions f and r, L 1–3, `all_s512.bin`.
- **C2** K4, direction r, L 1–2, full set (8 chunks; each chunk runs only if the heavy total + 18 s ≤ 475 s; a chunk not run is reported as not covered).
Run order = priority (C1, grid, audit, recount, C3, add-on B, C2) via `run_cycle188.sh` (45c5bbd8…), each job under `setsid timeout`.
**Not run (cost):** L 3 beyond all_s512; I-184 (case 174 direction r strict on the other 7/8) does not fit the budget.

## Labels
K4 0 fits in a cell → `EXACT-EXCL` (that direction's alphabet lists, Vig/Beau, carved-index key, that cell's orders and perms; at most one
wrong crib key value, strict included). K4 > 0 → every fit decoded by `decode188.py` (independent CRT + string-level replay of all 97
letters); a solution needs a full coherent English decryption with the cribs at the official positions (one slot may differ),
reproducible. Any `X` line or a missing `END` invalidates the cell.

## Grid (I-152 empirical rank; I-182 second-batch rule)
F = fits L 1–2 (scored only if not all-zero), D = one-error mod-2 passes at L 2 (`pass2`, L 2 line), per direction. p⁺ = (1 + #nulls ≥ K4)/20,
p⁻ = (1 + #nulls ≤ K4)/20, floor 0.05, no multiplicity correction. A floor rank is a rank flag only and goes to a second batch (I-182).

## Add-on B: I-183 (second batch for the cycle-187 direction-r D flag; run only if heavy total + 40 s ≤ 470 s; script gate)
Statistic D = case 174's direction-r mod-2 passes at L 3 (`lrk186` from cycle 187, md5 4f41a243…, method 1, A vocabulary × B themed,
`pass2` on the L 3 vig line), on the disjoint row set **all.bin[256::512]** (324 rows, `all_r256s512.bin`, f9206375…). Texts
(`i183_texts188.txt`, 0425d914…): **40 parity-matched shuffles** (seeds 18841–18880, K4's letters permuted within the A–Z parity classes)
= **primary null**; 20 plain shuffles (seeds 18881–18900) = descriptive; K4. p_F = (1 + #matched ≥ K4)/41. **REPLICATED iff p_F ≤ 0.05**,
else NOT REPLICATED (flag closed). I-166 filtered inflation and the batch-to-batch spread vs cycle 187's 19 nulls reported descriptively.

## Controls (`plant188.py`, seed 18800; independent string-level encryptor; one carving error injected by shifting the B-index of the carved letter at a crib slot by δ)
Positives (found at q with planted A, B, form, L and the planted free slot t; planted c mod 2 and mod 13 listed; independent decode = planted
plaintext except at the erroneous slot): P1 f L1 Vig KA × SAINTLY/K (t 5, δ 7); P2 f L2 Beau PALIMPSEST/Z × MERCHANT/Z (t 18, δ 3); P3 f L2 Vig
BERLINCLOCK/Z × NOVEMBER/Z (error at a seed slot, carved position < 2); P4 f L3 Beau AZ × ITALIAN/K (non-unit last weight, t 0); P5 r L1 Vig
MEDITERRANEAN/Z × ABSCISSA/Z (t 23); P6 r L2 Beau OBLIQUE/Z × KA (t 12, δ 2: wrong mod 13 only); P7 r L3 Vig PLIGHT/K × PALIMPSEST/Z (seed row, t 14,
δ 13: wrong mod 2 only); P8 r L1 progressive, no error (found as strict, t −1); P9 f L2 KA × KA (t 13, δ 13); P10 f L1 LAYERTWO/Z × TOMB/Z (t 9) and
P11 r L1 Beau SLOWLY/Z × EGYPT/Z (t 15, δ 6) (recount positives). Negatives (no fit at q, both directions): N1 = P2's key with two wrong carved
letters; N2 random key + one error; N3 alphabet outside both lists (RAND1 × MERCHANT/Z, L2, one error); N4 order-4 plant + one error (run at L ≤ 3).
L ≤ 2 plants on q ± 100 with L 1–2; order-3 plants and N2/N4 on q ± 10 with L 1–3. Audit build H lines identical to the main build on q−2…q+3 for every plant.
