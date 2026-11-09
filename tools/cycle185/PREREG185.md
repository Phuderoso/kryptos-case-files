# Cycle 185 pre-registration — one-error audit of case 172 (Quagmire IV with both alphabets from the vocabulary and a linear-recurrence key behind K3's decimation law; IDEAS I-172)

Written and pushed before any K4 or registered-null run. Smoke / timing only on the reserved shuffle seed 9185
(`random.Random(9185).shuffle(list(K4))`, I-116), on `all_s64.bin`: every cell 0 fits, no overflow, no mismatch.
**Planted controls rehearsed before this push (I-119): 14/14** (main build on q ± 100, audit build on q−2…q+3 with identical H lines and
fitting-slot sets). The rehearsal is declared the registered control run (as in cycles 183–184): the binaries (`lrk185` md5 0120f084…,
`lrk185safe` d372a4c7…), `plant185.py` (seed 18500, md5 e0c45f48…) and `checkctl185.py` (1b0ce19f…) are unchanged after it.

## Question (audit slot; cycle 184 was a new family)
Case 172 excluded, **strictly**, Quagmire IV (plaintext-side alphabet A, ciphertext-side alphabet B, **both** from the 18,776-alphabet
vocabulary `alpha172.txt`, md5 92793b74…: 352,538,176 ordered pairs) × Vig/Beau with an affine linear-recurrence key
k[i] = c₁k[i−1] + … + c_Lk[i−L] + d (mod 26) on the plaintext index behind the 165,782 K3-law decimations / routes, L 1–4. Its N1 plant
(one wrong carved letter) was correctly missed. Does the exclusion survive **one wrong letter among the 24 crib positions** (a
mis-carved letter at that slot's carved position, or a wrong crib letter)? Also part of I-003.

## Method (exact; `lrk185.c` = `lrk183.c` verbatim apart from the header line)
Case 171's one-error solver, run on its direction-r path (**method 1**: Hamming-1 dilation of the mod-2 table, 25-probe syndrome join
on σ(pa_A) ⊕ (w₀ ≫ L) per (c, d) mod 2, duplicates removed per perm) with **both** lists = the vocabulary; GF(13) per allowed slot:
prefilter on the in-block rows avoiding the slot, then block-1 13-value loop through solve0 / block-2 solve0s (case 169's exact CRT
wildcard). Strict fits reported once (`t -1`). Audit build `-DSAFE=1` (**method 2**: every (A, B) pair looked up, no prefilter,
13-value loop on every slot). Overlap: pairs with A or B themed repeat case 171 (≈ 1 %), A = B repeats Quagmire III one-error (case 169);
kept, not removed.
**Chance rate** per (perm, pair, form) ≈ 24·26^(2L+2−24); 1.17 × 10¹⁴ configurations per full set: L 1 ≈ 1 × 10⁻¹³, L 2 ≈ 1 × 10⁻¹⁰,
L 3 ≈ 6 × 10⁻⁸ fits per text (full set). Every registered cell has full power.

**Timing line (I-169), reserved shuffle, all_s64 (2,591 perms), 6 threads:** L_max 1 1.5 s, L_max 2 6.6 s, **L_max 3 (top registered
order) ≈ 37.7 s** (1.13 × 10⁸ one-error mod-2 candidates). Full-set cost: L 1 ≈ 1.6 min, L ≤ 2 ≈ 7 min, L ≤ 3 ≈ 40 min, L ≤ 4 several
hours. Control rehearsal cost 180 s (the audit build, every pair, ≈ 1.6 s per perm, dominates) — larger than planned, so the scope is cut
to fit the 8-minute heavy budget (smoke + rehearsal ≈ 232 s already spent).

## Registered cells (budget-limited coverage, full power on each subset)
- **C1** K4, L 1–3, `all_s64.bin` (= all.bin[::64], 2,591 perms, f45bc54b…).
- **C2** K4, L 1–2, `all_s8.bin` (= all.bin[::8], 20,723 perms, 3dd34d3c…).
- **C3** K4, L 1, **full set** (`all.bin`, 946402ca…), 8 contiguous chunks of 20,723 rows (last chunk to 165,782); a chunk without `END`
  is reported as not run.
- **Audit** K4 L 1–3, main build vs `-DSAFE=1` on `all_s20000.bin` (= all.bin[::20000], 9 rows, md5 46533f11…): H lines must be identical.
- **Grid** K4 + 19 nulls `random.Random(s).shuffle(list(K4))`, s = **18511…18529** (`nulls185.txt`, md5 ef4235a7…), L 1–3 on
  `all_s2048.bin` (81 rows, 94a1a6c5…).
Run order = priority (C1, grid, audit, C2, C3) under `setsid timeout 300` (resumable). **Not run (cost):** L 2 on the other 7/8, L 3 on
the other 63/64, L 4 (queued as I-175 in IDEAS.md). Nothing registered is expected to be unable to pass its controls.

## Labels
K4 0 fits in a cell → `EXACT-EXCL` (one-error scope: vocabulary × vocabulary ordered pairs, Vig/Beau, key on the plaintext index, that
cell's orders and perms). K4 > 0 → every fit decoded (`decode185.py`, independent string-level replay, 23 crib letters checked); flagged
only if above the null range, never a signal without a readable decode. Solution criterion: a full coherent English decryption of the
97 letters with both cribs at the official positions (one crib letter may differ only at the wild slot), reproducible. Any `X` or
overflow line invalidates the cell.

## Grid (I-152: empirical rank)
F = fits L 1–3 on all_s2048 (scored only if not all-zero); D1 = one-error mod-2 passes at L 3 (= every L ≤ 3 by nesting).
p⁺ = (1 + #nulls ≥ K4)/20, p⁻ = (1 + #nulls ≤ K4)/20, grid = min over cells (floor 0.05, no multiplicity correction). A floor rank on a
diagnostic is a rank flag, not a signal; it would go to a pre-registered replication with the covariate-matched null primary (I-166,
Voynich C093), never a claim.

## Controls (`plant185.py`, seed 18500, independent string-level encryptor; plaintext as cycles 180–184; each plant behind perm q of
all.bin, then the carved letter at the error slot's carved position shifted by a random non-zero amount; `run_controls185.sh`, `checkctl185.py`)
Positives (found at q with planted A, B, form, L; wild slot = the planted slot and no other; planted (c, d) mod 2 and mod 13 listed;
replay = plaintext except at the mis-carved position); P1–P7 use alphabets **outside** the themed list: P1 L1 Vig MEDITERRANEAN/Z ×
SAINTLY/K err 25; P2 L2 Beau MERCHANT/Z × OBLIQUE/Z err 66 (block 2); P3 L3 Vig NOVEMBER/Z × PLIGHT/K err 21 (seed slot); P4 L3 Beau
ITALIAN/K × RATTLING/K non-unit last weight err 33; P5 L2 Vig WHIP/K × KNIGHTS/Z strict (`t -1`); P6 L1 progressive (c 1, d 3) Vig
MOUTHS/Z × HESITATING/K err 73; P7 L2 Vig SAINTLY/K × SAINTLY/K (A = B) err 63; recount plants P8 L1 Vig LAYER/Z × TOMB/Z err 22, P9 L2
Beau SLOWLY/Z × EGYPT/Z err 70, P10 L1 Beau KA × SHADOW/K err 30. Negatives (no fit at q): N1 two errors (66, 70); N2 random key;
N3 one-error L2 plant with a random alphabet outside the vocabulary (RAND1 × OBLIQUE/Z); N4 one-error order-4 plant (outside L ≤ 3).
**Independent recount** (`recount185.py` = recount183.py logic: L 1 by enumerating all 26³ streams with set lookups of the 24-tuple and
the 23-tuples; L 2 by numpy over all 26⁵; no table / CRT / syndrome / dilation / prefilter / elimination): slice = all.bin[::4000] + the
planted perms of P8, P9, P10 (45 rows, `mkslice185.py`); A, B ∈ `alpha_recount180.txt` (33 × 33); texts K4, n18511, n18512, P8, P9,
P10; L 1 everywhere, L 2 at P9's row with A = SLOWLY/Z. Compared with lrk185 **method 1 run with the full vocabulary on both sides**,
restricted to recount-list pairs (`cmprecount185.py`).

## Budget
Heavy ≤ 8 min including rehearsal: smoke/timing ≈ 52 s, control rehearsal 180 s, main run ≈ 3.7 min estimated (C1 ≈ 38 s, grid ≈ 23 s,
audit ≈ 15 s, C2 ≈ 53 s, C3 ≈ 95 s). One 6-thread job at a time; hard stop `timeout 300`. Recount niced, 1 thread, outside the budget.
