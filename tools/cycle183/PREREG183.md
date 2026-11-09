# Cycle 183 pre-registration — one-error audit of case 170 (Quagmire IV with a linear-recurrence key behind K3's decimation law; IDEAS I-165)

Written and pushed before any K4 or registered-null run. Smoke / timing only on the reserved shuffle seed 9183
(`random.Random(9183).shuffle(list(K4))`, I-116), on `all_s64.bin`: every cell 0 fits, no overflow, no mismatch. Cost on 1/64 (6 threads):
L 1–4 ≈ 1.45 s per direction, L 1–5 ≈ 6.8 s per direction, L 1–6 ≈ 66 s (direction f; → not run).
**Planted controls rehearsed before this push (I-119): 14/14** (both directions; audit build on a ±20-row window on every plant, H lines
and fitting-slot sets identical). The rehearsal caught one checker issue, fixed before this push: the audit comparison used the full
M-line text, which differs by design for block-2 slots (main build: one `V -2` line per slot; audit build: one line per wildcard value);
it now compares the H lines and the set of fitting (L, form, q, A, B, slot). No solver or rule changed.
**Budget note.** Heavy compute ≤ 8 min this cycle, so the rehearsal outputs (`ctl_rehearsal`) are the registered control run: the
binaries (`lrk183` md5 dae240ba…, `lrk183safe` 5ed79c6d…) and `plant183.py` (seed 18300) are unchanged after the rehearsal; after the
push only the checker is re-run on those outputs.

## Question (audit; cycle 182 was a new family)
Case 170 excluded, **strictly**, Quagmire IV (plaintext-side alphabet A, ciphertext-side alphabet B) with an affine linear-recurrence
key k[i] = c₁k[i−1] + … + c_Lk[i−L] + d (mod 26) on the plaintext index behind the 165,782 K3-law decimations / routes, for A themed ×
B vocabulary (f) and A vocabulary × B themed (r), Vig/Beau, L 1–6. Its N1 plant (one wrong carved letter) was correctly missed. Does the
exclusion survive **one wrong letter among the 24 crib positions** (a mis-carved letter at that slot's carved position, or a wrong crib
letter)? Also part of I-003 (one-letter-error robustness).

## Method (exact; `lrk183.c`)
Scope exactly as case 170 (`alpha_themed180.txt` 144, md5 255a21fa…; `alpha172.txt` 18,776, md5 92793b74…; 2,703,744 pairs per
direction × Vig/Beau; key on the plaintext index). Slot t wild ⇔ its key value is a free unknown. Exact by CRT (cases 167/169): slot t
free fits mod 26 iff some v₂ passes GF(2) and some v₁₃ passes GF(13) for the same t (strict/strict reported once, `t -1`).
- **Mod 2.** Case 170's 2²⁴ table T, dilated to Hamming distance 1 (I-161): SM[x] = slot mask {t : T[x ⊕ eₜ] at L_max} + dilated
  L mask. Method 0 (f): union map U = ∪_A (W1 ⊕ pa_A). Method 1 (r): per (c, d) mod 2, x within one bit of V ⇔ σ(x) ⊕ (w₀ ≫ L) ∈ {0} ∪
  {σ(eₜ)} (up to 25 probes per (B, (c, d)), duplicates removed). Method 2 (audit): every pair looked up in SM.
- **GF(13).** Strict: lrk180's solve0. Per allowed slot t: prefilter = consistency of the in-block rows (both blocks) that do not
  contain slot t (necessary: the true key satisfies every such row); then exact: block-1 slot → v₁₃ ∈ Z₁₃ through solve0; block-2 slot →
  solve0s (case 169's exact shortcut). The mod-2 side is confirmed by solve0 / solve0s (`X` line if not). Audit build `-DSAFE=1`: no
  prefilter, 13-value loop on every slot.
- **Chance rate** per (perm, pair, form) ≈ 24·26^(2L+2−24); 1.79 × 10¹² configurations per full set (both directions): L 4 ≈ 7·10⁻⁷,
  **L 5 ≈ 4.5·10⁻⁴** fits per text (full set), L 6 ≈ 0.30.
- **Registered cells (budget-limited).** L 1–4 on the **full** set (full power). L 5 on `all_s64.bin` only (1/64 of the routes; full power
  on that subset, 1/64 coverage). **Not run (I-151 / cost):** L 5 on the full set (≈ 7 min per direction), L 6 (≈ 0.3 chance fits per
  text, ≈ 70 min per direction). Nothing registered here is expected to be unable to pass its controls.

## Texts and runs (`run_cycle183.sh`)
K4 (`data/k4.txt`, md5 dc4df49d…): L 1–4 both directions on the full set; L 1–5 on all_s64 (f45bc54b…) both directions; L 1–5 main and
audit build (method 2) on `all_s2048.bin` (= all.bin[::2048], 81 rows, md5 94a1a6c5…; H lines must be identical). 19 nulls =
`random.Random(s).shuffle(list(K4))`, s = **18311…18329** (`nulls183.txt`): L 1–4, both directions, all_s64.

## Labels
K4 0 fits → `EXACT-EXCL` (one-error scope: these pairs, forms, orders, routes; L 5 only on 1/64). K4 > 0 → every fit decoded
(`decode183.py`, independent string-level replay from the seed, 23 crib letters checked), `LOW-POWER` if inside the null range, flagged
if above, never a signal without a readable decode. Solution criterion: a full coherent English decryption of the 97 letters with both
cribs at the official positions (one crib letter may differ only at the wild slot), reproducible. Any `X` or overflow line invalidates
the cell.

## Grid (I-152: empirical rank)
Fit cells (f L 1–3, f L 4, r L 1–3, r L 4, all_s64) scored only if not all-zero. Diagnostics: D1 = direction f one-error mod-2 passes at
L 4 (= every L ≤ 4 by nesting), D2 = direction r the same. p⁺ = (1 + #nulls ≥ K4)/20, p⁻ = (1 + #nulls ≤ K4)/20, grid = min over cells
(floor 0.05, no multiplicity correction). A floor rank on a diagnostic is a rank flag, not a signal (I-166: if a covariate-matched
replication is ever registered for it, the matched-vs-filtered inflation is reported beside it).

## Controls (`plant183.py`, seed 18300, independent string-level encryptor; plaintext as cycles 180–182; each plant behind perm q of
all.bin, then the carved letter at the error slot's carved position shifted by a random non-zero amount; main build on q ± 100 both
directions, audit build on q ± 20 compared with the main build on the same rows; `run_controls183.sh`, `checkctl183.py`)
Positives (found at q in the planted direction with planted A, B, form, L; wild slot = the planted slot and no other; planted (c, d)
mod 2 and mod 13 listed; replay = plaintext except at the mis-carved position): P1 f L1 Vig KA × SHADOW/Z err 25; P2 f L3 Beau
PALIMPSEST/K × BERLIN/Z err 66 (block 2); P3 f L5 Vig IQLUSION/Z × LODESTONE/K err 21 (first seed slot); P4 f L4 Beau ABSCISSA/Z ×
COMPASS/K non-unit last weight err 33; P5 f L2 Vig SHADOW/K × LODESTONE/K strict (`t -1`); P6 f L1 progressive (c 1, d 3) Vig
BERLINCLOCK/K × MAGNETIC/Z err 73; P7 r L2 Beau MAGNETIC/Z × KA err 63; P8 r L4 Vig LODESTONE/Z × UNDERGRUUND/K err 30; P9 r L5 Beau
CARTER/Z × PALIMPSEST/K err 70; P10 r L1 Vig AZ × KA err 22. Negatives (no fit at q in either direction): N1 two errors (66, 70);
N2 random key; N3 one-error L3 plant with a pair outside the scope (TOMB/Z × SLOWLY/Z); N4 one-error order-6 plant (outside L ≤ 5).
**Independent recount** (`recount183.py`: L 1 by enumerating all 26³ streams and set lookups of the 24-tuple and the 23-tuples; L 2 by
numpy over all 26⁵ (c₁, c₂, d, k₂₁, k₂₂); no table / CRT / syndrome / dilation / prefilter / elimination): slice = all.bin[::4000] + the
planted perms of P1, P6, P7, P10 (46 rows, `mkslice183.py`, md5 5e35f72f…); A, B ∈ `alpha_recount180.txt` (33 × 33); texts K4,
n18311, n18312, P1, P6, P7, P10; L 1 everywhere, L 2 at P7's planted row with A = MAGNETIC/Z. Compared with lrk183's audit build
(method 2, same lists) per (text, L, row, A, B, form) on the set of fitting slots (`cmprecount183.py`).

## Budget
≈ 4 min heavy after the push (K4 full L 1–4 ≈ 2.3 min, L 5 on 1/64 ≈ 14 s, audit ≈ 10 s, nulls ≈ 1 min), one 6-thread job at a time
under `setsid timeout 600`; resumable. Smoke and rehearsal used ≈ 3.1 min. Recount niced, 1 thread, outside the budget.
