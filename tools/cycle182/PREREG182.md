# Cycle 182 pre-registration — Quagmire IV (two different keyed alphabets) with a linear-recurrence key behind K3's decimation law (IDEAS I-155), plus the I-160 replication

Written and pushed before any K4 or registered-null run. Smoke / timing only on the reserved shuffle seed 9182
(`random.Random(9182).shuffle(list(K4))`, I-116), on `all_s64.bin`: every cell 0 fits, no overflow, no mismatch; methods 0, 1 and
the audit method 2 (`-DSAFE=1`) gave identical H lines in both directions. Cost on 1/64 (6 threads): ≈ 0.5 s per direction.
**Planted controls rehearsed before this push (I-119): 14/14** (both directions plus the audit build on every plant; H lines identical).
Nothing was changed after the rehearsal.

## A. Question (new family; cycles 180/181 were Quagmire I–III and its one-error audit)
Cases 168/169 excluded the affine linear-recurrence key k[i] = c₁k[i−1] + … + c_Lk[i−L] + d (mod 26) behind the 165,782 K3-law
decimations / routes when the tableau uses **one** keyed alphabet (Quagmire I/II/III). Quagmire IV uses **two different** keyed
alphabets: A on the plaintext side, B on the ciphertext side. Vigenère c = B[(A.index(p) + k) mod 26], Beaufort c = B[(k − A.index(p)) mod 26].
Does K4 fit any such cipher with A, B from the registered lists, L ≤ 6, key on the plaintext index, behind any of the 165,782 perms?

**Scope.** Direction f: A ∈ themed (`alpha_themed180.txt`, 144, md5 255a21fa…) × B ∈ vocabulary (`alpha172.txt`, 18,776, md5 92793b74…).
Direction r: A ∈ vocabulary × B ∈ themed. 2,703,744 pairs per direction × Vig/Beau (rotations and the variant are covered by the affine
family, case 168). Pairs with A = B repeat Quagmire III (case 168) and are kept, not removed. Key on the plaintext index (M0), L 1–6.

## Method (exact; `lrk182.c`)
Mod 2 the 24 crib key bits are w = parity_B(carved letter) ⊕ parity_A(crib letter) = cp_B (per perm) ⊕ pa_A (constant). The 2²⁴ table
is lrk180's (bit L−1: some (c, d) mod 2 fits at order L). **Nesting:** an order-L solution is an order-(L+1) solution with c_{L+1} = 0
(fewer in-block equations, the same propagation), mod 2 and mod 13; the program checks it on the table (`X` line if violated).
- **method 0** (direction f, A small): U = ∪_A (W₆ ⊕ pa_A) as a 2²⁴ CSR map word → A list; per perm one lookup per B.
- **method 1** (direction r, A large): for each (c, d) mod 2 at order 6 the passing words form an affine space w₀ + span(w_j) whose low
  6 bits are the free seed (crib slots 21–26), so x ∈ V ⇔ σ(x) = w₀ ≫ 6 with σ linear; a hash join per (c, d) on σ(pa_A) ⊕ (w₀ ≫ 6).
- **method 2** (audit, `-DSAFE=1` build): every (A, B) pair looked up in the table, and no nesting shortcut in GF(13).
- Every mod-2 pass is re-checked against the table; GF(13) is lrk180's `solve0` (shortcut: order 6 first, lower L only if order 6 has a
  mod-13 solution, exact by nesting). Fit ⇔ mod 2 and mod 13 both solvable at that L; CRT gives the key.
- **Chance rate** per (perm, pair, form) ≈ 26^(2L+2−24); 1.79 × 10¹² configurations per full set (both directions): L 5 ≈ 2·10⁻⁵,
  **L 6 ≈ 0.013** fits per text. Every registered cell has full power.
- **Dead-on-arrival line (I-151).** L 7: ≈ 8.6 chance fits per full set (`LOW-POWER` by construction) → **not run**. Vocabulary ×
  vocabulary (3.5 × 10⁸ pairs) → not run (cost). Key on the carved index (M1) → not run (per-perm pair lookups, cost), queued.
  Nothing registered here is expected to be unable to pass its controls.

## Texts and runs (`run_cycle182.sh`)
K4 (`data/k4.txt`, md5 dc4df49d…): both directions on the **full** set, and on `all_s64.bin` (md5 f45bc54b…) for the grid, plus the
audit build (method 2) on all_s64 in both directions (H lines must equal method 0 / 1). 19 nulls = `random.Random(s).shuffle(list(K4))`,
s = **18211…18229** (`nulls182.txt`), both directions on all_s64.

## Labels
K4 0 fits → `EXACT-EXCL` (scope: these alphabet pairs, forms, L 1–6, key on the plaintext index, these perms). K4 > 0 → every fit decoded
(`decode182.py`, independent string-level replay, all 24 crib letters checked), `LOW-POWER` if inside the null range, flagged if above,
never a signal without a readable decode. Solution criterion: a full coherent English decryption of the 97 letters with both cribs at
the official positions, reproducible. Any `X` or overflow line invalidates the cell.

## Grid (I-152: empirical rank)
Fit cells (f L 1–5, f L 6, r L 1–5, r L 6, all_s64) scored only if not all-zero. Diagnostics: D1 = direction f mod-2 passes at order 6
(= every L ≤ 6 by nesting), D2 = direction r the same. p⁺ = (1 + #nulls ≥ K4)/20, p⁻ = (1 + #nulls ≤ K4)/20, grid = min over cells
(floor 0.05, no multiplicity correction). A floor rank on a diagnostic is a rank flag, not a signal.

## Controls (`plant182.py`, seed 18200, independent string-level encryptor; plaintext as cycles 180/181; each plant behind perm q of
all.bin; run on q ± 500, both directions and the audit build; `run_controls182.sh`, `checkctl182.py`)
Positives (found at q in the planted direction with planted A, B, form, L; planted (c, d) mod 2 and mod 13 listed; replay = plaintext):
P1 f L1 Vig KA × SHADOW/Z; P2 f L3 Beau PALIMPSEST/K × BERLIN/Z; P3 f L5 Vig IQLUSION/Z × LODESTONE/K; P4 f L6 Beau ABSCISSA/Z ×
COMPASS/K non-unit last weight; P5 f L2 Vig SHADOW/K × LODESTONE/K; P6 f L1 progressive (c 1, d 3) Vig BERLINCLOCK/K × MAGNETIC/Z;
P7 r L2 Beau MAGNETIC/Z × KA; P8 r L4 Vig LODESTONE/Z × UNDERGRUUND/K (B themed only); P9 r L6 Beau CARTER/Z × PALIMPSEST/K;
P10 r L1 Vig AZ × KA. Negatives (no fit at q in either direction): N1 = P2 with one wrong carved letter (slot 30); N2 random key;
N3 L3 plant with a pair outside the scope (TOMB/Z × SLOWLY/Z, neither themed); N4 order-7 plant (outside L ≤ 6).
**Independent recount** (`recount182.py`, numpy brute force over every (c, d) ∈ Z₂₆², no table / CRT / syndrome / nesting): slice =
all.bin[::4000] + the planted perms of P1, P5, P7 (45 rows, `mkslice182.py`, md5 55e3785c…); A, B ∈ `alpha_recount180.txt` (33 × 33);
texts K4, n18211, n18212, P1, P5, P7; L 1 everywhere, L 2 (every (c₁, c₂, d) ∈ Z₂₆³) at P5's and P7's planted row with the planted A.
Compared with lrk182 (audit build, method 2, same lists, L 1–2) per (text, L, row, A, B, form) (`cmprecount182.py`).

## B. Add-on: I-160 replication (one pre-registered test; audit fallback, cheap)
Case 169's D2 (lrk181 mode 1, one-error mod-2 passes, L 1–3, all_s64, 18,776 alphabets × q1/q2/q3, sum over L and types, Vigenère lines)
had K4 **18,432** above all 19 nulls (15,575–18,207). **Fresh nulls:** 40 plain shuffles, seeds **18241…18280**; and a covariate-matched
null (I-146): 20 shuffles **within K4's A–Z parity classes** (every position keeps the A–Z parity of its letter), seeds **18281…18300**.
K4 recomputed with the same binary (must give 18,432). p_F = (1 + #{≥ K4}) / (n + 1) per group. **Decision:** `REPLICATED` iff p_F ≤ 0.05
in both groups (the flag stays open, still not a fit); `NOT REPLICATED` (flag closed) if the plain p_F > 0.05; if only the plain group
passes, the excess is attributed to K4's A–Z parity pattern. Per-type splits are description only (q1 is fixed under the matched null
by construction). `run_i160_182.sh`.

## Budget
≈ 5 min heavy (K4 full ≈ 70 s, all_s64 runs ≈ 35 s, I-160 ≈ 3 min), one 6-thread job at a time under `setsid timeout 600`; resumable.
Rehearsal and smoke used ≈ 1 min. Recount niced, 1 thread, outside the budget.
