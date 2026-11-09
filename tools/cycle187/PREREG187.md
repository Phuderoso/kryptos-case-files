# Cycle 187 pre-registration — Quagmire IV with a linear-recurrence key on the carved index behind K3's decimation law (IDEAS I-164, pointer I-179)

Written and pushed before any K4 or registered-null run. Timing only on the reserved shuffle seed 9187
(`random.Random(9187).shuffle(list(K4))`, I-116), under rule **I-180** (top registered order only, 81 routes first, `timeout 60`):
`lrk186` L 1–3 on `all_s2048.bin` 0.18 s per direction (f and r, 0 fits, no mismatch); `lrk185` L 1–3 on `all_r1024s2048.bin` 1.75 s.
No order above 3 was timed. **Planted controls rehearsed before this push (I-119): 15/15** (13 s); the rehearsal is declared the registered
control run (as in cycles 183–185): binaries `lrk186` (md5 4f41a243…, built from `tools/cycle186/lrk186.c` c1c8b576…), `lrk186safe`
(922eaf1c…), `lrk185` (0120f084…), `plant187.py` (seed 18700, 2e6de3c0…), `checkctl187.py` (59d8f702…), `decode187.py` (5def3d45…)
are unchanged after it. **Heavy budget:** ≤ 8 min in total including controls and timing (17 s spent before this push).

## Question (new-family slot: 184 new, 185 audit, 186 no result)
Quagmire IV — plaintext-side alphabet A, ciphertext-side alphabet B — × Vigenère / Beaufort with an affine linear-recurrence key
k[j] = c₁k[j−1] + … + c_Lk[j−L] + d (mod 26) on the **carved index** j (M1: transpose first, then key; seed at carved positions 0…L−1),
behind the 165,782 K3-law decimations / routes (`all.bin`, 946402ca…). Direction **f** = A themed (`alpha_themed180.txt`, 144, 255a21fa…) ×
B vocabulary (`alpha172.txt`, 18,776, 92793b74…); direction **r** = A vocabulary × B themed. Variant and rotations are covered (k → k + e
only changes d). Earlier coverage: case 172 (vocabulary × vocabulary, plaintext index), cases 168/170 (Quagmire I–III, carved index).

## Method (exact; `lrk186.c` unchanged from cycle 186)
Method 1: per perm, mod-2 key-bit word w = cp_B ⊕ pp_A joined (hash) against the projected 2^(2L+1) mod-2 streams; candidates re-checked
by linear scan (X line if not); GF(13) by lrk180's loop over c mod 13 (seed, d linear); shortcut GF(13) at L_max first (exact by
nesting). Audit build `-DSAFE=1` (method 2: every (A, B) pair against the per-perm 2^24 bitset, no shortcut).
**Chance rate** per (perm, pair, form) ≈ 26^(2L+1−24); 8.96 × 10¹¹ configurations per direction on the full set → L 3 ≈ 8 × 10⁻¹³ fits
per text. Every registered cell has full power.

## Registered cells
- **C1** K4, direction f, L 1–3, **full set** (8 contiguous chunks of 20,723 rows, last to 165,782; a chunk without `END` = not run).
- **C2** K4, direction r, L 1–3, `all_s8.bin` (= all.bin[::8], 20,723 perms, 3dd34d3c…). (Direction r on the full set does not fit the budget.)
- **Grid** K4 + 19 nulls `random.Random(s).shuffle(list(K4))`, s = **18711…18729** (`nulls187.txt`, bd97a17f…), L 1–3, both directions,
  `all_s512.bin` (324 perms, 2a8c7ba2…).
- **Audit** K4 L 1–3 main vs SAFE on `all_s20000.bin` (9 rows, 46533f11…), both directions: H lines must be identical.
- **Recount** (independent numpy/brute, `recount187.py`): order 1 on the carved index, slice = all.bin[::4000] + planted rows of P10, P11
  (`slice187.bin`, 44 rows, 78b67ef0…), 33 × 33 ordered pairs of `alpha_recount180.txt` × 2 forms, texts K4, P10, P11, n18711, n18712;
  must equal `lrk186` (A = B = recount list, L 1) fit sets exactly.
Run order = priority (C1, grid, audit, C2, recount, add-on) via `run_cycle187.sh`, each job under `setsid timeout`.
**Not run (cost):** direction r on the other 7/8; L 4 (needs I-181).

## Labels
K4 0 fits in a cell → `EXACT-EXCL` (that direction's alphabet lists, Vig/Beau, carved-index key, L 1–3, that cell's perms; strict, no
carving error). K4 > 0 → every fit decoded by `decode187.py` (independent CRT + string-level replay of all 97 letters); a solution needs a full
coherent English decryption with both cribs at the official positions, reproducible. Any `X` line or a missing `END` invalidates the cell.

## Grid (I-152 empirical rank; I-182 second-batch rule)
F = fits L 1–3 (scored only if not all-zero), D = mod-2 passes at L 3 (`passLmax`), per direction. p⁺ = (1 + #nulls ≥ K4)/20,
p⁻ = (1 + #nulls ≤ K4)/20, floor 0.05, no multiplicity correction. A floor rank is a rank flag only; under I-182 it is never certified on
this batch alone — it goes to a pre-registered second batch.

## Add-on B: I-176 replication (run only if heavy total + 110 s ≤ 480 s at that point; script gate)
Statistic D1 = one-error mod-2 survivors at L 3 (`lrk185`, method 1, A = B = vocabulary, `pass2` on the L 3 line), on the disjoint row
set **all.bin[1024::2048]** (81 rows, `all_r1024s2048.bin`, a8a90dbd…). Texts (`i176_texts187.txt`, 319ef020…): **40 parity-matched
shuffles** (seeds 18741–18780; K4's letters permuted within the A–Z parity classes, I-146/I-160 covariate) = **primary null**; 20 plain
shuffles (seeds 18781–18800) = descriptive; K4. p_F = (1 + #matched ≥ K4)/41. **REPLICATED iff p_F ≤ 0.05**, else NOT REPLICATED (flag closed).
I-166: the plain shuffles filtered to the covariate band (A–Z parity agreement with K4 at or above the median of the 20) give the
filtered mean; inflation = filtered mean − matched mean, reported beside the verdict. Batch-to-batch spread (I-182): matched mean / SD
vs case 173's 19 nulls reported descriptively.

## Controls (`plant187.py`, seed 18700; independent string-level encryptor, plaintext as cycles 180–185, each plant behind perm q of all.bin)
Positives (found at q with planted A, B, form, L; planted (c, d) mod 2 and mod 13 listed; independent decode = planted plaintext);
B (f) or A (r) outside the themed list unless stated: P1 f L1 Vig KA × SAINTLY/K; P2 f L2 Beau PALIMPSEST/Z × MERCHANT/Z; P3 f L3 Vig
BERLINCLOCK/Z × NOVEMBER/Z (seed slot: a crib at carved position < 2); P4 f L3 Beau AZ × ITALIAN/K (non-unit last weight); P5 r L1 Vig
MEDITERRANEAN/Z × ABSCISSA/Z; P6 r L2 Beau OBLIQUE/Z × KA; P7 r L3 Vig PLIGHT/K × PALIMPSEST/Z (seed slot); P8 r L1 progressive (c 1,
d 3) MOUTHS/Z × SHADOW/K; P9 f L2 Vig KA × KA (A = B); P10 f L1 LAYERTWO/Z × TOMB/Z and P11 r L1 Beau SLOWLY/Z × EGYPT/Z (recount
positives). Negatives (no fit at q, both directions): N1 = P3 with one wrong carved letter; N2 random key; N3 alphabet outside both lists
(RAND1 × MERCHANT/Z, L2); N4 order-4 plant. Audit build H lines identical to the main build on q−2…q+3 for every plant.
